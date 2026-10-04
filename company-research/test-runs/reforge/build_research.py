# -*- coding: utf-8 -*-
"""Build research.json for the Reforge external-company study.

Run: python3 build_research.py  -> writes research.json next to this file.
All facts trace to EVIDENCE ids in build_evidence.py; judgments are marked inference/recommendation.
"""
import json
from pathlib import Path

from build_evidence import EVIDENCE

HERE = Path(__file__).resolve().parent
records = []


def F(label, value, kind=None):
    f = {"label": label, "value": value}
    if kind:
        f["kind"] = kind
    return f


def rec(id, company, section, kind, role, status, title, text, limitation, ev, rel=(), **extra):
    r = dict(id=id, companyId=company, section=section, kind=kind, role=role, status=status,
             title=title, text=text, limitation=limitation, evidenceIds=list(ev), relatedIds=list(rel))
    r.update(extra)
    records.append(r)
    return r


I, FA, RE = "inference", "fact", "recommendation"

# =====================================================================
# 01 执行结论
# =====================================================================
rec("rf-verdict", "reforge", "executive-summary", I, "judgment", "研究者判断（有条件）",
    "专家信誉＋申请制 cohort 证明了高价付费；会员续费受『需要时才学』限制，2022 年后扩张成本遇上需求收缩",
    "Reforge 起于两位增长操盘手的写作受众与行业关系：用申请制小批次 cohort 收高价，自举到约 1,000 万美元年收入（创始人自述）；"
    "2021–22 年融资 8,100 万美元，把项目从 10 个扩到约 20 个，收入到约 3,000 万美元。之后三轮裁员，先转团队席位与常年内容，再转 AI 工具，"
    "2026-03 被 Miro 收购（条款未披露），而 Miro 又在 2026-09 同意被 Bending Spoons 收购。现有证据下，可解释收缩的排序是：宏观收缩为触发、"
    "『阶段性需求』让年费会员难续为放大、竞争替代并存但证据最弱。可借鉴的是起步方法（受众→申请筛选→高价小批次→专家共建），不是融资后的扩题与年费会员结构。",
    "收入为创始人自述（第三方摘要），2023 年后无收入、会员或续费数据；排序依赖同类平台的代理证据，不是因果证明。",
    ["e-chargebee", "e-balfour-21m", "e-series-b", "e-joining-miro", "e-bending-spoons"],
    ["rf-decline", "rf-transfer", "rf-p-retention", "rf-investigation"])

rec("rf-m-revenue", "reforge", "executive-summary", FA, "metric", "创始人自述",
    "收入轨迹（自述）",
    "2021-02 Balfour 另称公司『8 位数收入且盈利』，与约 1,000 万美元的自举阶段一致；2023 年后没有公开数字。",
    "未说明是 ARR 还是确认收入，未审计；$30M 的时期在 Chargebee 摘要（融资后 18 个月）与 Class Central（2023 年）之间不一致。",
    ["e-chargebee", "e-balfour-21m", "e-classcentral"], ["rf-series-revenue", "rf-p-pay"],
    metric={"value": "≈$10M → ≈$30M", "unit": "美元／年（口径未说明）",
            "basis": "自举约 4 年到 $10M（约 2019 年，按 2015 起算推定）；2021-02 融资后 18 个月到 $30M（约 2022 年下半年）。"})

rec("rf-m-alumni", "reforge", "executive-summary", FA, "metric", "公司公告",
    "累计学员",
    "2021-02 时为『数千名』学员，2026-03 收购公告称超过 10 万。",
    "累计口径，包含已流失学员，不是当前付费会员或活跃用户。",
    ["e-joining-miro", "e-miro-blog", "e-a16z-reforge"], ["rf-p-outcome"],
    metric={"value": "100,000+", "unit": "累计学员（alumni）",
            "basis": "Reforge 与 Miro 2026-03-24 公告；未去重说明，非当前会员。"})

rec("rf-m-capital", "reforge", "executive-summary", FA, "metric", "公司公告",
    "累计股权融资",
    "A 轮 $21M（2021-02，a16z 领投）＋ B 轮 $60M（2022-03，Insight Partners 领投）；此前自举 5 年。",
    "融资不是客户收入；收购对价未披露，无法计算投资回报。",
    ["e-raise-21m", "e-series-b", "e-balfour-21m"], ["rf-d2", "rf-p-capital"],
    metric={"value": "$81M", "unit": "美元（两轮合计）",
            "basis": "只计公开宣布的 A、B 两轮；不含天使或债务（未查到）。"})


def proof(id, title, state, evidence, gap, nxt, ev, rel=(), na=None):
    p = {"proposition": title, "state": state, "evidence": evidence, "gap": gap, "next": nxt}
    if na:
        p["naReason"] = na
    return rec(id, "reforge", "executive-summary", I, "proof", state, title, evidence,
               "证明状态是研究者判断；证据多为公司或创始人自述。", ev, rel, proof=p)


proof("rf-p-pay", "高价付费需求：个人或雇主为 cohort 课程付款", "已证明",
      "2021-02 自述 8 位数收入且盈利、自举 5 年；投资方同时称其自举；个人价 $1,995/年至今未变。",
      "未审计；个人自付与雇主报销的比例未知。",
      "找收购或融资材料中的收入原始披露；查访谈全文中的付款构成。",
      ["e-balfour-21m", "e-a16z-reforge", "e-pricing"], ["rf-m-revenue"])
proof("rf-p-outcome", "学习交付带来可感知结果", "有信号",
      "早期 MVP 的 NPS 由 20 升到 72（创始人口述）；累计 10 万+ 学员；企业客户名单。",
      "无完课率、工作应用、晋升或团队绩效的数据；NPS 只有早期一次。",
      "找第三方学员调查或公司发布的结果样本，并区分自报与核验。",
      ["e-muas", "e-joining-miro", "e-itbrief"], ["rf-m-alumni"])
proof("rf-p-retention", "年费会员能形成持续使用与续费", "反证",
      "Balfour：最大流失原因一直是『我喜欢 Reforge，只是现在不需要』。这是对『持续需求』前提的反向证据。",
      "没有续费率或同批留存；反证的是需求连续性，不是给出续费水平。",
      "查访谈全文或收购材料中的续费率；区分个人与团队账户。",
      ["e-chargebee"], ["rf-decline", "rf-d3"])
proof("rf-p-team", "购买单位能从个人扩到团队与企业", "有信号",
      "2023-05 官方称过半会员在团队账户；团队档位按 10／30／50+ 席位售卖；官网称 1K+ 产品团队。",
      "『过半』未说明按人数还是收入；无净收入留存与席位使用率。",
      "查团队账户续约与扩席记录的任何公开披露。",
      ["e-teams-2023", "e-pricing", "e-home"], ["rf-d3"])
proof("rf-p-supply", "专家供给可以持续扩充课程", "有信号",
      "项目由 1 个（2015）扩到 10 个（2021-02）、约 20 个与 50+ 讲师（2022-08）；EIR 计划自 2019 年起。",
      "每门课需 50–100 小时专家共建；讲师分成未公开（竞争对手称 Reforge 留 50%）；讲师留存未知。",
      "对照 2022 与 2026 课程页讲师名单，看流失与新增。",
      ["e-raise-21m", "e-fall-2022", "e-eir-2019", "e-maven-guide"], ["rf-series-programs"])
proof("rf-p-tools", "AI 工具能形成付费产品", "未证明",
      "2024 年上线浏览器插件；2025-01 收购 Monterey 形成 Insights；2025 年推出 Research、Build（11 月）、Launch；2026-03 并入 Miro。",
      "没有用户数、付费客户或留存；被收购说明有战略价值，不等于已有产品市场匹配。",
      "查 Miro Product Acceleration 的定价与客户案例。",
      ["e-extension-2024", "e-monterey", "e-build-2025", "e-joining-miro"], ["rf-d4"])
proof("rf-p-capital", "融资后的经营可持续与资本回报", "未证明",
      "融资 $81M 后出现 2022-11、2023-04 两轮裁员（创始人公告）与 2024-10 第三轮（二手）；收购对价未披露。",
      "无利润、现金与对价数据。",
      "查是否有投资方或收购方披露交易对价。",
      ["e-layoff-2022", "e-layoff-2023", "e-classcentral", "e-itbrief"], ["rf-d2"])
proof("rf-p-learning-now", "学习业务在收购后独立存续", "有信号",
      "官方称 Learning 保持独立品牌、价格不变、春季 cohort 照常；2026-10 官网仍售 9 门直播课与 $1,995/年个人档。",
      "Miro 正被 Bending Spoons 收购（预计 2026 Q4 交割），学习业务的去留未知。",
      "交割后复查官网价格、课程与归属。",
      ["e-joining-miro", "e-courses", "e-pricing", "e-bending-spoons"], ["rf-status"])

# =====================================================================
# 02 现状
# =====================================================================
rec("rf-status", "reforge", "company-status", FA, "asset", "已核实（官方公告＋官网）",
    "现状：学习品牌仍在售，工具线已并入 Miro，母公司又将易主",
    "Reforge 不再是独立公司：2026-03 被 Miro 收购，工具入口跳转到 Miro；reforge.com 只保留学习业务。",
    "收购条款、留任人数与学习业务收入均未披露。",
    ["e-joining-miro", "e-miro-blog", "e-build-redirect", "e-bending-spoons", "e-courses"],
    ["rf-p-learning-now", "rf-d5"],
    fields=[F("所有权", "2026-03-24 Miro 宣布收购 Reforge 的人员、学习平台与产品；2026-09-10 Bending Spoons 同意以企业价值 $1.355B 收购 Miro，预计 2026 Q4 交割。"),
            F("学习业务", "Reforge Learning 作为独立品牌在 reforge.com 运营；9 门直播课（7 门 AI 主题）＋40+ 按需课；个人 $1,995/年。"),
            F("工具业务", "Insights、Research、Build 并入 Miro Product Acceleration；reforge.com/build 跳转到 miro.com/try-prototyping，/insights 显示 404。"),
            F("人员", "Balfour 任 Miro 首席增长官，Willerer 任首席战略官；其他人员去向未披露。"),
            F("阶段判断", "学习业务进入『被母公司保留的品牌』阶段；它能否继续独立取决于 Bending Spoons 交割后的安排。", I)])

# =====================================================================
# 03 产品盘点
# =====================================================================
rec("rf-products", "reforge", "product-map", FA, "asset", "已核实（官方）＋缺口",
    "产品盘点：从单一 cohort 到会员、团队席位、内容库，再到 AI 工具",
    "按出现顺序列出每类产品的客户、收费单位、交付方式与验证强度。",
    "各产品的收入占比与使用数据均未公开；早期价格未查到。",
    ["e-raise-21m", "e-series-b", "e-teams-2023", "e-changes-2023", "e-extension-2024", "e-monterey", "e-build-2025", "e-pricing", "e-home"],
    ["rf-economics", "rf-p-tools"],
    fields=[F("Growth Series（2015–）", "8 周 cohort，申请制，Balfour 与 Andrew Chen 主讲；首期约 1,000 份申请；早期价格未查到。验证强度：付费与口碑有信号（自述）。"),
            F("多项目 cohort＋年度会员（约 2019–2022）", "4–6 周 cohort，会员含 cohort 名额、内容库与社区；2021-02 有 10 个项目，2022-08 约 20 个；会员启用的确切年份未查到。验证强度：收入规模已证明（自述）。"),
            F("团队席位（2023-05–）", "Starter $9,995/10 席，Scale $23,995/30 席，Enterprise 50+ 席定制；个人 $1,995 改为含 1 个 cohort 名额。验证强度：团队占比有信号。"),
            F("内容库：Artifacts、Guides、按需课（2023–）", "1,400+ 真实工作文档、600+ 指南、40+ 按需课；直播课从每年两季改为每月。验证强度：无使用数据。"),
            F("AI 工具（2024–2026-03）", "浏览器插件（2024）、Insights（2025-01，经收购 Monterey）、Research、Build（2025-11）、Launch；2026-03 后并入 Miro。验证强度：无付费数据。"),
            F("组合判断", "主收费一直是年费会员与团队席位；内容库用来提高日常使用与续费；AI 工具是第二曲线尝试，最终以被收购而非收入证明其价值。", I)])

