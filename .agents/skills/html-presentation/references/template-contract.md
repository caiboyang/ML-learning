# 模板合同与交付

## 单一内容源

复制 `assets/template/deck.json` 到自己的工作目录，旁边可放 `assets/`。用 build.py 生成完整目录，再通过静态 HTTP 服务打开。生成目录是可发布结果；不要只上传 index.html。

顶层字段：`id`（短英文 slug，稳定且区别不同演讲）、`title`、`speaker`、`language`、`budget_label`、`slides`。

每页字段：

- `id`：稳定英文 slug，唯一；不要使用保留的 `top`。翻页、hash、同步、讲稿、缩略图都由它连接。
- `title`：纯文本标题，用于目录与浏览器标题。
- `label`：可选的短分类标签。
- `theme`：`dark`（默认）或 `paper`。
- `html`：可信作者编写的投影正文 HTML，通常 h2 + em + support；不可直接放未经检查的远端 HTML。生成器不对任意 HTML 进行安全清洗。
- `purpose`：演讲者视角的一句中文目的，不在投影上显示。
- `notes`：按讲述顺序排列的 `{"say":"要读的正文"}` 与 `{"cue":"不读的中文提示"}`。两者都是纯文本，生成时转义，不能混用。
- `budget_seconds`：非负整数或 null。它是计划上限/安排，不是口播实测。
- `media_seconds`：可选，估算中加上的视频等媒体播放秒数；勿同时用长停顿冒充媒体。
- `kind: "qa"`：总口播估算不计问答页。

`index.html`、`notes.html` 和 `timing.json` 均由生成器产出。缩略图直接嵌入同一 scene 的静态副本，不能独立编辑。修改源后重新 build；删除或排序也由同一个 slides 数组处理。

## 可直接使用的投影组件

`html` 只写正文，生成器负责外层 scene、页码和标签。最小标题页：

```html
<h2>A small test.<br><em>A better decision.</em></h2>
<p class="support">Learn before making a larger change.</p>
```

`h2` 是大标题，`em` 是衬线强调行，`support` 是简短辅助文字；`theme: "paper"` 切换浅底。三步闭环用现成类名：

```html
<h2>Test. Learn. <em>Adjust.</em></h2>
<div class="loop">
  <div class="loop-stages"><strong>Try</strong><span>→</span><strong>Check</strong><span>→</span><strong>Adjust</strong></div>
  <div class="loop-return">↖ Try again with what you learned</div>
</div>
```

当前页会依次强调步骤；离页暂停，reduced-motion 关闭动画。以上是可复用组件，不是每个主题必须包含的流程。新布局需要作者自行实现并验证；生成器不自动推断 HTML 的视觉布局，也不保证任意长度都能放进一屏。

## 可选视频

当前模板复用经过现场使用的单视频控制，不实现多媒体播放列表。需要视频时新增或替换一页，使用 `id: "video"`，在 html 放：

```html
<h2>A short demo.</h2>
<video id="demo-film" src="assets/demo.mp4" poster="assets/poster.jpg" playsinline preload="metadata"></video>
<p id="film-hint" hidden>Press V to play with sound</p>
```

素材放在 deck.json 旁的 assets/；build 会复制。修改主文件中的视频名即可，不改运行时的固定 ID。给 `media_seconds` 填实际时长。有声自动播放须先在投影窗完成准备手势；浏览器仍可拒绝，使用 V 手动播放。视频和字幕必须与当前讲稿对应。

## 可移植性和 provenance

- runtime 是本地 HTML/CSS/JavaScript，无 npm build、无后端、无账户需求；Python 3 标准库负责生成和验证，Node 只用于语法检查。
- 全部路径使用相对路径；CSS 的 Google Fonts 是可选网络依赖，有系统 fallback。离线环境可移除第一行 import；若必须像素一致，按字体许可证自行打包字体。
- 不带 `.git`、`.openai`、环境文件、用户目录路径、原站点 project ID、个人视频或二维码。原演讲已单独归档，不复制到此包。
- 来源：2026-10 的双页演讲实现（Sites v35）。保留视觉和交互方式，提取中性模板，并改为单源生成内容/缩略图/计时预算。
- 此包是 Git 仓库里的 skill + source template，不是已安装的 Template Gallery 条目。整文件夹复制到另一环境的 skill 目录即可按当地 discovery 规则使用；不需要全局安装才能手动调用 build.py。

## 文件布局

```
html-presentation/
  SKILL.md
  agents/openai.yaml
  references/{authoring,presenter,template-contract}.md
  scripts/{build,validate,test_build}.py
  assets/template/{deck.json,style.css,speaker.css,app.js,notes.js}
```

验收时同时保留内容源和生成结果。Git 包中默认不重复提交生成的 demo；用 SKILL.md 的三条命令即可重建。
