# MCP 2026-07-28：官方没有“MCP 2.0”

> **本文约定**
>
> 官方协议从未发布名为 “MCP 2.0” 的版本。
>
> 为了回应社区习惯，
> 本文只在教学意义上，
> 用 **“MCP 2.0”**
> 指代官方称为 **Modern era**
> 的 `2026-07-28` 及以后协议。
>
> 写代码、报 bug、声明兼容性时，
> 请始终写精确协议修订号：
> **`2026-07-28`**。

---

## 0. 阅读合同：我们在讨论哪个 MCP

### 0.1 冻结范围

本文冻结于 **2026-08-09**。

当前规范快照：

- 仓库：
  [`modelcontextprotocol/modelcontextprotocol`](https://github.com/modelcontextprotocol/modelcontextprotocol)
- 当前官方规范修订：
  [`2026-07-28`](https://modelcontextprotocol.io/specification/2026-07-28)
- 本文审计的当前规范 commit：
  [`5f5440bb26a62e2cf3440b92da5a667efa03b267`](https://github.com/modelcontextprotocol/modelcontextprotocol/tree/5f5440bb26a62e2cf3440b92da5a667efa03b267)
- 本文审计的 Legacy 对照 commit：
  [`38c84e9f93ad191d9eb26d92b945d17bd0efcaf3`](https://github.com/modelcontextprotocol/modelcontextprotocol/tree/38c84e9f93ad191d9eb26d92b945d17bd0efcaf3)
- Legacy 对照规范：
  [`2025-11-25`](https://modelcontextprotocol.io/specification/2025-11-25)

这里的“冻结”意味着：

1. 所有协议结论以这两个 commit 为审计锚点。
2. 所有网页链接优先指向带日期的规范页。
3. 不把 SDK `main` 的未来行为倒推为本文结论。
4. 不把某个 Host 的产品行为写成协议义务。
5. 不把某篇教程的示例写成官方 wire contract。

### 0.2 三种标签

全文使用三种标签区分证据强度：

- **【事实】**
  规范、schema、SEP 或官方发布材料直接支持。
- **【解释】**
  为帮助学习者建立心智模型而做的推导。
- **【评价】**
  对设计取舍的判断；
  不是协议本身宣称。

示例：

> **【事实】**
> Modern MCP 是无状态协议。
>
> **【解释】**
> “无状态”不是业务系统不能存状态，
> 而是不能把理解当前请求所需的协议状态
> 藏在上一次连接或握手里。
>
> **【评价】**
> 这更适合负载均衡和故障恢复，
> 但会把显式状态建模的责任交还给应用开发者。

### 0.3 规范词强度

MCP 规范沿用 RFC 风格的规范词：

| 英文 | 本文译法 | 应如何阅读 |
|---|---|---|
| MUST | 必须 | 不满足即不符合该条规范 |
| MUST NOT | 禁止 | 做了即不符合该条规范 |
| SHOULD | 应当 | 可以偏离，但应有充分理由 |
| SHOULD NOT | 不应 | 可以偏离，但应有充分理由 |
| MAY | 可以 | 可选能力 |

本文会尽量保留强度，
不会把 “SHOULD” 擅自升级为 “MUST”。

### 0.4 一句话结论

**【事实】**
官方当前规范使用日期版本，
其 schema 同时定义：

- `LATEST_PROTOCOL_VERSION = "2026-07-28"`
- `JSONRPC_VERSION = "2.0"`

见冻结 commit 的
[`schema/2026-07-28/schema.ts`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/5f5440bb26a62e2cf3440b92da5a667efa03b267/schema/2026-07-28/schema.ts)。

所以：

```text
MCP 2026-07-28
≠ JSON-RPC 2.0
≠ TypeScript SDK v2
≠ 官方 MCP 2.0
```

### 0.5 三只独立的“版本时钟”

```mermaid
flowchart LR
    A["协议时钟<br/>MCP 2026-07-28<br/>决定 wire contract"]
    B["信封时钟<br/>JSON-RPC 2.0<br/>决定 request / response 形状"]
    C["实现时钟<br/>TS SDK v2 · Go SDK v1.7<br/>决定某个包的 API"]
    A -. "彼此独立" .- B
    B -. "彼此独立" .- C
    C -. "彼此独立" .- A
```

不要写：

```text
我们的 Server 支持 MCP 2.0。
```

应写：

```text
我们的 Server 支持 MCP protocol revision 2026-07-28。
使用 TypeScript SDK v2.x 实现。
```

官方也明确把
`2026-07-28` 及以后称作 **Modern**，
把 `2025-11-25` 及以前称作 **Legacy**；
见
[Versioning and Compatibility](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)。

本文因此使用：

| 本文术语 | 精确定义 |
|---|---|
| Legacy MCP | `2025-11-25` 及以前的官方协议修订 |
| Modern MCP | `2026-07-28` 及以后的官方协议修订 |
| “MCP 1.0” | 只作为不精确的社区说法；本文尽量不用 |
| “MCP 2.0” | 只作为 Modern era 的教学简称 |

---

## 1. 从最底层开始：什么是 API

### 1.1 API 不是一种网络格式

API 是 **Application Programming Interface**。

最小定义是：

> 一方允许另一方按某个合同使用能力。

这个合同可以是：

- 本地函数；
- 系统调用；
- 动态链接库；
- 浏览器 DOM；
- HTTP 服务；
- 消息队列；
- 数据库驱动；
- 命令行程序；
- MCP Server。

因此，
“API 和 MCP 有什么区别”
这个问题本身有点像：

> “交通工具和火车有什么区别？”

API 是大类；
MCP 是其中一种特定的跨进程协议合同。

### 1.2 一个 API 合同至少回答什么

```mermaid
flowchart TD
    API["API 合同"]
    API --> N["名称<br/>调用什么"]
    API --> I["输入<br/>传什么"]
    API --> O["输出<br/>得到什么"]
    API --> E["错误<br/>失败怎样表示"]
    API --> S["语义<br/>这次调用意味着什么"]
    API --> P["策略<br/>身份 · 权限 · 限流 · 重试"]
```

例如一个天气函数：

```ts
getWeather(city: string): Promise<Weather>
```

只看签名，
我们知道输入输出，
但仍不知道：

- 城市名用中文还是 IATA code；
- 结果是当前天气还是预报；
- 超时是否可重试；
- 是否计费；
- 是否需要用户授权位置；
- 是否会记录查询；
- 错误是抛异常还是返回空值。

**【解释】**
协议价值通常不只在“能传字节”，
而在把这些语义变成多方可复用的合同。

### 1.3 进程内与进程外

进程内函数调用大致是：

```text
caller
  → 在同一地址空间放参数
  → 跳到函数代码
  → 拿到返回值
```

跨进程调用必须额外解决：

1. 如何序列化；
2. 如何寻址；
3. 如何传输；
4. 如何关联请求与响应；
5. 如何表示失败；
6. 如何处理超时、取消和重试；
7. 如何认证与授权；
8. 如何演进版本。

REST、RPC、JSON-RPC 和 MCP
都在回答其中一部分，
但层次不同。

---

## 2. REST：把远端世界看成资源

### 2.1 REST 的核心直觉

REST 风格通常把服务抽象成资源：

```http
GET /weather?city=Beijing
```

或者：

```http
GET /cities/Beijing/weather
```

常见 HTTP 动词表达：

- `GET`：读取；
- `POST`：创建或触发；
- `PUT`：整体替换；
- `PATCH`：局部修改；
- `DELETE`：删除。

**【解释】**
REST 的重心是：

> “这个资源现在是什么状态？”

而不是：

> “请调用名为 `getWeather` 的函数。”

### 2.2 REST 的消息路径

```mermaid
sequenceDiagram
    participant App as "应用"
    participant HTTP as "HTTP 网关"
    participant API as "天气 REST API"
    App->>HTTP: "GET /cities/Beijing/weather"
    HTTP->>API: "路由 + 认证 + 限流"
    API-->>HTTP: "200 + JSON"
    HTTP-->>App: "{ temperature: 24 }"
```

### 2.3 REST 擅长什么

- 浏览器和网关生态成熟；
- HTTP cache 语义成熟；
- URL 易于观测和路由；
- 资源 CRUD 容易理解；
- 与 CDN、WAF、反向代理自然配合。

### 2.4 REST 没有自动解决什么

仅有一个 OpenAPI 文档，
并不会自动告诉 AI Host：

- 哪些 endpoint 适合给模型调用；
- 哪个调用具有破坏性；
- 用户是否需要先批准；
- 结果应以怎样的内容块进入上下文；
- 哪些能力是 prompt、resource 或 tool；
- 如何向用户补问缺失字段；
- 如何跨不同服务使用统一发现流程。

这不代表 REST 做得不好。

它解决的是更一般的 Web API 问题，
并非专为 AI Host 与工具生态设计。

---

## 3. RPC：把远端世界看成方法调用

### 3.1 RPC 的核心直觉

RPC 是 **Remote Procedure Call**。

它试图让跨进程操作看起来像：

```ts
const weather = await remote.getWeather({
  city: "Beijing"
});
```

调用者面对：

- 方法名；
- 参数；
- 返回值；
- 远端错误。

### 3.2 REST 与 RPC 不是敌对阵营

```mermaid
flowchart LR
    Need["需求：获得北京天气"]
    Need --> REST["REST 视角<br/>GET /cities/Beijing/weather"]
    Need --> RPC["RPC 视角<br/>getWeather(city='Beijing')"]
    REST --> Same["都可能通过 HTTP<br/>都可能返回 JSON"]
    RPC --> Same
```

它们可以使用相同传输。

区别主要在应用语义：

- REST 强调资源和统一 HTTP 动词；
- RPC 强调具体方法和参数。

### 3.3 远端调用不能真的等同本地函数

本地函数失败时，
通常不会遇到：

- 网络分区；
- 请求已执行但响应丢失；
- 服务端升级造成 schema 不兼容；
- 同一个请求被重复提交；
- 认证 token 过期；
- 中间网关返回 HTML 错误页。

**【评价】**
好的 RPC 抽象应减少样板代码，
但不应让开发者忘掉分布式系统的不确定性。

---

## 4. JSON-RPC 2.0：MCP 使用的通用消息信封

### 4.1 JSON-RPC 管什么

MCP 的所有消息必须符合
[JSON-RPC 2.0](https://www.jsonrpc.org/specification)；
MCP 对消息又增加了自己的约束，
见当前
[Base Protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)。

下面四段只演示 **JSON-RPC 2.0 信封**，
方法名也是虚构的；它们故意省略 MCP 字段，
不能直接当作 Modern MCP `2026-07-28` 报文发送。
真正的 Modern request 还必须带完整 namespaced `_meta`，
成功结果也必须带 `resultType`；第 12 节会给出完整示例。

一个请求：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "math/add",
  "params": {
    "a": 2,
    "b": 3
  }
}
```

成功响应：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "value": 5
  }
}
```

错误响应：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "error": {
    "code": -32602,
    "message": "Invalid params"
  }
}
```

通知：

```json
{
  "jsonrpc": "2.0",
  "method": "events/changed",
  "params": {
    "name": "weather"
  }
}
```

通知没有 `id`，
接收方不能发响应。

### 4.2 `id` 是做什么的

同一连接中可能并发多个请求：

```mermaid
sequenceDiagram
    participant C as "Caller"
    participant S as "Server"
    C->>S: "id=1, slowOperation"
    C->>S: "id=2, fastOperation"
    S-->>C: "id=2, result"
    S-->>C: "id=1, result"
```

响应顺序可以不同于请求顺序。

调用者靠 `id` 做关联。

当前 MCP 进一步要求：

- request `id` 必须是字符串或整数；
- 不能为 `null`；
- 尚未完成的请求之间不能复用同一个 `id`。

见当前
[Base Protocol / Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic#requests)。

### 4.3 JSON-RPC 不管什么

JSON-RPC 本身不知道：

- 什么是 Tool；
- 如何列出 Tool；
- Tool 参数用什么 schema；
- 什么是 Prompt 或 Resource；
- 用户何时批准；
- Server 支持哪个 MCP 版本；
- Client 支持 elicitation 吗；
- HTTP OAuth 怎么做；
- MCP 内容如何表示图片、音频或资源链接。

所以 JSON-RPC 是信封，
不是 MCP 的全部。

### 4.4 MCP 对成功响应新增的关键要求

当前 MCP 的成功结果必须有 `resultType`：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "resultType": "complete",
    "value": 5
  }
}
```

核心值包括：

- `complete`：本次操作已完成；
- `input_required`：还需要 Client 提供输入；
- extension 可以声明额外值，例如 Tasks 的 `task`。

为兼容旧 Server，
缺少 `resultType` 的旧响应
由 Modern Client 当作 `complete`；
见
[Base Protocol / ResultType](https://modelcontextprotocol.io/specification/2026-07-28/basic#resulttype)。

### 4.5 分层不要混淆

```mermaid
flowchart TB
    Product["产品体验<br/>聊天 · IDE · Agent"]
    Host["AI Host 策略<br/>模型选择 · 用户批准 · 隔离"]
    MCP["MCP 应用语义<br/>tools · resources · prompts · discovery"]
    RPC["JSON-RPC 2.0 信封<br/>method · params · id · result/error"]
    Transport["传输绑定<br/>stdio 或 Streamable HTTP"]
    Network["OS / pipe / HTTP / TCP"]
    Product --> Host --> MCP --> RPC --> Transport --> Network
```

**【解释】**
MCP 的主要价值不在发明另一种 JSON，
而在 RPC 信封之上
统一 AI 工具生态的语义、发现和安全责任。

---

## 5. MCP 为什么存在

### 5.1 没有 MCP 时的 N×M 集成

假设有：

- 4 个 AI Host；
- 5 个数据或工具服务。

传统做法往往让每个 Host
分别实现每个服务的适配器：

```mermaid
flowchart LR
    H1["Host A"]
    H2["Host B"]
    H3["Host C"]
    H4["Host D"]
    S1["Git"]
    S2["Database"]
    S3["Drive"]
    S4["Issue Tracker"]
    S5["Weather API"]
    H1 --> S1
    H1 --> S2
    H1 --> S3
    H1 --> S4
    H1 --> S5
    H2 --> S1
    H2 --> S2
    H2 --> S3
    H2 --> S4
    H2 --> S5
    H3 --> S1
    H3 --> S2
    H3 --> S3
    H3 --> S4
    H3 --> S5
    H4 --> S1
    H4 --> S2
    H4 --> S3
    H4 --> S4
    H4 --> S5
```

这里没有声称
“MCP 从数学上消灭所有 N×M 工作”。

现实中仍有：

- 认证差异；
- UI 差异；
- Host 能力差异；
- 部署差异；
- 产品策略差异。

但 MCP 让双方至少共享：

- 消息模型；
- 发现方法；
- Tool/Resource/Prompt schema；
- 内容块；
- 能力声明；
- 错误结构；
- 版本兼容流程；
- HTTP 授权框架。

### 5.2 MCP 之后的标准边界

```mermaid
flowchart LR
    H1["Host A"] --> C1["MCP Client"]
    H2["Host B"] --> C2["MCP Client"]
    H3["Host C"] --> C3["MCP Client"]
    C1 --> P["MCP contract"]
    C2 --> P
    C3 --> P
    P --> M1["Git MCP Server"]
    P --> M2["DB MCP Server"]
    P --> M3["Drive MCP Server"]
    M1 --> S1["Git implementation"]
    M2 --> S2["Database API"]
    M3 --> S3["Drive REST API"]
```

**【事实】**
官方说明 MCP 受 Language Server Protocol 启发，
目标是形成模型应用连接外部系统的开放标准；
见
[MCP Specification](https://modelcontextprotocol.io/specification/2026-07-28)
和最初的
[2024-11-25 发布公告](https://www.anthropic.com/news/model-context-protocol)。

### 5.3 MCP 不替代后端 API

一个 GitHub MCP Server 可能内部仍调用：

```http
POST /repos/{owner}/{repo}/issues
```

一个数据库 MCP Server
可能内部仍执行 SQL。

一个本地文件 MCP Server
可能内部仍调用操作系统文件 API。

MCP 统一的是：

```text
AI Host ↔ MCP Server
```

而不是强迫所有后端改用 MCP：

```text
MCP Server ↔ 实际业务系统
```

### 5.4 MCP 与模型 tool calling

模型供应商常提供 tool/function calling：

```json
{
  "name": "get_weather",
  "description": "Get weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    },
    "required": ["city"]
  }
}
```

这和 MCP Tool 相似，
但边界不同：

| 模型 tool calling | MCP |
|---|---|
| Host 与某个模型 API 之间的合同 | Host/Client 与 MCP Server 之间的合同 |
| 描述模型如何选择工具 | 描述工具如何发现、调用和返回 |
| 通常不规定工具来自哪里 | 明确 Server、transport、capability 等 |
| 由模型厂商 API 定义 | 开放协议规范 |

**【解释】**
Host 通常会把 MCP Tool
转换成模型 API 接受的 tool schema，
再把模型选择转换成 `tools/call`。

这是一种常见实现路径，
不是规范要求 Host 内部必须采用的唯一架构。

---

## 6. Host、Client、Server：三个角色不要混成两个

当前官方角色定义见
[Architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture)。

### 6.1 Host

Host 是用户实际使用的 AI 应用，
例如：

- IDE；
- 桌面助手；
- 聊天应用；
- Agent runtime；
- 自动化平台。

Host 通常负责：

- 保存对话；
- 调用模型；
- 创建 MCP Client；
- 聚合多个 Server 的上下文；
- 展示 Tool；
- 获得用户同意；
- 执行安全策略；
- 隔离不同 Server；
- 决定把什么发给模型。

### 6.2 Client

MCP Client 是 Host 内部的协议参与者。

**【事实】**
一个 Client 与一个 Server
保持一对一关系。

一个 Host 可以创建多个 Client，
分别连接多个 Server。

Client 负责：

- 编码和发送 MCP 消息；
- 声明协议版本和 capabilities；
- 处理响应与通知；
- 执行兼容性流程；
- 把 Host 的许可决策落实为协议行为。

Client 不必是独立进程。

它可以只是 Host 进程中的一个对象或库实例。

### 6.3 Server

MCP Server 提供聚焦的能力：

- Tools；
- Resources；
- Prompts；
- 可选 utilities；
- 可选 extensions。

它可以是：

- Client 启动的本地 stdio 子进程；
- 远端 HTTP 服务；
- 某个企业系统前面的 adapter；
- 一个同时调用多个后端的聚合服务。

### 6.4 正确拓扑

```mermaid
flowchart TB
    U["用户"]
    H["Host<br/>模型 · 对话 · 同意 · 策略"]
    M["模型 API"]
    C1["MCP Client 1"]
    C2["MCP Client 2"]
    C3["MCP Client 3"]
    S1["Local Files Server"]
    S2["GitHub Server"]
    S3["Database Server"]
    U <--> H
    H <--> M
    H <--> C1
    H <--> C2
    H <--> C3
    C1 <--> S1
    C2 <--> S2
    C3 <--> S3
```

错误心智模型：

```text
模型 → 一个无所不知的 MCP 总服务器
```

更准确的心智模型：

```text
Host 代表用户，
协调模型和多个相互隔离的 Server。
```

### 6.5 信任边界

```mermaid
flowchart LR
    User["用户<br/>最终授权者"]
    Host["Host<br/>策略执行点"]
    Model["模型<br/>会建议但可能犯错"]
    SA["Server A<br/>不可信输入源"]
    SB["Server B<br/>不可信输入源"]
    World["外部系统<br/>文件 · SaaS · DB"]
    User -->|"许可与意图"| Host
    Host -->|"最小必要上下文"| Model
    Host -->|"每个 Client 单独连接"| SA
    Host -->|"每个 Client 单独连接"| SB
    SA --> World
    SB --> World
    SA -. "不应看到 B 的上下文" .- SB
```

**【事实】**
官方架构强调：

- Host 维护安全策略与 consent；
- Server 不应自动看到整个对话；
- Server 之间应保持隔离；
- Host 只暴露必要上下文。

见当前
[Architecture / Design Principles](https://modelcontextprotocol.io/specification/2026-07-28/architecture)。

---

## 7. 三个 Server 原语：Prompt、Resource、Tool

官方把核心 Server features 分成三类，
见
[Server Features](https://modelcontextprotocol.io/specification/2026-07-28/server)。

### 7.1 一张控制权图

```mermaid
flowchart TD
    P["Prompt<br/>用户控制"]
    R["Resource<br/>应用控制"]
    T["Tool<br/>模型控制"]
    U["用户主动选择模板"] --> P
    H["Host 决定读取上下文"] --> R
    M["模型建议调用动作"] --> T
    P --> C["进入 Host 的上下文与工作流"]
    R --> C
    T --> C
```

这里的“控制”是交互设计倾向，
不是绕过授权的许可证。

模型控制 Tool 意味着：

> 模型可以根据上下文主动建议调用。

不意味着：

> 模型说调用就必须执行。

### 7.2 Prompt：用户选择的模板

Prompt 适合：

- “总结这个仓库”；
- “生成 release note”；
- “进行安全审查”；
- 带参数的预定义工作流入口。

常用方法：

```text
prompts/list
prompts/get
```

`prompts/list`
让 Client 发现可用 Prompt。

`prompts/get`
根据名称和参数取得消息模板。

当前规范见
[Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)。

### 7.3 Resource：应用决定何时读取的上下文

Resource 适合：

- 文件内容；
- 数据库记录；
- Git history；
- 文档；
- 服务状态；
- 可通过 URI 标识的数据。

常用方法：

```text
resources/list
resources/templates/list
resources/read
```

Resource 以 URI 标识，
可以返回文本或二进制 blob。

当前规范见
[Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)。

### 7.4 Tool：模型可以建议调用的动作

Tool 适合：

- 搜索；
- 执行查询；
- 创建 issue；
- 修改文件；
- 发送消息；
- 调用外部系统。

常用方法：

```text
tools/list
tools/call
```

当前规范见
[Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)。

### 7.5 Tool 定义

概念化示例：

```json
{
  "name": "get_weather",
  "title": "查询天气",
  "description": "查询指定城市的当前天气",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    },
    "required": ["city"],
    "additionalProperties": false
  }
}
```

当前默认 JSON Schema dialect 是 2020-12。

实现必须至少支持该 dialect；
见
[Base Protocol / JSON Schema Usage](https://modelcontextprotocol.io/specification/2026-07-28/basic#json-schema-usage)。

### 7.6 为什么不把所有东西都做成 Tool

可以把“读文件”做成 Tool，
但 Resource 额外表达：

- 它是可寻址内容；
- Host 可决定何时读取；
- 可以列出与订阅变化；
- UI 可以把它展示为上下文对象。

可以把“代码审查模板”做成 Tool，
但 Prompt 额外表达：

- 它是用户主动选择的工作流入口；
- 返回的是对话消息模板；
- 不一定立即执行外部副作用。

**【评价】**
三个原语的价值不是技术上互不可替代，
而是保留控制权与交互语义。

把所有东西都塞进 Tool，
会丢失这层语义。

### 7.7 原语选择表

| 问题 | 更可能选择 |
|---|---|
| 用户是否主动选择一个模板？ | Prompt |
| 内容是否有稳定 URI？ | Resource |
| Host 是否应自行决定何时加载？ | Resource |
| 是否执行计算或副作用？ | Tool |
| 模型是否需要主动建议调用？ | Tool |
| 是否只是用户可复用的消息骨架？ | Prompt |

---

## 8. Legacy MCP：所谓“MCP 1.0”究竟做了什么

### 8.1 先纠正名称

**【事实】**
官方不把旧规范统称为 “MCP 1.0”。

Legacy 包括多个日期修订，
例如：

- `2024-11-05`
- `2025-03-26`
- `2025-06-18`
- `2025-11-25`

版本发布记录可从
[官方 GitHub Releases](https://github.com/modelcontextprotocol/modelcontextprotocol/releases)
审计。

本文用 `2025-11-25`
代表成熟的 Legacy 对照。

### 8.2 Legacy 的核心心智模型

Legacy Client 与 Server
先建立并初始化一个带状态 session：

```text
连接
  → initialize
  → 版本与 capability 协商
  → initialized 通知
  → operation
  → shutdown
```

官方 Legacy lifecycle 见
[2025-11-25 Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)。

Legacy architecture 直接称其为
“one stateful session per server”，
见
[2025-11-25 Architecture](https://modelcontextprotocol.io/specification/2025-11-25/architecture)。

### 8.3 三阶段生命周期

```mermaid
sequenceDiagram
    participant H as "Host / Legacy Client"
    participant S as "Legacy Server"
    H->>S: "initialize(version, capabilities, clientInfo)"
    S-->>H: "InitializeResult(version, capabilities, serverInfo)"
    H->>S: "notifications/initialized"
    Note over H,S: "Operation：使用协商后的能力"
    H->>S: "tools/list"
    S-->>H: "tools"
    H->>S: "tools/call"
    S-->>H: "result"
    Note over H,S: "Shutdown：由 transport / process 结束"
```

关键规则：

1. `initialize` 必须是首次交互。
2. Client 提议协议版本。
3. 双方交换 capabilities。
4. Server 返回协商后的协议版本。
5. Client 发 `notifications/initialized`。
6. 此后只能使用已协商能力。

### 8.4 Legacy initialize 示例

简化后的教学示例：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "sampling": {},
      "elicitation": {}
    },
    "clientInfo": {
      "name": "example-host",
      "version": "1.0.0"
    }
  }
}
```

Server 返回：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {
        "listChanged": true
      },
      "resources": {
        "subscribe": true,
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "example-server",
      "version": "1.0.0"
    }
  }
}
```

然后 Client 通知：

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

这些是教学裁剪，
精确字段应以冻结的
[Legacy schema commit](https://github.com/modelcontextprotocol/modelcontextprotocol/tree/38c84e9f93ad191d9eb26d92b945d17bd0efcaf3)
为准。

### 8.5 Legacy capability 的意义

能力协商避免一方盲目调用：

- Client 不支持 sampling，
  Server 就不应发 sampling request。
- Server 不支持 resources，
  Client 就不应调用 `resources/list`。
- Server 不声明 list changed，
  Client 就不能假设会收到变更通知。

这个目标是合理的。

Modern 没有取消 capability，
而是改变 capability 的携带方式。

### 8.6 Legacy transport 演进

早期 `2024-11-05`
有两种标准 transport：

- stdio；
- HTTP with SSE。

见
[2024-11-05 Transports](https://modelcontextprotocol.io/specification/2024-11-05/basic/transports)。

`2025-03-26`
引入 Streamable HTTP，
替代旧 HTTP+SSE。

到 `2025-11-25`，
Streamable HTTP 仍允许：

- `Mcp-Session-Id`；
- POST 请求；
- GET 打开 Server→Client SSE；
- SSE 事件恢复；
- Server→Client 独立 JSON-RPC 请求。

### 8.7 Legacy stdio

```mermaid
flowchart LR
    H["Host"]
    C["Legacy MCP Client"]
    P["Server 子进程"]
    IN["stdin<br/>Client → Server"]
    OUT["stdout<br/>Server → Client"]
    ERR["stderr<br/>日志"]
    H --> C
    C --> P
    C --> IN --> P
    P --> OUT --> C
    P --> ERR
```

优点：

- 无需监听网络端口；
- 本地权限可继承；
- 部署简单；
- 双向消息自然；
- 适合桌面 Host 启动工具进程。

约束：

- stdout 必须保持协议纯净；
- 日志写 stderr；
- 子进程生命周期由 Host 管理；
- 每个 Host 可能各自启动实例。

### 8.8 Legacy Streamable HTTP

```mermaid
sequenceDiagram
    participant C as "Legacy Client"
    participant LB as "Load Balancer"
    participant S as "Server Instance"
    C->>LB: "POST /mcp initialize"
    LB->>S: "route"
    S-->>C: "Mcp-Session-Id: abc"
    C->>LB: "POST /mcp + session abc"
    LB->>S: "sticky route / shared state"
    C->>LB: "GET /mcp + session abc"
    LB->>S: "open standalone SSE"
    S-->>C: "server-initiated messages"
```

这里已经能看到：

协议 session 与基础设施路由开始耦合。

但先不要急着批判。

下一节先完整走一遍
Legacy Tool 调用，
才能理解它带来的开发体验。

---

## 9. Legacy 端到端 Tool call

### 9.1 场景

用户问：

> 北京现在天气怎样？

系统中有：

- 一个聊天 Host；
- 一个模型 API；
- 一个 Legacy MCP Client；
- 一个 weather MCP Server；
- 一个实际天气 REST API。

### 9.2 完整路径

```mermaid
sequenceDiagram
    actor U as "用户"
    participant H as "Host"
    participant M as "模型"
    participant C as "Legacy MCP Client"
    participant S as "Weather MCP Server"
    participant A as "Weather REST API"
    H->>C: "连接 Server"
    C->>S: "initialize"
    S-->>C: "版本 + capabilities"
    C->>S: "notifications/initialized"
    C->>S: "tools/list"
    S-->>C: "get_weather schema"
    U->>H: "北京现在天气怎样？"
    H->>M: "用户消息 + tool schema"
    M-->>H: "建议 get_weather(city=北京)"
    H->>U: "如策略要求，展示并确认"
    U-->>H: "同意"
    H->>C: "调用 tool"
    C->>S: "tools/call"
    S->>A: "GET weather"
    A-->>S: "天气 JSON"
    S-->>C: "tool result"
    C-->>H: "结构化/文本内容"
    H->>M: "加入 tool result"
    M-->>H: "生成自然语言答案"
    H-->>U: "北京当前……"
```

### 9.3 `tools/list`

Legacy Client 发现工具：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

Server 返回：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "查询城市当前天气",
        "inputSchema": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string"
            }
          },
          "required": ["city"]
        }
      }
    ]
  }
}
```

### 9.4 Host 把 Tool 交给模型

这一段不是 MCP wire message。

Host 可能调用任意模型 API：

```json
{
  "messages": [
    {
      "role": "user",
      "content": "北京现在天气怎样？"
    }
  ],
  "tools": [
    {
      "name": "get_weather",
      "description": "查询城市当前天气",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string"
          }
        },
        "required": ["city"]
      }
    }
  ]
}
```

模型返回 Tool 选择，
同样不是 MCP 规范的一部分。

### 9.5 `tools/call`

Host 经 Client 发出：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "北京"
    }
  }
}
```

Server 调用天气后端，
再返回：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "北京：24°C，多云"
      }
    ],
    "isError": false
  }
}
```

Modern 响应还必须处理 `resultType`，
后文会给出当前版本的完整示例。

### 9.6 Tool 协议错误与 Tool 执行失败不同

协议错误：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32602,
    "message": "Unknown tool"
  }
}
```

