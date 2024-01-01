# Python 后端

API 文档：[ApiFox](https://apifox.com/apidoc/shared-8da81565-7e10-4bc9-a216-c914d00c2345)

## 使用说明

### 1. 依赖配置

本项目包含以下依赖

```
flask                   # 后端开发框架
ernie                   # 百度文心一眼 sdk
openai                  # openai sdk
chromadb                # 向量数据库chromadb
sentence-transformers   # embedding模型
```

### 2. 配置文件

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

#### 3. 运行

你就可以在命令行中输入`python src/run.py`运行此部分。

## 文件结构

```lua
.
|-- config.json     # 配置信息（主要是调用API的key）
|-- data
|   `-- chroma      # 存放向量数据库数据
`-- src
    |-- utils       # 包括配置信息读取在内和utils
    |-- api         # api编写
    |-- bots        # LLM操作 (目前只实现了ERNIE, GPT)
    |-- chroma.py   # 向量数据库操作
    `-- run.py      # 引导启动文件
```

## 后端架构

本后端提供的 API 主要分为两个

-   VectorDB: 对向量数据库的 CRUD 部分：
-   Bot: 提供对话功能

### 1. VectorDB

对于向量数据库，我们使用轻量级的[chroma](https://www.trychroma.com/)来存储聊天记录，
目的是方便读取近似消息与最近消息，定义如下。

-   近似消息：与用户 Query 语义最相似的消息，让 LLM 有长期机器
-   最近消息：与时间相关的最近消息内容

> 原本我们是将消息存入传统数据库 MySQL，但再使用 chroma 就会导致数据冗余。
> 后面为了方便维护，所以我们还是将消息都存入向量数据中。

#### (1) 数据库标识符

由于本后端需要面向多用户以及多身份的场景，
所以我们需要为每个用户，以及对应的每个身份都构建一个数据库，
我们以 11 位大陆手机号码作为用户的唯一标识符，
所以每个数据库的标识符为`{phone}-{botRole}`。

#### (2) 消息对象

一条消息被存放在向量数据库主要包含 3 部分内容：

-   id (str): 消息的唯一标识符
-   document (str): 消息内容
-   metadata：元数据
    -   id(int): 消息编号
    -   role(enum): 发送者的身份(user/assistant)
    -   time(int): 发送时间

> 由于 chroma 的设计问题，每条消息必须有一个字符串类型的 id，
> 但是字符串不适合条件查找，所以我们在元数据中额外引入一个 id。

#### (3) 方法

##### `get_nearest_messages` 获取最近的消息

该函数主要是通过`time`与`id`元数据进行条件查询，
获取 n 分钟内最多 m 条的消息内容。

##### `query_similar_context` 查找最近上下文

该函数是通过一条消息，查找与其最相关的一条消息，并返回其上下文。
我们还可以使用参数`window_size`来控制返回的消息对（一问一答）的数量。
在该函数中，判断语义相似度的方法就是比较两条消息之间的向量距离，
我们也提供了参数`threshold`来控制能接受的最大阈值，
防止查找一些不想关的上下文。

值得注意的是，查找的上下文的第一条消息必须释义用户消息开头，
我们会进行对其。

### 2. Bot

此部分主要封装了与 LLM 对话的内容，
目前我们仅实现实现了百度的[Ernie](https://github.com/PaddlePaddle/ERNIE-Bot-SDK)
和 openai 的 [ChatGPT](https://github.com/openai/openai-python)。

#### (1) 对话（增强版）

在增强对话方面，我们主要是通过提示工程的方法从两个方面对其改进，分别是人格和消息。
对于前者，我们主要分为三个部分，让 LLM 带有角色的**角色预设 Prompt**，
让 LLM 角色更丰满的**角色描述 Prompt**，该 Prompt 主要是让用户进行输入。
最后就是一些辅助的**系统 Prompt**。
而对于后者，我们也分为了三个部分，分别是前面提到的**近似消息**和**历史消息**，
以及用户发送需要回答的**用户消息**。

因此，在每次对话过程中，以上这些 Prompt 和消息组成了一次完整的对话交互。
值得注意的是，在实际实现过程中，近似消息和历史消息可能会重叠，也可能不会，
对于两种情况，我们做一下以下处理。

-   重叠情况：删除重叠部分并连接，构成连续的上下文
-   非重叠情况：不联系的上下文可能会对 LLM 生成有影响，
    所以我们将近似消息生成消息摘要，放在 Prompt 中。
