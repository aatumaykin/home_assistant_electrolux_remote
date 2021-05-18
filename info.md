# Electrolux remote device Component for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

**This component will set up the following platforms.**

| Platform        | Description                         |
| --------------- | ----------------------------------- |
| `climate`       | Add climate entity                  |

{% if not installed %}

## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Electrolux remote".

{% endif %}

{%- if version_installed == "main" %}

## You are running main!

This is **only** intended for development!

{%- elif (version_installed.replace("v", "").split(".")[0] | int) < 1 %}
## Version 0.0.9

### Features
- добавлены переключатели для конвекторов с типом conv и convector24
- добавлена поддержка бойлера Ballu Smart
- для всех устройств добавлен режим OFF

### Fix
- исправлены ошибки

## Version 0.0.8

### Features
- добавил appcode для устройств Ballu

## Version 0.0.7

### Features
- обработка команд climate.turn_off и climate.turn_on

## Version 0.0.6

### Features
- мелкие правки

## Version 0.0.5

### Fix
- исправлена установка

## Version 0.0.4

### Changes
- переписал логику компонентов с использованием координатора
- переработал логику кнопок вкл/выкл и auto для конвектора
- убрал пресет auto для термостата
  
### Fix
- strings.json

## Version 0.0.3

### Features
- в Climate Entity добавлены атрибуты от термостата и конвектора
- рефакторинг

## Version 0.0.2

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
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-4.png?raw=true" width="250">

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/Ailme/home_assistant_electrolux_remote.svg
[commits]: https://github.com/Ailme/home_assistant_electrolux_remote/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[license-shield]: https://img.shields.io/github/license/Ailme/home_assistant_electrolux_remote.svg
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40Ailme-blue.svg
[releases-shield]: https://img.shields.io/github/release/Ailme/home_assistant_electrolux_remote.svg
[releases]: https://github.com/Ailme/home_assistant_electrolux_remote/releases
[user_profile]: https://github.com/Ailme
