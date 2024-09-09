import logging
import os

from slack_bolt import App

from src.lib.snow_data_helper import SnowDataHelper

log_level = logging.INFO
_logger = logging
_logger.basicConfig(format='[%(asctime)s] %(levelname)s %(process)d --- [%(threadName)s] %(funcName)s: %(message)s',
                    level=log_level)

version = "v0.11"
SLACK_APP_ID = os.getenv('SLACK_APP_ID')
SLACK_REACTION_EMOJI = os.getenv('SLACK_REACTION_EMOJI')
SN_TASK_REGEXP = os.getenv('SN_TASK_REGEXP')
SN_REQ_ITEM_REGEXP = os.getenv('SN_REQ_ITEM_REGEXP')
SN_REQ_REGEXP = os.getenv('SN_REQ_REGEXP')
SN_INC_REGEXP = os.getenv('SN_INC_REGEXP')

# check if the environment variables are set
if (not SLACK_APP_ID or not SLACK_REACTION_EMOJI
        or not SN_TASK_REGEXP or not SN_REQ_ITEM_REGEXP
        or not SN_REQ_REGEXP or not SN_INC_REGEXP):
    _logger.error("Environment variables are not set")
    exit(1)

app: App = App(token=os.getenv('BOT_TOKEN'), logger=_logger.getLogger())
sdh: SnowDataHelper = SnowDataHelper(log_level=log_level, sn_host=os.getenv('SN_HOST'),
                                     sn_pass=os.getenv('SN_PASS'), sn_user=os.getenv('SN_USER'))


def check_msg(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
        logging.info(f"{message['user']}: {message['text'].strip()}")
        next()


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        view_dict = {
            "type": "home",
            "blocks": [
                {"type": "header",
                 "text": {
                     "type": "plain_text",
                     "text": f"Hi Im your friendly SNOW Bot :robot_face:, version: {version}",
                     "emoji": True
                 }
                 },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Welcome home :house:*"}
                }
            ]
        }

        client.views_publish(
            user_id=event["user"],
            view=view_dict
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


def get_actor_email(user_id: str) -> (str, dict):
    actor_user_data = app.client.users_profile_get(user=user_id)
    actor_email = actor_user_data.data['profile']['email']
    return actor_email, actor_user_data