# =====================================================================
# 04 渠道盘点
# =====================================================================
rec("rf-channels", "reforge", "channel-map", FA, "asset", "部分核实",
    "渠道盘点：创始人写作带来申请，专家与学员口碑放大，雇主预算完成付款",
    "区分触达、信任、付款三种作用；没有任何渠道归因数据。",
    "渠道作用来自创始人口述与官方说明；转化率、获客成本、各渠道收入占比均未公开。",
    ["e-muas", "e-a16z-reforge", "e-expense", "e-teams-2023", "e-tweet-2019", "e-miro-blog"],
    ["rf-loop"],
    fields=[F("主渠道：创始人写作（2015–）", "Balfour 与 Chen 的博客形成『内容回路』驱动首批申请（创始人口述）。"),
            F("放大器：专家合作者", "每个项目与知名操盘手共建并由其主讲（2019 年起多位讲师同季开课），借其名声与受众招生。"),
            F("转化页：申请与筛选", "申请制按角色、阶段与公司类型录取；筛选本身也是信用背书。"),
            F("付款方：雇主 L&D 预算", "帮助中心鼓励向公司报销；2023 年过半会员在团队账户。报销比例未知。"),
            F("口碑", "投资方称数千学员主要靠口碑获得；无可核实的推荐率。"),
            F("企业销售（2023–）与 Miro 分发（2026–）", "团队档提供客户成功与 SSO；工具线借 Miro 的 1 亿用户分发。学习业务是否接入 Miro 渠道未知。"),
            F("渠道判断", "早期获客几乎不花钱，依赖少数人的个人信誉；这让起步便宜，也让增长受制于专家供给与雇主预算周期。", I)])

# =====================================================================
# 05 起步资产
# =====================================================================
rec("rf-assets", "reforge", "asset-map", I, "asset", "研究者整理（有来源）",
    "起步资产：信誉、受众、专家网络与申请筛选互补，工程与企业销售是后补的",
    "列出每项资源解决的瓶颈、控制者、实际投入与证据；『当时已有／仍缺』分开。",
    "投入时长与持股均未公开；控制关系按公开角色推断。",
    ["e-amplitude-2016", "e-lenny-balfour", "e-muas", "e-a16z-reforge", "e-tweet-2019", "e-raise-21m", "e-promptled"],
    ["rf-team", "rf-s1", "rf-s2"],
    fields=[F("专业信誉（解决可信度）", "Balfour：HubSpot 增长 VP，三次联合创业；控制者 Balfour。当时已有。", FA),
            F("分发（解决首批申请）", "Balfour 与 Chen（时任 Uber 增长负责人）的博客受众；控制者两人各自。当时已有。", FA),
            F("专家网络（解决内容供给）", "Casey Winters、Shaun Clowes、Kevin Kwok 等 2019 年同季授课；每个项目 50–100 小时共建。初期部分已有，后通过 EIR 扩充。", FA),
            F("交付形式（解决学习质量）", "线上多周 cohort＋申请筛选，学员彼此是学习资源。当时已设计。", FA),
            F("资本（解决扩题速度）", "前 5 年靠现金流；2021–22 年融资 $81M。后期补上。", FA),
            F("仍缺", "起步时没有企业销售与工程团队；2024 年做工具时只有约 25% 员工能转到产品公司，另靠收购补创业型人才。", FA),
            F("资产配合判断", "信誉让高价可信，受众让获客便宜，筛选保证同侪质量，专家网络把一门课变成目录；缺任一项，『高价小批次』都难成立。", I)])

# =====================================================================
# 06 团队与分工
# =====================================================================
rec("rf-team", "reforge", "team-map", FA, "team", "部分核实",
    "团队与分工",
    "只列公开可核实的角色；持股、全职状态与工时多数未披露，未披露不等于没有投入。",
    "合作讲师名单按公开帖子与官网整理，背景未逐人核实；团队规模来自不同时间的口述。",
    ["e-amplitude-2016", "e-a16z-reforge", "e-eir-2022", "e-willerer", "e-extension-2024", "e-monterey", "e-supra", "e-chargebee"],
    ["rf-assets"],
    people=[
        {"name": "Brian Balfour", "role": "创始人／CEO（2015–2026-03），现任 Miro 首席增长官",
         "background": "HubSpot 增长 VP；此前联合创办 Viximo 等三家公司",
         "responsibility": "实际：发起并主讲 Growth Series；自述对 2022-11 裁员决策负全责；主导转向工具与出售",
         "commitment": "CEO 职位；持股与收购后承诺期未披露",
         "evidenceIds": ["e-amplitude-2016", "e-lenny-balfour", "e-layoff-2022", "e-miro-blog"]},
        {"name": "Andrew Chen", "role": "Growth Series 共同创建者；2021 起任董事（a16z 合伙人）",
         "background": "时任 Uber 增长负责人，知名增长博主",
         "responsibility": "实际：共建并讲授首个项目；领投 A 轮并加入董事会",
         "commitment": "非全职（先后在 Uber、a16z 任职）；在 Reforge 的权益未披露",
         "evidenceIds": ["e-amplitude-2016", "e-a16z-reforge"]},
        {"name": "Tom Willerer", "role": "EIR（2022 起）→ COO（约 2023-07 起，整理站资料）→ Miro 首席战略官",
         "background": "Coursera CPO、Opendoor CPO、Netflix 产品 VP",
         "responsibility": "实际：COO；具体分管范围未公开",
         "commitment": "全职状态未披露",
         "evidenceIds": ["e-eir-2022", "e-willerer", "e-miro-blog"]},
        {"name": "课程合作者与 EIR（Casey Winters、Shaun Clowes、Kevin Kwok、Elena Verna、Ravi Mehta、Sachin Rekhi 等）",
         "role": "项目共建者／主讲人／驻场专家",
         "background": "大型科技公司的增长、产品与营销负责人（未逐人核实）",
         "responsibility": "实际：共建或主讲课程，每个项目 50–100 小时共建；2026 年 Rekhi、Mehta 仍主讲直播课",
         "commitment": "兼职、按项目；分成未公开（竞争对手称 Reforge 留 50%，未核实）",
         "evidenceIds": ["e-tweet-2019", "e-series-b", "e-raise-21m", "e-courses", "e-maven-guide"]},
        {"name": "Dan Wolchonok", "role": "新产品 VP",
         "background": "未在本研究中核实",
         "responsibility": "实际：带 2–3 人团队做 AI 浏览器插件（2024）",
         "commitment": "未披露",
         "evidenceIds": ["e-extension-2024"]},
        {"name": "Monterey AI 团队（Chun Jiang、Ben Kramer 等）", "role": "2025-01 随收购加入",
         "background": "Monterey AI 创始团队，做客户反馈分析",
         "responsibility": "推断：负责 Insights 产品线（由 Monterey 产品更名而来）",
         "commitment": "收购条款与留任期未披露",
         "evidenceIds": ["e-monterey", "e-promptled"]},
        {"name": "团队规模（集体）", "role": "全体员工",
         "background": "转型前人数未公开",
         "responsibility": "2022-11、2023-04 两轮裁员（人数未公开）；2024-10 第三轮（二手，称只留约 25%）；2025 年访谈称团队 25 人；2025-12 约 40 人、4–5 个产品",
         "commitment": "按 4–7 人小组并行做产品（自述）",
         "evidenceIds": ["e-layoff-2022", "e-layoff-2023", "e-classcentral", "e-supra", "e-chargebee"]}])

# =====================================================================
# 07 收入与资本
# =====================================================================
rec("rf-economics", "reforge", "economics", I, "asset", "情景分析（非经营数据）",
    "收入与单位经济：价格清楚，成本与续费不透明",
    "下表把已知价格与未知成本分开；『情景』字段是研究者的推算，不是公司数据。",
    "讲师分成、获客成本、续费率均未公开；情景只用来指出敏感变量。",
    ["e-pricing", "e-teams-2023", "e-expense", "e-raise-21m", "e-maven-guide", "e-chargebee"],
    ["rf-series-revenue", "rf-p-retention"],
    fields=[F("收费单位", "个人 $1,995/年；Starter 约 $1,000／席／年（$9,995÷10）；Scale 约 $800／席／年（$23,995÷30）；Enterprise 定制。", FA),
            F("付款人", "个人自付或雇主 L&D 报销（官方鼓励）；2023 年过半会员在团队账户。", FA),
            F("主要成本", "每个项目 50–100 小时专家共建；直播交付；平台与内容团队；讲师分成未公开。", FA),
            F("情景：若讲师分成接近 50%", "竞争对手的说法若成立，每个个人会员约有 $1,000 留给平台覆盖获客、平台与团队；会员若一年后不续，获客与制作成本必须在首年收回。这是推算，不是事实。", I),
            F("敏感变量", "续费率、团队席位占比与扩席、讲师分成、每门课的复用年数、获客是否仍靠免费渠道。", I),
            F("资本结构", "自举 5 年后两轮共 $81M；随后三轮裁员；收购对价未披露。", FA)])

rec("rf-series-revenue", "reforge", "economics", FA, "series", "自述＋缺失",
    "收入规模序列（自述）",
    "只有三个公开节点，其中两个没有具体数值；不能画成连续趋势。",
    "口径未说明（ARR 或确认收入）；时期存在冲突；2023 年后完全缺失。",
    ["e-chargebee", "e-balfour-21m", "e-classcentral", "e-joining-miro"], ["rf-m-revenue"],
    series={"unit": "百万美元／年", "definition": "创始人或报道给出的年收入规模（口径未说明）",
            "points": [
                {"period": "2015（首门课）", "value": None, "basis": "首个 Growth Series", "evidenceIds": ["e-spring-2025"],
                 "missingReason": "已查官方博客与访谈，未见首年收入"},
                {"period": "约 2019（自举第 4 年）", "value": 10, "basis": "『Bootstrapped to $10M in four years』；年份按 2015 起算推定", "evidenceIds": ["e-chargebee"]},
                {"period": "2021-02（A 轮时）", "value": None, "basis": "『8 位数收入、盈利』", "evidenceIds": ["e-balfour-21m"],
                 "missingReason": "只给量级（≥$10M），没有具体数值"},
                {"period": "约 2022 下半年（A 轮后 18 个月）", "value": 30, "basis": "『grew to $30M in 18 months』；Class Central 转载称为 2023 年数字", "evidenceIds": ["e-chargebee", "e-classcentral"]},
                {"period": "2023–2025", "value": None, "basis": "裁员与转型期", "evidenceIds": ["e-classcentral"],
                 "missingReason": "已查公司博客、访谈摘要与媒体，未找到收入数字"},
                {"period": "2026-03（被收购）", "value": None, "basis": "收购公告", "evidenceIds": ["e-joining-miro", "e-itbrief"],
                 "missingReason": "收购条款与收入未披露"}]})

# =====================================================================
# 08 自身路径（全部关键步骤在主页面）
# =====================================================================
rec("rf-origin-summary", "reforge", "own-origin", I, "asset", "研究者整理",
    "自身路径：先证明高价付费，再扩目录，然后改购买单位，最后换产品形态",
    "每一步分开『做了什么』『结果』与『机制解释』；2015–2022 是加法，2022–2026 是收缩与换道。",
    "早期价格、批次规模与会员启用年份未查到；后期效果多无公开数据。",
    ["e-muas", "e-raise-21m", "e-teams-2023", "e-joining-miro"], ["rf-s1", "rf-s7"])


def step(id, stage, title, text, action, result, mech, ev, rel=()):
    return rec(id, "reforge", "own-origin", FA, "step", "事实＋解释字段", title, text,
               "『机制』字段是研究者解释；结果多为公司或创始人自述。", ev, rel, stage=stage,
               fields=[F("动作", action), F("结果", result), F("机制", mech, I)])


