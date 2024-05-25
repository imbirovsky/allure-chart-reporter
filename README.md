# Allure Chart Reporter

<img src="https://qaband.com/wp-content/uploads/telegram_slack.png" width="720">


Welcome to the Allure Chart Reporter project!

This is a test automation framework that leverages the power of `Python`, `Kotlin`, `Maven` and `GitHub Actions`
to provide a comprehensive testing solution.

The project includes a `GitHub Actions workflow` that automates the process of running tests, generating an Allure test
report, and sending a summary of the test results along with a chart to Telegram and Slack.

This project is designed to be run on GitHub Actions, making it a great choice for teams looking for a CI/CD integrated
testing solution. Whether you're a developer looking to catch bugs early or a QA engineer seeking to automate your test
runs, Allure Chart Reporter has got you covered.

Read on to learn more about how to set up and use this project.

## Table of Contents

- [Allure Chart Reporter](#allure-chart-reporter)
- [Getting Started](#getting-started)
    - [**Using this implementation in your own project**](#using-this-implementation-in-your-own-project)
- [main.yml](#mainyml)
    - [Workflow Triggers](#workflow-triggers)
    - [Environment Variables](#environment-variables)
    - [Workflow Steps](#workflow-steps)
    - [Secrets](#secrets)
- [Test Results Chart Generator (generate_chart.py)](#test-results-chart-generator-generate_chartpy)
    - [Requirements](#requirements)
    - [Usage](#usage)
    - [Customization](#customization)
- [Telegram Test Results Notifier](#telegram-test-results-notifier)
    - [Requirements](#requirements-1)
    - [Environment Variables](#environment-variables-1)
    - [Usage](#usage-1)
    - [Customization](#customization-1)
    - [Additional Features](#additional-features)
- [Slack Test Results Notifier (send_slack.py)](#slack-test-results-notifier-send_slackpy)
- [Tests Classes](#tests-classes)

## Getting Started

This project is designed to be run on GitHub Actions. The workflow is configured to run tests, generate a test report,
and send a summary of the test results along with a chart to Telegram and Slack.

To get started with this project:

1. Fork or clone the repository to your own GitHub account.
2. Navigate to the 'Actions' tab in your GitHub repository and enable GitHub Actions if it's not already enabled.

   
> **Note**: GitHub Pages is a paid feature. You don't necessarily have to use it. In any case, you will receive a summary of the test results along with a chart, but without the ability to open the full report (button '🔗 Link to report'). 
> To do this, you need to fill in the value for ALLURE_LINK with a link (e.g. https://github.com/)


3. Set up the necessary secrets in the 'Secrets' section under 'Settings' in your GitHub repository. The required
   secrets are
    - `ALLURE_LINK`: the link to the Allure report (your GitHub project - Settings - Pages - Your site is published
      at `https://<username>.github.io/<repository>/`)

    - `PERSONAL_ACCESS_TOKEN`: a personal access token with the `repo` scope (GitHub - Settings - Developer settings -
      Personal access tokens - Generate new token - Select `repo` scope - Generate token - Copy token)
    - `TELEGRAM_BOT_TOKEN`: the token for your Telegram bot
    - `TELEGRAM_CHAT_ID`: the chat ID for your Telegram bot
    - `SLACK_BOT_TOKEN`: the token for your Slack bot
    - `SLACK_CHAT_ID`: the chat ID for your Slack bot

<img src="https://qaband.com/wp-content/uploads/github_secrets.png" width="560">
      
4. After this, you need to run the tests. Once the tests are passed, a `reports` branch will be created.
5. Set up GitHub Pages:
    - go to your repository on GitHub
    - click on the "Settings" tab
    - scroll down to the "GitHub Pages" section
    - in the "Source" dropdown menu, select the `reports` branch
    - click "Save"
   
<img src="https://qaband.com/wp-content/uploads/github_pages.png" width="560">

6. After this, you can run the tests in one of the following ways (`main.yml`):
    - `on: push`: the tests will run every time you push changes to the repository.
    - `on: schedule`: the tests will run on a schedule (e.g. every day at 12:00).
    - `on: workflow_dispatch`: the tests will run manually.To do this:
        - go to your GitHub repository
        - click on the "Actions" tab
        - in the left sidebar, click the workflow you want to run
        - above the list of workflow runs, select "Run workflow"
        - select the branch where the workflow will run and click the "Run workflow" button
    - `on: repository_dispatch`: the tests will run when you send a POST request to the repository.

7. After the tests are run, you will receive a summary of the test results along with a chart in Telegram / Slack.

**Please note that this project is not designed to be run locally on your machine.**


### Using this implementation in your own project

If you do not wish to clone or fork the entire project, but want to use this implementation in your own project, you need to:  
- Copy the `main.yml` file to your project at the path `.github/workflows/`
- Copy the `generate_chart.py` file to your project at the path `chart/generate_chart.py`
- Copy the `font.ttf` file to your project at the path `chart/font.ttf`
- Copy the `send_telegram.py` file to your project at the path `chart/send_telegram.py`
- Copy the `send_slack.py` file to your project at the path `chart/send_slack.py`

The structure of the project should be as follows:

<pre>
├── .github
│   └── workflows
│       └── main.yml
├── chart
│   ├── font.ttf
│   ├── generate_chart.py
│   ├── send_slack.py
│   └── send_telegram.py
└── src
    └── test
 </pre>

## main.yml

### Workflow Triggers

The workflow can be triggered in one of the following ways:

- `on: schedule`: on a schedule (e.g., at midnight every day)
- `on: workflow_dispatch`: manually, from the GitHub UI
- `on: repository_dispatch`: from an external event by calling GitHub's API
- `on: push`: whenever you push changes to the repository

### Environment Variables

The workflow uses the following environment variables:

- `TEST_REPORT_URL`: the URL of the Allure test report
- `ALLURE_RESULT_DIR`: the directory where Allure results are stored

### Workflow Steps

The workflow consists of the following steps:

1. Checkout the repository.
2. Set up JDK.
3. Run tests using Maven.
4. Load test report history.
5. Build the test report using Allure.
6. Publish the test report to GitHub Pages.
7. Install `jq` for processing JSON data.
8. Generate a message for the test report.
9. Install Python and the required packages.
10. Generate a chart based on the test results.
11. Upload the chart as an artifact.
12. Download the chart artifact.
13. Send a notification to Telegram with the test results and the chart.
14. Send a notification to Slack with the test results and the chart.

### Secrets

The workflow requires the following secrets:

- `ALLURE_LINK`: the link to the Allure report
- `PERSONAL_ACCESS_TOKEN`: a personal access token with the `repo` scope
- `TELEGRAM_BOT_TOKEN`: the token for your Telegram bot
- `TELEGRAM_CHAT_ID`: the chat ID for your Telegram bot
- `SLACK_BOT_TOKEN`: the token for your Slack bot
- `SLACK_CHAT_ID`: the chat ID for your Slack bot

Please ensure that these secrets are set in the 'Secrets' section under 'Settings' in your GitHub repository.

## Test Results Chart Generator (generate_chart.py)

<img src="https://qaband.com/wp-content/uploads/chart.png" width="560">

This Python script generates a pie chart of test results and saves it as a PNG image. The chart shows the number and
percentage of tests that passed, failed, were broken, or were skipped.
Script uses data from `summary.json` file that is generated by Allure.

### Requirements

- Python 3
- matplotlib
- PIL (Pillow)
- A custom font file (TTF format)

### Usage

Run the script from the command line with the following arguments:

```bash
python generate_chart.py total passed failed broken skipped sum_duration
```

Where:

- `total` is the total number of tests.
- `passed` is the number of tests that passed.
- `failed` is the number of tests that failed.
- `broken` is the number of tests that were broken.
- `skipped` is the number of tests that were skipped.
- `sum_duration` is the total duration of all tests in milliseconds.

The script will generate a pie chart and save it as `chart.png` in the current directory.

## Customization

You can customize the appearance of the chart by modifying the following variables in the script:

- `LOGO_NAME`: the name that appears at the top of the legend. Currently, this is set to 'qaband.com'. You can change
  this to any string you like, and the new value will be displayed on the chart.
- `CUSTOM_FONT`: the font properties object for the custom font.

You can also customize the colors of the pie slices by modifying the `data` list in the `generate_chart` function.

## Telegram Test Results Notifier

<img src="https://qaband.com/wp-content/uploads/telegram.png" width="560">

This Python script sends a summary of test results along with a chart to a specified Telegram chat. The summary includes
the total number of tests, and the number of tests that passed, failed, were broken, or were skipped.

### Requirements

- Python 3
- requests
- telegram

### Environment Variables

The script uses the following environment variables:

- `GITHUB_RUN_ID`: the ID of the GitHub Actions run.
- `GITHUB_RUN_NUMBER`: the number of the GitHub Actions run.
- `GITHUB_REPOSITORY`: the name of the GitHub repository.

### Usage

Run the script from the command line with the following arguments:

```bash
python send_telegram.py token chat_id photo_path total passed failed broken skipped report_link allure_report_path
```

Where:

- `token` is the token for your Telegram bot
- `chat_id` is the chat ID for your Telegram bot
- `photo_path` is the path to the chart image
- `total` is the total number of tests
- `passed` is the number of tests that passed
- `failed` is the number of tests that failed
- `broken` is the number of tests that were broken
- `skipped` is the number of tests that were skipped
- `report_link` is the URL of the Allure test report
- `allure_report_path` is the directory where Allure results are stored

> **It should be noted that if the test Failed / Broken / Skipped = 0, then the block with the status where the tests are 0 will not be displayed in the Telegram message**.

### Customization

You can customize the appearance of the message by modifying the `format_test_message` function in the script.
The maximum number of tests to report in the message can be adjusted by changing the `MAX_TESTS_FOR_TELEGRAM_REPORT`
variable

### Additional Features
By default, the test name will be used for display in the list of failed / broken / skipped tests.

Also, it's important to note that the ability to add a request and response code to the test name has been
implemented. To do this, you need to update the test name as follows:

```kotlin
    fun updateTestNameForAllureReport(param: String) {
    val lifecycle = Allure.getLifecycle()
    lifecycle.updateTestCase { testResult: TestResult ->
        testResult.name += param
    }
}
```

Where

- `param`: is the string that you want to add to the test name. Pass the request here.

Here's how you can use this for all GET requests:

```kotlin

private val requestData = "${HTTPS}${URL}${ACTION}${RANDOM}"
// https://api.chucknorris.io/jokes/random

  fun sendGetRequest(requestUrl: String, code: Int = 200, contentType: String = "application/json"): ValidatableResponse {
    updateTestNameForAllureReport("\n$requestUrl")
    val response = sendRequest().contentType(contentType).get(requestUrl).then()
    logResponse(response)
    response.statusCode(code)
    return response
}
```

In report you will see:

```
   • Get information about country
   https://restcountries.com/v3.1/name/country_404   
   404 Not Found
```

When a request is present in the test name, the response code will be displayed in the Allure report:

<img src="https://qaband.com/wp-content/uploads/telegram_with_url_and_code.png" width="480">

## Slack Test Results Notifier (send_slack.py)

<img src="https://qaband.com/wp-content/uploads/slack.png" width="560">

This Python script sends a summary of test results along with a chart to a specified Slack channel. The summary includes
the total number of tests, and the number of tests that passed, failed, were broken, or were skipped.

> The logic of the script is similar to the logic of the script for Telegram. The difference is that in Slack, the text and image will be sent as two separate messages.

The difference is the formatting of the message for Slack and the use of a different API to send the message and image.

## Tests Classes

The project includes a set of test classes that demonstrate how to write tests using the `RestAssured` library.

`TestNG` is used as the test framework.

The tests are written in `Kotlin` and are designed to test a simple REST API.

Using the `Allure` library, the tests generate a report that includes information about the test results, request and
response details, and test duration.

`Data Provider` is used to pass parameters to the test methods.

The test classes include the following:

- `constants.Constants.kt`: contains constants used in the tests
- `helpers.AllureHelper.kt`: contains helper function for update test name
- `helpers.RequestHelper.kt`: contains helper functions for sending requests
- `tests.ChuckNorrisJokesTests.kt`: contains tests for checking all statuses (failed, passed, broken, skipped). The tests use the [Chuck Norris Jokes API](https://api.chucknorris.io/), which is free to use.
- `resources.json_schemes`: contains JSON schemas for checking the response body

## 🇺🇦 Support Ukraine

In these challenging times, Ukraine needs the support of the global community. Consider making a donation to help the people of Ukraine. Every contribution, no matter how small, can make a difference.

You can donate through the following platforms:

- [Come Back Alive](https://savelife.in.ua/en/donate/)
- [AZOV](https://www.azov.one/en/donate/)
- [UNITED24](https://u24.gov.ua/)

Remember, every little bit helps. 

Thank you for your support ❤️