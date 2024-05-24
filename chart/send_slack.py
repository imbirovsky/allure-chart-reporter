import os
import json
import sys
import glob
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

RUN_ID = os.getenv('GITHUB_RUN_ID')
RUN_NUMBER = os.getenv('GITHUB_RUN_NUMBER')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
RUN_URL = f"https://github.com/{REPO_NAME}/actions/runs/{RUN_ID}"
MAX_TESTS_FOR_TELEGRAM_REPORT = 7
URL_REGEX = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)


def is_url(string):
    return re.match(URL_REGEX, string) is not None


def get_failed_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['failed'])


def get_broken_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['broken'])


def get_skipped_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['skipped'])


def get_tests_by_status(allure_report_path, statuses):
    tests = []
    for file in glob.glob(f"{allure_report_path}/*.json"):
        with open(file) as f:
            data = json.load(f)
        if 'status' in data and data['status'] in statuses:
            response_code = None
            for attachment in data.get('attachments', []):
                if 'HTTP/1.1' in attachment['name']:
                    response_code = attachment['name'].replace('HTTP/1.1 ', '')
                    break
            test = {
                'name': data['name'],
                'status': data['status'],
                'response_code': response_code
            }
            tests.append(test)
    tests.sort(key=lambda test: is_url(test['name'].split('\n')[1]) if len(test['name'].split('\n')) > 1 else False)
    return tests


def create_blocks(report_link, message):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "🔗  Link to report"
                    },
                    "url": report_link
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "ℹ️  View Run Details"
                    },
                    "url": RUN_URL
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "🇺🇦  Stop Russian Aggression"
                    },
                    "url": "https://war.ukraine.ua/"
                }
            ]
        }
    ]
    return blocks


def format_test_message(status, count, tests):
    message = ""
    if int(count) > 0:
        message += f"• *{status.capitalize()} ({count}):*\n"
        for i, test in enumerate(tests):
            if i >= MAX_TESTS_FOR_TELEGRAM_REPORT:
                break
            name_parts = test['name'].split('\n')
            message += f"\t • `{name_parts[0]}`"
            if len(name_parts) > 1 and is_url(name_parts[1]):
                message += f'\n\t\t<{name_parts[1]}|{name_parts[1]}>'
            if test['response_code']:
                message += f"\n\t\t`{test['response_code']}`"
            if i < len(tests) - 1:
                message += "\n"
        if len(tests) > MAX_TESTS_FOR_TELEGRAM_REPORT:
            message += f"\t`And {len(tests) - MAX_TESTS_FOR_TELEGRAM_REPORT} more {status} tests...`\n"
    return message


def send_message_and_image_to_slack(token, channel_id, image_path, total, passed, failed, broken, skipped, report_link,
                                    allure_report_path):
    client = WebClient(token=token)
    try:
        with open(image_path, 'rb') as file_content:
            response = client.files_upload_v2(
                channels=channel_id,
                file=file_content,
            )
        image_url = response["file"]["url_private"]

        message = f"*Test Results | #{RUN_NUMBER}* \n\n"
        message += f"• *Total ({total})*\n\n"
        if int(passed) > 0:
            message += f"• *Passed ({passed})*\n\n"

        failed_tests = get_failed_tests(allure_report_path)
        broken_tests = get_broken_tests(allure_report_path)
        skipped_tests = get_skipped_tests(allure_report_path)

        failed_message = format_test_message('failed', failed, failed_tests)
        if failed_message:
            message += failed_message + "\n\n"

        broken_message = format_test_message('broken', broken, broken_tests)
        if broken_message:
            message += broken_message + "\n\n"

        skipped_message = format_test_message('skipped', skipped, skipped_tests)
        if skipped_message:
            message += skipped_message + "\n\n"

        message = message.rstrip()
        # message += f"\n\n•••\n\n"
        print(f"Message: {message}")

        blocks = create_blocks(report_link, message)
        client.chat_postMessage(
            channel=channel_id,
            text=message,
            blocks=json.dumps(blocks)
        )
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


if __name__ == "__main__":
    token = sys.argv[1]
    channel_id = sys.argv[2]
    image_path = sys.argv[3]
    total = sys.argv[4]
    passed = sys.argv[5]
    failed = sys.argv[6]
    broken = sys.argv[7]
    skipped = sys.argv[8]
    report_link = sys.argv[9]
    allure_report_path = sys.argv[10]

    send_message_and_image_to_slack(token, channel_id, image_path, total, passed, failed, broken, skipped, report_link,
                                    allure_report_path)