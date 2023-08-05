import pytest
from data_team_py_slack_notifier.data_team_py_slack_notifier import parse_event


@pytest.fixture
def mock_event_sns_success():
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "58fee2ac-7c63-5667-bd4e-bbf3af704c0f",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring",
                    "Subject": None,
                    "Message": '{"version":"0","id":"e3b6465b-835f-a022-28cc-7524776f3395","detail-type":"Glue Job State Change","source":"aws.glue","account":"309161096106","time":"2021-07-07T16:05:36Z","region":"eu-west-2","resources":[],"detail":{"jobName":"DE-209-test","severity":"INFO","state":"SUCCEEDED","jobRunId":"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181","message":"Job run succeeded"}}',
                    "Timestamp": "2021-07-07T16:05:39.180Z",
                    "SignatureVersion": "1",
                    "Signature": "OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_success(mock_event_sns_success):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        (
            "aws.glue",
            "DE-209-test",
            "2021-07-07T16:05:36Z",
            "jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181",
            "SUCCEEDED",
            "Job run succeeded",
        ),
        None,
    )
    result = parse_event(*mock_event_sns_success)
    assert result == expected_result


@pytest.fixture
def mock_event_sns_failure():
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "58fee2ac-7c63-5667-bd4e-bbf3af704c0f",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring",
                    "Subject": None,
                    "Message": '{"version":"0","id":"e3b6465b-835f-a022-28cc-7524776f3395","detail-type":"Glue Job State Change","source":"aws.glue","account":"309161096106","time":"2021-07-07T16:05:36Z","region":"eu-west-2","resources":[],"detail":{"jobName":"DE-209-test","severity":"INFO","state":"FAILED","jobRunId":"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181","message":"Job run has failed."}}',
                    "Timestamp": "2021-07-07T16:05:39.180Z",
                    "SignatureVersion": "1",
                    "Signature": "OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_failure(mock_event_sns_failure):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        (
            "aws.glue",
            "DE-209-test",
            "2021-07-07T16:05:36Z",
            "jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181",
            " :no_entry: *FAILED* :no_entry: ",
            "Job run has failed.",
        ),
        None,
    )
    result = parse_event(*mock_event_sns_failure)
    assert result == expected_result


@pytest.fixture
def mock_event_custom_process_failure():
    event = {
        "source": "somesource",
        "time": "sometime",
        "detail": {
            "jobName": "somejob",
            "state": "some failed string",
            "message": "process has failed.",
        },
    }
    context = None
    return event, context


def test_parse_event_custom_failure(mock_event_custom_process_failure):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        (
            "somesource",
            "somejob",
            "sometime",
            "Untracked",
            " :no_entry: *some failed string* :no_entry: ",
            "process has failed.",
        ),
        None,
    )
    result = parse_event(*mock_event_custom_process_failure)
    assert result == expected_result


@pytest.fixture
def mock_event_custom_process_key_error():
    event = {
        "unexpected_key_here": "somesource",
        "time": "sometime",
        "detail": {
            "jobName": "somejob",
            "state": "some failed string",
            "message": "process has failed.",
        },
    }
    context = None
    return event, context


def test_parse_event_custom_process_key_error(mock_event_custom_process_key_error):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        (
            "*This is an unknown source. Check where this comes from*",
            "somejob",
            "sometime",
            "Untracked",
            " :no_entry: *some failed string* :no_entry: ",
            "process has failed.",
        ),
        None,
    )
    result = parse_event(*mock_event_custom_process_key_error)
    assert result == expected_result