step("rf-s1", "2015 · 洞察与切入点", "在 HubSpot 任职时，与 Andrew Chen 做 8 周 Growth Series",
     "Balfour 认为市面培训多为入门级，满足不了其增长团队；与在做 SVBR 实验的 Chen 合作。",
     "推出 SVBR Growth Series：8 周增长讲座系列，后更名 Reforge。",
     "2016-06 媒体已称其为两人共同主持的 8 周项目；官方称 2015 年为首门课。",
     "用『高阶、操盘手视角』避开入门教育；两人的受众就是首批渠道，不需要先建分发。",
     ["e-muas", "e-amplitude-2016", "e-spring-2025", "e-raise-21m"], ["rf-assets"])
step("rf-s2", "2015–2016 · 人工验证", "申请制筛选首批学员，先跑 MVP 再改版",
     "按角色、阶段、公司类型录取，不以收入最大化为目标；按假设清单逐项验证格式。",
     "申请筛选、小批次授课；收集学员反馈后改第二版。",
     "约 1,000 份申请；NPS 由 MVP 的 20 升到下一版 72（创始人口述）。",
     "筛选保证同侪质量，是高价可被接受的条件之一；口碑反馈来自 cohort 体验而非内容本身。",
     ["e-muas"], ["rf-tradeoff"])
step("rf-s3", "约 2016–2020 · 产品化", "从 1 个项目扩到多个，引入专家合作者、EIR 与年度会员",
     "把创始人个人内容扩展为多位操盘手共建的课程目录。",
     "与 Casey Winters 等共同授课（2019 春季）；2019-11 发起 EIR；推出年度会员（启用年份未查到）。",
     "自举约 4 年到 $10M（自述）；2021-02 有 10 个项目、数千学员。",
     "专家共建扩大供给，会员把单次购买变成年度关系；但会员的续费前提此时尚未被检验。",
     ["e-tweet-2019", "e-eir-2019", "e-chargebee", "e-raise-21m", "e-a16z-reforge"], ["rf-loop"])
step("rf-s4", "2021-02 至 2022-08 · 资本扩张", "融资 $81M，项目扩到约 20 个",
     "Balfour 称现金流不足以支撑从每年少量新题扩到 30+ 题目。",
     "A 轮 $21M（a16z）、B 轮 $60M（Insight）；招募更多 EIR；2022-08 约 20 个项目、50+ 讲师。",
     "自述融资后 18 个月收入到约 $30M。",
     "资本把内容与人员成本前置，固定成本上升；收入增长与扩题同期，但不能分辨新题贡献。",
     ["e-balfour-21m", "e-series-b", "e-fall-2022", "e-chargebee"], ["rf-d2"])
step("rf-s5", "2022-11 至 2023-12 · 收缩与重组", "两轮裁员后，转向团队席位与常年内容",
     "第一轮以宏观为由，第二轮称战略调整；随后改价格与产品结构。",
     "2023-05 推团队产品，个人会员 cohort 名额由 2 降为 1；2023-12 推 Artifacts、Guides、每月直播课、AI 搜索。",
     "官方称过半会员在团队账户；收入与续费变化未公开。",
     "把购买单位从个人移到团队，把价值从季节性 cohort 移到随时可用的工作素材，针对的是『需要时才用』的问题。",
     ["e-layoff-2022", "e-layoff-2023", "e-teams-2023", "e-changes-2023"], ["rf-d3"])
step("rf-s6", "2024 至 2025 · 第二曲线", "转做 AI 工具，小团队并行出产品",
     "Balfour 称 2022 年下行重创 edtech，AI 带来生存问题；学员难把内容用到日常工作。",
     "2024 年上线 AI 浏览器插件；2024-10 第三轮裁员（二手：留约 25%）；2025-01 收购 Monterey 形成 Insights；2025 年推出 Research、Build（11 月）、Launch。",
     "约 25 人、9 个月推出 5 个产品（播客标题）；2025-12 约 40 人、4–5 个产品；无付费数据。",
     "把『学→做』的缺口做成工作流软件，试图从阶段性需求转向日常高频使用。",
     ["e-chargebee", "e-extension-2024", "e-classcentral", "e-monterey", "e-build-2025", "e-supra"], ["rf-d4"])
step("rf-s7", "2026-03 起 · 退出与再易主", "并入 Miro，学习业务保持独立；Miro 又将被 Bending Spoons 收购",
     "工具需要更大的分发与协作场景；Miro 想解决『决定做什么』的问题。",
     "工具并入 Miro Product Acceleration；Learning 独立；Balfour、Willerer 进入 Miro 高管层。",
     "条款未披露；学习业务价格与 cohort 未变（官方）；2026-09 Bending Spoons 同意收购 Miro。",
     "工具线的价值由 Miro 的分发兑现；学习业务成了附属品牌，前景取决于新所有者的重组方式。",
     ["e-joining-miro", "e-miro-blog", "e-build-redirect", "e-bending-spoons"], ["rf-d5"])

rec("rf-tradeoff", "reforge", "own-origin", FA, "tradeoff", "三种证据身份分开",
    "取舍与反模式：已证实的取舍、分析建议与未知",
    "只有前三项有直接来源；其余是研究者从结果推出的建议或仍未知的问题，不能当作管理层当时的考虑。",
    "公开资料中几乎没有管理层放弃某条路线的记录，因此不从沉默推断『克制』。",
    ["e-muas", "e-balfour-21m", "e-teams-2023"], ["rf-s2", "rf-d2"],
    fields=[F("已证实取舍：按适配录取，不按收入最大化", "创始人称拒绝『收入最大化』录取，看角色、阶段、公司类型。"),
            F("已证实取舍：自举 5 年才融资", "Balfour 称『Capital is a means to an end』，在 8 位数收入、盈利后才融资。"),
            F("已证实取舍：缩减个人会员内含的 cohort 名额", "2023-05 由 2 个降为 1 个，同时推团队产品。"),
            F("分析建议：续费未证明前不先扩题", "扩题提高固定成本，而『需要时才学』意味着题目多不一定换来续费。", RE),
            F("分析建议：给阶段性需求设计按次购买", "单课、季卡或团队按项目购买，可能比年费更贴合需求节奏；未经验证。", RE),
            F("未知", "管理层是否评估过低价订阅（类似 Lenny）或开放平台分成（类似 Maven）；没有公开材料。", I)])

# =====================================================================
# 09 自身回路
# =====================================================================
rec("rf-loop", "reforge", "own-growth", I, "loop", "逐边证据状态",
    "自身回路：获客回路成立，续费与工具回路未闭合",
    "前四条边有不同强度的信号；『扩题→续费』有反向信号，『工具→高频使用』没有证据。所以这是一条强获客、弱留存的流程，不是已闭合的飞轮。",
    "所有边都缺归因数据；状态只说明证据强度，不说明效应大小。",
    ["e-muas", "e-teams-2023", "e-fall-2022", "e-chargebee"], ["rf-p-retention", "rf-decline"],
    edges=[
        {"from": "创始人与专家写作", "to": "申请与付费学员", "mechanism": "高阶框架建立信任，免费内容引导申请",
         "status": "有信号：创始人称内容回路驱动申请；无归因数据", "evidenceIds": ["e-muas"]},
        {"from": "筛选后的同侪 cohort", "to": "学员体验与口碑", "mechanism": "同侪质量提升学习体验，带来推荐",
         "status": "有信号：早期 NPS 20→72；投资方称靠口碑获客；无推荐率", "evidenceIds": ["e-muas", "e-a16z-reforge"]},
        {"from": "学员晋升或成为管理者", "to": "团队采购", "mechanism": "学过的人为团队买席位",
         "status": "有信号：2023 年过半会员在团队账户；『晋升→采购』因果未核实", "evidenceIds": ["e-teams-2023"]},
        {"from": "资深学员与操盘手", "to": "新课程供给", "mechanism": "校友与专家网络成为讲师或 EIR",
         "status": "有信号：EIR 计划、50+ 讲师；校友转讲师比例未知", "evidenceIds": ["e-eir-2019", "e-fall-2022"]},
        {"from": "课程目录扩大", "to": "会员续费", "mechanism": "题目多让会员每年都有可学的内容",
         "status": "反向信号：最大流失原因是『现在不需要』；扩题未证明能续费", "evidenceIds": ["e-chargebee"]},
        {"from": "AI 工具嵌入工作流", "to": "高频持续使用与付费", "mechanism": "在写文档、做原型时直接用 Reforge",
         "status": "未证明：无使用或付费数据；工具已并入 Miro，回路未闭合", "evidenceIds": ["e-extension-2024", "e-joining-miro"]}])

# =====================================================================
# 10 关键决策
# =====================================================================


def decision(id, title, text, d, ev, rel=()):
    return rec(id, "reforge", "historical-choices", I, "decision", "复盘（研究者解释）", title, text,
               "『备选』除注明外均为研究者构造，不代表管理层讨论过；结果出现在选择之后不等于由选择导致。",
               ev, rel, decision=d)


decision("rf-d1", "2015：做高价申请制 cohort，而不是免费内容或自学视频课",
         "起步方式决定了此后的收入结构：高价、小批次、依赖专家时间。",
         {"period": "2015–2016", "context": "Balfour 在 HubSpot 任职，认为高阶从业者培训稀缺；手里有两人的博客受众。",
          "knownThen": "已知：两人博客有受众、市面培训偏入门（自述）。不知道：高价能否持续、需求是否连续。",
          "options": "实际：8 周 cohort、申请制。研究者构造：付费通讯、录播视频课、线下会议；无证据显示曾讨论。",
          "chosen": "SVBR Growth Series，申请筛选、小批次。",
          "outcome": "约 1,000 份申请；NPS 升到 72；自举约 4 年到 $10M（均为自述）。",
          "tradeoff": "高价与筛选限制规模；讲师时间是容量上限；没有日常使用场景。",
          "assessment": "在『受众已有、内容高阶、雇主可报销』三个条件下，这是低资本验证付费的有效方式；直接证据只有自述数字。",
          "falsifier": "若同期同类高阶课程不筛选、低价也取得同等付费与口碑，则『筛选＋高价』不是关键因素。"},
         ["e-muas", "e-chargebee", "e-spring-2025"], ["rf-s1", "rf-s2"])
decision("rf-d2", "2021–2022：结束自举，融资 $81M 扩题",
         "在盈利状态下选择用资本换速度，时点贴近教育赛道估值高点。",
         {"period": "2021-02 至 2022-03", "context": "已 8 位数收入且盈利；想从每年少量新题扩到 30+ 题目，现金流不够（自述）。",
          "knownThen": "已知：疫情期线上学习热、2021 年全球 edtech 风投 $20.8B 创纪录。不知道：2022 年科技业裁员与预算收紧。",
          "options": "实际：A、B 两轮融资扩题、扩 EIR。研究者构造：继续自举、只深化增长与产品两个核心方向。",
          "chosen": "两轮共 $81M；项目扩到约 20 个、讲师 50+。",
          "outcome": "自述 18 个月内收入到约 $30M；随后 2022-11、2023-04 两轮裁员。",
          "tradeoff": "内容与人员成本前置；若需求阶段性，新题未必带来续费；资本方对增长速度的预期上升。",
          "assessment": "扩题在上行期带来收入增长，但把公司变得对需求下滑更敏感。不能据此断定融资导致收缩。",
          "falsifier": "若有数据显示 2022 年后的下滑主要来自原有核心课程而非新题目，扩题就不是主要拖累。"},
         ["e-balfour-21m", "e-series-b", "e-fall-2022", "e-holoniq", "e-chargebee", "e-layoff-2022"], ["rf-s4", "rf-p-capital"])
