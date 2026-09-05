# Machine Learning Study Notes

Welcome to my Machine Learning and AI study notes repository! This repository contains structured study notes, deep dives, and visual guides on various ML topics.

## Contents

### 1. Reinforcement Learning from Human Feedback (RLHF)
* [Chapter 6: Policy Gradients Study Notes](https://caiboyang.github.io/ML-learning/ch06_rlhf_policy_gradients/RLHF_Policy_Gradients_Study_Notes.html) 
  * *A comprehensive breakdown of policy gradient algorithms (REINFORCE, RLOO, PPO, GRPO, GSPO, CISPO) bridging intuition, theoretical formulas, and engineering architecture for large language models.*

### 2. Building with the Claude API
* [Phase 3 · Tool Use 周](https://caiboyang.github.io/ML-learning/phase3_tool_usage/Tool_Use_Study_Notes.html)
  * *工具调用学习笔记，约 55 分钟。从一个前提——**Claude 只能产出文本，碰不到外界**——推出四个问题，四篇 reading 各答一个：schema 怎么写才让模型调对（含 `strict` / `input_examples` / `tool_choice`）、一次调用在协议层怎么往返（`tool_use` → `tool_result`、三条会 400 的格式红线、`stop_reason` 驱动的 agentic loop）、代码到底谁在跑（client vs server tools 及版本语义）、上生产后什么会塌（prompt cache、tool search、programmatic tool calling、间接 prompt injection）。附按症状查表、课程录制后的 API 变更对照，以及一份可直接运行的参考实现。*

### 3. AI Talks & Interview Distillations
* [Demis Hassabis × Sequoia AI Ascent 2026 — *Three Quarters of the Way to AGI*](https://caiboyang.github.io/ML-learning/demis-hassabis-agi-ascent-2026/)
  * *An editorial distillation of the 27-minute fireside chat: the 75% / 2030 deadline framing, AI-for-science, simulations as a new method, ML as the right description language for biology, and tool-then-agency sequencing. ([source video](https://www.youtube.com/watch?v=AFpeWo1GTeg))*

### 4. Agent Engineering

* 🎓 [从一个 Agent 到一支可控团队 — Multi-Agent Systems 十步学习路径](https://caiboyang.github.io/ML-learning/multi-agent-systems/learn/)
  * *从 single-agent baseline 开始，用十步建立多智能体系统的决策与工程坐标：什么时候值得拆分、为什么要按上下文边界拆、ADK 的 hierarchy / Sequential / Parallel / Loop 如何表达控制流，以及 planning 为什么不等于 multi-agent。后半程用任务合同、局部失败恢复、single-agent 对照评测和一个最小研究 Lab，把“多开几个 agent”变成可验证的系统设计。页面提供步骤导航与可展开自测答案。*
  * *与下面的研究笔记配套：**这篇给取舍和顺序，那篇给完整 schema、失败轨迹、评估矩阵与来源边界**。建议先走完十步，再把研究笔记当作实现参考。*

* 📚 [Multi-Agent Systems 研究笔记：何时拆分、如何协作、怎样评测](https://caiboyang.github.io/ML-learning/multi-agent-systems/Multi_Agent_Systems_Research.html)（[Markdown 原文](multi-agent-systems/Multi_Agent_Systems_Research.md)）
  * *基于 Anthropic、Google ADK 与 LangChain 三份一手材料，建立 decomposition / assignment / execution / communication / synthesis / evaluation 六维坐标系；区分来源事实、综合解释与实践建议，并覆盖 provider-neutral 的任务合同、端到端失败恢复、成本与延迟权衡、single-agent baseline 评估矩阵、自测题和渐进式最小 Lab。*

* 🎓 [把上下文压小而不压坏 — 从零学 Agent Context Compression](https://caiboyang.github.io/ML-learning/agent-context-compression/learn/)
  * *十步学习路径，从零基础起步。假设你只知道「LLM 有上下文窗口」，读完能自己设计并评估一套压缩策略。先看一次 agent 被撑爆的死亡现场，再讲窗口这堵墙的三个反直觉性质（每轮重发全部历史、装得下≠用得好、墙的位置未必是文档写的那个）；然后建立六层坐标系，手把手走完最小可用实现的六步，逐个拆解五个必踩的坑；最后是三个决定系统形态的设计选择、压缩解决不了的边界，以及怎么验证自己压对了。*
  * *与下面的知识库配套：**这篇给取舍和顺序，那篇给源码和常量**。建议先读这篇建立坐标系，再拿那篇当参考手册查。*

* 🧪 [SKILL.state：从压缩历史到维护状态 — 可视化论文学习页](https://caiboyang.github.io/ML-learning/agent-context-compression/skill-state/)
  * *接着 Compression Research 学习 arXiv:2608.26263v3。通过立体状态分层、仓库逐步演示、成本滑块与可切换实验图表理解执行状态；对应原研究六层模型，区分结构化摘要、状态补丁、日志和 recall，并标注实验口径冲突与适用边界。*

* 📚 [开源 Agent 平台的 Context Compression 机制研究](https://caiboyang.github.io/ML-learning/agent-context-compression/Agent_Context_Compression_Research.html)（含 19 张 Mermaid 图；[Markdown 原文](agent-context-compression/Agent_Context_Compression_Research.md)）
  * *十五个平台的横向对照。十一个开源平台有可核实的内建压缩策略：OpenClaw、Hermes Agent、OpenHands SDK、Codex CLI、opencode、kimi-code、Cline、Goose、Letta、Google ADK、DeepSeek Harness；另纳入压缩算法未公开的闭源 Antigravity，以及代表三种责任划分的框架生态：LangGraph core / LangChain agent middleware（原语 + 可选内建策略）、AutoGen（确定性视图）、CrewAI（overflow-only）。已弃用的 Gemini CLI 移入附录保留设计分析，不计入统计（个人账户 2026-06-18 停服，企业与付费 API key 路径仍可用）。逐文件读源码 + 官方文档交叉验证，附版本快照矩阵；冲突处以源码为准，结尾单列一致性说明。*
  * *另设一节**效果评测**，梳理 2026 年的实证工作：CompactionRL（只换摘要器就有 6.5 分区间）、ConstraintRot（压缩把治理约束违规率从 0% 抬到 30%，最高 59%）、Slipstream（按轨迹而非文本判定保真度），并逐条对应回设计清单。*
  * *先建立统一的六层参照模型（测量/触发/选点/减法/重组/持久化）解决各家术语打架的问题；再用一整节讲**设计理念**——头尾保留中间压缩在利用长上下文检索的 U 形曲线（Lost in the Middle）、迭代更新在规避有损压缩的级联失真、保留用户原话背后的信息论不对称、为什么不能告诉模型"上下文快满了"、摘要器为何是一个信任降级点、压缩与 prompt cache 的根本张力（含 DeepSeek Harness 那条「让摘要调用本身成为缓存前缀的延长」的解法）；然后逐家深挖，最后横向对比触发哲学（绝对余量 vs 百分比 vs cadence）、减法哲学、持久化模型，以及 OpenClaw × Hermes 逐项对照与可借鉴设计清单。*

* 🎓 [把「感觉变好了」变成一个数字 — 从零学 Agent Evals](https://caiboyang.github.io/ML-learning/agent-evals/learn/)
  * *十步学习路径，从零基础起步。假设你写过 agent 但没系统做过 eval，读完能自己设计、实现并校准一套评测。先算一笔账：真实成功率 75% 的 agent 什么都不改重跑一遍，**35.5% 看起来更好、29.0% 打平、35.5% 看起来更差**——噪声本身是对称的，方向是流程给的（只在上涨时宣布改进、重跑到满意为止、确认偏误），所以「把观察到的上涨当证据」等于把那 35.5% 全收成假阳性。然后讲 agent 为什么不能像软件那样测（没有 stack trace，因为失败的是推理；trace 才是事实来源），建立 run / trace / thread 三层坐标系与 task / trial / grader / outcome 的词汇表，拆解三种打分器的死角，讲透 **pass@k 与 pass^k** 和被普遍跳过的误差棒（50 个任务的 95% 区间有 ±13.6 分；配对比较、加题优先于加重复、聚类标准误可达朴素值 3 倍）。*
  * *后半程是三块硬骨头：**LLM judge 怎么校准到值得信**（Critique Shadowing 七步、为什么禁用 1–5 分量表、为什么不能报原始一致率、以及把 judge 当有误差的仪器做通过率修正）；**误差分析**为什么才是真正产生价值的一步（开放式/轴心编码、只标第一个失败点、按维度切开失败率、转移失败矩阵）；以及 **eval 自己会坏**的三种方式——题写坏了、饱和、以及**被你自己磨损**（dev suite 与发布留出集必须分开）。编码 benchmark 那条线被完整跟到了今天：SWE-bench（2023，人工标注发现 68.3% 有问题）→ Verified（2024，去坏题并重排难度后 GPT-4o 从 16% 到 33.2%，模型一个字节没改）→ 因污染与饱和被弃用、转向 Pro（2026）→ **Pro 自己约 30% 是坏的，OpenAI 于 2026-07-08 撤回推荐**。三年三代，每代都在同一个位置出问题。另含评测控制面隔离、必须按过程评分的三类义务、硬门不参与加权、「第一处偏离」检查链（末端是 grader 输入与判定，让「是我们的 eval 错了」保持在候选假设里），以及「按症状查表」十六条。*
  * *素材：LangChain（Harrison Chase）的 observability × eval 讲解、Anthropic 的 Demystifying Evals for AI Agents、Hamel Husain 的 LLM-as-a-Judge 与 Evals FAQ；扩展了 Miller 的误差棒、Shankar 的 criteria drift、MT-Bench 的 judge 偏差与 τ-bench 的 pass^k。文中还并列了 Anthropic 与 Hamel 在「要不要 eval 驱动开发」上的**真实分歧**并给出调和方案。*

* 📚 [Agent Evals 参考手册：证据链、Grader 合同与统计口径](https://caiboyang.github.io/ML-learning/agent-evals/Agent_Evals_Research.html)（[Markdown 原文](agent-evals/Agent_Evals_Research.md)）
  * *与上面的学习页配套：**那篇给取舍和顺序，这篇给字段、模板和来源边界**。统一词典（task / trial / run / trace / trajectory / output-artifact / outcome，并说明这些词在各平台粒度不一致时该核对什么）、成功判据的三层分层（task-result contract / process obligations / experience quality）、grader 梯子、Judge Contract 的 YAML、误差修正的三个前提、误差棒的完整口径、按「第一处偏离」归因的检查表、四类 agent 的 grader 重心、最小 harness 的目录与不可变 trial 产物 schema、release gate 示例、十二个反模式，以及三份可直接抄的 checklist（task review / judge review / experiment handoff）。*
  * *每条陈述都标注了 **【来源事实】/【综合解释】/【实践建议】**，并附来源账本与证据边界；文末单列与学习页的一致性检查十一条。*

* 🎓 [从 API 到 MCP 2.0 — 零基础十步学习路径](https://caiboyang.github.io/ML-learning/mcp-2.0/learn/)
  * *从普通 API、RPC 与 JSON-RPC 的底层差异讲起，还原 MCP 1.0 的 Host / Client / Server、生命周期与 primitives，再解释 MCP 2.0 为什么走向 stateless、MRTR、显式状态 handle 与缓存，并串起 extensions、auth 和迁移。本专题正文统一使用 **MCP 1.0 → MCP 2.0** 的教学分代，分别对应官方 **2025-11-25 及以前 → 2026-07-28 及以后**；wire 报文与兼容声明仍使用日期版本。*
  * *与下面的参考手册配套：建议先读学习页建立问题意识和协议心智模型，再用手册核对规范、线级报文与迁移细节。*

* 📚 [从 MCP 1.0 到 MCP 2.0：协议模型与迁移参考手册](https://caiboyang.github.io/ML-learning/mcp-2.0/MCP_2_0_Research.html)（[Markdown 原文](mcp-2.0/MCP_2_0_Research.md)）
  * *从 API / RPC / JSON-RPC 与 MCP 1.0 的协议基础，逐层深挖 MCP 2.0 的 stateless 请求、MRTR、显式状态 handle、缓存、extensions、auth 和兼容迁移；配套时序图、状态机、线级示例与官方日期版本来源，适合作为查阅手册。*

---
*More notes will be added here soon...*
