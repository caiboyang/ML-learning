---
name: html-presentation
description: "创建或小幅修改可现场演讲的 HTML slides 与独立讲稿页；复用双屏联动、键盘切页、总计时/本页计时和提示样式。适用于网页演讲、speaker notes、扩展屏演示；普通文章和原生 PPTX 不自动转成此格式。"
---

# HTML presentation + speaker guide

交付能在现场连续讲的网页演示，不是需要观众点击探索的 dashboard。此包自带中性模板，不依赖原演讲、原项目或付费前端框架。

## 工作方式

1. 先确认听众是谁。若用户和已有材料尚未明确听众对象，agent 必须主动询问，例如：“这次主要讲给谁听？他们对这个主题大概了解多少？”得到回答后再确定切入口和口播深度，不默认是技术人员、学生或管理者。已明确的听众信息直接沿用，不重复询问。再确定听众为什么关心、演讲者身份、已有材料、目标时间及问答时间。不要从一个 bug 推断整个产品定位；团队成果用 we，个人经历才用 I。
2. 新写或重写口播时，先读 [通用口播方法](references/speechwriting.md)：从听众处境和所需判断选择切入口，建立主线，再写可直接讲出的正文、例子和转场。它适用于不同领域，不把某次 AI 演讲的故事当成固定结构。再按 [写作与视觉规范](references/authoring.md) 保留用户认可的视觉基准并映射到屏幕；一屏只承担一个推进主线的作用。用户进入最终排练阶段时，冻结结构，只改点名的页和必要转场。
3. 从 `assets/template/deck.json` 复制内容源到新目录。构建时脚本仍从本 skill 目录读取模板，不必给每个演讲复制一套 skill；迁移到没有本 skill 的环境时，才一起携带完整 skill 文件夹。相对路径以本文件所在目录解析。按 [模板合同](references/template-contract.md) 填写，再运行：

   ```bash
   python3 <skill-dir>/scripts/build.py /path/to/deck.json --output /path/to/site
   python3 <skill-dir>/scripts/validate.py /path/to/site
   python3 -m http.server 8765 --bind 127.0.0.1 --directory /path/to/site
   ```

   浏览 `http://127.0.0.1:8765/notes.html`。若端口被占用，换一个空闲端口，并同步修改打开的 URL；不要停止不属于本次任务的服务。**从讲稿按钮打开投影窗**；独立打开 index 不会自动联动。没有 Python 时可以交付现成生成结果，但不能声称已运行构建验证。
4. 读取 [现场操作与同步协议](references/presenter.md)，保留稳定的 slide ID。生成器同时生成演示、讲稿、页码、顺序、缩略图和英文时长估算，避免逐处手工复制。涉及反馈、迭代或重试时，优先复用 [动态闭环组件](assets/components/loop.html)，按 [模板合同](references/template-contract.md) 替换步骤和返回条件；不能只写三个词或用静态回转符号替代动态 loop。线性流程不强加循环。新增视频时按合同设置固定 video ID；普通演讲可以完全没有视频。
5. 运行脚本测试、结构校验，并按 [交付验证](references/verification.md) 保存逐页截图和检查结果，按 presenter 文档做实际浏览器检查：切页与动画、两个窗口联动、刷新/重连、双计时器、字号/溢出，以及有视频时的播放。可用浏览器工具不足时明确报告未验证的项目，不用截图假装联动已验证。
6. 汇报实际改动和可打开入口。此 skill 本身不授权部署、发消息、提交或发布；需要发布时使用用户选定的托管流程，不复用原演讲的项目 ID、二维码或私密素材。

讲稿布局参考：[实际生成的中性模板预览](assets/notes-preview.png)。

## 三个分离

- **投影内容 / 口播 / 舞台提示**：投影少字；口播是能读出来的完整短句；中文动作提示放进黄色【括号】，出现在动作发生之前，不混入口播。
- **预算 / 估算 / 实测**：彩排可在“备课总览”导出本次逐页实际时间，重置前保存。预算是安排，不是承诺。英文词数除以假设语速，再加媒体时长；停顿和临场展开另外计。时间以彩排校准，不让演讲者故意拖慢或临时补背景来填预算。
- **内容 / 可复用机制**：deck.json 放主题、讲稿和个人素材；template 放外观、键盘、同步、计时。不要把真实案例、私密群二维码、已发布站点身份复制到通用模板。

## 包内检查

```bash
python3 -m unittest discover -s <skill-dir>/scripts -p 'test_*.py'
node --check <skill-dir>/assets/template/app.js
node --check <skill-dir>/assets/template/notes.js
```

本包来自实用的双页演讲实现，原演讲独立保存在 ai-study-community 的 `docs/presentations/global-career-ai-2026/`。复用本包无需克隆那个仓库。