decision("rf-d3", "2023：从季节性 cohort 转向团队席位与常年内容",
         "第一次正面处理『需要时才用』：把购买者换成团队，把价值换成随时可用的素材。",
         {"period": "2023-05 至 2023-12", "context": "两轮裁员之后；官方称过半会员在团队账户。",
          "knownThen": "已知：团队用户价值更高（官方）。公开资料没有续费数据。",
          "options": "实际：团队产品、个人 cohort 名额减半、Artifacts／Guides／每月直播。研究者构造：降价个人订阅、按课单买。",
          "chosen": "团队席位＋常年内容库＋更短更频繁的直播课。",
          "outcome": "收入影响未公开；2024-10 又有第三轮裁员（二手）。",
          "tradeoff": "个人会员的价值被削减，可能流失个人用户；内容库需要持续投入。",
          "assessment": "方向对准了问题，但后续仍需裁员并转工具，说明这一步至少不足以恢复增长；具体效果无法评估。",
          "falsifier": "团队账户与个人账户的续费率对比；若团队续费显著更高且收入回升，则这一步有效、后续转型另有原因。"},
         ["e-teams-2023", "e-changes-2023", "e-classcentral"], ["rf-s5", "rf-p-team"])
decision("rf-d4", "2024–2025：从教育转做 AI SaaS 工具",
         "第二曲线押在『学→做』的工作流软件上，靠小团队与收购补人才。",
         {"period": "2024 至 2025", "context": "Balfour：2022 年下行重创 edtech，AI 带来生存问题；学员难把课程用到日常工作。",
          "knownThen": "已知：插件已上线；只有约 25% 员工能转到产品公司（自述）。不知道：工具能否收费、与 Cursor、v0、Lovable 等的竞争结果。",
          "options": "实际：自建＋收购 Monterey，小组并行推出 5 个产品。研究者构造：只做 AI 课程（Section 的早期路径）、单独出售学习业务。",
          "chosen": "AI 工具线（Insights、Research、Build、Launch）与 AI 课程并行。",
          "outcome": "2025 年陆续发布；2026-03 被 Miro 收购，工具并入 Miro。",
          "tradeoff": "资源从学习业务分流；进入竞争激烈的 AI 工具市场；团队需要创业型人才。",
          "assessment": "工具线让公司对 Miro 有战略价值（收购公告重点在工具与人才），但收购不证明工具已有付费规模。",
          "falsifier": "Miro 是否保留并单独收费这些工具、披露客户数；若很快下线，工具线的价值主要在人才。"},
         ["e-chargebee", "e-promptled", "e-monterey", "e-supra", "e-joining-miro"], ["rf-s6", "rf-p-tools"])
decision("rf-d5", "2026-03：出售给 Miro，学习业务保持独立",
         "退出方式把工具与人才交给有分发的平台，学习品牌留在原地。",
         {"period": "2026-03", "context": "工具需要分发与协作场景；Miro 有 1 亿用户、25 万以上组织。",
          "knownThen": "已知：Miro 有 1 亿用户、正扩展到产品开发场景。不知道：Miro 自身会在半年后被出售（其估值较 2022 年大幅下降是 2026-09 才见报的信息）。",
          "options": "实际：并入 Miro。研究者构造：继续独立融资、单独出售学习业务。",
          "chosen": "Miro 收购人员、学习平台与产品；Learning 独立运营。",
          "outcome": "2026-09-10 Bending Spoons 同意收购 Miro，预计 Q4 交割；Reforge Learning 的安排未知。",
          "tradeoff": "失去独立性；学习品牌的未来交给两层新所有者。",
          "assessment": "退出说明团队与工具的价值被认可；没有对价，无法判断是否回报了 $81M 融资。",
          "falsifier": "披露的收购对价，或 Bending Spoons 交割后对 Reforge Learning 的处置。"},
         ["e-joining-miro", "e-miro-blog", "e-itbrief", "e-bending-spoons"], ["rf-s7", "rf-status"])

# =====================================================================
# 11 收缩诊断
# =====================================================================
rec("rf-decline", "reforge", "decline-diagnosis", I, "asset", "暂定排序（有条件）",
    "收缩诊断：宏观收缩是触发，阶段性需求是放大，竞争替代证据最弱",
    "可观察的现象是三轮裁员、价格结构调整与转型，而不是一条收入下降曲线；三种机制可能同时存在。",
    "没有 2022 年后的收入、会员或续费数据；排序靠当事人陈述与同类平台对比，不是贡献比例。",
    ["e-layoff-2022", "e-holoniq", "e-section-tc", "e-maven-li", "e-lenny-fr", "e-lenny-pass", "e-maven-guide", "e-chargebee", "e-teams-2023"],
    ["rf-p-retention", "rf-d2", "rf-investigation"],
    fields=[F("环境变化", "支持：2022-11 第一次裁员自述原因为宏观前景；2022 年全球 edtech 风投降 49%；Section 2022-05 裁员约 25% 并转企业。反证与缺口：Maven 在 2023-11 累计销售 $20M、Lenny 订阅到 100 万+，说明产品与增长类学习需求没有消失；缺企业培训预算数据。"),
            F("竞争替代", "支持：Lenny 年费 $200 并附送大量工具；Maven 讲师留 90%，并公开称 Reforge 留 50%；免费播客与 AI 助手也能提供框架类内容。反证与缺口：没有学员或讲师流向数据；2026 年仍有知名讲师在 Reforge 授课。"),
            F("自身回路", "支持：Balfour 称最大流失原因是『现在不需要』；2023 年先动会员结构，再转工具，说明问题出在需求节奏。反证与缺口：无续费率；团队账户可能已部分缓解。"),
            F("条件排序与依据", "前提：2022 年后的需求收缩在科技职场是普遍的。在此前提下，环境排第一作为触发（时序最贴近，且有当事人陈述）；自身回路排第二作为放大（同样有当事人陈述，并解释了为何没有随环境恢复而反弹、而是转型）；竞争替代排第三，只有市场结构推断。这是暂定排序，不估算贡献比例。", I),
            F("推翻条件与调查顺序", "先找 2021–2024 年的续费率或会员数：若续费在 2022 年前已下滑，自身回路升为第一。再对照 Maven、Lenny 2022–23 的同期表现：若同类也同步下滑，环境解释更稳；若它们同期明显增长，而 Reforge 讲师或团队客户转向它们，竞争解释上调。缺这些数据时保持暂定。", I)])

# =====================================================================
# 12 借鉴顺序
# =====================================================================
rec("rf-transfer", "reforge", "transfer-order", RE, "transfer", "条件式建议（用途未确认）",
    "借鉴顺序：先学起步验证法，后学团队售卖，谨慎对待年费会员，暂不学融资扩题与转工具",
    "读者对象假定为：已有可触达目标从业者的写作、社群或专家关系，想做职业教育或知识产品的团队。用户用途未确认，分类会随回答调整。",
    "Reforge 的成功段只有自述数字；单个案例不证明方法有效，需与 Lenny、Maven、Section 的不同路径对照。",
    ["e-muas", "e-teams-2023", "e-chargebee", "e-raise-21m", "e-promptled", "e-changes-2023"],
    ["rf-question", "lenny-transfer", "maven-transfer", "section-transfer"],
    fields=[F("现在复制：申请制小批次验证高价付费", "最小动作：一个主题、一位有信誉的讲师、一批经筛选的学员。观察：申请→录取→实付→完课→30 天内用到工作的比例，各自保留分母。承载上限：讲师时间（Reforge 每门课 50–100 小时共建）。"),
            F("现在复制：随课交付可直接用的工作素材", "最小动作：每门课附模板与真实文档。观察：素材被复用的次数与人数。承载上限：素材维护人力。"),
            F("以后复制：团队席位", "先证明：同一雇主内已有多人自发购买或报销。重新评估：出现多家公司各有 3 人以上学员时，再设团队价与管理功能。"),
            F("谨慎借鉴：年费会员与大内容库", "保留：内容库和社区作为附加价值。改掉：默认需求持续的年费假设，改为单课、季卡或按项目购买并量续费。失败界限：第二年续费明显低于首年预期时停止扩题。"),
            F("暂不复制：融资后快速扩题", "机会成本：固定成本前置，需求下滑时只能裁员。重新开启：核心题目的续费与团队扩席已被证明。"),
            F("暂不复制：从教育转 AI SaaS 工具", "机会成本：需要工程与创业型人才（Reforge 靠收购 Monterey 补足），且与通用 AI 工具正面竞争。重新开启：已有稳定团队客户，并能在其工作流中观察到重复使用。")])

# =====================================================================
# 13 下一步调查
# =====================================================================
rec("rf-investigation", "reforge", "next-investigation", RE, "action", "调查计划（研究者）",
    "下一步调查：先补续费，再用同类平台区分环境与竞争，最后追踪新所有者",
    "外部研究不给 Reforge 安排运营，只安排取证顺序；每轮写明观察什么、怎样改判断。",
    "多数内部数据外部拿不到；若始终取不到，结论保持条件式。",
    ["e-supra", "e-chargebee", "e-bending-spoons"], ["rf-decline", "rf-contract", "rf-question"],
    milestones=[
        {"period": "第一轮（1–2 周）", "action": "取得 Supra Insider、Chargebee 等访谈的完整文字稿，查续费率、会员数、团队账户占比；查 Miro 或投资方是否披露对价",
         "owner": "研究 Agent", "observe": "是否有任何同口径的续费或会员时间序列",
         "decision": "找到续费下滑早于 2022 → 自身回路升为第一；找不到 → 维持暂定排序并在页面保留缺口。"},
        {"period": "第二轮（2–4 周）", "action": "对照 2022 与 2026 Reforge 讲师名单，查讲师是否转到 Maven 或自营；收集 Maven、Lenny、Section 2022–23 的同期公开指标",
         "owner": "研究 Agent；如需访谈讲师或学员，须用户另行授权",
         "observe": "讲师流向比例；同类平台同期是增长还是下滑",
         "decision": "同类同步下滑 → 环境解释上调；同类增长且讲师外流 → 竞争解释上调。"},
        {"period": "第三轮（Bending Spoons 交割后，约 2026 Q4–2027 Q1）", "action": "复查 reforge.com 的价格、课程、品牌归属与 Miro 内工具的存续",
         "owner": "研究 Agent；用户如是会员可提供续费通知",
         "observe": "价格或课程是否调整；Learning 是否被出售、合并或关停",
         "decision": "据此更新『现状』与证明命题 rf-p-learning-now，并重写首屏判断。"}])

rec("rf-contract", "reforge", "next-investigation", RE, "contract", "外部研究的数据缺口约定",
    "所需数据、现有代理与缺口边界",
    "没有任何内部记录访问权；下表约定若用户或公开披露能提供数据时需要的口径，以及当前使用的代理证据。",
    "代理证据只能限定结论强度，不能替代内部数据。",
    ["e-chargebee", "e-teams-2023", "e-maven-guide", "e-pricing"], ["rf-investigation"],
    fields=[F("唯一对象标识", "需要：会员或公司账户 ID 跨报名、付款、续费去重。当前：无，只有累计学员 10 万+（不可去重）。"),
            F("实际付款", "需要：按年、按个人／团队拆分的净收款与折扣。当前代理：标价与创始人自述的收入量级。"),
            F("分期留存与续费", "需要：按入会年份的批次续费率，区分个人与团队；未到期与缺记录分开。当前代理：CEO 对流失原因的定性陈述。"),
            F("成果标准", "需要：课程前定义的工作应用任务与达标数。当前代理：早期 NPS 一次。"),
            F("交付成本", "需要：每门课专家工时、讲师分成、直播交付工时。当前代理：50–100 小时共建（官方）；分成只有竞争对手说法。"),
            F("渠道来源", "需要：首触与促成渠道（创始人内容、讲师、推荐、企业销售）。当前：无归因数据。"),
            F("更新责任", "研究 Agent 每轮记录查询日期与范围；不假定能接触 Reforge 或 Miro 后台。")])

rec("rf-question", None, "next-investigation", RE, "question", "待回答（无回答不等于同意）",
    "向用户的问题（本轮 2 个）",
    "问题 1：这次研究 Reforge 是为了给你自己的业务做决定（例如你在做职业教育、知识付费或 AI 产品工具），还是只想理解它可以借鉴什么？如果是前者，请用一两句话说明业务和当前要做的选择。"
    "问题 2：你手上有没有能分享的 Reforge 内部或会员信息，例如你或团队的会员续费情况、团队账户价格、讲师分成？只需汇总口径，不要个人信息。",
    "两题都允许回答『不知道』或给区间；未回答时报告保持外部研究口径。",
    [], ["rf-transfer", "rf-decline", "rf-contract"],
    fields=[F("影响", "问题 1 决定是否需要补主路线、四道门槛与会议摘要，并改写借鉴顺序；问题 2 可能直接改变『阶段性需求』排序与单位经济情景。"),
            F("当前处理", "按外部研究交付；借鉴建议写成条件式；自有业务决策项在覆盖清单标为不适用并说明原因。")])

