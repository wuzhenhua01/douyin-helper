# douyin-helper

## 安装minicap

2. 确定您的设备支持ABI与SDK版本
```shell
adb shell getprop ro.product.cpu.abi
```
```shell
adb shell getprop ro.build.version.sdk
```

2. 推送适配二进制文件
```shell
adb push stf-binaries/node_modules/minicap-prebuilt/prebuilt/arm64-v8a/lib/android-29/minicap /data/local/tmp
```
```shell
adb shell chmod +x /data/local/tmp/minicap
```
```shell
adb push stf-binaries/node_modules/minicap-prebuilt/prebuilt/arm64-v8a/lib/android-29/minicap.so /data/local/tmp /data/local/tmp
```

3. 获取屏幕分辨率
```shell
adb shell wm size
```
4. 运行minicap
```shell
adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P1600x2560@1024x1280/0
```
5. 创建本地转发
```shell
adb forward tcp:1717 localabstract:minicap
```
