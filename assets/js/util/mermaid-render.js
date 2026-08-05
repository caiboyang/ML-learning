/*
 * 共享的 Mermaid 渲染器。
 *
 * GitHub Pages（Jekyll）不原生渲染 mermaid，把 ```mermaid 围栏原样输出成代码块，
 * 这里在客户端补一次渲染。在 github.com 上直接看 .md 时这段会被忽略，
 * 走 GitHub 自带的 mermaid 渲染。
 *
 * 引用方式（笔记 .md 末尾）：
 *   <script type="module" src="../assets/js/util/mermaid-render.js"></script>
 * 用相对路径而非 Liquid 的 relative_url —— 这些 .md 没有 front matter，
 * 不依赖 Liquid 是否被求值。**前提是引用它的笔记位于仓库根下一层。**
 *
 * 选择器覆盖两种 DOM 结构：
 *   - 本仓库当前的输出：language-mermaid 直接落在 <code> 上
 *   - Kramdown + Rouge 的另一种形态：落在外层 wrapper 上
 */
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.16.0/dist/mermaid.esm.min.mjs";

const blocks = [
  ...new Set([
    ...document.querySelectorAll("code.language-mermaid"),
    ...document.querySelectorAll(".language-mermaid code"),
  ]),
];

if (blocks.length > 0) {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "neutral",
  });

  for (const [index, block] of blocks.entries()) {
    const source = block.textContent.trim();
    const target =
      block.closest(".language-mermaid.highlighter-rouge") ||
      block.closest("pre") ||
      block;

    try {
      // 解析失败就整块跳过，把原始代码块留在页面上作为兜底。
      const parsed = await mermaid.parse(source, { suppressErrors: true });
      if (!parsed) {
        continue;
      }

      const { svg, bindFunctions } = await mermaid.render(
        `mermaid-diagram-${index}`,
        source,
      );
      const diagram = document.createElement("div");
      diagram.className = "mermaid-diagram";
      diagram.style.overflowX = "auto";
      diagram.innerHTML = svg;

      target.replaceWith(diagram);
      bindFunctions?.(diagram);
    } catch (error) {
      console.error(`Unable to render Mermaid diagram ${index + 1}`, error);
    }
  }
}
