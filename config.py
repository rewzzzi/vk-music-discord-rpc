import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.vk_token: str = os.getenv("VK_TOKEN", "")
        self.vk_user_id: str = os.getenv("VK_USER_ID", "")
        self.discord_client_id: str = os.getenv("DISCORD_CLIENT_ID", "")
        self.poll_interval: int = int(os.getenv("POLL_INTERVAL", "5"))

        if not self.vk_token:
            raise ValueError("VK_TOKEN не указан. Заполните .env файл.")
        if not self.discord_client_id:
            raise ValueError("DISCORD_CLIENT_ID не указан. Заполните .env файл.")
