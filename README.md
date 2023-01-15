# mpy-esp32-test

microPython-esp32测试代码

# 菜鸡勿喷

mian文件夹为自己编写的esp32-wroom开发板和lcd 160x128屏幕（st7735）的代码

![723d6a18ae622b9d66f4f562983eb7e](https://user-images.githubusercontent.com/73768260/212539963-b8978582-51d0-42ee-a29f-eadd4f70c542.jpg)

## 目前拥有的功能及使用说明

**功能**

1.可以显示如上图的界面（天气，时间，动画）

2.可以连接mqtt服务器，使用mqtt控制多个Pin引脚

~~3.wifi 3次连接失败可从新等待配置
4.wifi 短暂的断开、再次连接，mqtt服务也可从新连接~~

**使用说明**

1.第一次开机后需要配置wifi 信息
连接到此设备的wifi 后使用apiPost等工具发送以下json信息到 [http://192.168.4.1/](http://192.168.4.1/)，等待返回信息
```json
{"type":"0","ssid":"TP-LINK_803F","passwd":"ks123456","ip":"","mask":"","gateway":"","dns":"","timeout":""}
```
其他的可在config.py文件里边修改，暂未作wifi/远程 修改适配


## 配置
| 屏幕  | esp32 |
|-----|-------|
| scl | 13    |
| sda | 12    |
| rst | 14    |
| dc  | 27    |
| cs  | 26    |
| blk | 25    |

main文件夹所需要的文件代码及说明

| 名称            | 说明        |
|---------------|-----------|
| function      | 一些功能性代码文件 |
| libs          | 第三方库      |
| res           | 图片资源等     |
| ui            | 屏幕显示代码    |
| config.py     | 所有配置代码    |
| main.py       | 启动        |
| Tool.py       | 工具        |
| WiFiConfig.py | wifi配置    |

以上代码必须烧录到设备中

## 说明
此版本为测试版本，通过各路大神的开源教程加自己的想法缝合出来的作品。
由于mpy的特性，以及对mpy不够了解熟练和第一次缝合。少了对代码性能的优化。
当然也做不到用 Arduino / idf 等语言的复杂功能。

**此项目的核心想法：**

**此版本的不足：**

**下一版本的构思：**