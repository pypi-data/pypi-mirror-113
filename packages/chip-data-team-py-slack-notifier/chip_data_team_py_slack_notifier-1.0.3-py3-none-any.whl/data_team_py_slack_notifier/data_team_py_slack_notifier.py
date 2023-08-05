import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
import re

notification_message_template = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": " _SERVICE_: {val}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_PROCESS_: {val}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_TIME_: {val}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_JOB ID_: {val}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_STATE_: {val} ",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_NOTIFICATION MESSAGE_: {val}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"--------------------",
            },
        },
    ]
}


def error_handler(err, event):
    """
    An error handler for different cases that we catch.
    """
    if isinstance(err, KeyError):
        print(f"KeyError {err}. The event is {event}")
        status_code = 500
    response = {"statusCode": status_code, "error": json.dumps(str(err))}
    return response


def construct_slack_process_notification_params(process):
    """
    Creates the slack message. The SDK expects a dict of the form below.
    """

    if re.search("succeeded", process.state, flags=re.IGNORECASE):
        state = process.state
    else:
        state = f" :no_entry: *{process.state}* :no_entry: "

    return (
        process.source,
        process.job_name,
        process.time,
        process.job_run_id,
        state,
        process.message,
    )


def construct_notification_message(notification_message_params):
    for i in range(len(notification_message_params)):
        print(notification_message_params[i])
        notification_message_template["blocks"][i]["text"][
            "text"
        ] = notification_message_template["blocks"][i]["text"]["text"].format(
            val=notification_message_params[i]
        )

    return notification_message_template


def notify(message={}, channel="#datya-team-processes-notifications"):
    """
    Sends message to Slack based on channel and slack_token retrieved from the Slack bot.
    """
    slack_token = os.environ["SLACK_TOKEN"]
    client = WebClient(token=slack_token)

    try:
        response = client.chat_postMessage(channel=channel, **message)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(
            f"Got an error whilst trying to send the slack message: {e.response['error']}"
        )


class AwsSNSHandler:
    def __init__(self, event):
        self._sns_type = event["Records"][0]["Sns"]["Type"]
        self.__sns_message_id = event["Records"][0]["Sns"]["MessageId"]
        self.__sns_topic_arn = event["Records"][0]["Sns"]["TopicArn"]
        self.__sns_subject = event["Records"][0]["Sns"]["Subject"]
        self.__sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
        self.__sns_message = Process(self.__sns_message)

    @property
    def sns_type(self):
        return self._sns_type

    @property
    def sns_message_id(self):
        return self.__sns_message_id

    @property
    def sns_topic_arn(self):
        return self.__sns_topic_arn

    @property
    def sns_subject(self):
        return self.__sns_subject

    @property
    def sns_message(self):
        return self.__sns_message


class Process:
    def __init__(self, process_details):
        self._detail_type = process_details.get("detail-type")
        self.__source = process_details.get("source")
        self.__account = process_details.get("account")
        self.__time = (
            process_details.get("time")
            or process_details.get("Timestamp")
            or process_details.get("timestamp")
        )
        self.__region = process_details.get("region")

        if all(
            i in process_details.keys()
            for i in ["requestContext", "requestPayload", "responseContext"]
        ):
            # This looks like a Lambda function notification
            if not self.__source:
                self.__source = "AWS Lambda"

            self.__job_name = process_details["requestContext"]["functionArn"]
            self.__severity = None
            self.__state = (
                "SUCCEEDED"
                if process_details["requestContext"]["condition"] == "Success"
                else "FAILED"
            )
            self.__job_run_id = "Untracked"
            self.__message = (
                f"Lambda function has finished with the following state: {self.__state}"
            )

        else:
            # This looks like a Glue function notification
            self.__job_name = process_details["detail"]["jobName"]
            self.__severity = process_details["detail"].get("severity")
            self.__state = process_details["detail"]["state"]
            self.__job_run_id = process_details["detail"].get("jobRunId", "Untracked")
            self.__message = process_details["detail"]["message"]

        if not self.__source:
            self.__source = "*This is an unknown source. Check where this comes from*"

    @property
    def detail_type(self):
        return self._detail_type

    @property
    def source(self):
        return self.__source

    @property
    def account(self):
        return self.__account

    @property
    def time(self):
        return self.__time

    @property
    def region(self):
        return self.__region

    @property
    def job_name(self):
        return self.__job_name

    @property
    def severity(self):
        return self.__severity

    @property
    def state(self):
        return self.__state

    @property
    def job_run_id(self):
        return self.__job_run_id

    @property
    def message(self):
        return self.__message


def parse_event(event, context):
    """
    The event parser. It must be unit-testable and it should handle custom processes as expected by the Process class.
    It checks if the event comes from SNS, if it doesn`t it just passes the event to Process class.

    Returns: response, notification_message
    """
    response = {}
    if (
        "Records" in event.keys()
        and isinstance(event["Records"], list)
        and isinstance(event["Records"][0], dict)
        and "EventSource" in event["Records"][0]
        and event["Records"][0]["EventSource"] == "aws:sns"
    ):
        try:
            sns_event = AwsSNSHandler(event)
        except KeyError as e:
            response = error_handler(e, event)
            return response, json.dumps(event), e
        process = sns_event.sns_message
    else:
        try:
            process = Process(event)
        except KeyError as e:
            response = error_handler(e, event)
            return response, json.dumps(event), e
    notification_message_params = construct_slack_process_notification_params(process)
    response = {
        "statusCode": 200,
        "body": "ok",
    }

    return response, notification_message_params, None


def notification_handler(event, context):
    """
    The starting point for the notification process. Call this with your event and context.
    """
    response, notification_message_params, err = parse_event(event, context)
    if not err:
        notification_message = construct_notification_message(
            notification_message_params
        )
    else:
        notification_message = {
            "text": f""" :no_entry: *The slack notifier failed. Can`t tell anything about the process. Notifier has received an input key it can`t deal with.* :no_entry: . The event is {notification_message_params}"""
        }
    notify(notification_message)
    return response
