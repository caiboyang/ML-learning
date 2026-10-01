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

在浏览器打开 `http://127.0.0.1:8765/`。这只是本机预览，不是部署。替换 JSON 中的公司、数据、日期和证据；没有真实来源的条目不能仅删除“教学构造”标签就拿去使用。`notice` 应保留实际证据范围，例如内部自报、未审计或缺少留存。

## 数据结构

[research.schema.json](../assets/research-dashboard/research.schema.json) 定义字段类型与枚举；[research.json](../assets/research-dashboard/research.json) 是虚构自有业务测试夹具；[external-research.json](../assets/research-dashboard/external-research.json) 是有来源的 Clubhouse 外部研究示例。前者只验证自有业务流程；后者展示真实证据的支持范围，均须按新任务重新取证。所有文本按纯文本呈现，不接受 HTML；来源链接只接受具有有效 URI 的 HTTP/HTTPS；校验器必须启用 URI format。运行时遇到无效 URL 会保留来源正文并显示不可点击的提示，不中断报告加载。稳定 ID 使用小写字母、数字和连字符，必须全局唯一，且不能与页面固定 ID 冲突。

| 对象 | 字段 | 含义 |
| --- | --- | --- |
| `meta` | `taskType, title, question, asOf, scope, notice, verdictId, keyMetricIds, subjectCompanyId, actionSectionId` | 任务类型、对象、问题、截止日、范围与证据边界；首屏引用判断与指标 ID，不另抄数字；指定研究对象和页尾行动／调查的主节 |
| `companies[]` | `id, name, period, case?` | 可切换对象及分析时期；不把当前形态当早期形态 |
| `sections[]` | `id, title, part, overviewIds, thesis, conclusion, evidenceIds` | 任意稳定 ID、必填的具体产物标题、覆盖部分、在总览展示的记录、论点与结论 |
| `topics[]` | `id, title, parentSectionId, argument, verdictId, modules` | 对应主节、一行论证路线及 3–6 个模块；引用同一批记录 |
| `records[]` | `id, companyId, section, kind, role` | 一条可定位记录；`companyId: null` 为明确标识的全局内容 |
| 记录正文 | `title, text, status, limitation` | 判断、叙述、证明或决策状态、始终可见的限制 |
| 记录关系 | `evidenceIds, relatedIds` | 来源 ID 与相关结论、问题、行动 ID；不可悬空 |
| 可选表达 | `stage, metric, fields, edges, comparisonIds` | 阶段标签、带口径指标、同字段描述表、带证据状态的回路边 |
| `evidence[]` | `id, title, nature, date, locator, url, support, limitation` | 来源身份、日期、具体位置、支持范围和局限；无公开链接时 `url: null` 并写记录位置 |

`taskType` 为 `own-business`（自有业务决策）或 `external-company`（外部公司研究）。`sections[]` 的 `id` 和 `title` 按实际议题填写，不限定六／七节。`part` 用于覆盖检查与排序，顺序为 `verdict → assets → decisions → choices → validation → paths → questions`，同 part 内保持 JSON 顺序。它落实“研究对象 → 决策与下一步 → 公司对标 → 证据”：`assets` 包括目标公司的自身路径与回路；`paths` 只放对标分析。自有业务可无 `decisions`；外部研究需要历史决策、借鉴条件与调查，不能只换标题。`questions` 的证据与问答覆盖也可由内置证据库、核验专题和调查中的问题完成，不必为枚举凑一个空主节。

