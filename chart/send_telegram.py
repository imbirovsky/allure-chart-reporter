import re
import json
import requests
import sys
import glob
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def is_url(string):
    url_regex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return re.match(url_regex, string) is not None

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
    return tests

def get_failed_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['failed'])

def get_broken_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['broken'])

def get_skipped_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['skipped'])

def format_test_message(status, count, get_tests_func, allure_report_path):
    message = ""
    if int(count) > 0:
        message += f"<b>• {status.capitalize()}: {count}</b>\n"
        tests = get_tests_func(allure_report_path)
        for i, test in enumerate(tests):
            if i >= 5:
                break
            name_parts = test['name'].split('\n')
            message += f"\t • <code>{name_parts[0]}</code>"
            if len(name_parts) > 1 and is_url(name_parts[1]):
                message += f'\n\t\t\t<a href="{name_parts[1]}">{name_parts[1]}</a>'
            if test['response_code']:
                message += f" - <code>{test['response_code']}</code>"
            message += "\n"
        if len(tests) > 5:
            message += f"\t\t<code>And {len(tests) - 5} more {status} tests...</code>\n"
    return message

def send_photo_and_message(token, chat_id, photo_path, total, passed, failed, broken, skipped, report_link, allure_report_path):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    message = "Tests completed\n\n"
    message += f"<b>• Total: {total}</b>\n"
    if int(passed) > 0:
        message += f"<b>• Passed: {passed}</b>\n"
    message += format_test_message('failed', failed, get_failed_tests, allure_report_path)
    message += format_test_message('broken', broken, get_broken_tests, allure_report_path)
    message += format_test_message('skipped', skipped, get_skipped_tests, allure_report_path)

    # Check if the message exceeds the limit
    if len(message) > 4050:
        message = message[:4050] + "\n\nMessage is cut off as it exceeds the limit of 4096 characters."

    print(f"Sending message: {message}")  # Log the message before sending
    with open(photo_path, 'rb') as photo:
        files = {'photo': photo}
        keyboard = [
            [InlineKeyboardButton("🔗 Link to report", url=report_link)],
            # [InlineKeyboardButton("🔄 Restart the tests", callback_data='confirm_restart')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        data = {
            'chat_id': chat_id,
            'caption': message,
            'parse_mode': 'HTML',
            'reply_markup': json.dumps(reply_markup.to_dict())
        }
        response = requests.post(url, files=files, data=data)
        print(response.json())
        return response.json()

if __name__ == "__main__":
    token = sys.argv[1]
    chat_id = sys.argv[2]
    photo_path = sys.argv[3]
    total = sys.argv[4]
    passed = sys.argv[5]
    failed = sys.argv[6]
    broken = sys.argv[7]
    skipped = sys.argv[8]
    report_link = sys.argv[9]
    allure_report_path = sys.argv[10]
    send_photo_and_message(token, chat_id, photo_path, total, passed, failed, broken, skipped, report_link, allure_report_path)