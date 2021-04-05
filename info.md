# Electrolux remote device Component for Home Assistant

{%- if version_installed == "main" %}

## You are running main!

This is **only** intended for development!

{%- elif (version_installed.split(".")[0] | int) < 1 %}
## Version 0.0.2 (unreleased)

### Features
- добавлен минимальный функционал для термостата
- добавлены названия для устройств, если задано название помещения в приложении
- рефакторинг

## [Version 0.0.1](https://github.com/Ailme/home_assistant_electrolux_remote/releases/tag/v0.0.1)

### Features
Добавлена поддержка только одного вида конвекторов, которые в приложении обозначены как "convector24"

Управление конвектором:
- вкл/выкл
- изменение температуры
- переключение режимов

{% endif %}

## Usage:
Компонент работает через облако эмулируя работу приложения Home Comfort: climatic appliances

- установить компонент либо в custom_components (через копирование либо через HACS)
- перейти в интеграции HA и найти в поиске "Electrolux Remote"
- заполнить логин/пароль от приложения Home Comfort: climatic appliances
- после авторизации на сервере автоматически должно добавиться устройство Climate связанное с конвектором


## Screenshot
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-1.png?raw=true" width="250">
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-2.png?raw=true" width="250">
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-3.png?raw=true" width="250">
