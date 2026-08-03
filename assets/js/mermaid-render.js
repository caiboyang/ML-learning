import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.16.0/dist/mermaid.esm.min.mjs";

const blocks = document.querySelectorAll("pre > code.language-mermaid");

if (blocks.length > 0) {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
  });

  for (const [index, block] of [...blocks].entries()) {
    const source = block.textContent.trim();

    try {
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

      block.closest("pre").replaceWith(diagram);
      bindFunctions?.(diagram);
    } catch (error) {
      console.error(`Unable to render Mermaid diagram ${index + 1}`, error);
    }
  }
}
