# QQBilibiliLiveChecker

检查指定的多个 B 站直播间是否开播，并通过 Mirai HTTP API 向指定 QQ 群内发送提醒

## 使用方法

+ 搭建 [Mirai HTTP API](https://github.com/project-mirai/mirai-api-http) 服务，并确保开启 http 接口
+ 使用 config.json.templ 文件为模版创建 config.json 文件，按照提示填写信息
+ 运行 ``python3 livechecker.py``
