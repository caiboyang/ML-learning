# 配色：用户可选，视觉风格不变

新演讲开始时，主动确认听众和场合，并问有没有学校色、品牌色或偏好的配色。上下文已给出就复用，不重复问。用户可以用自然语言选择，不要求填写配置；agent 负责把选择写入 deck.json。没有偏好可先用 forest，说明它是可替换的默认方案。不要把某场学校演讲的绿色当成所有主题的固定风格。

保留大字、少字、留白、衬线强调、简洁几何插画与闭环动画。只改变颜色角色的值，不因换色重做版式、增加文字或改变图的调性。正式演讲不加调色器；配色在制作时选定，也不随操作系统自动切换。

## 使用方式

顶层 `"palette": "forest"`（绿）、`"blue"`（蓝）或 `"plum"`（梅紫）。这是本模板自配的三个方案，不是 Google 或 Apple 官方认证配色。每页的 `theme: "dark" / "paper"` 仍决定深底或浅底，与整套 palette 是两件事。

例如用蓝色方案并调整品牌强调色：

```json
{
  "palette": "blue",
  "colors": {
    "dark_accent": "#b6d2ff",
    "light_accent": "#1e4f91"
  }
}
```

以上字段合并到完整 deck.json，不是独立内容源。`colors` 可只覆盖需要的角色，只接受不透明六位十六进制色值。用户给一个品牌色时，agent 应为深浅背景分别选合适的明度；不是把同一色值直接用在所有地方。若用户拿不准，可展示同一页的两三种方案，不强制增加审批步骤。

| 角色 | 用途 |
| --- | --- |
| dark_surface / light_surface | 深底 / 浅底背景 |
| dark_text / light_text | 对应背景上的主文字 |
| dark_muted / light_muted | 辅助文字、说明 |
| dark_accent / light_accent | 强调文字、闭环箭头和轨迹 |
| highlight | 少量装饰点缀；不保证适合作为文字颜色 |

生成器输出 theme.css，并同时应用到投影、讲稿和缩略图。新插画使用这些 CSS 变量；家电图参考已留出颜色变量。品牌 logo、截图、视频和黑白二维码不自动染色。黄色 cue 保持专用，并保留括号和中文提示，不能仅靠颜色区分“读 / 不读”。

## 验证

生成器检查深浅背景上的 text、muted、accent 均达到 4.5:1，因为同一角色可能用于小标签。配置不合格会在生成前报错，应调整色值后重建。这个检查不是整个网页的无障碍认证：半透明叠加、图片上的字、highlight 文字、自定义 HTML 和动画状态仍要实际检查。

有意义的图形和箭头要清楚可见；状态还要有文字、箭头或形状，不只靠红绿。保持线条足够粗，避免名义对比度合格但投影看不清。检查深底页、浅底页、讲稿、缩略图和至少一张图，确认同色含义一致；有条件时用实际投影设备和后排视距检查。

## 依据与适用范围

- [Google Android / Material 颜色指南](https://developer.android.com/design/ui/mobile/guides/styles/color)：按角色组织背景与前景配对，分别处理深浅色方案。本模板借用角色方法，没有引入 Material 组件库或自动主题算法。
- [Apple HIG Color](https://developer.apple.com/design/human-interface-guidelines/color)：颜色含义保持一致，自定义配色考虑深浅背景及对比度。这里把应用界面原则用于演讲；不照搬系统动态外观，也不模仿 Liquid Glass。
- [WCAG 文字对比度](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)：普通文字 4.5:1，大文字 3:1。本模板对通用文字角色统一采用更保守的 4.5:1。
- [WCAG 非文字对比度](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)：理解内容所需的图形通常要求与相邻颜色达到 3:1；不是要求所有装饰边框都达到该值。
