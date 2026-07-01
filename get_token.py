"""
Получение VK токена вручную через браузер.
Запустите: python get_token.py
"""
import webbrowser
import urllib.parse
import re
import sys

APP_ID = "6287487"
SCOPE = "status,offline"
REDIRECT = "https://oauth.vk.com/blank.html"

params = urllib.parse.urlencode({
    "client_id": APP_ID,
    "scope": SCOPE,
    "redirect_uri": REDIRECT,
    "display": "page",
    "response_type": "token",
    "v": "5.131",
})
url = f"https://oauth.vk.com/authorize?{params}"

print("Открываю страницу авторизации ВКонтакте...")
webbrowser.open(url)

print("""
После входа браузер перейдёт на пустую страницу.
Скопируйте ВСЮ адресную строку и вставьте сюда:
""")

raw = input("> ").strip()

# Вытащить токен и user_id из URL или принять как сырой токен
token_match = re.search(r"access_token=([^&]+)", raw)
uid_match = re.search(r"user_id=([^&]+)", raw)

token = token_match.group(1) if token_match else raw
user_id = uid_match.group(1) if uid_match else ""

if not token:
    print("Токен не найден. Попробуйте снова.")
    sys.exit(1)

print(f"\nТокен: {token[:20]}...")
if user_id:
    print(f"User ID: {user_id}")

# Сохранить в .env
try:
    with open(".env", "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    lines = []

new_lines, replaced_token, replaced_uid = [], False, False
for line in lines:
    if line.startswith("VK_TOKEN="):
        new_lines.append(f"VK_TOKEN={token}\n")
        replaced_token = True
    elif line.startswith("VK_USER_ID="):
        new_lines.append(f"VK_USER_ID={user_id}\n")
        replaced_uid = True
    else:
        new_lines.append(line)

if not replaced_token:
    new_lines.append(f"VK_TOKEN={token}\n")
if not replaced_uid:
    new_lines.append(f"VK_USER_ID={user_id}\n")

with open(".env", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("\nСохранено в .env. Запускайте: python main.py")
