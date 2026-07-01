import requests
import logging

log = logging.getLogger(__name__)

API_URL = "https://api.vk.com/method"
API_VERSION = "5.131"


class VKClient:
    def __init__(self, token: str, user_id: str = ""):
        self.token = token
        self.user_id = user_id
        self.session = requests.Session()

    def _call(self, method: str, **params) -> dict:
        params["access_token"] = self.token
        params["v"] = API_VERSION
        if self.user_id:
            params.setdefault("user_id", self.user_id)

        r = self.session.get(f"{API_URL}/{method}", params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        if "error" in data:
            err = data["error"]
            raise RuntimeError(f"VK API {err['error_code']}: {err['error_msg']}")

        return data["response"]

    def get_current_track(self) -> dict | None:
        """Возвращает текущий трек из статуса или None если ничего не играет."""
        status = self._call("status.get")

        audio = status.get("audio")
        if not audio:
            return None

        return {
            "artist": audio.get("artist", "Unknown"),
            "title": audio.get("title", "Unknown"),
            "duration": audio.get("duration", 0),
            "id": f"{audio.get('owner_id')}_{audio.get('id')}",
        }

    def get_self_user_id(self) -> str:
        users = self._call("users.get")
        return str(users[0]["id"])
