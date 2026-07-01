import time
import logging
from pypresence import Presence, InvalidID, DiscordNotFound, PipeClosed

log = logging.getLogger(__name__)


class DiscordRPC:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self._rpc: Presence | None = None
        self._track_start: float = 0.0
        self._connect()

    def _connect(self) -> bool:
        try:
            rpc = Presence(self.client_id)
            rpc.connect()
            self._rpc = rpc
            log.info("Подключено к Discord RPC")
            return True
        except (DiscordNotFound, InvalidID, FileNotFoundError):
            log.warning("Discord не запущен или приложение не найдено")
            self._rpc = None
            return False
        except Exception as e:
            log.warning(f"Ошибка подключения к Discord: {e}")
            self._rpc = None
            return False

    def update(self, track: dict) -> None:
        if self._rpc is None:
            if not self._connect():
                return

        try:
            resp = self._rpc.update(
                details=track["title"],
                state=track["artist"],
                start=int(self._track_start),
            )
            log.info(f"Discord ответил: {resp}")
        except (PipeClosed, AttributeError):
            log.warning("Discord RPC соединение разорвано, переподключение...")
            self._rpc = None
            self._connect()
        except Exception as e:
            log.error(f"Ошибка обновления Discord RPC: {e}")

    def clear(self) -> None:
        if self._rpc is None:
            return
        try:
            self._rpc.clear()
        except Exception:
            pass

    def set_track_start(self) -> None:
        self._track_start = time.time()

    def close(self) -> None:
        if self._rpc:
            try:
                self._rpc.close()
            except Exception:
                pass