表示：

- 方法或参数层面无法正确执行；
- Client 应把它当 RPC 失败。

Tool 执行结果中的失败：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "天气供应商暂时不可用"
      }
    ],
    "isError": true
  }
}
```

表示：

- `tools/call` 协议调用成功到达；
- Tool 的业务执行失败；
- Host 可以把结果反馈给模型，
  让模型修正参数或向用户解释。

当前 Tool 行为以
[2026-07-28 Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
为准。

### 9.7 这一链路最容易混淆的四份合同

| 合同 | 参与方 |
|---|---|
| 用户界面合同 | 用户 ↔ Host |
| 模型 tool calling 合同 | Host ↔ 模型 API |
| MCP 合同 | MCP Client ↔ MCP Server |
| 后端 REST 合同 | MCP Server ↔ 天气 API |

排查问题时必须先问：

> 错误发生在哪一份合同里？

否则很容易把：

- 模型没有选工具；
- Host 拒绝调用；
- MCP schema 校验失败；
- 天气 API 429；

混成一句含糊的：

> “MCP 不工作。”

---

## 10. Early design 做对了什么，又付出了什么

### 10.1 不应从结论倒推“旧设计愚蠢”

Legacy MCP 的目标环境很大一部分是：

- 桌面应用；
- IDE；
- Host 启动本地子进程；
- 一次连接对应一个使用上下文；
- Server 需要向 Client 请求 sampling、roots 或 elicitation；
- 双方希望只在开头协商一次能力。

在这个环境里，
有状态 session 有真实收益。

### 10.2 Early design 的收益

| 设计 | 当时的直接收益 |
|---|---|
| `initialize` | 一次性交换版本、身份展示信息和能力 |
| session capability | 后续消息不必重复声明 |
| Server→Client request | sampling、elicitation 等像普通 RPC 一样自然 |
| 长连接 SSE | Server 可随时推送请求和通知 |
| `Mcp-Session-Id` | Server 能把多次 HTTP 调用关联到同一协议上下文 |
| 连接生命周期 | 开始、运行、结束容易映射到进程或 UI 生命周期 |

### 10.3 Early design 的隐含假设

```mermaid
flowchart TD
    A["连接稳定"]
    B["一个连接≈一个会话"]
    C["后续请求会回到同一逻辑 Server"]
    D["能力在会话中不会改变"]
    E["Server 可长期保存 session state"]
    F["Client 能接收 Server 主动请求"]
    A --> Good["Legacy 模型体验顺畅"]
    B --> Good
    C --> Good
    D --> Good
    E --> Good
    F --> Good
