"""Clubhouse test data → round-7 rules: coverage[] and a key benchmark case. argv: in out [--no-case]"""
import json, sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
with_case = "--no-case" not in sys.argv

def cov(item, status, ids, gap=""):
    return dict(item=item, status=status, recordIds=ids, gap=gap)

if with_case:
    def step(i, stage, title, action, result, mech, evs, lim):
        d["records"].append(dict(id=i, companyId="stage", section="key-case", kind="inference", role="step", status="时间与证据分列",
            title=title, text=action, limitation=lim, evidenceIds=evs, relatedIds=[], stage=stage,
            fields=[{"label": "动作", "value": action}, {"label": "结果", "value": result}, {"label": "机制判断", "value": mech, "kind": "inference"}]))
    d["records"].append(dict(id="kc-verdict", companyId="stage", section="key-case", kind="inference", role="judgment", status="研究者判断",
        title="Discord 把语音舞台放在常回来的社区里，砍掉了陌生人广场",
        text="同一种形式，Discord 先放进已有服务器，再试跨社区的公开发现；发现半年后关闭，社区内的 Stage 保留。它走的正是 Clubhouse 借鉴顺序里的“先密度、后扩张”。",
        limitation="Discord 只公布了累计和月度社区数，没有同批留存。", evidenceIds=["e-stage", "e-stage-end"], relatedIds=["transfer-order"]))
    step("kc-s1", "2021-03", "01 先放进已有社区", "在服务器里推出 Stage 语音舞台。", "由服务器管理员和成员使用，不需要重新找人。",
         "已有成员关系解决了“凑不齐人”。", ["e-stage"], "推出时的使用量未公开。")
    step("kc-s2", "2021-06", "02 试跨社区的公开发现", "在几个国家试点 Stage Discovery，让人发现别的社区的活动。", "试点规模未公开。",
         "这是 Clubhouse 式的陌生人广场。", ["e-stage"], "试点细节有限。")
    step("kc-s3", "2021-10", "03 关掉广场，留下社区", "关闭 Stage Discovery，继续投入社区内的 Stage。", "近百万社区用过 Stage，每月数十万社区办语音活动。",
         "社区内能留下，公开发现不值得继续投入。", ["e-stage-end"], "关闭理由是公司表述。")
    d["records"].append(dict(id="kc-tradeoff", companyId="stage", section="key-case", kind="inference", role="tradeoff", status="已证实取舍",
        title="取舍：放弃公开发现，保留社区内舞台", text="已证实：公司公告关闭发现、继续投入 Stage。分析：放弃了“像 Clubhouse 一样做公开广场”的机会。",
        limitation="放弃的机会成本没有数据。", evidenceIds=["e-stage-end"], relatedIds=[]))
    d["records"].append(dict(id="kc-loop", companyId="stage", section="key-case", kind="inference", role="loop", status="研究者判断",
        title="回路：活动让社区更常回来，社区让活动有人来", text="两条边都在社区内部闭合。", limitation="没有边级数据。", evidenceIds=["e-stage-end"], relatedIds=[],
        edges=[{"from": "已有社区成员", "to": "语音活动有人参加", "mechanism": "成员本来就常回来", "status": "有信号（每月数十万社区办活动）", "evidenceIds": ["e-stage-end"]},
               {"from": "语音活动", "to": "社区更活跃", "mechanism": "固定活动给回来的理由", "status": "推断", "evidenceIds": ["e-stage-end"]},
               {"from": "公开发现", "to": "新社区成员", "mechanism": "陌生人发现活动", "status": "反证：试点后关闭", "evidenceIds": ["e-stage-end"]}]))
    sec = dict(id="key-case", title="重点案例：Discord Stage", part="paths", overviewIds=["kc-verdict", "kc-s1", "kc-s2", "kc-s3", "kc-loop"],
               thesis="Discord 用同一种形式走对了顺序：先在常回来的社区里用，公开发现试了就收。",
               conclusion="选它做重点案例，是因为它最接近 Clubhouse 应走的借鉴顺序；Spaces 的起点（现成关注关系）别人借不到。",
               evidenceIds=["e-stage", "e-stage-end"])
    i = [s["id"] for s in d["sections"]].index("peers")
    d["sections"].insert(i, sec)
    for c in d["companies"]:
        if c["id"] == "stage":
            c["case"] = dict(parentSectionId="key-case", argument=["已有社区", "社区内交付", "砍掉广场", "回路与迁移"], verdictId="kc-verdict", modules=[
                dict(id="kc-m1", title="01 互补起点资产", recordIds=["pf-stage", "kc-s1"], thesis="服务器和成员关系是现成的。", conclusion="Clubhouse 缺的正是这一块。"),
                dict(id="kc-m2", title="02 首次交付", recordIds=["kc-s2"], thesis="先社区内，再试广场。", conclusion="广场试点没有撑住。"),
                dict(id="kc-m3", title="03 取舍", recordIds=["kc-tradeoff", "kc-s3"], thesis="关掉发现，留下舞台。", conclusion="放弃规模叙事，换回访。"),
                dict(id="kc-m4", title="04 回路与迁移", recordIds=["kc-loop", "transfer-order"], thesis="回路在社区内闭合。", conclusion="可迁移的是“先密度、后扩张”。")])

case_ids = ["kc-verdict", "kc-s1", "kc-s2", "kc-s3"] if with_case else []
d["coverage"] = [
    cov("任务与证明状态", "有实质依据", ["verdict", "p-activation", "p-cohort", "p-revisit", "p-content", "p-creator", "p-monetize"]),
    cov("业务、团队与分工", "部分完成", ["a-products", "a-channels", "team"], "内部分工、每人投入未公开；只写到两位创始人的对外角色。"),
    cov("每家对标", "部分完成", ["cmp-matrix", "pf-spaces", "pf-stage", "pf-greenroom", "pf-houseparty"], "四家只有档案和一个关键动作，没有逐家完整的起点—动作—反馈—迁移拆解。"),
    cov("重点案例", "有实质依据", case_ids) if with_case else
    cov("重点案例", "关键缺口", [], "本版按 --no-case 生成，未收录重点案例：缺少逐步动作、结果、取舍和反馈回路的四模块拆解。"),
    cov("数据核验", "部分完成", ["ser-installs", "ser-wau", "m-wau", "m-installs"], "同批留存从未公开；周活只有两个公司口径的点。"),
    cov("判断更新与下一轮记录", "部分完成", ["data-needs"], "本次没有新证据触发判断更新，没有 change 记录。"),
    cov("自有业务决策", "不适用", [], "外部公司研究，不替 Clubhouse 制定路线。"),
    cov("外部公司决策", "有实质依据", ["dec-slow", "dec-scale", "dec-open", "dec-reset", "transfer-order", "next-plan"]),
    cov("增长放缓或衰退", "有实质依据", ["dx"]),
    cov("可交付性", "有实质依据", []),
]
json.dump(d, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", "with case" if with_case else "no case")
