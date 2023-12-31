# Python 后端使用说明

## 依赖配置

本项目包含以下依赖

```
flask                   # 后端开发框架
ernie                   # 百度文心一眼 sdk
openai                  # openai sdk
chromadb                # 向量数据库chromadb
sentence-transformers   # embedding模型
```

## 配置文件

在运行后端之前，请先配置好根目录下的配置文件`config.json`。
目前本项目仅支持`ernie`和`gpt`两种大语言模型，
配置时请在`botKind`中填写对应类型，然后在`key`中填写对应的密钥。

```json
{
    "botKind": "gpt",
    "databasePath": "",
    "key": {
        "ernie": {
            "apiType": "aistudio",
            "accessToken": "<>"
        },
        "gpt": {
            "apiKey": "sk-<>"
        }
    }
}
```

### 运行

你就可以在命令行中输入`python src/run.py`运行此部分。
