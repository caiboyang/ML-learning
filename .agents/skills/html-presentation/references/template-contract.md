# 模板合同与交付

## 单一内容源

复制 `assets/template/deck.json` 到自己的工作目录，旁边可放 `assets/`。用 build.py 生成完整目录，再通过静态 HTTP 服务打开。生成目录是可发布结果；不要只上传 index.html。

顶层字段：`id`（短英文 slug，稳定且区别不同演讲）、`title`、`speaker`、`language`、`budget_label`、`slides`。可选 `palette`（forest / blue / plum）和 `colors`（语义角色覆盖），见 [配色指南](color.md)。

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

`index.html`、`notes.html`、`theme.css` 和 `timing.json` 均由生成器产出。缩略图直接嵌入同一 scene 的静态副本，不能独立编辑。修改源后重新 build；删除或排序也由同一个 slides 数组处理。

## 可直接使用的投影组件

`html` 只写正文，生成器负责外层 scene、页码和标签。最小标题页：

```html
<h2>A small test.<br><em>A better decision.</em></h2>
<p class="support">Learn before making a larger change.</p>
```

`h2` 是大标题，`em` 是衬线强调行，`support` 是简短辅助文字；`theme: "paper"` 切换浅底。

### 动态三步闭环（反馈 / 迭代 / 重试）

复制 [assets/components/loop.html](../assets/components/loop.html) 的完整 SVG，放进该页的 `html`，位于 h2 与 support 之间。`assets/template/deck.json` 的 `loop` 页是完整可构建示例。生成器不会自动读取或 include 组件文件；作者在内容源中嵌入 SVG 后，现有 build.py 会原样生成投影及缩略图，共享 style.css 已包含动画，theme.css 提供用户选定的颜色，无需逐个 demo 写内联样式或新 JavaScript。

按主题只替换以下文字，保留 class、viewBox 和路径：

- 三个 `cycle-word`：例如 `Small trial` → `Check` → `Decide`，用短标签。
- `cycle-repeat`：说明返回条件，例如 `Adjust and retry, if worthwhile.`。若存在成功退出或停止，在 support 说明 `Pass: expand a step. Miss: fix or stop.`；不要让观众误以为必须无限重复。
- SVG 的 `aria-label`：同步说明步骤顺序与返回条件。口播和 cue 按同一顺序讲。

这套 SVG 有闭合轨迹、方向箭头、沿轨迹移动的线段及依次强调的节点。深底/浅底颜色自动随 theme 和 palette 切换，`.scene.is-current` 时播放，离页暂停；缩略图保持静态；reduced-motion 关闭动画但保留箭头、节点与返回说明。组件没有全局 ID，可在多个页面重复使用而不发生 marker 引用冲突。

参考中的三个步骤是可替换内容，不要求所有演讲出现 loop。只有真实存在反馈返回时才选这个组件；普通检查清单和线性流程不要画成闭环。需要更多步骤或长说明时先重新组织内容，再单独验证布局，不能缩小字硬塞进现有节点。

旧 `.loop-stages` / `.loop-return` 仍保留以兼容已有内容；新闭环采用 SVG 组件，不能把旧版只有节点强调的效果当成完整流动动画。新布局需要作者自行实现并验证；生成器不保证任意长度都能放进一屏。

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
  references/{authoring,color,presenter,speechwriting,template-contract,verification}.md
  scripts/{build,palettes,validate,test_build}.py
  assets/components/loop.html
  assets/template/{deck.json,style.css,speaker.css,app.js,notes.js}
```

验收时同时保留内容源和生成结果。Git 包中默认不重复提交生成的 demo；用 SKILL.md 的三条命令即可重建。
