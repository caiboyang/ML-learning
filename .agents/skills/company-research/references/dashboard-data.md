# 交互模板与数据约定

完整公司调研默认使用本模板，交付可双击离线打开的单文件 HTML；Markdown 只作为按需提供的文字版，用户明确指定其他格式时遵从。模板没有框架、外部字体或脚本依赖。数据优先从 `script#research-data[type="application/json"]` 读取；没有内嵌数据时才读取同目录 `research.json`。默认交付不需要服务器，不自动部署或发布。

## 默认单文件交付

先替换示例数据并完成下方结构、引用和内容验收，再从 skill 目录运行：

```sh
python3 scripts/export-report.py /path/to/research.json /path/to/company-report.html
```

脚本将模板、样式、脚本和 JSON 合并到一个文件，用纯文本方式渲染数据，并转义内嵌 JSON 的 HTML 结束标签。导出不代替研究或数据校验。将文件改名、移到其他目录后再次双击验证；专题链接取当前文件路径，保留查询参数和锚点，不依赖 `index.html`。阅读与筛选离线可用，打开外部原始来源仍需要网络。单文件需要浏览器启用 JavaScript，不包含后端或持久化输入。

## 编辑与本机预览

复制整个 [research-dashboard](../assets/research-dashboard/index.html) 所在目录到交付目录，保留五个文件：`index.html`、`styles.css`、`app.js`、`research.json`、`research.schema.json`。在复制后的目录运行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

在浏览器打开 `http://127.0.0.1:8765/`。这只是本机预览，不是部署。替换 JSON 中的虚构公司、数据、日期和证据；没有真实来源的条目不能仅删除“教学构造”标签就拿去使用。`notice` 应保留实际证据范围，例如内部自报、未审计或缺少留存。

## 数据结构

[research.schema.json](../assets/research-dashboard/research.schema.json) 定义字段类型与枚举；[research.json](../assets/research-dashboard/research.json) 是完整示例。所有文本按纯文本呈现，不接受 HTML；来源链接只接受 HTTP/HTTPS。稳定 ID 使用小写字母、数字和连字符，必须全局唯一，且不能与页面固定 ID 冲突。

| 对象 | 字段 | 含义 |
| --- | --- | --- |
| `meta` | `taskType, title, question, asOf, scope, notice, verdictId, keyMetricIds` | 任务类型、对象、问题、截止日、范围与证据边界；首屏引用判断与指标 ID，不另抄数字 |
| `companies[]` | `id, name, period, case?` | 可切换对象及分析时期；不把当前形态当早期形态 |
| `sections[]` | `id, title?, thesis, conclusion, evidenceIds` | 本次研究论点、节末结论与证据；顺序与目录一致，可覆写标题 |
| `topics[]` | `id, title, verdictId, modules` | 横向对照、建议复盘、决策、数据核验四类专题；引用同一批记录 |
| `records[]` | `id, companyId, section, kind, role` | 一条可定位记录；`companyId: null` 为明确标识的全局内容 |
| 记录正文 | `title, text, status, limitation` | 判断、叙述、证明或决策状态、始终可见的限制 |
| 记录关系 | `evidenceIds, relatedIds` | 来源 ID 与相关结论、问题、行动 ID；不可悬空 |
| 可选表达 | `stage, metric, fields, edges, comparisonIds` | 阶段标签、带口径指标、同字段描述表、带证据状态的回路边 |
| `evidence[]` | `id, title, nature, date, locator, url, support, limitation` | 来源身份、日期、具体位置、支持范围和局限；无公开链接时 `url: null` 并写记录位置 |

`taskType` 为 `own-business`（自有业务决策）或 `external-company`（外部公司研究）。自有业务六部分依次是 `verdict, assets, paths, choices, validation, questions`；外部研究在 `paths` 后加入 `decisions`，并将 `choices` 展示为借鉴顺序，`validation` 展示为下一步调查与数据缺口。可在 `sections[].title` 定制标题。改变类型后，Agent 必须重写对应论点和内容：外部研究需要历史决策及观察结果、借鉴条件、调查计划，不能只改标题而保留替公司安排运营的内容。

