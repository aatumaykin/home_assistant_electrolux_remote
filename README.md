# Electrolux remote device Component for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]



Компонент работает через облако эмулируя работу приложения Home Comfort: climatic appliances и Ballu Home

## Usage:
- установить компонент либо в custom_components (через копирование либо через HACS)
- перейти в интеграции HA и найти в поиске "Electrolux Remote"
- заполнить логин/пароль от приложения Home Comfort: climatic appliances
- в зависимости от производителя в поле appcode выбрать Electrolux или Ballu
- после авторизации на сервере в интеграции должны появиться устройства

## Features
Поддерживаются устройства Electrolux и Ballu:
- конвекторы Electrolux с блоком управления Transformer Electronic
- конвекторы Ballu с блоком управления Transformer Digital Inverter
- термостат Electrolux ETS-16
- бойлеры (Сenturio IQ, Centurio IQ 2.0, Smart)

## Screenshot
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-1.png?raw=true" width="250">
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-2.png?raw=true" width="250">
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-3.png?raw=true" width="250">
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-4.png?raw=true" width="250">

Можно использовать вместе с [Lovelace simple thermostat card](https://github.com/nervetattoo/simple-thermostat#setpoints-config)

<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-5.png?raw=true" width="250">
<img src="https://github.com/Ailme/home_assistant_electrolux_remote/blob/main/img/img-6.png?raw=true" width="250">

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
