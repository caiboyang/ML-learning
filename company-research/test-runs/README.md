# 公司调研 skill 的测试运行

这里存放用 [company-research skill](../../.agents/skills/company-research/SKILL.md) 实际跑出的两次外部公司研究。它们是 skill 的**留出测试用例**，不是 skill 的示例：skill、方法报告和 demo 都不引用这里的内容，改 skill 时也不应以这两家公司的结论为依据。

| 公司 | 页面 | 取证日期 | 说明 |
| --- | --- | --- | --- |
| Clubhouse | [index.html](clubhouse/index.html) | 2026-10-02 | 先按当时的 skill 从零取证（`build_base.py`），再按第 7 轮规则补覆盖清单和重点案例（`build_round7.py`） |
| Reforge | [index.html](reforge/index.html) | 2026-10-03 | 证据台账在 `build_evidence.py`，记录与章节在 `build_research.py` |

每个目录里：

- `research.json`：研究数据，按 skill 的 schema 组织；
- `index.html`：用 skill 的导出脚本生成的单文件页面，可离线打开；
- `build_*.py`：生成 `research.json` 的脚本，研究内容都写在脚本里。

抓取的原始网页快照属于第三方内容，没有放进仓库；每条证据都保留了原始链接。

## 重新生成与校验

在仓库根目录运行：

```sh
npm ci --prefix .agents/skills/company-research/scripts --ignore-scripts

# Clubhouse
python3 company-research/test-runs/clubhouse/build_base.py /tmp/clubhouse-base.json
python3 company-research/test-runs/clubhouse/build_round7.py /tmp/clubhouse-base.json company-research/test-runs/clubhouse/research.json

# Reforge（第一个参数是“可交付性”一项的缺口说明；仓库中的 research.json 写入的是当次浏览器验收结果）
python3 company-research/test-runs/reforge/build_research.py "<可交付性缺口说明>"

for c in clubhouse reforge; do
  node .agents/skills/company-research/scripts/validate-report.cjs company-research/test-runs/$c/research.json
  python3 .agents/skills/company-research/scripts/export-report.py company-research/test-runs/$c/research.json company-research/test-runs/$c/index.html
done
```

两份数据都能通过当前 skill 的 schema 与语义校验；Reforge 另有几条“限制说明重复”的提示，属于编辑层面的警告。

## 再次测试时

用这两家公司重新测试 skill 时，请从 skill 本身从零开始，不要读取或复用这里的产物，否则测不出 skill 的泛化能力。
