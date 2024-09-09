# SNow 2 Slack Bot

## Overview

The Snow 2 Slack Bot project is designed to interact with ServiceNow data and provide useful information within Slack.
It leverages the Slack Bolt framework and ServiceNow APIs to fetch and display data related to tasks, request items, requests,
incidents, and change requests.
The dedicated ServiceNow application offers many features, and this bot provides **only** details for ServiceNow links. The [slack_manifest.yaml](slack_manifest.yaml)
file can be used for Slack application creation.
Extra permissions in [slack_manifest.yaml](slack_manifest.yaml)  are needed for adding info cards on reaction added to messages where the bot is added.
If this feature is not needed, many of these permissions can be removed.

## Features

- Handle link shared events and unfurl ServiceNow links in Slack.
- Handle reaction added events to fetch and display ServiceNow data.
- Unified data fetching for various ServiceNow entities.
- Slack app home tab with a welcome message.

## Prerequisites

- Python 3.6+
- Slack App with necessary permissions
- ServiceNow instance with API access

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/slack.card.integration.git
    cd slack.card.integration
    ```

2. Modify the ServiceNow mapping file [snow_maps.py](src/lib/snow_maps.py) and check the `build_snow_url` method in [snow_data_helper.py](src/lib/snow_data_helper.py) to ensure your ServiceNow instance has the same URL pattern.

   Also, if using [slack_manifest.yaml](slack_manifest.yaml), adjust the ServiceNow domain in the `unfurl_domains` node.

3. Build the Docker image and provide the `.env` file as a parameter at runtime:
    ```sh
    docker build -t snow2slack-bot .
    docker run --env-file .env snow2slack-bot
    ```

4. Alternatively create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
   and install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root directory and add the following environment variables (you can copy the [bot.env.example](config/bot.env.example) file as a template):
    ```env
    SLACK_APP_ID=your_slack_app_id
    BOT_TOKEN=your_slack_bot_token
    APP_TOKEN=your_slack_app_token
    SN_HOST=your_servicenow_host
    SN_USER=your_servicenow_username
    SN_PASS=your_servicenow_password
    SLACK_REACTION_EMOJI=snow_cloud
    SN_TASK_REGEXP=SCTASK[0-9]{7}
    SN_REQ_ITEM_REGEXP=RITM[0-9]{7}
    SN_REQ_REGEXP=REQ[0-9]{7}
    SN_INC_REGEXP=INC[0-9]{7}
    ```

## Usage

1. Start the Slack bot:
   Run Docker:
   ```sh
   docker run --env-file .env snow2slack-bot
   ``` 
   OR after activation of virtual environment:
   ```sh
   python snow2slack-bot.py
    ```

2. The bot will listen for link shared and reaction added events in Slack and respond accordingly.

## Project Structure

- `snow2slack-bot.py`: Entry point for the Slack bot.
- `src/Core.py`: Core configuration and initialization of the Slack app and ServiceNow helper.
- `src/lib/snow_data_helper.py`: Helper class for interacting with ServiceNow data.
- `app_actions_snow.py`: Event handlers for Slack events.
- `helpers/http-client.private.env.json`: ServiceNow credentials for development.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.