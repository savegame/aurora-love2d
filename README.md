# LÖVE 2D for AuroraOS

LÖVE is an *awesome* framework you can use to make 2D games in Lua. It's free, open-source, and works on Windows, macOS, Linux, Android, and iOS.  

Port of LÖVE for AuroraOS and SailfishOS made by sashikknox.  
[Donate to sashikknox](https://boosty.to/sashikknox)  

# Build 
- download and install [AuroraSDK](https://developer.auroraos.ru/doc/software_development/sdk/downloads) (or SailfishOS SDK)
- list avaliable targets (use sfdk tool from SDK)
    ```
    ~/AuroraOS/bin/sfdk engine exec sb2-config -l
    ```
    its show something like
    ```
    AuroraOS-5.0.0.60-base-aarch64.default
    AuroraOS-5.0.0.60-base-aarch64
    AuroraOS-5.0.0.60-base-armv7hl.default
    AuroraOS-5.0.0.60-base-armv7hl
    AuroraOS-5.0.0.60-base-x86_64.default
    AuroraOS-5.0.0.60-base-x86_64
    ```
    where target names with `.default` suffixes - its snapshots. 
- Choose target "AuroraOS-5.0.0.60-base-aarch64" and build an RPM
    ```
    ~/AuroraOS/bin/sfdk -c "target=AuroraOS-5.0.0.60-base-aarch64" prepare
    ~/AuroraOS/bin/sfdk -c "target=AuroraOS-5.0.0.60-base-aarch64" build
    ```