`kind` 是 `fact`、`inference` 或 `recommendation`；`status` 单独解释已证明、有信号、待验证、现在复制等状态。内部自报不会因为选了 `fact` 而变成独立核验事实，证据的 `nature` 与记录的 `limitation` 必须保留。

`role` 表达记录作用：`judgment / metric / proof / asset / profile / step / tradeoff / loop / transfer / route / advice / gate / meeting / action / contract / question / comparison / team / decision / series / funnel / change`。它决定展示组件，不自动推断事实或证明业务完整。指标用指标行，证明用表，步骤用时间线，建议用采纳看板，路线用阶段卡，计划用分段时间表，会议用独立决定条目；解释与合同保留正文和字段表。混合历史事实与复盘解释的整条记录应标 `inference`，不要用事实标签掩盖解释。

- `metric` 含显示值 `value`、单位 `unit`、分母／时间／对象口径 `basis`。这是展示值，不会自动做经营计算；研究者先复算再填写。
- `fields` 是 `{label, value, kind?}` 数组；混合记录的解释字段应标 `kind: inference`，事实筛选会隐藏该解释字段，但保留口径与限制。其余字段继承记录性质，适用于公司档案、门槛、迁移与数据合同。替换为真实客户、资产、动作和记录，不保留空壳。
- `comparisonIds` 指向有 `fields` 的公司档案。`columns` 可定义所需字段名称，例如 `["起点资产", "第一批用户", "结果", "启示"]`；省略时采用起点资产、第一批用户、第一个产品、第一种收入。矩阵和搜索都读取这些字段并尊重字段性质筛选，避免维护两套值。
- `edges` 每条含 `from, to, mechanism, status, evidenceIds`，说明回流发生的方式与证据；未闭合的链路称为流程，不称已成立的飞轮。
- `proof` 必须包含 `proposition, state, evidence, gap, next`；`state` 为已证明／有信号／未证明／反证／不适用。状态为不适用时必须有 `naReason`。按业务定义命题，不能机械套用付费服务的六项。证明状态是判断，通常标为 `kind: inference`，证据记录另标身份。
- `meeting` 必须包含 `confirmationType, decision, basis, condition, owner, reviewAt`；确认类型为必须确认／信任底线／产品边界／明确删除。每条决定独立记录，不借用路线类型。
- `route` 包含 `priority, condition`，明确当前推荐／第二阶段／暂缓及进入条件；`advice` 的 `adoption` 为立即采用／带条件采用／明确删除／待确认。这两种分类互不替代。
- `action` 的 `milestones[]` 包含 `period, action, owner, observe, decision`：阶段、动作、负责人、观察与继续／停止条件；不能只有日期。
- `team` 的 `people[]` 包含 `name, role, background, responsibility, commitment, evidenceIds`，逐人呈现团队与分工。姓名未披露就写未知；`responsibility` 明确实际、拟议或待确认，不能把分析建议写成已任命。
- `decision` 包含 `period, context, knownThen, options, chosen, outcome, tradeoff, assessment, falsifier`，分别呈现当时约束和信息、备选身份、实际选择、后续观察、机会成本、研究者复盘与反证。与面向未来的 `route`、会议确认 `meeting` 分开。
- `series` 包含 `unit, definition, points[]`；每点含 `period, value, basis, evidenceIds`。数值非负或 `null`，缺失不变成零；不同指标分别建序列，口径变化写入 `basis`，不可比时拆序列。按观察顺序展示带数值的比例条与表格，条长从零起，不暗示等距时间。未披露／未到期的具体原因仍写 `basis`。
- `funnel` 包含 `cohort, overlap, nodes[]`。每节点含 `id, parentId, label, count, denominator, basis, proved, unproved, evidenceIds`，节点 ID 在该漏斗内唯一，根的 `parentId: null`，其他父节点必须存在且无循环。人数和分母为非负整数或 `null`；已知人数不大于分母。每节点写事件、窗口、分母定义及支持／未支持判断，通常整条标为解释。分支可能重叠时说明交集，不相加也不串成连续转化。
- `change` 包含 `before, newEvidence, direction, after, impact`；`direction` 为上调／下调／维持。记录新证据性质，并将变化落实到被关联的判断、图表与行动。
- `companies[].case` 包含 `verdictId` 和四个 `modules[]`；每个模块含 `id, title, thesis, conclusion, recordIds`，按互补资产、交易交付、取舍、回路迁移组织。记录可复用，不复制正文。没有充分材料的公司不生成空专题。
- `topics[].id` 为 `comparisons / advice / decision / audit`，通过 `?view=...` 直达。模块字段同公司专题，跨视图可复用记录；同一视图内一条记录只出现一次，避免重复锚点。对照页逐家公司同结构展开；建议页分类复盘；决策页区分自有路线和外部历史取舍；核验页包含口径、序列、漏斗分支、判断变化和数据合同。专题与记录目录由当前视图生成，末尾回到验证或下一步调查。
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