# ---------------- 判断更新（核验专题） ----------------
rec("rf-change-status", "reforge", "executive-summary", I, "change", "研究过程中的公开资料更新",
    "发现两次收购后，『独立经营』判断下调",
    "研究开始时把 Reforge 当作仍在独立运营的会员制学习公司。",
    "新证据是官方公告与媒体报道，不是用户回答。",
    ["e-joining-miro", "e-bending-spoons", "e-build-redirect"], ["rf-status", "rf-p-learning-now"],
    change={"before": "Reforge 是独立运营的学习公司，研究重点是会员业务。",
            "newEvidence": "2026-03-24 双方公告：Miro 收购 Reforge，工具并入 Miro；2026-09-10 报道：Bending Spoons 同意收购 Miro；工具入口实际跳转到 Miro（访问记录）。",
            "direction": "下调", "after": "现状改为『学习品牌在 Miro 内独立运营，归属受 Bending Spoons 交割影响』；新增退出决策与第三轮调查。",
            "impact": "首屏判断、现状节、命题 rf-p-learning-now、决策 rf-d5、调查第三轮均已改写。"})
rec("rf-change-maven", "reforge", "executive-summary", I, "change", "排除无来源说法",
    "排除『Reforge 2023 年收购 Maven』的说法",
    "一条搜索摘要称 Reforge 收购了 Maven 的课程平台；若成立会彻底改变供给与竞争判断。",
    "排除依据是多份官方与媒体资料的矛盾，以及该说法没有任何来源。",
    ["e-maven-claim", "e-maven-li", "e-maven-fee", "e-maven-guide"], ["maven-verdict", "rf-decline"],
    change={"before": "待核实：Reforge 可能在 2023 年收购了 Maven 课程平台。",
            "newEvidence": "Maven 创始人 2023-11 仍以独立公司发布业绩；Maven 帮助中心 2025–2026 仍把 Reforge 当竞品比较；未见任何收购公告。原说法来自无来源聚合页。",
            "direction": "下调", "after": "不采用该说法；Maven 作为独立竞品进入对标。",
            "impact": "横向对照与收缩诊断中的竞争解释以 Maven 独立为前提。"})
rec("rf-change-decline", "reforge", "executive-summary", I, "change", "研究过程中的判断更新",
    "竞争替代从首要解释降为第三",
    "研究初期假设：2022 年后收缩主要因为 Lenny、Maven 与免费内容分流。",
    "新证据是当事人陈述与同类平台公开数据，仍不是因果证明。",
    ["e-chargebee", "e-layoff-2022", "e-section-tc", "e-maven-li"], ["rf-decline", "rf-transfer"],
    change={"before": "竞争替代是首要解释。",
            "newEvidence": "Balfour 称最大流失原因是『现在不需要』；第一次裁员自述为宏观原因；Section 同期裁员转企业；Maven 同期仍增长（均为自述或报道）。",
            "direction": "下调", "after": "排序改为环境触发、自身回路放大、竞争并存但证据最弱。",
            "impact": "收缩诊断改写；借鉴顺序中『年费会员』降为谨慎借鉴；调查计划第二轮加入讲师流向核对。"})

rec("rf-series-programs", "reforge", "executive-summary", FA, "series", "公司公告",
    "cohort 项目数序列（2015–2022）",
    "只统计 cohort 项目；2023 年后改为按需课程库（2025-02 共 40 门直播＋按需），口径不同，不放进本序列。",
    "『约 2018 年 4 门』的年份来自播客录制时间推测；2022-08 为『约 20』。",
    ["e-spring-2025", "e-muas", "e-raise-21m", "e-series-b", "e-fall-2022"], ["rf-p-supply"],
    series={"unit": "个项目", "definition": "官方或创始人公告中同时开设的 cohort 项目数",
            "points": [
                {"period": "2015", "value": 1, "basis": "单一 Growth Series", "evidenceIds": ["e-spring-2025", "e-joining-miro"]},
                {"period": "播客录制时（年份不明）", "value": 4, "basis": "播客称录制时有 4 门课", "evidenceIds": ["e-muas"]},
                {"period": "2021-02", "value": 10, "basis": "A 轮公告：增长、产品、营销、工程共 10 个项目", "evidenceIds": ["e-raise-21m"]},
                {"period": "2022-03", "value": 16, "basis": "B 轮公告：产品 6、增长 5、工程 3、营销 2", "evidenceIds": ["e-series-b"]},
                {"period": "2022-08", "value": 20, "basis": "秋季『约 20 个项目』、50+ 讲师", "evidenceIds": ["e-fall-2022"]}]})

rec("rf-funnel-first", "reforge", "executive-summary", I, "funnel", "大部分节点缺失",
    "首期 Growth Series 的已知与未知",
    "唯一公开的早期数字是申请数；录取、付款、完课都没有公开，不能用申请数证明付款。",
    "申请数是创始人口述的约数；年份有冲突。",
    ["e-muas"], ["rf-s2", "rf-p-pay"],
    funnel={"cohort": "首期 SVBR Growth Series 的申请者（约 2015–2016）",
            "overlap": "录取与付款可能不是同一批人（例如雇主后付）；节点之间不做相乘或相加。",
            "nodes": [
                {"id": "applied", "parentId": None, "label": "提交申请", "count": 1000, "denominator": None,
                 "basis": "创始人口述『about 1000 applications』；分母（触达人数）未知",
                 "proved": "高阶增长课程有明显兴趣", "unproved": "付款意愿与价格接受度", "evidenceIds": ["e-muas"]},
                {"id": "admitted", "parentId": "applied", "label": "录取", "count": None, "denominator": 1000,
                 "basis": "按适配筛选录取；人数未公开", "proved": "存在筛选机制", "unproved": "录取率与批次规模", "evidenceIds": ["e-muas"]},
                {"id": "paid", "parentId": "admitted", "label": "付款入学", "count": None, "denominator": None,
                 "basis": "价格与付款人数未公开", "proved": "无", "unproved": "首期收入与付款人（个人或雇主）", "evidenceIds": ["e-muas"]},
                {"id": "rated", "parentId": "paid", "label": "反馈评分", "count": None, "denominator": None,
                 "basis": "MVP NPS 20 → 下一版 72；样本量未知", "proved": "改版后满意度提升（自述）", "unproved": "学习成果与复购", "evidenceIds": ["e-muas"]}]})

# =====================================================================
# 14 重点案例：Lenny's Newsletter
# =====================================================================
rec("lenny-verdict", "lenny", "featured-benchmark", I, "judgment", "研究者判断",
    "同样起于操盘手写作，Lenny 用低价订阅＋免费播客＋工具捆绑，把阶段性学习变成每周阅读",
    "Lenny 与 Reforge 起点最像：都是一线操盘手用写作积累受众。不同在于 Lenny 把价格压到年费 $200 左右，靠免费播客扩大受众、靠工具捆绑提高付费价值，"
    "团队不设全职员工。这条路避开了『需要时才学』的问题，代价是高度依赖个人品牌，难以复制给多讲师的课程公司。",
    "Lenny 的付费人数与收入未公开；『避开阶段性需求』是推断，没有其续费数据。",
    ["e-lenny-2020", "e-lenny-fr", "e-lenny-pass", "e-lenny-about"], ["lenny-transfer", "rf-transfer"])

rec("lenny-profile", "lenny", "peer-comparison", FA, "profile", "公开资料",
    "Lenny's Newsletter 起点档案",
    "按横向矩阵的统一字段填写。",
    "付费人数、收入、续费均未公开。",
    ["e-lenny-2020", "e-lenny-fr", "e-lenny-pass", "e-lenny-about"], ["lenny-verdict"],
    fields=[F("公司与阶段", "个人媒体，2019 年起；2026 年约 120 万订阅、无全职员工、约 10 名合同工"),
            F("起点资产", "Airbnb 7 年产品负责人经验（经 Localmind 被收购进入）＋写作能力"),
            F("第一批用户", "推特与客座文章带来的产品经理读者：首条推文带来 500 订阅"),
            F("最初产品", "每周免费通讯与读者问答，10 个月后推出 $15/月付费"),
            F("收入证明", "付费上线后约 500 付费、年约 $65K（2020，自述）；播客年收入超 $500K（2024 报道标题）"),
            F("扩张依赖", "个人品牌与持续写作；Substack 平台；播客嘉宾；工具厂商愿意捆绑"),
            F("与 Reforge 的资产差距", "只有一位核心作者，没有多讲师课程与企业销售；但获客与交付成本远低于 cohort", I),
            F("当前可学动作", "先长期免费输出建立受众，再用低价订阅收费；用捆绑提高付费价值与可报销性", RE)])

rec("lenny-assets", "lenny", "featured-benchmark", I, "asset", "研究者整理（有来源）",
    "互补起点资产：一个人的经验、写作与平台工具",
    "Lenny 的起点资产比 Reforge 少：没有合伙讲师与筛选机制，但有平台（Substack）解决收费与分发的工程问题。",
    "投入时长与收入只有片段性自述。",
    ["e-lenny-2020", "e-lenny-fr"], ["lenny-s1", "lenny-s2"],
    fields=[F("专业知识（解决内容可信度）", "Airbnb 7 年产品负责人；控制者 Lenny。当时已有。", FA),
            F("分发（解决首批读者）", "推特与客座文章：首条推文 500 订阅、客座文章后到 1,000 与 3,000。当时需从零积累。", FA),
            F("平台（解决收费与发送）", "Substack 提供付费与邮件发送，无需自建工程。当时已有（外部平台）。", FA),
            F("嘉宾网络（解决后期内容供给）", "2022 年起的播客嘉宾；不需要分成，换取曝光。后期补上。", FA),
            F("仍缺", "没有团队与企业销售；没有续费或付费数据公开。", FA),
            F("配合判断", "经验让内容可信，平台让收费零成本，免费内容积累受众；『一个人＋平台』让固定成本极低，这是他能用低价的前提。", I)])


def lstep(id, stage, title, text, action, result, mech, ev, rel=(), company="lenny", section="featured-benchmark"):
    return rec(id, company, section, FA, "step", "事实＋解释字段", title, text,
               "『机制』字段是研究者解释；数字多为当事人自述。", ev, rel, stage=stage,
               fields=[F("动作", action), F("结果", result), F("机制", mech, I)])


lstep("lenny-s1", "2019 · 洞察与切入点", "离开 Airbnb 后把经验写成长文",
      "离开 Airbnb、休假期间开始写作；第一篇 Medium 长文进入热门。",
      "把 7 年 Airbnb 经验写成长文，随后转到 Substack 每周发布。",
      "首条推文带来 500 订阅；两篇客座文章后到 3,000；系列文章后到 5,000；三个月后到 9,000（自述）。",
      "用免费、具体的操盘经验建立信任；借他人平台的客座文章获取首批读者。",
      ["e-lenny-2020", "e-lenny-fr"], ["lenny-assets"])
lstep("lenny-s2", "2019–2020 · 人工交付", "每周写作与读者问答，免费 10 个月",
      "以读者提问驱动选题，每周交付。",
      "坚持免费更新约 10 个月，问答形式来自读者真实问题。",
      "积累约 1.5 万免费订阅（2020 年中）。",
      "问答让作者知道读者真正要解决的问题，相当于人工做需求调研。",
      ["e-lenny-2020"], ["lenny-s3"])
lstep("lenny-s3", "2020 春 · 收入证明", "推出 $15/月付费订阅",
      "在免费受众基础上开收费。",
      "上线付费，做一周推广。",
      "首两天约 200 付费，一周后 250；2020-08 约 500 付费、年约 $65K（未扣费，自述）。",
      "低价、可自付也可报销；付费转化率约 3%（500/15,000，同期口径）。",
      ["e-lenny-2020"], ["lenny-profile"])