```

这些不是永远错误的假设。

本地 stdio 场景中，
它们经常成立。

问题在于：

> 协议把这些部署假设，
> 变成了所有远端实现都要承担的基础条件。

### 10.4 得失不是同一维度

Legacy 优化的是：

- 交互连续性；
- 双向调用自然度；
- 单连接编程模型；
- 初始化后消息简洁。

Modern 优化的是：

- 横向扩容；
- 故障恢复；
- 网关可见性；
- 显式状态；
- 请求独立性；
- 兼容与 extension 演进。

**【评价】**
这不是从“有功能”退化到“没功能”，
而是把连续交互重新编码成
可重试的请求状态和显式 extension。

---

## 11. 远端生产环境暴露了什么问题

官方动机最集中地记录在：

- [SEP-2575：Make MCP Stateless](https://modelcontextprotocol.io/seps/2575-stateless-mcp)
- [SEP-2567：Sessionless via Explicit State Handles](https://modelcontextprotocol.io/seps/2567-sessionless-mcp)
- [2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [2026-07-28 官方发布说明](https://blog.modelcontextprotocol.io/posts/2026-07-28/)

### 11.1 横向扩容

Legacy 请求依赖 initialize 建立的状态时：

```mermaid
flowchart LR
    C["Client<br/>session abc"]
    LB["Load Balancer"]
    S1["Instance 1<br/>知道 abc"]
    S2["Instance 2<br/>不知道 abc"]
    Store["共享 session store"]
    C --> LB
    LB -->|"sticky route"| S1
    LB -. "误路由会失败" .-> S2
    S1 <--> Store
    S2 <--> Store
