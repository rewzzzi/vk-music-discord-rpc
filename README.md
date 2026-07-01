# VK Music → Discord RPC

Отображает текущий трек из ВКонтакте в статусе активности Discord.

![Python](https://img.shields.io/badge/Python-3.10+-blue)

## Как выглядит

В профиле Discord появляется (пример):
```
🎵 VK Music
   for her
   whatsaheart
   0:42
```

## Требования

- Python 3.10+
- Discord (десктоп)
- Аккаунт ВКонтакте с включённой трансляцией музыки в статус

## Установка

```bash
git clone https://github.com/rewzzzi/vk-music-discord-rpc
cd vk-music-discord-rpc
pip install -r requirements.txt
```

## Настройка

### 1. Токен ВКонтакте

```bash
python get_token.py
```

Откроется браузер → авторизуйтесь → скопируйте всю адресную строку и вставьте в терминал. Токен сохранится автоматически.

> Если часто меняется IP / используется VPN — скрипт поддерживает авторизацию через Kate Mobile, токены которой не привязаны к IP.

### 2. Discord приложение

1. Откройте [discord.com/developers/applications](https://discord.com/developers/applications)
2. **New Application** → введите имя (например `VK Music`)
3. Скопируйте **Application ID**

### 3. Файл конфигурации

```bash
cp .env.example .env
```

Заполните `.env`:

```env
VK_TOKEN=ваш_токен
VK_USER_ID=ваш_id  # необязательно, определяется автоматически
DISCORD_CLIENT_ID=id_вашего_приложения
POLL_INTERVAL=5
```

### 4. Включить трансляцию в ВКонтакте

Музыка → ⋮ → **Транслировать музыку в статус**

### 5. Включить отображение в Discord

Настройки → Настройки активности → **Отображать текущую активность как сообщение о статусе**

## Запуск

**С терминалом** (видны логи):
```bash
python main.py
```

**Без терминала** (фоновый режим с иконкой в трее):

Двойной клик на `start.pyw`

Иконка VK появится в системном трее. Правая кнопка → текущий трек / Выйти.

### Автозапуск с Windows

Нажмите `Win + R` → введите `shell:startup` → скопируйте туда ярлык на `start.pyw`.

## Зависимости

|      Пакет      |       Назначение        |
|-----------------|-------------------------|
| `pypresence`    | Discord Rich Presence   |
| `requests`      | VK API                  |
| `python-dotenv` | Конфигурация            |
| `pystray`       | Иконка в трее           |
| `Pillow`        | Отрисовка иконки        |
| `vk_api`        | Авторизация в ВКонтакте |
