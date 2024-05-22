import re
import json
import requests
import sys
import glob
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

MAX_TESTS_FOR_TELEGRAM_REPORT = 7
MAX_SYMBOLS_FOR_MESSAGE = 4060
URL_REGEX = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)


def is_url(string):
    return re.match(URL_REGEX, string) is not None


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
    # Сортировка тестов так, чтобы тесты с URL были в конце списка
    tests.sort(key=lambda test: is_url(test['name'].split('\n')[1]) if len(test['name'].split('\n')) > 1 else False)
    return tests


def get_failed_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['failed'])


def get_broken_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['broken'])


def get_skipped_tests(allure_report_path):
    return get_tests_by_status(allure_report_path, ['skipped'])


def format_test_message(status, count, tests):
    message = ""
    if int(count) > 0:
        message += f"<b>• {status.capitalize()} ({count}):</b>\n"
        for i, test in enumerate(tests):
            if i >= MAX_TESTS_FOR_TELEGRAM_REPORT:
                break
            name_parts = test['name'].split('\n')
            message += f"\t • <code>{name_parts[0]}</code>"
            if len(name_parts) > 1 and is_url(name_parts[1]):
                message += f'\n\t\t\t<a href="{name_parts[1]}">{name_parts[1]}</a>'
            if test['response_code']:
                message += f" - <code>{test['response_code']}</code>"
            if i < len(tests) - 1:
                message += "\n"
        if len(tests) > MAX_TESTS_FOR_TELEGRAM_REPORT:
            message += f"\t\t\t<code>And {len(tests) - MAX_TESTS_FOR_TELEGRAM_REPORT} more {status} tests...</code>\n"
    return message


def create_keyboard(report_link):
    keyboard = [
        [InlineKeyboardButton("🔗 Link to report", url=report_link)],
        [InlineKeyboardButton("🔄 Restart the tests", callback_data='confirm_restart')],
        InlineKeyboardButton("🇺🇦 Stop Russian Aggression", url='https://war.ukraine.ua/')
    ]
    return InlineKeyboardMarkup(keyboard)


def send_photo_and_message(token, chat_id, photo_path, total, passed, failed, broken, skipped, report_link,
                           allure_report_path):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    message = f"\n\n•••\n\n"
    message += f"<b>• Total ({total})</b>\n\n"
    if int(passed) > 0:
        message += f"<b>• Passed ({passed})</b>\n\n"

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

    # Check if the message exceeds the limit
    if len(message) > MAX_SYMBOLS_FOR_MESSAGE:
        message = message[:MAX_SYMBOLS_FOR_MESSAGE] + "\n\nThe message is too large, check out the full Allure report."

    message = message.rstrip()
    message += "\n\n•••\n\n"

    print(f"Sending message: {message}")  # Log the message before sending
    with open(photo_path, 'rb') as photo:
        files = {'photo': photo}
        reply_markup = create_keyboard(report_link)
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
    send_photo_and_message(token, chat_id, photo_path, total, passed, failed, broken, skipped, report_link,
                           allure_report_path)
