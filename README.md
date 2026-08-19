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

* 🎓 [不再凭感觉调 Agent — 十步建立 Eval 系统](https://caiboyang.github.io/ML-learning/agent-evals/learn/)
  * *从一次「agent 说已完成、grader 给了 100 分、真实环境却没有变化」的错误现场出发，建立 Task → Trial → Transcript + Task Result → Graders → Decision 的完整证据链。十步讲清 success contract、20–50 个初始任务的构造、capability / regression 分工、dev / holdout 边界、code / model / human grader 的选择、Critique Shadowing 与 LLM judge 校准、pass@k / pass^k、run / trace / thread、生产失败回流，以及一个不绑定平台的最小 eval harness。*
  * *与下面的参考手册配套：学习页用同一个退款案例串起十步主线；手册再展开完整词典、跨 Agent 类型设计、可复制模板与来源边界。*

* 📚 [Agent Evals：从「感觉变好了」到可复现实验](https://caiboyang.github.io/ML-learning/agent-evals/Agent_Evals_Research.html)（[Markdown 原文](agent-evals/Agent_Evals_Research.md)）
  * *以 Anthropic 的 agent eval 体系、Hamel Husain 的 Critique Shadowing 和 LangChain 的 observability → evaluation 飞轮为三条主轴，并扩展到 evaluator criteria drift、LLM judge 的 position / verbosity / self-enhancement 偏差、τ-bench 的最终状态与 pass^k。覆盖 task / trial / output / outcome / grader / harness 统一词典、数据集与 grader 设计、随机性、trace 首个偏离点、不同 agent 类型、最小目录与 release gate、十二个反模式和可复制 checklist；参考手册明确区分来源事实、综合解释与实践建议，学习页则在各步末给出对应来源与扩展边界。*

* 🎓 [把上下文压小而不压坏 — 从零学 Agent Context Compression](https://caiboyang.github.io/ML-learning/agent-context-compression/learn/)
  * *十步学习路径，从零基础起步。假设你只知道「LLM 有上下文窗口」，读完能自己设计并评估一套压缩策略。先看一次 agent 被撑爆的死亡现场，再讲窗口这堵墙的三个反直觉性质（每轮重发全部历史、装得下≠用得好、墙的位置未必是文档写的那个）；然后建立六层坐标系，手把手走完最小可用实现的六步，逐个拆解五个必踩的坑；最后是三个决定系统形态的设计选择、压缩解决不了的边界，以及怎么验证自己压对了。*
  * *与下面的知识库配套：**这篇给取舍和顺序，那篇给源码和常量**。建议先读这篇建立坐标系，再拿那篇当参考手册查。*

* 📚 [开源 Agent 平台的 Context Compression 机制研究](https://caiboyang.github.io/ML-learning/agent-context-compression/Agent_Context_Compression_Research.html)（含 19 张 Mermaid 图；[Markdown 原文](agent-context-compression/Agent_Context_Compression_Research.md)）
  * *十五个平台的横向对照。十一个开源平台有可核实的内建压缩策略：OpenClaw、Hermes Agent、OpenHands SDK、Codex CLI、opencode、kimi-code、Cline、Goose、Letta、Google ADK、DeepSeek Harness；另纳入压缩算法未公开的闭源 Antigravity，以及代表三种责任划分的框架生态：LangGraph core / LangChain agent middleware（原语 + 可选内建策略）、AutoGen（确定性视图）、CrewAI（overflow-only）。已弃用的 Gemini CLI 移入附录保留设计分析，不计入统计（个人账户 2026-06-18 停服，企业与付费 API key 路径仍可用）。逐文件读源码 + 官方文档交叉验证，附版本快照矩阵；冲突处以源码为准，结尾单列一致性说明。*
  * *另设一节**效果评测**，梳理 2026 年的实证工作：CompactionRL（只换摘要器就有 6.5 分区间）、ConstraintRot（压缩把治理约束违规率从 0% 抬到 30%，最高 59%）、Slipstream（按轨迹而非文本判定保真度），并逐条对应回设计清单。*
  * *先建立统一的六层参照模型（测量/触发/选点/减法/重组/持久化）解决各家术语打架的问题；再用一整节讲**设计理念**——头尾保留中间压缩在利用长上下文检索的 U 形曲线（Lost in the Middle）、迭代更新在规避有损压缩的级联失真、保留用户原话背后的信息论不对称、为什么不能告诉模型"上下文快满了"、摘要器为何是一个信任降级点、压缩与 prompt cache 的根本张力（含 DeepSeek Harness 那条「让摘要调用本身成为缓存前缀的延长」的解法）；然后逐家深挖，最后横向对比触发哲学（绝对余量 vs 百分比 vs cadence）、减法哲学、持久化模型，以及 OpenClaw × Hermes 逐项对照与可借鉴设计清单。*

* 🎓 [从 API 到 MCP 2.0 — 零基础十步学习路径](https://caiboyang.github.io/ML-learning/mcp-2.0/learn/)
  * *从普通 API、RPC 与 JSON-RPC 的底层差异讲起，还原 MCP 1.0 的 Host / Client / Server、生命周期与 primitives，再解释 MCP 2.0 为什么走向 stateless、MRTR、显式状态 handle 与缓存，并串起 extensions、auth 和迁移。本专题正文统一使用 **MCP 1.0 → MCP 2.0** 的教学分代，分别对应官方 **2025-11-25 及以前 → 2026-07-28 及以后**；wire 报文与兼容声明仍使用日期版本。*
  * *与下面的参考手册配套：建议先读学习页建立问题意识和协议心智模型，再用手册核对规范、线级报文与迁移细节。*

* 📚 [从 MCP 1.0 到 MCP 2.0：协议模型与迁移参考手册](https://caiboyang.github.io/ML-learning/mcp-2.0/MCP_2_0_Research.html)（[Markdown 原文](mcp-2.0/MCP_2_0_Research.md)）
  * *从 API / RPC / JSON-RPC 与 MCP 1.0 的协议基础，逐层深挖 MCP 2.0 的 stateless 请求、MRTR、显式状态 handle、缓存、extensions、auth 和兼容迁移；配套时序图、状态机、线级示例与官方日期版本来源，适合作为查阅手册。*

---
*More notes will be added here soon...*