lstep("lenny-s4", "2022 起 · 扩张", "开播客，免费分发换受众",
      "在通讯之外增加免费音视频。",
      "2022 年上线播客，远程录制，每期准备 2–10 小时。",
      "每期 10–20 万下载、YouTube 50 万+ 订阅（2026 专访）；播客年收入超 $50 万（2024 报道标题）。",
      "播客既是免费获客渠道，又有赞助收入；嘉宾为曝光而来，不需分成。",
      ["e-lenny-fr", "e-lenny-cnbc"], ["lenny-loop"])
lstep("lenny-s5", "2023–2024 · 社区与活动", "付费社区与线下峰会",
      "把付费读者连接起来。",
      "付费订阅含私有 Slack；2024 年办 Lenny and Friends Summit。",
      "社区约 3–4 万人（不同时间口径）；峰会约 1,200 人（自述）。",
      "社区提高付费的日常价值，部分弥补『阅读是单向的』问题。",
      ["e-lenny-fr", "e-lenny-about"], ["lenny-loop"])
lstep("lenny-s6", "2025-02 起 · 价值捆绑", "年费订阅附送一年 AI 与产品工具",
      "把工具厂商的获客预算变成订阅的附加价值。",
      "2025-02 首次捆绑 Granola、Notion、Superhuman、Linear、Perplexity；2026 年扩到 34 个工具。",
      "Annual $200/年（22 个工具）、Insider $400/年（34 个工具），称总价值 $39,000+；订阅约 120 万。",
      "捆绑让『订阅本身就回本』，更容易自付或报销；工具厂商用它获取新客户。",
      ["e-lenny-bundle", "e-lenny-pass", "e-lenny-fr"], ["lenny-loop"])

rec("lenny-tradeoff", "lenny", "featured-benchmark", FA, "tradeoff", "三种证据身份分开",
    "Lenny 的取舍与反模式",
    "已证实取舍均来自 2026 年专访的当事人陈述；其余是分析建议或未知。",
    "当事人陈述可能美化；无法验证他拒绝过哪些具体机会的机会成本。",
    ["e-lenny-fr"], ["lenny-verdict"],
    fields=[F("已证实取舍：不雇全职员工", "约 10 名合同工；固定成本极低。"),
            F("已证实取舍：不做付费广告", "称投放广告没有价值，增长靠内容。"),
            F("已证实取舍：拒绝几乎所有合作请求", "每周约 200 封请求，拒绝 99.9%。"),
            F("已证实取舍：降低更新频率保质量", "从每月 4 篇降到 2–4 篇，自称担心价值不够。"),
            F("分析建议", "对多讲师课程公司，可学的是『免费内容建受众＋低价可报销』；不可学的是一个人包办全部内容。", RE),
            F("未知", "付费续费率、捆绑对转化的实际作用、收入构成。", I)])

rec("lenny-loop", "lenny", "featured-benchmark", I, "loop", "逐边证据状态",
    "Lenny 的回路：免费内容带受众，低价与捆绑带付费",
    "受众增长有公开数字；付费转化、续费与捆绑效果无公开数据，回路后半段未证实。",
    "所有边都无归因数据。",
    ["e-lenny-2020", "e-lenny-fr", "e-lenny-pass"], ["lenny-transfer"],
    edges=[
        {"from": "免费通讯与播客", "to": "订阅受众", "mechanism": "具体经验与嘉宾访谈带来分享与搜索",
         "status": "有信号：从 500 到约 120 万订阅；无渠道拆分", "evidenceIds": ["e-lenny-2020", "e-lenny-fr"]},
        {"from": "订阅受众", "to": "付费订阅", "mechanism": "低价、可报销、附送工具",
         "status": "有信号：2020 年约 3% 转化；当前付费数未公开", "evidenceIds": ["e-lenny-2020", "e-lenny-about"]},
        {"from": "付费收入与受众规模", "to": "嘉宾与工具伙伴", "mechanism": "受众越大，嘉宾与厂商越愿意合作",
         "status": "有信号：34 个工具伙伴、播客嘉宾持续；因果未核实", "evidenceIds": ["e-lenny-pass", "e-lenny-fr"]},
        {"from": "嘉宾与工具伙伴", "to": "更好的免费内容与付费价值", "mechanism": "新内容与新工具回流到订阅",
         "status": "未证明：没有续费或满意度数据，回路未闭合", "evidenceIds": ["e-lenny-pass"]}])

rec("lenny-transfer", "lenny", "featured-benchmark", RE, "transfer", "条件式建议",
    "从 Lenny 可借鉴与不可借鉴的部分",
    "对照 Reforge：Lenny 解决了获客与价格可接受度，但没有解决『深度学习交付』，两者是不同产品。",
    "Lenny 的个人品牌规模不可复制；建议只适用于已有写作受众的读者。",
    ["e-lenny-2020", "e-lenny-pass", "e-lenny-fr"], ["rf-transfer"],
    fields=[F("可迁移", "免费内容先行、低价订阅、提供报销模板、把伙伴的获客预算变成订阅价值。"),
            F("缺失前提", "持续高质量的个人写作；足够大的受众让工具厂商愿意捆绑。"),
            F("不可照搬", "零全职员工的模式不适合需要直播交付和多讲师协作的 cohort 课程。"),
            F("对 Reforge 的启示", "若 Reforge 在 2022 年前就提供低价阅读层，可能缓解『需要时才学』带来的流失；这是推断，无法验证。", I)])

# =====================================================================
# 15 横向对照：其他对标（档案与步骤在专题；矩阵在主页面）
# =====================================================================
rec("rf-profile", "reforge", "peer-comparison", FA, "profile", "公开资料",
    "Reforge 起点档案（研究对象）",
    "放进矩阵作为对照基线。",
    "收入为自述；后期数据缺失。",
    ["e-muas", "e-chargebee", "e-raise-21m", "e-teams-2023"], ["rf-verdict"],
    fields=[F("公司与阶段", "职业教育公司，2015 年起；2026-03 被 Miro 收购"),
            F("起点资产", "两位增长操盘手的信誉与博客受众＋硅谷增长专家网络"),
            F("第一批用户", "科技公司中高级增长与产品从业者，申请筛选"),
            F("最初产品", "8 周 Growth Series cohort"),
            F("收入证明", "自举约 4 年到 $10M、融资后到约 $30M（自述）"),
            F("扩张依赖", "专家共建课程、雇主 L&D 预算、2021–22 年的风险资本"),
            F("与 Reforge 的资产差距", "（基线）"),
            F("当前可学动作", "申请制小批次验证高价付费；随课交付工作素材", RE)])

rec("maven-verdict", "maven", "peer-comparison", I, "judgment", "研究者判断",
    "Maven 把 cohort 形式做成平台：讲师拿 90%，平台不承担内容成本，但要自己解决讲师留存",
    "与 Reforge 用同一种交付形式（cohort），却把内容成本与风险交给讲师，平台只收 10%。它在 2022–23 年行业下行期仍增长，"
    "但早期也经历了『网红创作者不把平台当回事』的供给问题，靠转向专家与市场流量修复。",
    "Maven 数字多为 GMV 与创始人自述；讲师留存改善数据来自二手整理。",
    ["e-maven-a16z", "e-maven-tc", "e-maven-li", "e-maven-fee", "e-maven-secondary"], ["maven-transfer"])
rec("maven-profile", "maven", "peer-comparison", FA, "profile", "公开资料",
    "Maven 起点档案",
    "按横向矩阵的统一字段填写。",
    "GMV 不是 Maven 收入；平台收入约为 GMV 的 10%（推算）。",
    ["e-maven-a16z", "e-maven-tc", "e-maven-li", "e-maven-fee"], ["maven-verdict"],
    fields=[F("公司与阶段", "cohort 课程平台，2020 年创立，2021-01 上线；2023 年 15 名全职员工"),
            F("起点资产", "创始人分别来自 Udemy、altMBA、Socratic：课程市场、cohort 教学与产品经验"),
            F("第一批用户", "有大量粉丝的创作者及其受众"),
            F("最初产品", "帮创作者开多周 cohort 课，平台抽成"),
            F("收入证明", "上线 4 个月课程销售超 $1M；18 个月 $9M；2023-11 累计 $20M（GMV）"),
            F("扩张依赖", "讲师持续开课；平台市场流量（2023 年约 25% 销售）"),
            F("与 Reforge 的资产差距", "没有自有内容与品牌讲师，但没有内容固定成本；Reforge 反之", I),
            F("当前可学动作", "让讲师承担内容、平台提供招生与工具；按讲师收入留存衡量供给健康", RE)])
lstep("maven-s1", "2020-10 至 2021-05 · 首次交易", "先手工跑课再做软件，上线即放量",
      "创始人先测课程本身，再搭平台。",
      "2021-01 上线；首批讲师多为大粉丝量创作者。",
      "4 个月课程销售超 $1M，4 门课前三个月各超 $100K；2021-05 获 a16z 领投 A 轮。",
      "创作者自带受众，平台一开始几乎不需要获客。",
      ["e-maven-a16z", "e-maven-secondary"], ["maven-s2"], company="maven", section="peer-comparison")
lstep("maven-s2", "2022 · 供给转向", "从网红创作者转向专业专家",
      "发现粉丝多不等于能开好课，创作者把 Maven 当副业。",
      "转向有专业资质的专家，补学生门户与 LMS 功能。",
      "18 个月 $9M、300+ cohort；课程数从最多 15 门到 100+（报道）。",
      "专家更依赖课程收入，更可能持续开课；供给质量比受众规模更重要。",
      ["e-maven-tc", "e-maven-secondary"], ["maven-s3"], company="maven", section="peer-comparison")
lstep("maven-s3", "2023–2024 · 扩张", "市场流量与讲师留存改善",
      "平台开始为讲师带来新学员。",
      "加强 Maven 市场导流，保持 10% 抽成。",
      "2023-11 累计 $20M、25% 销售来自市场、15 名全职员工；二手资料称讲师收入留存从 73% 升到 120–140%（2024-06）。",
      "平台导流让讲师离不开平台，形成供给留存；这正是 Reforge 自营模式没有的杠杆。",
      ["e-maven-li", "e-maven-fee", "e-maven-secondary"], ["maven-loop"], company="maven", section="peer-comparison")
rec("maven-loop", "maven", "peer-comparison", I, "loop", "逐边证据状态",
    "Maven 回路：讲师带学员，平台导流留讲师",
    "前两条边有公开数字；导流对讲师留存的因果只有二手资料。",
    "GMV 与留存均为自述或二手。",
    ["e-maven-li", "e-maven-secondary"], ["maven-transfer"],
    edges=[
        {"from": "讲师自有受众", "to": "课程销售", "mechanism": "讲师带来大部分学员", "status": "有信号：约 75% 销售非平台来源（2023）", "evidenceIds": ["e-maven-li"]},
        {"from": "平台市场", "to": "讲师额外收入", "mechanism": "Maven 把学员导给讲师", "status": "有信号：约 25% 销售来自市场", "evidenceIds": ["e-maven-li"]},
        {"from": "讲师额外收入", "to": "讲师持续开课", "mechanism": "收入越多越不愿离开", "status": "线索：讲师收入留存 120–140%（二手）", "evidenceIds": ["e-maven-secondary"]}])
rec("maven-transfer", "maven", "peer-comparison", RE, "transfer", "条件式建议",
    "Maven 借鉴与风险",
    "适合有课程市场或招生能力、但不想承担内容成本的团队。",
    "Maven 盈利情况未公开。",
    ["e-maven-fee", "e-maven-tc"], ["rf-transfer"],
    fields=[F("可迁移", "用讲师收入留存衡量供给健康；把平台导流作为留住讲师的理由。"),
            F("缺失前提", "足够的学员流量；讲师愿意自己招生。"),
            F("不可照搬", "10% 抽成要求极轻的团队；做不到统一的课程质量与品牌。")])