```

运维只有几种选择：

- sticky routing；
- 共享 session store；
- 将所有相关消息固定在一个有状态 actor；
- 失败时让整个 session 重建。

这些都不是不可能，
但会增加：

- 基础设施复杂度；
- 故障模式；
- 成本；
- 回收和过期逻辑；
- 灰度升级难度。

### 11.2 故障恢复

若保存 session 的实例崩溃：

- Client 的连接还可能存在假象；
- 新实例没有初始化上下文；
- 未完成的 Server→Client request 需要恢复；
- SSE event id 与 replay buffer 要维护；
- Client 和 Server 要判断从哪里继续。

**【解释】**
状态不是消失了，
而是以最难观测的方式
散落在连接、内存和重连逻辑中。

### 11.3 session 的语义没有收敛

SEP-2567 指出，
不同 Client 把 session 理解为：

- 一次 Tool call；
- 一次应用启动；
- 一个页面；
- 一个聊天 thread；
- 一段登录状态；
- 一个用户。

于是 Server 很难知道：

> session 中保存的状态究竟应该共享到哪里？

一个购物车可能希望跨页面共享；

同一用户的两个并行沙箱
又必须隔离。

单个模糊 session scope
无法同时表达两者。

### 11.4 Server callback 与网络拓扑

Legacy Server 可以向 Client 发独立 request。

远端环境因此要保证：

- Client 有可持续接收通道；
- 代理不会提前关闭连接；
- 负载均衡能把回调路由到正确 Client；
- 请求与重连状态能恢复；
- callback 的授权语境没有丢失。

### 11.5 网关深度解析

若所有 HTTP 请求都是：

```http
POST /mcp
```

网关只看 URL
无法知道它是：

- `tools/call`；
- `resources/read`；
- `prompts/get`；
- `tools/list`。

想做差异化：

- WAF 规则；
- 审计；
- 限流；
- 路由；
- 成本统计；

就必须解析 JSON body。

### 11.6 缓存困难

如果 Tool 列表可以隐式依赖 session，
网关和 Client 难以回答：

- 列表可缓存多久；
- 可否跨用户复用；
- 列表顺序是否稳定；
- 何时失效。

### 11.7 为什么这些是协议问题

可以在 SDK 内打补丁，
但当每个 SDK 都独立约定：

- session 恢复；
- callback 重试；
- list cache；
- feature negotiation；
- gateway headers；

生态会再次碎片化。

所以 `2026-07-28`
把这些问题提升到协议层处理。

---

## 12. Modern MCP 总览：从隐式 session 到自描述请求

### 12.1 官方定义

**【事实】**
当前 MCP 是无状态协议：

- 处理请求所需信息包含在请求中；
- Server 不能从同一连接上的早先请求推断版本、capability 或身份；
- 一个连接可以交错多个 task、thread 或 conversation；
- 跨请求状态必须由 Client 携带显式 identifier。

见
[Base Protocol / Statelessness](https://modelcontextprotocol.io/specification/2026-07-28/basic#statelessness)。

### 12.2 “无状态”不是什么意思

它不表示：

- Tool 不能创建数据库记录；
- Server 不能保存 job；
- OAuth 不能有 token；
- Client 不能有对话；
- Task 不能长时间运行；
- Resource 不能变化；
- Server 不能缓存。

它表示：

> 这些状态不能只靠
> “你还在上次那条连接上”
> 来隐式定位。

### 12.3 Modern 主路径

```mermaid
sequenceDiagram
    participant C as "Modern Client"
    participant G as "Gateway"
    participant S as "任意 Server 实例"
    opt "Client 需要预先发现"
        C->>G: "server/discover + per-request _meta"
        G->>S: "route"
        S-->>C: "版本 + capabilities + cache hints"
    end
    C->>G: "tools/call + per-request _meta"
    G->>S: "按 header 路由"
    S-->>C: "resultType=complete"