`overviewIds` 决定主节展示的完整产物记录，每个分析节至少一项；内置证据库不属于 `sections[]`。具体分工以 [呈现规范](result-presentation.md#主页面与专题分工) 为准。语义校验要求研究对象或全局的 `proof / step / decision / loop / advice / route / action / contract / transfer` 及全部 `comparison` 出现在主页面；独立主节只涉及一家公司的案例步骤也须全部展示。普通对标的档案和步骤、补充 `series / funnel / change` 可仅在子页。记录通过 `record.section` 归属主节，子页可复用主产物并增加论证；每条记录必须能从主页面或专题访问。主节末尾按 `parentSectionId` 自动生成子页入口；记录 ID 不进入目录。来源库作为目录最后一项。

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
- `series` 包含 `unit, definition, points[]`；每点含 `period, value, basis, evidenceIds`；`value: null` 时必须有 `missingReason`，按数据原文显示缺失原因。数值非负或 `null`，缺失不变成零；不同指标分别建序列，口径变化写入 `basis`，不可比时拆序列。按观察顺序展示带数值的比例条与表格，条长从零起，不暗示等距时间。例如“已查资料但没有可靠数据”“尚未到观察期”必须区分；`basis` 继续说明对象、分母与窗口。
- `funnel` 包含 `cohort, overlap, nodes[]`。每节点含 `id, parentId, label, count, denominator, basis, proved, unproved, evidenceIds`，节点 ID 在该漏斗内唯一，根的 `parentId: null`，其他父节点必须存在且无循环。人数和分母为非负整数或 `null`；已知人数不大于分母。每节点写事件、窗口、分母定义及支持／未支持判断，通常整条标为解释。分支可能重叠时说明交集，不相加也不串成连续转化。
- `change` 包含 `before, newEvidence, direction, after, impact`；`direction` 为上调／下调／维持。记录新证据性质，并将变化落实到被关联的判断、图表与行动。
- `companies[].case` 包含 `parentSectionId, argument, verdictId` 和 3–6 个 `modules[]`，重点案例通常用四模块；每个模块含 `id, title, thesis, conclusion, recordIds`。模块内容按 [案例合同](research-contract.md#重点公司专题的最低结构) 填写，版式按呈现规范。
- `topics[].id` 使用任意稳定 ID（保留 `case` 给公司案例路由），例如 `comparisons / advice / decision / audit`，通过 `?view=...` 直达。`parentSectionId` 指向主要展开的主节，`argument` 用 3–6 个短语呈现论证路线；模块数量受 schema 约束；类型和内容要求见 [呈现规范](result-presentation.md#主页面与专题分工)。模块字段同公司专题，跨视图可复用记录；同一视图内不得重复记录 ID。专题末尾由 `meta.actionSectionId` 生成返回入口。
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

来源明细始终保留完整支持边界；团队行、序列点、漏斗节点与回路边的来源也参与反向索引和可选的来源搜索。“只看事实”不隐藏记录自身的限制。点击关联记录或来源的返回链接时，若目标被过滤，会恢复必要条件，再定位并聚焦。直接访问记录锚点也应可用。`?view=case&company=servicebench` 直接打开四模块专题；若目标在当前专题之外，总览包含该记录时回总览，否则进入包含它的专题，恢复必要筛选再定位。少量内容可删不必要的筛选，但不能删来源和口径。

JSON 是唯一内容来源。Agent 按 [研究合同](research-contract.md#怎样提问才有用) 处理回答并更新关联记录；模板只渲染，不自动推理。

## 验收

先用支持 Draft 7 的 JSON Schema 校验器验证结构，再检查 schema 不表达的语义：ID 全局唯一（漏斗节点另有局部命名空间）；不与固定页面 ID 重复；公司、来源、关联记录全部存在；首屏引用角色正确；主节标题与 part 覆盖、任意 section ID、父子页引用、行动入口与总览记录归属正确，每条记录有可访问页面；同视图无重复记录、漏斗父节点存在且无环、数量不超过分母；每个关键判断有证据或明确缺口；实际金额与比率复算一致。校验 schema 不等于核实业务事实。

逐项填写 [研究合同的内容覆盖清单](research-contract.md#内容覆盖清单交付时逐项填写)，为团队、每家对标、数据核验、决策复盘等标出实际记录与支持证据。存在一个空组件、填了“未知”或通过结构校验，都不能替代实质分析。

在 1280×900 和 390×844 视口操作公司切换、组合搜索、性质筛选、空结果、重置、目录、证据链接及返回；从带记录 hash 的 URL 重新进入，检查可读、聚焦与导航。检查控制台、正文溢出和键盘操作；布局标准按 [呈现验收](result-presentation.md#展示验收) 检查；运行验证还包括跨断点目录状态、专题直达、返回行动、仅来源命中及隐藏判断的事实视图。打印当前视图时保留日期、范围和记录边界；需要全量打印时先重置筛选。

单文件导出后移到另一目录并改名，使用 `file://` 打开；检查总览、四类专题、来源往返与被筛选记录的显露，不启动服务。另用外部研究数据验证关键决策、借鉴顺序和调查内容，而不是仅把同一份运营计划换标题。模板依赖 JavaScript；禁用脚本时只显示说明，需要无脚本阅读时另行生成正文版本。真实研究仍须按研究合同补齐专题与证据深度。

## 仓库在线演示

仓库的 `company-research/demo/` 包含生成副本。默认入口 `index.html` 与 `external.html` 都是 Clubhouse 单文件报告；`report.html` 是次要的虚构自有业务测试示例。源模板的 `index.html` 仍是可复制的数据加载入口，两者由同步脚本明确区分，不手改生成文件。从仓库根目录运行 `python3 scripts/sync-company-research-demo.py` 更新，运行同一命令加 `--check` 检查漂移；它不联网、不部署。模板与 skill 内导出脚本可复制到其他项目，不依赖仓库生成脚本。报告与 README 指向隐藏 skill 目录的链接使用 GitHub 源码绝对链接，避免 Jekyll 默认排除点目录带来的失效链接。


## 可复现的仓库验证

验证工具只用于开发，不进入交付 HTML。仓库 `scripts/package.json` 与锁文件固定 AJV 8 和 URI format 插件。需要 Node.js/npm 与 Python 3；从仓库根目录运行：

```sh
npm ci --prefix scripts --ignore-scripts
python3 scripts/sync-company-research-demo.py
npm test --prefix scripts
```

测试覆盖两种任务数据、Schema、缺失原因、HTTP(S) URL、引用、父子页与记录可达性、主产物完整性（包含“子页可达但主页面缺项”的负例）、单文件完整性和示例同步。复制 skill 到其他仓库后，可用支持 Draft 7 与 URI format 的校验器并执行上述语义检查，不依赖本仓库测试脚本。浏览器验收仍须另外进行。