公司、搜索词、内容性质按 AND 组合。公司条件保留全局记录；默认搜索可见正文和公司名称，勾选“包含关联来源”才搜索来源全文。界面单独标记仅来源命中，显示匹配条数和条件。这些条数是文档记录数，不是客户或财务合计。全局结论和首屏目标业务指标不随正文公司筛选重算，界面明确标识；指标不属于筛选结果的经营汇总。选择事实时隐藏首屏推论、章节论点与结论，以及混合记录中的解释字段，仍保留事实口径和限制。

来源明细始终保留完整支持边界；团队行、序列点、漏斗节点与回路边的来源也参与反向索引和可选的来源搜索。“只看事实”不隐藏记录自身的限制。点击关联记录或来源的返回链接时，若目标被过滤，会恢复必要条件，再定位并聚焦。直接访问记录锚点也应可用。`?view=case&company=servicebench` 直接打开四模块专题；若目标在当前专题之外，恢复总览后定位。少量内容可删不必要的筛选，但不能删来源和口径。

JSON 是唯一内容来源。每次用户回答后检查：证明状态、资产可用性、对标匹配、迁移分类、主路线、门槛、行动、摘要和图表。模板不会根据一句回答自动推理这些变化；Agent 负责更新所有受影响记录，并记录原因。

## 验收

先用支持 Draft 7 的 JSON Schema 校验器验证结构，再检查 schema 不表达的语义：ID 全局唯一（漏斗节点另有局部命名空间）；不与固定页面 ID 重复；公司、来源、关联记录全部存在；首屏引用角色正确；任务对应的六节或七节 ID、专题模块与记录引用完整；同视图无重复记录、漏斗父节点存在且无环、数量不超过分母；每个关键判断有证据或明确缺口；实际金额与比率复算一致。校验 schema 不等于核实业务事实。

逐项填写 [研究合同的内容覆盖清单](research-contract.md#内容覆盖清单交付时逐项填写)，为团队、每家对标、数据核验、决策复盘等标出实际记录与支持证据。存在一个空组件、填了“未知”或通过结构校验，都不能替代实质分析。

在 1280px 和 390px 宽度操作公司切换、组合搜索、性质筛选、空结果、重置、目录、证据链接及返回；从带记录 hash 的 URL 重新进入，检查可读、聚焦与导航。检查控制台、正文溢出和键盘操作；还要从窄屏拉宽，确认目录自动展开，测试专题直达、返回行动、仅来源命中及隐藏判断的事实视图。打印当前视图时保留日期、范围和记录边界；需要全量打印时先重置筛选。

单文件导出后移到另一目录并改名，使用 `file://` 打开；检查总览、四类专题、来源往返与被筛选记录的显露，不启动服务。另用外部研究数据验证关键决策、借鉴顺序和调查内容，而不是仅把同一份运营计划换标题。模板依赖 JavaScript；禁用脚本时只显示说明，需要无脚本阅读时另行生成正文版本。真实研究仍须按研究合同补齐专题与证据深度。

## 仓库在线演示

仓库的 `company-research/demo/` 包含五个源文件的生成副本与单文件 `report.html`，用于演示，不单独编辑。从仓库根目录运行 `python3 scripts/sync-company-research-demo.py` 更新，运行同一命令加 `--check` 检查漂移；它不联网、不部署。模板与 skill 内导出脚本可复制到其他项目，不依赖仓库生成脚本。报告与 README 指向隐藏 skill 目录的链接使用 GitHub 源码绝对链接，避免 Jekyll 默认排除点目录带来的失效链接。
