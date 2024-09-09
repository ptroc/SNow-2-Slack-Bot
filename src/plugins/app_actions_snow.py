import re

from src import Core


@Core.app.event("link_shared")
def handle_link_shared_event(ack, body, logger):
    """
    Handle link shared event for ServiceNow links and unfurl them. Supports sc_task, sc_req_item, sc_request,
    incident and change_request.

    :param ack: Acknowledge function to confirm receipt of the event
    :param body: Event payload containing details of the shared link
    :param logger: Logger instance for logging information
    """
    ack()
    # logger.info(body)
    event = body["event"]
    channel_id = event["channel"]
    message_ts = event["message_ts"]
    logger.info("Link shared event")
    unfurls = {}

    for link in event['links']:
        if "sys_id" in link['url'] and "/target/" in link['url']:
            logger.info(f"URL: {link['url']}")
            url_data = Core.sdh.parse_snow_url(link['url'])
            logger.info(f"URL data: {url_data}")
            if "/target/sc_task.do" in link['url']:
                unfurls[link['url']] = __create_unfurls(Core.sdh.get_data_for_sc_task(sys_id=url_data["sys_id"]))
            elif "/target/sc_req_item.do" in link['url']:
                unfurls[link['url']] = __create_unfurls(Core.sdh.get_data_for_sc_req_item(sys_id=url_data["sys_id"]))
            elif "/target/sc_request.do" in link['url']:
                unfurls[link['url']] = __create_unfurls(Core.sdh.get_data_for_sc_request(sys_id=url_data["sys_id"]))
            elif "/target/incident.do" in link['url']:
                unfurls[link['url']] = __create_unfurls(Core.sdh.get_data_for_incident(sys_id=url_data["sys_id"]))
            elif "/target/change_request.do" in link['url']:
                unfurls[link['url']] = __create_unfurls(Core.sdh.get_data_for_change_request(sys_id=url_data["sys_id"]))
            else:
                continue

    Core.app.client.chat_unfurl(channel=channel_id, ts=message_ts, unfurls=unfurls)


@Core.app.event("reaction_added")
def handle_reaction_added_events(body, say, logger):
    """
    Handle reaction added events for ServiceNow task, request item, request, and incident numbers.

    :param body: Event payload containing details of the reaction
    :param say: Function to send a message to the channel
    :param logger: Logger instance for logging information
    """
    if body["event"]["reaction"] != Core.SLACK_REACTION_EMOJI or body["event"]["item"]["type"] != "message":
        return
    message_ts = body["event"]["item"]["ts"]
    channel_id = body["event"]["item"]["channel"]
    history_query = Core.app.client.conversations_history(
        channel=channel_id,
        inclusive=True,
        oldest=message_ts,
        limit=1
    )
    src_msg_txt = history_query["messages"][0]['text']

    # Check for ServiceNow task, request item, request and incident numbers

    # Check ServiceNow request task
    regex = rf"({Core.SN_TASK_REGEXP})"
    matches = re.finditer(regex, src_msg_txt, re.MULTILINE | re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=1):
        __sc_task_data = Core.sdh.get_sc_task_data_by_effective_number(match.group())

        if "request_item" in __sc_task_data[0]:
            request_item_data = Core.sdh.get_sc_req_item_data(sys_id=__sc_task_data[0]["request_item"]["value"])
        else:
            request_item_data = None
        out = __create_unfurls(Core.sdh.unify_data_for__sc_task(task_data=__sc_task_data[0],
                                                                request_item_data=request_item_data))

        say(blocks=out['blocks'], thread_ts=message_ts)
        # logger.info(out)

    # Check ServiceNow request item
    regex = rf"({Core.SN_REQ_ITEM_REGEXP})"
    matches = re.finditer(regex, src_msg_txt, re.MULTILINE | re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=1):
        __sc_req_item_data = Core.sdh.get_sc_req_item_data_by_effective_number(match.group())
        out = __create_unfurls(Core.sdh.unify_data_for__sc_req_item(__sc_req_item_data[0]))
        say(blocks=out['blocks'], thread_ts=message_ts)
        # logger.info(out)

    # Check ServiceNow request
    regex = rf"({Core.SN_REQ_REGEXP})"
    matches = re.finditer(regex, src_msg_txt, re.MULTILINE | re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=1):
        __sc_request_data = Core.sdh.get_sc_request_data_by_effective_number(match.group())
        out = __create_unfurls(Core.sdh.unify_data_for__sc_req_item(__sc_request_data[0]))
        say(blocks=out['blocks'], thread_ts=message_ts)
        # logger.info(out)

    # Check ServiceNow incident
    regex = rf"({Core.SN_INC_REGEXP})"
    matches = re.finditer(regex, src_msg_txt, re.MULTILINE | re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=1):
        _incident_data = Core.sdh.get_incident_data_by_effective_number(match.group())
        out = __create_unfurls(Core.sdh.unify_data_for__incident(_incident_data[0]))
        say(blocks=out['blocks'], thread_ts=message_ts)
        # logger.info(out)


def __create_unfurls(data: dict):
    """
    Create unfurls for Slack messages.

    :param data: Data to be unfurled
    :return: Dictionary containing the unfurled message blocks
    """
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": data['task_effective_number'],
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description*:\n{data['short_description']}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Created:*\n{data['sys_created_on']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Priority:*\n{data['priority']}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Last updated by:*\n{data['sys_updated_by']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Last updated:*\n{data['sys_updated_on']}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Created by:*\n{data['sys_created_by']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*State:*\n{data['state']}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{data['target_link']}|View item>"
                }
            }
        ]
    }


@Core.app.event("message")
def handle_message_events(body, logger):
    """
    Handle message events.

    :param body: Event payload containing details of the message
    :param logger: Logger instance for logging information
    """
    pass