```

这里没有：

- `initialize`；
- `notifications/initialized`；
- `Mcp-Session-Id`；
- “这条连接属于哪个 conversation”的隐式假设。

### 12.4 每个请求的必需 metadata

当前请求 `_meta` 中：

| 字段 | 强度 | 用途 |
|---|---|---|
| `io.modelcontextprotocol/protocolVersion` | MUST | 当前请求采用的协议修订 |
| `io.modelcontextprotocol/clientCapabilities` | MUST | 当前请求可用的 Client capabilities |
| `io.modelcontextprotocol/clientInfo` | SHOULD include | 展示、日志、调试 |
| `io.modelcontextprotocol/logLevel` | MAY | 该请求希望的最低日志级别 |

精确要求见
[Base Protocol / `_meta`](https://modelcontextprotocol.io/specification/2026-07-28/basic#_meta)。

注意：

- `clientInfo` **不是 MUST**；
- 规范说 Client **SHOULD** 在每个请求携带；
- 它是自报信息；
- 不能用作认证或安全决策。

### 12.5 一个 Modern `tools/call`

```json
{
  "jsonrpc": "2.0",
  "id": "call-42",
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "北京"
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "example-host",
        "version": "2.4.0"
      }
    }
  }
}
```

成功响应：

```json
{
  "jsonrpc": "2.0",
  "id": "call-42",
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "北京：24°C，多云"
      }
    ],
    "isError": false,
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "weather-server",
        "version": "3.1.0"
      }
    }
  }
}
```

`serverInfo` 同样是自报展示信息，
不是可信身份。

### 12.6 必需 metadata 缺失

若缺少必需 per-request 字段：

- JSON-RPC error：
  `-32602 Invalid params`
- HTTP：
  `400 Bad Request`

若操作需要 Client 没声明的 capability：

- `MissingRequiredClientCapabilityError`
- code：
  `-32021`
- `data.requiredCapabilities`
  列出缺少的能力。

见当前
[Base Protocol / Error Codes](https://modelcontextprotocol.io/specification/2026-07-28/basic#error-codes)。

---

## 13. 版本与 capability：没有初始化，如何协商

### 13.1 `server/discover`

**【事实】**
Modern Server **MUST** 实现 `server/discover`。

Modern Client 调用它是 **optional**。

Client 可以：

1. 先 discover；
2. 或直接调用任意 RPC，
   再处理版本错误。

见
[Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)。

### 13.2 完整 discovery request

```json
{
  "jsonrpc": "2.0",
  "id": "discover-1",
  "method": "server/discover",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {
        "name": "ExampleClient",
        "version": "1.0.0"
      },
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

官方示例响应：

```json
{
  "jsonrpc": "2.0",
  "id": "discover-1",
  "result": {
    "resultType": "complete",
    "supportedVersions": [
      "2026-07-28"
    ],
    "capabilities": {
      "tools": {},
      "resources": {}
    },
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "ExampleServer",
        "version": "1.0.0"
      }
    },
    "instructions": "Provides weather utilities.",
    "ttlMs": 3600000,
    "cacheScope": "public"
  }
}
```

### 13.3 版本不支持

若 Server 不支持请求版本：

```json
{
  "jsonrpc": "2.0",
  "id": "call-42",
  "error": {
    "code": -32022,
    "message": "Unsupported protocol version",
    "data": {
      "requested": "2026-07-28",
      "supported": [
        "2025-11-25"
      ]
    }
  }
}
```

Client 从共同支持版本中选择，
再用新请求重试。

### 13.4 为什么 discover 不是新 initialize

| `initialize` | `server/discover` |
|---|---|
| Legacy 首次交互，必须调用 | Modern Client 可选调用 |
| 建立会话上下文 | 只查询 Server 声明 |
| capability 供后续 session 隐式使用 | 每个请求仍携带 Client capability |
| 有 `initialized` 通知 | 没有对应完成通知 |
| 与生命周期绑定 | 可缓存的普通 RPC |

### 13.5 capability 的现代含义

capability 表示：

> 该参与方支持某种协议行为。

它不表示：

- 用户已经授权；
- 当前 token 有权限；
- 当前 Server 一定会使用该能力；
- capability 名字本身可信；
- Host 必须把能力展示给模型。

### 13.6 Extension negotiation

Modern 正式提供 extension map。

官方 extension 使用：

```text
io.modelcontextprotocol/...
```

第三方应使用反向 DNS：

```text
com.example/...
```

Extension 必须是 opt-in；
一方支持、另一方不支持时，
支持方 **MUST** 二选一：

- 回退到 core protocol behavior；
- 或用适当错误拒绝请求。

Extension 自身 **SHOULD** 说明预期 fallback。
因此“明确失败”也可能是合规选择，
不能一概要求静默降级。

见
[Extensions Overview](https://modelcontextprotocol.io/extensions/overview)。

---

## 14. 显式状态 handle：无状态不等于无连续性

### 14.1 为什么需要 handle

有些操作天然跨请求：

- 分页查询；
- 沙箱；
- 购物车；
- 长任务；
- 上传会话；
- 外部工作流；
- MRTR 中间状态。

Modern 不禁止这些状态。

规范要求跨请求状态由 Client
在每个相关请求中携带显式 identifier。
一种常见做法是创建 Tool 返回 handle，
后续 Tool 再把它当普通参数传回：

```mermaid
sequenceDiagram
    participant C as "Client"
    participant S1 as "Server Instance A"
    participant DB as "Durable State"
    participant S2 as "Server Instance B"
    C->>S1: "create_workspace"
    S1->>DB: "保存状态"
    S1-->>C: "workspaceHandle=w_8K..."
    C->>S2: "run(handle=w_8K..., command=...)"
    S2->>DB: "按 handle + auth context 查找"
    DB-->>S2: "workspace"
    S2-->>C: "complete"
```

### 14.2 handle 的推荐性质

**【事实】**
Handle 不是新的 protocol method、schema type 或 wire feature；
它只是 Tool 结果和参数里的普通应用数据。

**【非规范设计建议】**
这类 handle 通常最好：

- 显式出现在参数或结果中；
- 对 Client opaque；
- 可在任意实例解析或查找；
- 有清晰 scope；
- 有过期策略；
- 与授权上下文共同校验；
- 不依赖 transport connection identity。

SEP-2567 给出完整动机，
见
[Sessionless via Explicit State Handles](https://modelcontextprotocol.io/seps/2567-sessionless-mcp)。

### 14.3 handle 不是权限

危险写法：

```text
只要知道 workspaceHandle，
就允许访问 workspace。
```

正确写法：

```text
lookup(
  handle,
  authenticated_subject,
  tenant,
  required_scope
)
```

如果 handle 本身是 bearer secret：

- 需要足够熵；
- 不能出现在日志和 URL；
- 需要 TTL；
- 需要可撤销；
- 泄露后风险等同 credential。

### 14.4 connection 不是 conversation

当前规范明确说：

- stdio process 不是 conversation；
- HTTP connection 不是 session；
- Client 可在同一 transport 中交错无关请求；
- Server 不得把 process identity
  当作 conversation continuity。

**【解释】**
Host 可以有十个聊天 thread，
复用同一个 Server process。

Server 需要 thread 状态时，
必须通过显式、经过授权的参数表达。

---

## 15. MRTR：把 Server 回调改写成可重试结果

MRTR 是 **Multi Round-Trip Requests**。

规范入口：

- [Message Patterns](https://modelcontextprotocol.io/specification/2026-07-28/basic#message-patterns)
- [SEP-2322：MRTR](https://modelcontextprotocol.io/seps/2322-MRTR)

### 15.1 它解决什么

Tool 执行到一半可能需要：

- 用户补充字段；
- 用户选择选项；
- Client 执行 elicitation；
- Client 进行 sampling；
- Client 提供 roots 信息。

Legacy：

```text
Server → Client 发一条独立 request
```

Modern：

```text
Server ← 返回 input_required
Client 解决输入
Client → 重试原 RPC
```

### 15.2 时序

```mermaid
sequenceDiagram
    participant C as "Client"
    participant S1 as "Server A"
    participant U as "用户 / Client feature"
    participant S2 as "Server B"
    C->>S1: "tools/call id=10"
    S1-->>C: "resultType=input_required"
    Note over S1,C: "inputRequests + opaque requestState"
    C->>U: "展示表单或执行 Client feature"
    U-->>C: "inputResponses"
    C->>S2: "重试 tools/call id=11"
    Note over C,S2: "原样 requestState + inputResponses"
    S2-->>C: "resultType=complete"
```

### 15.3 三个关键不变量

1. 重试使用新的 JSON-RPC `id`。
2. `requestState` 对 Client opaque。
3. Client 必须把 `requestState` 原样返回。

不要：

- 解析并修改 `requestState`；
- 把 JSON-RPC `id` 当业务状态 handle；
- 假设重试回到原实例；
- 在没有 capability 时发起对应 input request。

### 15.4 概念化响应

```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "approval": {
        "method": "elicitation/create",
        "params": {
          "mode": "form",
          "message": "请选择部署环境",
          "requestedSchema": {
            "type": "object",
            "properties": {
              "environment": {
                "type": "string",
                "enum": [
                  "staging",
                  "production"
                ]
              }
            },
            "required": [
              "environment"
            ]
          }
        }
      }
    },
    "requestState": "opaque-state-from-server"
  }
}
```

这里的 `approval` 是 Server 分配的关联 key；
重试时 `inputResponses.approval`
必须放对应的 `ElicitResult`，
并用新的 JSON-RPC `id`、原样带回 `requestState`。

### 15.5 MRTR 的代价

它带来：

- 更容易横向扩容；
- 更清晰的重试边界；
- 不需要 Server 主动连回 Client；
- 中间状态显式传递。

也要求开发者处理：

- 幂等性；
- state TTL；
- 重放；
- 用户取消；
- 重试时外部副作用是否已经发生；
- 多轮输入的授权一致性。

**【评价】**
MRTR 消除了协议对持久回调通道的依赖，
没有消除分布式 workflow 的复杂性。

---

## 16. Modern transports

当前标准 binding 仍是：

- stdio；
- Streamable HTTP。

见
[Transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)。

### 16.1 Modern stdio

当前 stdio 仍然是：

- Client 启动 Server 子进程；
- stdin/stdout 交换 UTF-8 JSON-RPC；
- 每条消息一行；
- Server 可把日志写 stderr；
- stdout 不能混入非协议内容。

见
[stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)。

变化在于协议语义：

- Client request 每次自描述；
- Server 不再发独立 JSON-RPC request；
- 需要输入时返回 MRTR；
- 同一 process 可承载无关 conversation。

### 16.2 Modern Streamable HTTP

```mermaid
flowchart LR
    C["Client"]
    G["Gateway<br/>读取 method/name headers"]
    S1["Stateless Instance 1"]
    S2["Stateless Instance 2"]
    S3["Stateless Instance 3"]
    C -->|"POST /mcp<br/>request A"| G
    C -->|"POST /mcp<br/>request B"| G
    G --> S1
    G --> S2
    G --> S3
```

每个请求独立 POST 到 MCP endpoint。

响应可以是：

- 单个 JSON；
- 与本请求绑定的 SSE stream。

长期通知使用：

```text
subscriptions/listen
```

见
[Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)。

### 16.3 关键 HTTP headers

Modern Streamable HTTP 的 Client 义务包括：

| Header | 强度与适用范围 | 作用 |
|---|---|---|
| `Accept: application/json, text/event-stream` | 每个 JSON-RPC POST **MUST** 同时声明两种响应类型 | Client 必须能接单个 JSON 或请求范围内的 SSE |
| `MCP-Protocol-Version` | 每个 POST **MUST** | 声明协议版本；必须与 body 一致 |
| `Mcp-Method` | 所有 JSON-RPC request **REQUIRED** | 镜像 body 的 `method` |
| `Mcp-Name` | `tools/call`、`resources/read`、`prompts/get` **REQUIRED** | 镜像 `params.name` 或 `params.uri` |
| `Authorization` | 启用授权时 | 携带为该 MCP Server 签发的 Bearer token |

`Origin` 属于另一条 Server 安全义务：
Server **MUST** 验证收到的 Origin，
但规范没有把它列成非浏览器 Client 每次必发的 request metadata header。

`Mcp-Name` 适用于例如：

- `tools/call`
- `resources/read`
- `prompts/get`

Server **MAY** 在 Tool `inputSchema` 的 primitive 属性上声明
`x-mcp-header`；一旦声明，Streamable HTTP Client **MUST**
把对应参数镜像成 `Mcp-Param-{Name}`。
`Mcp-Name` 或 `Mcp-Param-*` 的值不能安全表示为普通 ASCII 时，
必须使用规范的 `=?base64?…?=` sentinel 编码；
Server 比对 body 前必须先解码。

Header 与 JSON body 不一致时：

- `HeaderMismatch`
- code `-32020`

### 16.4 Header 为什么重要

```mermaid
flowchart TD
    Req["POST /mcp"]
    Headers["Mcp-Method: tools/call<br/>Mcp-Name: delete_file"]
    Gateway["Gateway / WAF"]
    Policy["更严格审批 · 限流 · 审计"]
    Body["JSON-RPC body"]
    Req --> Headers --> Gateway --> Policy
    Req --> Body
    Gateway -->|"仍需 Server 校验 header/body 一致"| Body
```

Headers 让基础设施不必深度解析 body
就能初步分类。

但它们不是可信授权声明。

Server 仍必须：

- 解析 body；
- 验证一致性；
- 验证 token；
- 验证 Tool 参数；
- 执行业务权限。

### 16.5 被移除的 HTTP 状态机制

在 Modern core 中已移除：

- `Mcp-Session-Id`；
- standalone GET SSE；
- `Last-Event-ID` resumability；
- 基于 session 的消息路由。

**deprecated** 与 **removed** 不同：

- 这些 session / Modern handshake 相关机制
  已从 Modern core 移除；
- Legacy Server 仍可能合法使用；
- HTTP+SSE 作为 Legacy transport
  在弃用登记中；
- 兼容 Client 仍可能需要实现 fallback。

### 16.6 订阅不是 session

```mermaid
sequenceDiagram
    participant C as "Client"
    participant S as "Server"
    C->>S: "subscriptions/listen"
    Note over C,S: "这是一个长时间未完成的 request"
    S-->>C: "notifications/subscriptions/acknowledged"
    Note over C,S: "必须是该 subscription 的第一条消息"
    S-->>C: "notification + subscriptionId"
    S-->>C: "notification + subscriptionId"
    alt "HTTP"
        C-xS: "关闭 response stream"
    else "stdio"
        C-->>S: "notifications/cancelled(request id)"
    end
```

长请求仍是请求/响应模式。

状态范围属于这个 request，
而不是底层 connection。

Server 发出的订阅通知必须携带：

```text
_meta["io.modelcontextprotocol/subscriptionId"]
```

以便 Client 关联来源；
首条消息必须是
`notifications/subscriptions/acknowledged`，
并携带同一 subscription ID。
取消方式依 transport 而异：
HTTP 关闭 SSE response stream；
stdio 发送引用 `subscriptions/listen` request ID 的
`notifications/cancelled`。
见
[Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)
和
[Base Protocol / `_meta`](https://modelcontextprotocol.io/specification/2026-07-28/basic#_meta)。

---

## 17. 缓存、Extension 与 Client features

缓存不是泛泛建议。Server 对以下操作的 `resultType: "complete"` 结果 **MUST** 携带 `ttlMs` 与 `cacheScope`：

```text
server/discover · tools/list · prompts/list
resources/list · resources/templates/list · resources/read
```

`ttlMs` **MUST >= 0**；`private` 缓存 **MUST NOT** 跨 authorization context 共享。`input_required` 中间结果不可缓存，带 `inputResponses` 或 `requestState` 的 MRTR 重试结果也 **MUST NOT** 缓存，因为这些输入不在普通 cache key 内。详见当前 [Caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching)。

TTL 是新鲜度 hint，不是数据不变保证，也不是后台轮询周期；通知会立即使相关 cache stale。Tool 列表另应保持确定性顺序，以利稳定缓存和模型 prompt cache。缓存不等于授权：调用时仍须重新鉴权。变更流使用 `subscriptions/listen`，不再把可变 catalog 藏在 session 内；完整变化见 [Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)。

正式 extension 通过 capabilities opt-in、可独立演进；一方不支持时，支持方必须选择回退 core 或明确拒绝，extension 自身应说明预期 fallback，不能把 extension 冒充 core。当前代表：

- [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview)：Tool 可关联 `ui://` 资源，在 Host 的 sandboxed iframe 中展示；支持情况由 Host 决定。
- [Tasks](https://modelcontextprotocol.io/extensions/tasks/overview)：长任务可返回 `resultType: "task"` 与 durable `taskId`，Client 用 `tasks/get`、`tasks/update`、`tasks/cancel`；状态包括 `working`、`input_required`、`completed`、`failed`、`cancelled`。取消是 cooperative：`tasks/cancel` 只确认取消意图，Server 不保证停下，Task 仍可能 `completed` 或 `failed`。它是官方 extension，不是所有实现都必须支持；最终设计见 [SEP-2663](https://modelcontextprotocol.io/seps/2663-tasks-extension)。

```mermaid
stateDiagram-v2
    [*] --> working
    working --> input_required
    input_required --> working: "tasks/update"
    working --> completed
    working --> failed
    working --> cancelled: "tasks/cancel（若被采纳）"
    input_required --> cancelled: "tasks/cancel（若被采纳）"
```

Client feature 状态必须精确区分：

| Feature | `2026-07-28` 状态 | 新实现应怎样做 |
|---|---|---|
| Elicitation | 当前 core feature | 在 MRTR 中向用户补问；form 不得索取密码、token、API key、支付凭据，敏感流程用 URL mode；见 [Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation) |
| Sampling | **deprecated，尚未 removed** | 兼容实现仍可支持；新 Server 优先直接接模型 API；见 [Sampling](https://modelcontextprotocol.io/specification/2026-07-28/client/sampling) |
| Roots | **deprecated，尚未 removed** | 仅是信息提示，从来不是文件权限边界；新设计用 Tool 参数、Resource URI 或 Server 配置；见 [Roots](https://modelcontextprotocol.io/specification/2026-07-28/client/roots) |
| Logging | **deprecated，尚未 removed** | stdio 用 stderr，服务端观测优先 OpenTelemetry |

官方[弃用登记](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)规定 Roots、Sampling、Logging、DCR 最早只能在 `2027-07-28` 当日或之后的修订移除。教程不能把 deprecated 写成“已不能用”，也不能把 Modern 已移除的 session 机制写成“只是建议不用”。

---

## 18. HTTP Authorization 与安全责任

HTTP 授权是可选能力；启用时，MCP Server 是 OAuth protected resource，Client 是 OAuth client，Authorization Server 独立存在。stdio **SHOULD NOT** 套用这套 HTTP OAuth 流程，通常从环境取得凭据。规范见 [Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)。

```mermaid
sequenceDiagram
    participant C as "MCP Client"
    participant R as "MCP Resource Server"
    participant P as "Protected Resource Metadata"
    participant A as "Authorization Server"
    C->>R: "POST /mcp without token"
    R-->>C: "401 + WWW-Authenticate resource_metadata=URL"
    C->>P: "GET resource_metadata URL"
    P-->>C: "authorization_servers"
    C->>A: "发现 AS metadata / 注册 client"
    C->>A: "Authorization Code + PKCE + resource"
    A-->>C: "code + 可选 iss"
    C->>C: "按 AS 宣告与响应 presence 规则校验 iss"
    C->>A: "code + verifier + resource"
    A-->>C: "audience-bound access token"
    C->>R: "Authorization: Bearer …"
    R->>R: "校验 issuer · audience · scope"
    R-->>C: "MCP response"
```

最低安全清单：

- Authorization Code + PKCE S256；跳转前记录经验证的 expected issuer。若响应带 `iss`，Client **MUST** 与 expected issuer 做精确比较；若 AS 宣告支持 response `iss` 却漏发，Client **MUST** 拒绝。若既未宣告也未返回，最低规范允许继续；要求所有 AS 都必须返回 `iss` 属于更严格的本地策略。
- 授权和 token 请求携带 `resource`；Server 校验 audience。
- Bearer token 只放 `Authorization` header，不放 query。
- 禁止 token passthrough：Server 只接受为自己签发的 token。
- Client registration 绑定 issuer；优先预注册或 Client ID Metadata Document；DCR 已 deprecated。
- HTTP Server 必须验证 `Origin` 防 DNS rebinding；本地服务默认绑定 loopback。
- `clientInfo`/`serverInfo` 是自报展示信息，禁止当身份。
- Tool 描述、annotations、Prompt、Resource 内容均视为不可信输入。
- 外部 JSON Schema `$ref` 默认禁止联网解析；限制 schema 深度、子 schema 数或验证时间，防 SSRF/DoS；见 [JSON Schema Usage](https://modelcontextprotocol.io/specification/2026-07-28/basic#json-schema-usage)。
- 每次按认证主体、tenant、scope 校验显式 handle；handle 不是授权。
- Host 对副作用 Tool 保留可见性、确认、拒绝和审计；Server 间最小权限隔离。

更完整的 OAuth 威胁说明见 [Authorization Security Considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)。

---

## 19. 迁移与兼容：不要在一条连接里猜版本

```mermaid
flowchart TD
    Start["Client 要连接 Server"]
    T{"Transport?"}
    Start --> T
    T -->|"stdio"| D["先发 server/discover probe"]
    D -->|"DiscoverResult / recognized modern error"| M["留在 Modern；必要时换共同版本重试"]
    D -->|"非 Modern error 或 timeout"| L["回退 initialize；同 process 也可双栈"]
    T -->|"HTTP"| H["带 Modern headers 发第一个请求"]
    H -->|"2xx / recognized modern JSON-RPC error"| M
    H -->|"4xx 且无 recognized modern error body"| L
```

迁移顺序：

1. 先冻结当前 Legacy 行为和 conformance tests。
2. Server 实现 `server/discover`，同时保留 Legacy `initialize` 处理路径；双栈可共用 endpoint/process。
3. 让核心 handler 不再读取 initialize/session 隐式状态。
4. 为每个 request 校验版本与 Client capabilities。
5. 跨请求业务状态改成显式 identifier；若采用 handle 设计模式，补授权、TTL、幂等和重放测试。
6. Server→Client request 改成 MRTR；长任务评估 Tasks extension。
7. HTTP 移除 `Mcp-Session-Id` 依赖、standalone GET SSE 与 event resume；通知改 `subscriptions/listen`。
8. 增加 `Accept`、`MCP-Protocol-Version`、`Mcp-Method`/`Mcp-Name` 等 required headers，并验证 header/body 一致。
9. 增加 cache hints 与确定性 list 顺序。
10. 观测双栈流量，再按官方 deprecation policy 退役 Legacy。

兼容性要点：

- Modern Server 必须有 `server/discover`；Modern Client不必须预调用。
- stdio 双栈 Client 应先 discovery；只有非 recognized-modern error 或 timeout 才 fallback。HTTP 只有 `4xx` 且没有 recognized modern JSON-RPC error body 才 fallback；`UnsupportedProtocolVersionError` 证明对端是 Modern，应选择共同版本重试。双栈 Server 可以在同一 process/endpoint 依据 opening shape 选择 era；见 [Discovery / When to Call](https://modelcontextprotocol.io/specification/2026-07-28/server/discover#when-to-call)。
- Modern Client 收到旧响应缺少 `resultType` 时按 `complete`。
- 旧 `resource not found` code `-32002` 仍应被兼容 Client 接受；Modern 改用 `-32602`。
- Tasks 的旧实验 wire shape 与当前 extension 不兼容，必须显式迁移。
- “SDK 能编译”不证明协议兼容；抓取实际 wire message 验证版本、metadata、headers、error 和 retry。

---

## 20. MCP 不解决的边界

MCP 不自动保证：

- Tool 是安全或正确的；
- 模型会选对 Tool；
- 用户真的理解了批准内容；
- OAuth token scope 足够细；
- Tool call 具有幂等性；
- 后端 API 不会 429；
- 多步事务具有原子性；
- Resource 内容没有 prompt injection；
- Server 保存的业务状态不会丢；
- Host UI 会支持全部 extension；
- sandbox、数据驻留、审计与合规已经完成；
- 同名 Tool 在不同 Server 上语义一致。

**【评价】**
MCP 标准化“接口和责任落点”，不是把责任消灭。越接近真实副作用，越要依赖 Host policy、Server authorization 和后端事务共同防护。

---

## 21. 问题 → 证据 → 变化 → 剩余责任总表

| 问题 | 官方证据 | Modern 变化 | 仍由谁负责 |
|---|---|---|---|
| session 阻碍扩容 | [SEP-2575](https://modelcontextprotocol.io/seps/2575-stateless-mcp) | 移除 initialize/session；每请求自描述 | Server 设计 durable state；平台部署 |
| session scope 含糊 | [SEP-2567](https://modelcontextprotocol.io/seps/2567-sessionless-mcp) | 移除 session；跨请求状态显式引用，handle 只是普通 Tool 数据的设计模式 | 应用定义 scope、TTL、auth binding |
| callback 依赖双向流 | [SEP-2322](https://modelcontextprotocol.io/seps/2322-MRTR) | `input_required` + retry | 幂等、取消、重放、副作用边界 |
| 版本/能力藏在握手 | [Versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning) | per-request `_meta` + optional discovery | Client 选择兼容版本 |
| 网关看不懂 POST | [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) | method/name headers | 网关策略；Server 一致性校验 |
| catalog 难缓存 | [Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) | TTL、scope、稳定顺序、listen | 权限变化与失效策略 |
| 长任务阻塞 | [Tasks](https://modelcontextprotocol.io/extensions/tasks/overview) | opt-in Tasks extension | durable worker、进度、保留期 |
| OAuth mix-up/token 误投 | [Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) | `iss`、PKCE、resource audience | AS 配置、token storage、scope |
| Tool 可造成副作用 | [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) | schema、结果与安全指导 | Host consent；Server authorization |
| schema 可触发 SSRF/DoS | [Base Protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic#json-schema-usage) | 禁止默认远程 `$ref`、要求资源边界 | validator 配额、allowlist、监控 |

---

## 22. 来源分级、漂移与一致性

来源优先级：

1. 冻结 commit 的 TypeScript schema：wire shape 的 source of truth。
2. 带日期的 `2026-07-28` / `2025-11-25` normative spec。
3. Final SEP、官方 changelog、deprecated registry。
4. 官方发布博客与 SDK 文档：解释动机和实现，但不覆盖 schema。
5. 社区教程：只作延伸阅读，绝不反推当前规范。

一致性规则：

- 网页与 schema 冲突：以冻结 schema 为准并记录 doc drift。
- 不带日期 Learn 页面与日期规范冲突：以日期规范为准。
- 发布博客的简化 JSON 漏字段：以 normative spec 为准。
- SDK README 与 wire 抓包冲突：分别记录 SDK 文档行为和实际行为。
- 同一修正必须同步更新正文、表格、Mermaid、迁移步骤和结论。
- 所有 “MUST / SHOULD / MAY” 在改写前复核原文强度。
- 所有 “deprecated / removed / optional extension” 分开检索，禁止互换。

### 22.1 非规范延伸阅读

以下资料只帮助换一个角度理解，**不进入事实证据链**：

- Microsoft 的 [MCP for Beginners：2026-07-28 Release Candidate](https://github.com/microsoft/mcp-for-beginners/blob/main/01-CoreConcepts/mcp-2026-07-28-release-candidate.md)：图解清楚，但标题和正文明确基于 RC，仓库 `main` 还会漂移；其简化请求示例不能替代 final schema。
- [mcp-from-scratch](https://github.com/pguso/mcp-from-scratch)：零依赖手写 JSON-RPC/stdio，适合理解 Legacy 内部；README 明确针对 `2025-11-25`，生命周期和 sampling 不能照搬到 Modern。
- Postman，2026-07-29，[MCP goes stateless — and Postman's ready](https://blog.postman.com/mcp-goes-stateless-and-postmans-ready/)：适合理解双栈测试与 Inspector 工作流；产品自动探测行为不是 MCP Client 的普遍规范义务。
- MCP Migration Studio，2026-06-09，[2026-07-28 migration guide](https://mcpmigrate.dev/blog/mcp-spec-2026-07-28-migration-guide)：迁移排查清单实用，但文章基于 RC；其中 `_meta` 示例使用未加命名空间的键且漏掉必需 `clientCapabilities`，不能复制到 final 实现。
- [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)：威胁分类实用；session-ID 等机械细节可能仍指向 Legacy，最终以日期规范为准。
- Microsoft Azure Architecture Blog 的 [API vs MCP decision matrix](https://techcommunity.microsoft.com/blog/azurearchitectureblog/decision-matrix-api-vs-mcp-tools-%E2%80%94-the-great-integration-showdown-%F0%9F%A5%8A/4499385)：适合作为“MCP 不取代 API”的工程反方视角，不是协议证据。

阅读任何 “MCP 2.0 tutorial” 或 SDK v2 guide 时，先确认其目标 revision，再检查它是否把 JSON-RPC 2.0、SDK v2、Legacy Tasks 或 `initialize` 误当当前协议。

---

## 23. 最终心智模型

```mermaid
flowchart TB
    U["用户意图与批准"]
    H["Host<br/>对话 · 模型 · 策略 · 隔离"]
    C["每 Server 一个 MCP Client"]
    P["Modern MCP 2026-07-28<br/>无状态 JSON-RPC 应用协议"]
    T["stdio / Streamable HTTP"]
    S["MCP Server<br/>Prompt · Resource · Tool"]
    B["后端 API / DB / Files"]
    U --> H --> C --> P --> T --> S --> B
    S -. "input_required" .-> C
    C -. "MRTR 新 id 重试" .-> S
```

记住四句话：

1. 官方没有语义版本 “MCP 2.0”；本文只把它当 Modern era 教学简称。
2. JSON-RPC 2.0 是信封，MCP `2026-07-28` 才是协议修订。
3. Modern 的核心不是“功能更多”，而是每请求自描述、显式状态和可重试交互。
4. 协议建立共同边界；授权、隔离、幂等、事务和用户控制仍需实现者完成。

---

<script type="module" src="../assets/js/util/mermaid-render.js"></script>
