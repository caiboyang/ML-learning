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
* [开源 Agent 平台的 Context Compression 机制研究](https://caiboyang.github.io/ML-learning/agent-context-compression/Agent_Context_Compression_Research.html)
  * *十个平台的横向对照：OpenClaw、Hermes Agent、OpenHands SDK、Codex CLI、Gemini CLI、Cline、Goose、Letta、Google ADK、Antigravity。逐文件读源码 + 官方文档交叉验证（冲突处以源码为准，结尾单列一致性说明）。先建立统一的六层参照模型（测量/触发/选点/减法/重组/持久化）解决各家术语打架的问题，再逐家深挖，最后横向对比：触发哲学（绝对余量 vs 百分比 vs cadence）、减法哲学（map-reduce 分块 / 区间重叠 / 只留用户原话）、持久化模型（append-only 事件 / soft archive / 双可见性），以及 OpenClaw × Hermes 的逐项对照与可借鉴设计清单。*

---
*More notes will be added here soon...*