rec("section-verdict", "section", "peer-comparison", I, "judgment", "研究者判断",
    "Section 与 Reforge 同期遇到消费者端增长停滞，比 Reforge 更早转企业与 AI，最终变成企业 AI 采用软件＋服务",
    "Section 的轨迹（2022-05 裁员约 25%、转企业、2023 年转 AI 课程、再转软件）和 Reforge 高度相似，是『环境解释』的旁证；"
    "差别在于它没有 Reforge 那样的从业者社区起点，靠名人教授品牌起步。",
    "Section 无收入数据；时间相似不证明原因相同。",
    ["e-section-tc", "e-section-pq", "e-section-ti", "e-section-about"], ["section-transfer", "rf-decline"])
rec("section-profile", "section", "peer-comparison", FA, "profile", "公开资料",
    "Section 起点档案",
    "按横向矩阵的统一字段填写。",
    "数字为公司或媒体自述，无收入。",
    ["e-section-tc", "e-section-pq", "e-section-ti", "e-section-about"], ["section-verdict"],
    fields=[F("公司与阶段", "商业技能教育公司，2019 年起；现为企业 AI 采用软件与服务"),
            F("起点资产", "Scott Galloway 的个人品牌与名校教授资源；CEO Greg Shove 的创业经验"),
            F("第一批用户", "想要 MBA 式知识的在职个人"),
            F("最初产品", "2–3 周课程，每门 $995，名校教授主讲"),
            F("收入证明", "2021-03 时 1 万学员；无收入数字"),
            F("扩张依赖", "名人品牌获客、风险资本（A 轮 $30M）、后转企业销售"),
            F("与 Reforge 的资产差距", "有更强的大众品牌，没有从业者专家网络与雇主报销场景", I),
            F("当前可学动作", "需求转向时尽早把客户从个人换成企业，并把课程变成企业要的结果（AI 采用）", RE)])
lstep("section-s1", "2019–2021 · 切入点与资本", "名人教授短课，$995 一门，融资 $30M",
      "用 Galloway 的品牌做『MBA 精华』。",
      "推出 2–3 周课程；2021-03 A 轮 $30M。",
      "2021-03 时 1 万学员、70% 完课率（公司自述）。",
      "名人品牌降低获客成本，但课程制作成本高。",
      ["e-section-tc"], ["section-s2"], company="section", section="peer-comparison")
lstep("section-s2", "2022 · 收缩", "改会员制后裁员约 25%，转企业",
      "消费者增长不及预期。",
      "2022-03 改为一价会员；2022-05 裁员 32 人，转向企业客户。",
      "CEO 称原因是财务失误、尚无 PMF、招人过多、课程制作贵。",
      "与 Reforge 2022-11 裁员时间接近，支持行业性收缩；但 Section 自认 PMF 不足，原因不完全相同。",
      ["e-section-tc"], ["section-s3"], company="section", section="peer-comparison")
lstep("section-s3", "2023–2026 · 第二曲线", "更名 Section，转 AI 课程，再转企业 AI 采用软件",
      "AI 成为企业培训新预算。",
      "2023-03 更名；2023-09 宣布 12 个月 50 门 AI 课；现产品为 Section HQ 与 Section Coach。",
      "2023-09 累计 3.3 万学员、200+ 企业伙伴（新闻稿）；当前无公开客户数。",
      "把『学习』重新包装成企业要的『AI 采用结果』，购买者从个人变成 AI 负责人。",
      ["e-section-pq", "e-section-ti", "e-section-about"], ["section-loop"], company="section", section="peer-comparison")
rec("section-loop", "section", "peer-comparison", I, "loop", "逐边证据状态",
    "Section 回路：品牌带个人学员，企业转型后回路尚未证实",
    "个人端回路在 2022 年停滞（CEO 自认）；企业端缺数据。",
    "无收入与留存数据。",
    ["e-section-tc", "e-section-ti"], ["section-transfer"],
    edges=[
        {"from": "Galloway 品牌与内容", "to": "个人学员", "mechanism": "名人效应降低获客成本", "status": "有信号：1 万→3.3 万学员（自述）", "evidenceIds": ["e-section-tc", "e-section-ti"]},
        {"from": "个人学员", "to": "企业采购", "mechanism": "学员把课程带进公司", "status": "未证明：200+ 企业伙伴，口径不明", "evidenceIds": ["e-section-ti"]}])
rec("section-transfer", "section", "peer-comparison", RE, "transfer", "条件式建议",
    "Section 借鉴与风险",
    "作为旁证：两家公司在相似时点做了相似调整。",
    "Section 的结果（企业 AI 业务是否成立）未知。",
    ["e-section-tc", "e-section-about"], ["rf-transfer"],
    fields=[F("可迁移", "个人需求疲软时，把产品改成企业能衡量结果的项目。"),
            F("缺失前提", "企业销售能力与能交付的结果指标。"),
            F("不可照搬", "名人品牌起步；以名校教授为供给的高制作成本模式。")])

rec("rf-comparison", None, "peer-comparison", I, "comparison", "统一字段",
    "起点、第一批用户、收入证明与可学动作",
    "四家都面向在职知识工作者，但起点资产与收费结构不同：Reforge 自营高价 cohort，Lenny 低价订阅，Maven 平台抽成，Section 名人品牌转企业。",
    "相似度没有量化定义，用文字判断，不打分。",
    ["e-muas", "e-lenny-2020", "e-maven-a16z", "e-section-tc"], ["rf-transfer"],
    comparisonIds=["rf-profile", "lenny-profile", "maven-profile", "section-profile"],
    columns=["公司与阶段", "起点资产", "第一批用户", "最初产品", "收入证明", "扩张依赖", "与 Reforge 的资产差距", "当前可学动作"])

# =====================================================================
# Sections / topics / companies / coverage
# =====================================================================
proofs = ["rf-p-pay", "rf-p-outcome", "rf-p-retention", "rf-p-team", "rf-p-supply", "rf-p-tools", "rf-p-capital", "rf-p-learning-now"]
SRC = ["e-chargebee", "e-joining-miro"]


def sec(id, title, part, ov, thesis, conclusion, ev):
    return dict(id=id, title=title, part=part, overviewIds=ov, thesis=thesis, conclusion=conclusion, evidenceIds=ev)


sections = [
    sec("executive-summary", "执行结论", "verdict", ["rf-verdict", "rf-m-revenue", "rf-m-alumni", "rf-m-capital"] + proofs,
        "Reforge 证明了从业者愿为高阶 cohort 付高价，但没有证明年费会员能留住人，也没有证明 AI 工具能单独收费。",
        "下一步最有价值的证据是 2021–2024 年的续费数据；进入『数据核验』专题看收入序列、早期漏斗与判断更新。",
        ["e-chargebee", "e-balfour-21m", "e-joining-miro"]),
    sec("company-status", "现状（2026）", "assets", ["rf-status"],
        "Reforge 只剩学习品牌在独立运营，且其母公司 Miro 本身正被 Bending Spoons 收购，学习业务的前景比收购公告所说的更不确定。",
        "研究现状时以『被保留的附属品牌』看待 Reforge Learning；交割后需要复查。",
        ["e-joining-miro", "e-bending-spoons"]),
    sec("product-map", "产品盘点", "assets", ["rf-products"],
        "Reforge 的收费核心始终是年费会员与团队席位，内容库与 AI 工具都是为了解决『学了用不上、用完就走』。",
        "评价各产品时要分开收费、留存与战略价值三种作用；只有收费作用有公开证据。",
        ["e-pricing", "e-teams-2023", "e-changes-2023"]),
    sec("channel-map", "渠道盘点", "assets", ["rf-channels"],
        "早期获客几乎完全来自少数操盘手的个人信誉与写作，雇主预算负责付款；这让起步便宜，也让增长受专家供给与预算周期约束。",
        "借鉴者若没有可调用的个人信誉渠道，就不能复制 Reforge 的低成本获客。",
        ["e-muas", "e-expense"]),
    sec("asset-map", "起步资产", "assets", ["rf-assets"],
        "高价小批次能成立，靠的是信誉、受众、筛选与专家网络四项资产同时到位，缺任何一项都难成立。",
        "比较对标时先比这四项资产，而不是比课程形式。",
        ["e-muas", "e-amplitude-2016"]),
    sec("team-map", "团队与分工", "assets", ["rf-team"],
        "Reforge 的关键供给来自兼职的外部专家而非全职员工，转型期又靠收购补创业型人才，团队规模在 2024 年后降到几十人。",
        "外部专家的分成与投入是理解单位经济的关键缺口。",
        ["e-raise-21m", "e-chargebee", "e-promptled"]),
    sec("economics", "收入与资本", "assets", ["rf-economics", "rf-series-revenue"],
        "价格结构清楚，但决定盈利的续费率、讲师分成与获客成本都不透明，且收入只有两个自述数值。",
        "单位经济只能做情景分析；不能据此判断 Reforge 是否赚钱。",
        ["e-pricing", "e-chargebee"]),
    sec("own-origin", "自身路径", "assets", ["rf-origin-summary", "rf-s1", "rf-s2", "rf-s3", "rf-s4", "rf-s5", "rf-s6", "rf-s7"],
        "Reforge 先用最少资本证明高价付费，再用资本扩目录；2022 年后的每一步都在处理同一个问题：需求是阶段性的。",
        "最值得借鉴的是前两步；后五步更多是警示。四模块拆解见『自身路径分析』专题。",
        ["e-muas", "e-chargebee"]),
    sec("own-growth", "自身回路", "assets", ["rf-loop"],
        "获客回路（内容→申请→口碑→团队采购）有信号，留存回路（扩题→续费、工具→高频）没有闭合。",
        "Reforge 是强获客、弱留存的流程，不是已成立的飞轮。",
        ["e-muas", "e-chargebee"]),
    sec("historical-choices", "关键决策", "decisions", ["rf-d1", "rf-d2", "rf-d3", "rf-d4", "rf-d5"],
        "五个关键选择中，起步方式与融资扩题决定了后来的成本结构；之后三次调整都在补救需求节奏问题。",
        "复盘只能区分当时可知与事后结果，管理层的真实备选大多未知。",
        ["e-balfour-21m", "e-teams-2023", "e-joining-miro"]),
    sec("decline-diagnosis", "收缩诊断", "decisions", ["rf-decline"],
        "在『2022 年后需求收缩是行业普遍现象』的前提下，宏观是触发、阶段性需求是放大，竞争替代证据最弱。",
        "续费数据能直接改写排序；拿不到时保持暂定，不估算贡献比例。",
        ["e-layoff-2022", "e-chargebee"]),
    sec("transfer-order", "借鉴顺序", "choices", ["rf-transfer"],
        "Reforge 最可迁移的是起步验证法，最不该照搬的是融资后扩题与年费会员假设。",
        "分类以读者已有写作受众或专家关系为前提；用途确认后会重排。",
        ["e-muas", "e-chargebee"]),
    sec("next-investigation", "下一步调查", "validation", ["rf-investigation", "rf-question", "rf-contract"],
        "目前最大的未知是续费与会员规模；有了它才能区分『需求阶段性』与『竞争分流』哪个更重要。",
        "拿不到内部数据时保留缺口与代理证据的边界；用户回答后改写借鉴顺序与诊断。",
        ["e-chargebee", "e-supra"]),
    sec("featured-benchmark", "重点案例：Lenny", "paths",
        ["lenny-verdict", "lenny-assets", "lenny-s1", "lenny-s2", "lenny-s3", "lenny-s4", "lenny-s5", "lenny-s6", "lenny-tradeoff", "lenny-loop", "lenny-transfer"],
        "Lenny 与 Reforge 起点资产最接近（操盘手写作受众），却选了低价订阅与免费播客，正好用来检验『阶段性需求』是否可以靠低价高频绕开。",
        "选 Lenny 而不选 Maven 作为重点，是因为它与 Reforge 的起点相同、收费结构相反；这不证明低价订阅更好，只说明它避开了 Reforge 的流失原因。",
        ["e-lenny-2020", "e-lenny-fr"]),
    sec("peer-comparison", "横向对照", "paths", ["rf-comparison"],
        "四家面对同一批在职学习者，差别在谁承担内容成本、谁付款、需求是否高频。",
        "Maven 与 Section 的逐家拆解见『横向对照详解』专题；它们分别检验平台化与转企业两条路线。",
        ["e-maven-a16z", "e-section-tc"]),
]


