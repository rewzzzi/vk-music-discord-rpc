import logging
import sys
import threading
from config import Config
from vk import VKClient
from discord_rpc import DiscordRPC
from tray import TrayIcon

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

_stop = threading.Event()


def worker(config: Config, vk: VKClient, rpc: DiscordRPC, tray: TrayIcon) -> None:
    current_id: str | None = None

    while not _stop.is_set():
        try:
            track = vk.get_current_track()

            if track is None:
                if current_id is not None:
                    log.info("Музыка остановлена")
                    rpc.clear()
                    tray.set_track(None)
                    current_id = None
            elif track["id"] != current_id:
                current_id = track["id"]
                rpc.set_track_start()
                log.info(f"Сейчас играет: {track['artist']} — {track['title']}")
                rpc.update(track)
                tray.set_track(track)
            else:
                rpc.update(track)

        except Exception as e:
            log.error(f"Ошибка: {e}")

        _stop.wait(config.poll_interval)

    rpc.clear()
    rpc.close()


def main() -> None:
    try:
        config = Config()
    except ValueError as e:
        print(f"\nОшибка конфигурации: {e}")
        print("Скопируйте .env.example в .env и заполните токены.\n")
        sys.exit(1)

    vk = VKClient(config.vk_token, config.vk_user_id)
    rpc = DiscordRPC(config.discord_client_id)

    if not config.vk_user_id:
        try:
            uid = vk.get_self_user_id()
            vk.user_id = uid
            log.info(f"VK user id: {uid}")
        except Exception as e:
            log.error(f"Не удалось получить VK user id: {e}")

    tray = TrayIcon(on_quit=_stop.set)

    t = threading.Thread(target=worker, args=(config, vk, rpc, tray), daemon=True)
    t.start()

    log.info("Запущено. Иконка в трее — правая кнопка для выхода.")
    tray.run()  # Блокирует до выхода из трея


if __name__ == "__main__":
    main()
