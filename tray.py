import pystray
from PIL import Image, ImageDraw, ImageFont


def _make_image() -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill="#0077FF")
    try:
        font = ImageFont.truetype("arialbd.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
    d.text((size // 2, size // 2), "VK", fill="white", anchor="mm", font=font)
    return img


class TrayIcon:
    def __init__(self, on_quit):
        self._on_quit = on_quit
        self._track_label = "Ничего не играет"
        self._icon = pystray.Icon(
            name="vk_music_rpc",
            icon=_make_image(),
            title="VK Music → Discord",
            menu=self._build_menu(),
        )

    def _build_menu(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(self._track_label, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Выйти", self._quit),
        )

    def _quit(self, icon, item):
        self._on_quit()
        icon.stop()

    def set_track(self, track: dict | None) -> None:
        if track:
            self._track_label = f"{track['artist']} — {track['title']}"
        else:
            self._track_label = "Ничего не играет"
        self._icon.menu = self._build_menu()
        self._icon.title = f"VK Music: {self._track_label}"

    def run(self) -> None:
        self._icon.run()