@pytest.fixture
def mock_event_sns_key_error_1():
    event = {
        "Records": [
            {
                "WrongKeyHere": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "58fee2ac-7c63-5667-bd4e-bbf3af704c0f",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:glue-monitoring",
                    "Subject": None,
                    "Message": '{"version":"0","id":"e3b6465b-835f-a022-28cc-7524776f3395","detail-type":"Glue Job State Change","source":"aws.glue","account":"309161096106","time":"2021-07-07T16:05:36Z","region":"eu-west-2","resources":[],"detail":{"jobName":"DE-209-test","severity":"INFO","state":"SUCCEEDED","jobRunId":"jr_c4a93310af669b1fe899952ed184fe712ff5c471bab7a1c002f8784dc81be181","message":"Job run succeeded"}}',
                    "Timestamp": "2021-07-07T16:05:39.180Z",
                    "SignatureVersion": "1",
                    "Signature": "OzlczeD9GPBWpFCO6ikTJwBtwnCDxs2KtiVFVzZ77fMamD9mhnJxVFjrCKcx2DOtIUtYs6wGuBp07UCIMPs53Ak4yK3Bz4fRsQVq1YOoYRCODnlF1M7ye1zSvQj4y7eS3w1FncUu7sHw3vPnyqXxJ8w9aN61SUKha1FGDJZG46Deupno5mLcu81x9cmcPpThEiyj+kPigd9vu4QXaBs/7EzKlIeLtMOj8y7WtLoCYXev58WsYqnGeByCZB5xUhxwcmD0fhK6ofiin4aTCurIkhYMGbJ/52cIksJ69SAV9oFSgoUdPVauTLHe5MrLZyadsYn/cDV5gekWaOVq/vMU7w==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:glue-monitoring:8827e346-e2db-42f7-95f0-d66759181897",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_key_error_1(mock_event_sns_key_error_1):
    expected_result = {"statusCode": 500, "error": "\"'detail'\""}

    result = parse_event(*mock_event_sns_key_error_1)
    assert isinstance(result[2], KeyError)
    assert result[0] == expected_result


@pytest.fixture
def mock_event_sns_key_error_2():
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:ProcessesMonitoring:cc124953-2820-4dbe-90de-7c52890512da",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "6cd6c36c-5ebf-597d-becc-9a0614d5b377",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:ProcessesMonitoring",
                    "Subject": None,
                    "Message": '{"version":"1.0","timestamp":"2021-07-15T14:37:30.563Z","requestContext":{"requestId":"526692d1-daa1-421c-be4d-5ff56927c621","functionArnWRONGKEYHERE":"arn:aws:lambda:eu-west-2:309161096106:function:ETLGoogleSpreadsheetToDB:$LATEST","condition":"Success","approximateInvokeCount":1},"requestPayload":{  "google_sheets_key": "1ZAchu2BTSHO3kGEuhnrM_IABuZyONucqWfU5SVN-V2w",  "google_sheets_worksheet": "Actioned",  "google_sheets_columns_range": 20,  "google_sheets_columns_remapping": {    "User Ref": "user_id",    "Unblocked": "unblocked"  },  "google_sheets_flag_drop_duplicates": true,  "etl_landing_database": "fraud_db",  "etl_landing_table": "actioned"},"responseContext":{"statusCode":200,"executedVersion":"$LATEST"},"responsePayload":"OK"}',
                    "Timestamp": "2021-07-15T14:37:30.610Z",
                    "SignatureVersion": "1",
                    "Signature": "u0K/RqT6J/TA+XXnQII9JTdIOJstEhxxmDAa0dqslCbaA0urySjIpb6jI3tdnemb07wxWu8cqo85W0Sehgh+CRiciaxMeXByJTlcwrIU8b8/0J24F6T8XqJC4l6zt1w9UHZ/7zPxX74EmmbhZifPLjBI5bKa2pxaNe9Hl9pINBpZyEt7Z89e7lI6jCRH4wFUVZV+UiNCQkOP+4Y39zU5qw4QQkerqeGHEunGIfUT+VFEx8zJB7Bp9bGsR8LkDuABQ0JEJkwnjWgjufgc6+VFyGRutWmofazoQKlk0kv7xR8oT1lCnfAPSAddU5CRalJioiKx+4f4u8houKpANr7kkg==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:ProcessesMonitoring:cc124953-2820-4dbe-90de-7c52890512da",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_key_error_2(mock_event_sns_key_error_2):
    expected_result = {"statusCode": 500, "error": "\"'functionArn'\""}
    result = parse_event(*mock_event_sns_key_error_2)

    assert isinstance(result[2], KeyError)
    assert result[0] == expected_result


@pytest.fixture
def mock_event_sns_lambda_1():
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:eu-west-2:309161096106:ProcessesMonitoring:cc124953-2820-4dbe-90de-7c52890512da",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "129b6aeb-c962-5c4e-b654-3381a75ec42c",
                    "TopicArn": "arn:aws:sns:eu-west-2:309161096106:ProcessesMonitoring",
                    "Subject": None,
                    "Message": '{"version":"1.0","timestamp":"2021-07-15T17:10:20.060Z","requestContext":{"requestId":"f2c12a7e-99d5-4860-9aab-2ea8ec114ab8","functionArn":"arn:aws:lambda:eu-west-2:309161096106:function:ETLGoogleSpreadsheetToDB:$LATEST","condition":"Success","approximateInvokeCount":1},"requestPayload":{  "google_sheets_key": "1ZAchu2BTSHO3kGEuhnrM_IABuZyONucqWfU5SVN-V2w",  "google_sheets_worksheet": "Actioned",  "google_sheets_columns_range": 20,  "google_sheets_columns_remapping": {    "User Ref": "user_id",    "Unblocked": "unblocked"  },  "google_sheets_flag_drop_duplicates": true,  "etl_landing_database": "fraud_db",  "etl_landing_table": "actioned"},"responseContext":{"statusCode":200,"executedVersion":"$LATEST"},"responsePayload":"OK"}',
                    "Timestamp": "2021-07-15T17:10:20.087Z",
                    "SignatureVersion": "1",
                    "Signature": "KpUlXUY3AUi0SwDdtWIyj+FVSMzoNDFNHqxkZQEmoJTqKCBnYwDqzXIzmymc/7o317qFOZNk25GoinccrQ57b0eL9bVVcMqf5HF/T/Ap6+CzQU5DUEIUjIKw1HuL7uuN14AaN1EG1RWc6s4NN17ZB5y3b2w42ro+FLhkblgDpr4W0MduWrK6wrPob71Oua7l19HLSQJ3Wf4hqyP3lkWu04WZcol0psSasD0Cgeb2/iLW4q/rvbBzDbH8JGvYyHTUsnkZYdrrpXQBmwAbDvpjlEbKN7xKXtmfAVyBcf32xvF9aEhavhGbrqygIRam56ScQv+J67L262JS8wYv1xB8Mg==",
                    "SigningCertUrl": "https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:309161096106:ProcessesMonitoring:cc124953-2820-4dbe-90de-7c52890512da",
                    "MessageAttributes": {},
                },
            }
        ]
    }
    context = None
    return event, context


def test_parse_event_sns_lambda_1(mock_event_sns_lambda_1):
    expected_result = (
        {"statusCode": 200, "body": "ok"},
        (
            "AWS Lambda",
            "arn:aws:lambda:eu-west-2:309161096106:function:ETLGoogleSpreadsheetToDB:$LATEST",
            "2021-07-15T17:10:20.060Z",
            "Untracked",
            "SUCCEEDED",
            "Lambda function has finished with the following state: SUCCEEDED",
        ),
        None,
    )
    result = parse_event(*mock_event_sns_lambda_1)
    assert result == expected_result
