# LÖVE (Love2D) for AuroraOS

LÖVE is an *awesome* framework you can use to make 2D games in Lua. It's free, open-source, 
and works on Windows, macOS, Linux, Android, and iOS.  

[LÖVE official page](https://love2d.org).

Port of LÖVE for AuroraOS and SailfishOS made by sashikknox.  
[Donate to sashikknox](https://boosty.to/sashikknox)  

# Использование шаблона
1. Весь код и ресурсы проектa распологайте в папке `game`, так что бы был доступен файл `game/main.lua`
2. В папку `icons` положите `*.png` файлы со всемb размерами иконок вашего приложения, заменив те что 
там уже лежат. Цифра в имени файла обозначает размер иконки, т.е. 86x86, 108x108, 128x128, 172x172 
пикселей.
3. Отредактируйте `rpm/game.spec` файл, и поставьте туда свои значения:

| паравметр | значение |
| :--| :--|
|%define _app_orgname|Обратное доменное имя организации, например `ru.sashikknox`|
|%define _app_appname|Название приложения, например `AwesomeGame`|
|%define _app_launcher_name|Название приложения в сетке приложений, например `Офигенная игра`|
|Summary:|Тут может быть описание вашего приложения, краткое|
|Release:|Cюда пишете инкрементируемый номер версии вашего приложения, например `1`|
|Version:|Тут может быть и текстовое значение версии, но по калссике сюда идет версия вида `1.0.0`, но можете обозвать как угодно|
|License:|Сюда можете вписать лицензию вашего проекта|

Далее при сборке пакета содержимаое папки game упакуется в `game.love` файл, который уже будет 
запускать движок Love2D, а так же сгенерирует все необходимые файлы для работ вашего проекта 
в ОС Аврора.

# Build 
- download and install [AuroraSDK](https://developer.auroraos.ru/doc/software_development/sdk/downloads)
- list avaliable targets (use sfdk tool from SDK)
    ```
    ~/AuroraOS/bin/sfdk engine exec sb2-config -l
    ```
    its show something like
    ```
    AuroraOS-5.1.3.85-MB2-aarch64.default
    AuroraOS-5.1.3.85-MB2-aarch64
    AuroraOS-5.1.3.85-MB2-armv7hl.default
    AuroraOS-5.1.3.85-MB2-armv7hl
    AuroraOS-5.1.3.85-MB2-x86_64.default
    AuroraOS-5.1.3.85-MB2-x86_64
    ```
    where target names with `.default` suffixes - its snapshots. 
- Choose target "AuroraOS-5.1.3.85-MB2-aarch64" and build an RPM
    ```
    ~/AuroraOS/bin/sfdk -c "target=AuroraOS-5.1.3.85-MB2-aarch64" build-init
    ~/AuroraOS/bin/sfdk -c "target=AuroraOS-5.1.3.85-MB2-aarch64" prepare
    ~/AuroraOS/bin/sfdk -c "target=AuroraOS-5.1.3.85-MB2-aarch64" build
    ```
