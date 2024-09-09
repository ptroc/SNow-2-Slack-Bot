import os

from slack_bolt.adapter.socket_mode import SocketModeHandler

from src import Core


if __name__ == "__main__":
    SocketModeHandler(app=Core.app, app_token=os.getenv('APP_TOKEN')).start()