def mod(id, title, ids, thesis, conclusion):
    return dict(id=id, title=title, thesis=thesis, conclusion=conclusion, recordIds=ids)


topics = [
    dict(id="audit", title="数据核验", parentSectionId="executive-summary", verdictId="rf-verdict",
         argument=["口径与自报边界", "收入与项目序列", "早期漏斗", "证明状态", "判断更新"],
         modules=[
             mod("audit-scope", "01 口径与自报边界", ["rf-m-revenue", "rf-m-alumni", "rf-m-capital"],
                 "三个首屏数字分别是自述收入、累计学员与融资额，没有一个能说明当前经营状况。",
                 "不能把累计学员当会员，也不能把融资当收入。"),
             mod("audit-series", "02 收入与项目序列", ["rf-series-revenue", "rf-series-programs"],
                 "收入只有两个数值点，项目数在 2022 年达到顶峰，二者同步上升但无法分辨新题贡献。",
                 "2023 年后口径改变与缺失并存，不能画成连续趋势。"),
             mod("audit-funnel", "03 早期漏斗", ["rf-funnel-first"],
                 "首期唯一可靠的数字是约 1,000 份申请，付款与完课都缺失。",
                 "申请数只能证明兴趣，不能证明付款。"),
             mod("audit-proof", "04 证明状态", proofs,
                 "付费已证明，续费有反证，工具与资本回报未证明。",
                 "下一轮优先补续费数据。"),
             mod("audit-change", "05 判断更新", ["rf-change-status", "rf-change-maven", "rf-change-decline", "rf-contract"],
                 "研究过程中有三次判断变更，都来自新公开资料而非用户回答。",
                 "变更已写入首屏、现状、诊断与借鉴顺序。")]),
    dict(id="origin", title="自身路径分析", parentSectionId="own-origin", verdictId="rf-verdict",
         argument=["互补起点资产", "首次交易与交付", "取舍与反模式", "回路与迁移"],
         modules=[
             mod("origin-assets", "01 互补起点资产", ["rf-assets", "rf-team"],
                 "信誉、受众、筛选与专家网络同时到位，使高价小批次在没有资本时成立。",
                 "工程与企业销售是后补的，转型时成为瓶颈。"),
             mod("origin-validation", "02 首次交易与交付验证", ["rf-s1", "rf-s2", "rf-s3"],
                 "首期靠申请筛选与改版建立口碑，再用专家共建扩目录；付款细节未公开。",
                 "首次交易的价格与人数是最大的早期缺口。"),
             mod("origin-tradeoffs", "03 取舍与反模式", ["rf-tradeoff"],
                 "已证实的取舍只有三项；『续费前不扩题』是事后建议。",
                 "不从沉默推断管理层的克制。"),
             mod("origin-transfer", "04 回路与迁移", ["rf-loop", "rf-transfer"],
                 "获客回路可迁移，留存回路未闭合，因此只迁移起步方法。",
                 "迁移前先确认自己有可调用的信誉与受众。")]),
    dict(id="decision", title="历史决策复盘", parentSectionId="historical-choices", verdictId="rf-verdict",
         argument=["起步方式", "融资扩题", "重组与转工具", "退出", "收缩解释"],
         modules=[
             mod("history-start", "01 起步与融资", ["rf-d1", "rf-d2"],
                 "起步方式让付费成立，融资扩题让成本结构变重。",
                 "两者的时点都合理，问题在于没有先证明续费。"),
             mod("history-restructure", "02 重组与转工具", ["rf-d3", "rf-d4"],
                 "两次调整都针对需求节奏，第二次直接换了产品形态。",
                 "公开资料不足以评估调整效果。"),
             mod("history-exit", "03 退出", ["rf-d5"],
                 "出售给 Miro 兑现了工具与人才价值，但学习业务的前景随之不确定。",
                 "对价未知，无法评估资本回报。"),
             mod("history-decline", "04 收缩解释与反证", ["rf-decline"],
                 "环境、竞争与自身回路三类解释并存，排序依赖未核实的前提。",
                 "调查优先级来自能区分解释的证据。")]),
    dict(id="comparisons", title="横向对照详解", parentSectionId="peer-comparison", verdictId="rf-verdict",
         argument=["统一维度", "Lenny：低价订阅", "Maven：平台抽成", "Section：转企业"],
         modules=[
             mod("cmp-matrix", "01 统一矩阵", ["rf-comparison", "rf-profile"],
                 "四家对内容成本、付款人与使用频率做了不同取舍。",
                 "形式相似（都是课程或内容）不代表资产相同。"),
             mod("cmp-lenny", "02 Lenny's Newsletter", ["lenny-verdict", "lenny-profile", "lenny-s1", "lenny-s3", "lenny-s6", "lenny-loop", "lenny-transfer"],
                 "同样的起点资产，低价高频的收费结构避开了阶段性需求。",
                 "只适用于有持续个人写作能力的读者。"),
             mod("cmp-maven", "03 Maven", ["maven-verdict", "maven-profile", "maven-s1", "maven-s2", "maven-s3", "maven-loop", "maven-transfer"],
                 "平台抽成把内容成本转给讲师，下行期仍增长，但供给质量需要主动管理。",
                 "适合有招生流量、不想承担内容成本的团队。"),
             mod("cmp-section", "04 Section", ["section-verdict", "section-profile", "section-s1", "section-s2", "section-s3", "section-loop", "section-transfer"],
                 "与 Reforge 同期收缩、同样转企业与 AI，是环境解释的旁证。",
                 "时间相似不证明原因相同。")])]

companies = [
    dict(id="reforge", name="Reforge", period="2015–2026（截至 2026-10-03）"),
    dict(id="lenny", name="Lenny's Newsletter", period="2019–2026",
         case=dict(parentSectionId="featured-benchmark", verdictId="lenny-verdict",
                   argument=["互补起点资产", "首次交易与交付", "取舍与反模式", "回路与迁移"],
                   modules=[
                       mod("lenny-m-assets", "01 互补起点资产", ["lenny-assets", "lenny-profile"],
                           "一个人的操盘经验＋Substack 平台，固定成本极低，这是能用低价的前提。",
                           "没有平台与个人写作能力就无法照搬。"),
                       mod("lenny-m-first", "02 首次交易与交付验证", ["lenny-s1", "lenny-s2", "lenny-s3"],
                           "10 个月免费问答相当于人工需求调研，付费上线首两天即有约 200 人付款。",
                           "早期转化约 3%（同期口径），当前转化未知。"),
                       mod("lenny-m-tradeoffs", "03 取舍与反模式", ["lenny-tradeoff"],
                           "不雇全职、不投广告、拒绝大多数合作，是当事人公开说明的取舍。",
                           "这些取舍的机会成本无法从公开资料评估。"),
                       mod("lenny-m-loop", "04 回路与迁移", ["lenny-s4", "lenny-s5", "lenny-s6", "lenny-loop", "lenny-transfer"],
                           "免费播客扩受众、捆绑提高付费价值；回路后半段缺续费数据。",
                           "可迁移『免费建受众＋低价可报销』，不可迁移个人品牌规模。")])),
    dict(id="maven", name="Maven", period="2020–2025"),
    dict(id="section", name="Section（原 Section4）", period="2019–2026"),
]

ALL_PROOF_REFS = proofs
coverage = [
    dict(item="任务与证明状态", status="部分完成",
         recordIds=["rf-verdict"] + proofs,
         gap="用户未说明用途，按外部研究处理并已提问；8 个命题中只有付费已证明，其余因 2023 年后无公开数据停在有信号／反证／未证明。"),
    dict(item="业务、团队与分工", status="部分完成",
         recordIds=["rf-products", "rf-channels", "rf-assets", "rf-team", "rf-economics"],
         gap="产品、渠道与团队只有公开片段：讲师分成、个人投入时长、渠道归因、各产品收入占比均未公开；团队规模来自不同时间的口述。"),
    dict(item="每家对标", status="部分完成",
         recordIds=["rf-comparison", "lenny-profile", "maven-profile", "section-profile", "maven-loop", "section-loop", "maven-transfer", "section-transfer"],
         gap="三家均按统一结构拆解，但 Lenny 付费数与收入未公开，Maven 讲师留存改善来自二手整理，Section 无收入；均无内部资料。"),
    dict(item="重点案例", status="部分完成",
         recordIds=["lenny-verdict", "lenny-assets", "lenny-s1", "lenny-s3", "lenny-tradeoff", "lenny-loop", "lenny-transfer"],
         gap="Lenny 四模块均有来源，但回路后半段（续费、捆绑效果）无数据；首次交易后的转化与续费缺失，迁移判断只能条件式。"),
    dict(item="数据核验", status="部分完成",
         recordIds=["rf-series-revenue", "rf-series-programs", "rf-funnel-first", "rf-m-revenue"],
         gap="无同批漏斗（首期只有申请数）；收入序列口径不明且 $30M 的时期有冲突；2023 年后收入、会员、续费全部缺失。"),
    dict(item="判断更新与下一轮记录", status="部分完成",
         recordIds=["rf-change-status", "rf-change-maven", "rf-change-decline", "rf-contract", "rf-question"],
         gap="三次判断变更来自研究过程中的新公开资料，尚无用户回答；数据合同只能约定外部可得代理与缺口，无内部字段可复算。"),
    dict(item="自有业务决策", status="不适用", recordIds=[],
         gap="用户没有说明代表 Reforge 或自有业务，本次按外部研究处理，不虚构经营授权；若用户回答用途为自有业务，需要补主路线、四道门槛与会议摘要。"),
    dict(item="外部公司决策", status="部分完成",
         recordIds=["rf-d1", "rf-d2", "rf-d3", "rf-d4", "rf-d5", "rf-transfer", "rf-investigation"],
         gap="五个关键选择都有时点与结果，但管理层当时的备选与理由大多未公开，备选多为研究者构造；结果与选择之间的因果未证。"),
    dict(item="增长放缓或衰退", status="部分完成",
         recordIds=["rf-decline", "rf-d2", "rf-d4", "section-verdict"],
         gap="三类解释都有支持与反证，但没有收入或续费时间序列；排序为依赖前提的暂定排序，调查顺序已给出。"),
    dict(item="可交付性", status="部分完成", recordIds=[],
         gap="PLACEHOLDER"),
]

meta = dict(
    taskType="external-company",
    title="Reforge：从增长课程到并入 Miro",
    question="Reforge 如何靠从业者专家课程起步并做到数千万美元收入？2022 年后为何收缩、转做 AI 工具并被 Miro 收购？哪些机制在什么条件下值得借鉴？",
    asOf="2026-10-03",
    scope="研究对象 Reforge（2015–2026，含 Reforge Learning 与 2024–2026 的 AI 工具线）；对标 Lenny's Newsletter（重点案例）、Maven、Section。只用公开资料，没有任何内部记录。",
    notice="外部公司研究，不代表 Reforge 或任何对标公司，也不替它们安排经营。关键收入与团队数字多为创始人自述或二手转述、未经审计；2023 年后收入、会员数、续费率均未公开。用户用途未确认，借鉴建议均为条件式。",
    verdictId="rf-verdict",
    keyMetricIds=["rf-m-revenue", "rf-m-alumni", "rf-m-capital"],
    subjectCompanyId="reforge",
    actionSectionId="next-investigation")


def build(deliverability_gap):
    coverage[-1]["gap"] = deliverability_gap
    return dict(meta=meta, companies=companies, sections=sections, topics=topics,
                records=records, evidence=EVIDENCE, coverage=coverage)


if __name__ == "__main__":
    import sys
    gap = sys.argv[1] if len(sys.argv) > 1 else (
        "已通过 Draft 7 Schema 与语义检查并导出单文件；浏览器验收结果见交付说明。研究内容的完成度以上方九项为准，不因页面可用而视为完成。")
    data = build(gap)
    (HERE / "research.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("records", len(records), "evidence", len(EVIDENCE), "sections", len(sections), "topics", len(topics))
