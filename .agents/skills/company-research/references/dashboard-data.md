# 交互模板与数据约定

在交付研究网页时使用本文件。纯 Markdown 任务不需要启动模板。模板是无框架、无外部字体和脚本依赖的静态起点；研究数据通过同目录 JSON 加载，需要静态 HTTP 服务，不能保证直接双击 `file://` 可用。

## 复制与运行

复制整个 [research-dashboard](../assets/research-dashboard/index.html) 所在目录到交付目录，保留五个文件：`index.html`、`styles.css`、`app.js`、`research.json`、`research.schema.json`。在复制后的目录运行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

在浏览器打开 `http://127.0.0.1:8765/`。这只是本机预览，不是部署。替换 JSON 中的虚构公司、数据、日期和证据；没有真实来源的条目不能仅删除“教学构造”标签就拿去使用。`notice` 应保留实际证据范围，例如内部自报、未审计或缺少留存。

## 数据结构

[research.schema.json](../assets/research-dashboard/research.schema.json) 定义字段类型与枚举；[research.json](../assets/research-dashboard/research.json) 是完整示例。所有文本按纯文本呈现，不接受 HTML；来源链接只接受 HTTP/HTTPS。稳定 ID 使用小写字母、数字和连字符，必须全局唯一，且不能与页面固定 ID 冲突。

| 对象 | 字段 | 含义 |
| --- | --- | --- |
| `meta` | `title, question, asOf, scope, notice` | 对象、研究问题、截止日、范围与证据边界；所有视图共用 |
| `companies[]` | `id, name, period` | 可切换对象及分析时期；不把当前形态当早期形态 |
| `records[]` | `id, companyId, section, kind, role` | 一条可定位记录；`companyId: null` 为明确标识的全局内容 |
| 记录正文 | `title, text, status, limitation` | 判断、叙述、证明或决策状态、始终可见的限制 |
| 记录关系 | `evidenceIds, relatedIds` | 来源 ID 与相关结论、问题、行动 ID；不可悬空 |
| 可选表达 | `stage, metric, fields, edges, comparisonIds` | 阶段标签、带口径指标、同字段描述表、带证据状态的回路边 |
| `evidence[]` | `id, title, nature, date, locator, url, support, limitation` | 来源身份、日期、具体位置、支持范围和局限；无公开链接时 `url: null` 并写记录位置 |

`section` 对应六部分：`verdict` 阶段与决策，`assets` 业务与资产，`paths` 对标路径，`choices` 迁移与路线，`validation` 验证与数据合同，`questions` 问答。证据索引另行集中渲染，各记录保留就近来源链接。

`kind` 是 `fact`、`inference` 或 `recommendation`；`status` 单独解释已证明、有信号、待验证、现在复制等状态。内部自报不会因为选了 `fact` 而变成独立核验事实，证据的 `nature` 与记录的 `limitation` 必须保留。

`role` 表达记录作用：`judgment / metric / asset / profile / step / tradeoff / loop / transfer / route / gate / action / contract / question / comparison`。它帮助组织语义，不自动推断事实或检查业务是否完整。

- `metric` 含显示值 `value`、单位 `unit`、分母／时间／对象口径 `basis`。这是展示值，不会自动做经营计算；研究者先复算再填写。
- `fields` 是 `{label, value, kind?}` 数组；混合记录的解释字段应标 `kind: inference`，事实筛选会隐藏该解释字段，但保留口径与限制。其余字段继承记录性质，适用于公司档案、门槛、迁移与数据合同。替换为真实客户、资产、动作和记录，不保留空壳。
- `comparisonIds` 指向公司档案记录，矩阵直接读取其统一字段，避免在矩阵和详情中维护两套值。
- `edges` 每条含 `from, to, mechanism, status, evidenceIds`，说明回流发生的方式与证据；未闭合的链路称为流程，不称已成立的飞轮。
- 问答用 `role: question` 记录问题、回答、日期、原判断和变化，并通过 `relatedIds` 指向受影响的结论与行动。页面不保存回答、不调用模型；Agent 完成核对和推理后更新数据，再刷新呈现。

最小记录示例（仍需放进完整数据并提供关联证据）：

```json
{
  "id": "c1",
  "companyId": "example",
  "section": "verdict",
  "kind": "inference",
  "role": "judgment",
  "status": "有信号",
  "title": "小批次付款成立，重复交付待验证",
  "text": "当前应验证另一个交付者能否在相同范围内完成任务。",
  "limitation": "样本小，结果来自团队自报，尚未核对明细。",
  "evidenceIds": ["e1"],
  "relatedIds": ["q1", "a1"]
}
```

## 视图与更新约定

公司、搜索词、内容性质按 AND 组合。公司条件保留全局记录；搜索覆盖记录、公司名称和关联来源，界面显示匹配条数和条件。这些条数是文档记录数，不是客户或财务合计。全局结论不随公司切换重算，必须在界面中说明。

来源明细始终保留完整支持边界；“只看事实”不隐藏记录自身的限制。点击关联记录或来源的返回链接时，若目标被过滤，会恢复能显示它的条件，再定位并聚焦。直接访问记录锚点也应可用。少量内容可以删除不必要的筛选，但不能删来源和口径。

JSON 是唯一内容来源。每次用户回答后检查：证明状态、资产可用性、对标匹配、迁移分类、主路线、门槛、行动、摘要和图表。模板不会根据一句回答自动推理这些变化；Agent 负责更新所有受影响记录，并记录原因。

## 验收

先用支持 Draft 7 的 JSON Schema 校验器验证结构，再检查 schema 不表达的语义：ID 全局唯一；不与页面固定 ID 重复；公司、来源、关联记录全部存在；每个关键判断有证据或明确缺口；实际金额与比率复算一致。校验 schema 不等于核实业务事实。

在 1280px 和 390px 宽度操作公司切换、组合搜索、性质筛选、空结果、重置、目录、证据链接及返回；从带记录 hash 的 URL 重新进入，检查可读、聚焦与导航。检查控制台、正文溢出和键盘操作。打印当前视图时保留日期、范围和记录边界；需要全量打印时先重置筛选。

模板依赖 JavaScript 渲染正文，禁用脚本时只显示说明。若任务要求无脚本阅读或完整离线单文件，应由 Agent 生成带正文的静态 HTML，不把此动态模板声称为已满足该要求。它演示的是最小交互结构；真实研究仍须按研究合同补齐专题与证据深度。
