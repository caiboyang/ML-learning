#!/usr/bin/env python3
"""
截面动量最小实验 —— 只验证「回测流程」，不复现任何论文。

    python3 quantitative-trading/lab_momentum.py            # 数据里没有动量
    python3 quantitative-trading/lab_momentum.py --signal   # 数据里有动量
    python3 quantitative-trading/lab_momentum.py --help

为什么默认「没有动量」？
    因为一个诚实的回测框架，在无信号的数据上必须交出接近零的结果。
    先看到它交白卷，你才有理由相信它在 --signal 模式下给出的正收益。
    这就是学习页第 09 步说的「破坏性检验」，只是把顺序倒过来做。

依赖：Python 3.8+ 标准库。无需第三方包、账户或网络。
数据：固定种子的合成收益，**不是市场数据**；任何结果都不能当作真实业绩证据。

时间口径（全程只有这一套，写死在 decide() 里）：
    决策时点  月 m 收盘
    形成窗口  月 m-11 … m-1（共 11 个月）
    跳过      月 m —— 12-2 惯例，规避短期反转
    持有      月 m+1，赚取该月收益
    成本      在 m+1 建仓时按 |Δw| 扣，先扣后计收益
注意：跳过最近一个月是后续文献的标准化惯例，不是 Jegadeesh-Titman (1993)
      原文的算法（原文在形成期与持有期之间跳过的是一周）。
"""

import argparse
import math
import random

N_ASSETS = 12
N_MONTHS = 240
FORMATION = 11      # 形成窗口长度（月）
SKIP = 1            # 跳过最近几个月
TOP_FRAC = 0.25     # 多头/空头各取的比例
SEED = 20260907


# --------------------------------------------------------------------------
# 1. 合成数据
# --------------------------------------------------------------------------
def make_returns(n_assets, n_months, seed, with_momentum):
    """返回 rets[m][i]：第 m 月、第 i 个资产的简单收益。

    with_momentum=False：每个资产是独立随机游走 + 一个共同市场因子。
                         结构上不存在任何可被动量捕捉的东西。
    with_momentum=True ：给每个资产一个缓慢漂移的「趋势状态」，
                         使过去收益对未来收益有微弱正相关。
    """
    rng = random.Random(seed)
    drift = [0.0] * n_assets
    rets = []
    for _ in range(n_months):
        market = rng.gauss(0.0, 0.035)                 # 共同因子：谁都躲不掉
        row = []
        for i in range(n_assets):
            if with_momentum:
                # 趋势状态本身是缓慢均值回复的 AR(1)，制造可持续数月的方向
                drift[i] = 0.94 * drift[i] + rng.gauss(0.0, 0.0022)
            row.append(market + drift[i] + rng.gauss(0.0, 0.055))
        rets.append(row)
    return rets


# --------------------------------------------------------------------------
# 2. 决策：只允许看见 m 以前的数据
# --------------------------------------------------------------------------
def decide(rets, m, n_assets):
    """在月 m 收盘做决策，返回目标权重 w[i]（多空各半，总敞口 1）。

    只读取 rets[m-FORMATION-SKIP+1 : m-SKIP+1]，即月 m-11 … m-1。
    **rets[m] 及以后一律不读** —— 这条是整个实验的核心不变量。
    """
    lo = m - FORMATION - SKIP + 1
    hi = m - SKIP + 1                                   # 右端不含，故最后一个月是 m-1
    if lo < 0:
        return [0.0] * n_assets

    scores = []
    for i in range(n_assets):
        window = [rets[t][i] for t in range(lo, hi)]
        # 简单收益要复利，不能直接求和
        cum = 1.0
        for r in window:
            cum *= (1.0 + r)
        cum -= 1.0
        # 同窗口的波动率，做风险调整；每个资产收敛成一个数
        mean = sum(window) / len(window)
        var = sum((r - mean) ** 2 for r in window) / (len(window) - 1)
        sigma = math.sqrt(var)
        scores.append(cum / sigma if sigma > 1e-12 else 0.0)

    k = max(1, int(round(n_assets * TOP_FRAC)))
    order = sorted(range(n_assets), key=lambda i: scores[i])
    w = [0.0] * n_assets
    for i in order[-k:]:
        w[i] = +0.5 / k                                 # 多头腿合计 +0.5
    for i in order[:k]:
        w[i] = -0.5 / k                                 # 空头腿合计 −0.5
    return w


# --------------------------------------------------------------------------
# 3. 回测
# --------------------------------------------------------------------------
def drift(w, r):
    """持有一期之后，权重会被价格推走。返回下一期交易前的实际权重。

    组合收益 r_p = Σ w_i r_i；仓位 i 的价值变成 w_i(1+r_i)，NAV 变成 (1+r_p)。
    所以交易前权重 = w_i(1+r_i) / (1+r_p)。
    **即使目标权重一模一样，回到目标也需要交易** —— 漏掉这一段会低估换手。
    """
    rp = sum(w[i] * r[i] for i in range(len(w)))
    denom = 1.0 + rp
    if abs(denom) < 1e-9:                      # NAV 归零，退化处理
        return [0.0] * len(w)
    return [w[i] * (1.0 + r[i]) / denom for i in range(len(w))]


def backtest(rets, cost_bp, invert=False):
    """按前面的时间口径跑一遍，返回每月净收益序列。

    invert=True 时把目标权重整体取反，用于自检 (e)。
    换手按「新目标 − 漂移后的交易前权重」计算，而不是「新目标 − 上期目标」。
    """
    n_months, n_assets = len(rets), len(rets[0])
    held = [0.0] * n_assets                    # 交易前的实际权重
    monthly = []
    for m in range(n_months - 1):
        w = decide(rets, m, n_assets)
        if invert:
            w = [-x for x in w]
        turnover = sum(abs(w[i] - held[i]) for i in range(n_assets))
        cost = turnover * cost_bp / 10_000.0
        gross = sum(w[i] * rets[m + 1][i] for i in range(n_assets))   # 赚 m+1 的收益
        monthly.append(gross - cost)
        held = drift(w, rets[m + 1])           # 下一期开盘前，权重已经漂走了
    return monthly


def backtest_gross(rets, invert=False):
    """零成本的逐期毛收益，用于自检 (e) 的反号不变量。"""
    n_months, n_assets = len(rets), len(rets[0])
    out = []
    for m in range(n_months - 1):
        w = decide(rets, m, n_assets)
        if invert:
            w = [-x for x in w]
        out.append(sum(w[i] * rets[m + 1][i] for i in range(n_assets)))
    return out


def buy_and_hold(rets, cost_bp):
    """**真正的**买入持有：第一个月等权建仓，之后权重随价格自由漂移，不再交易。

    注意区别：每月都用固定 1/N 权重算收益，等于每月再平衡回等权，
    那是另一个策略（而且会漏收再平衡成本）。两者结果可以差很多。
    """
    n_months, n_assets = len(rets), len(rets[0])
    value = [1.0 / n_assets] * n_assets        # 建仓后各仓位的价值
    nav = 1.0 - (1.0 * cost_bp / 10_000.0)     # 建仓换手 = 1.0，只在这里收一次成本
    value = [v * nav for v in value]
    monthly = []
    for m in range(n_months - 1):
        prev = sum(value)
        value = [value[i] * (1.0 + rets[m + 1][i]) for i in range(n_assets)]
        monthly.append(sum(value) / prev - 1.0 if prev else 0.0)
        if m == 0:                             # 把建仓成本折进第一期收益
            monthly[0] = sum(value) / 1.0 - 1.0
    return monthly


# --------------------------------------------------------------------------
# 4. 指标
# --------------------------------------------------------------------------
def equity(monthly):
    nav, curve = 1.0, [1.0]
    for r in monthly:
        nav *= (1.0 + r)
        curve.append(nav)
    return curve


def stats(monthly):
    curve = equity(monthly)
    n = len(monthly)
    total = curve[-1] - 1.0
    cagr = curve[-1] ** (12.0 / n) - 1.0 if n else 0.0
    mean = sum(monthly) / n
    var = sum((r - mean) ** 2 for r in monthly) / (n - 1) if n > 1 else 0.0
    sd = math.sqrt(var)
    sharpe = (mean / sd) * math.sqrt(12) if sd > 1e-12 else 0.0   # 无风险利率设为 0
    peak, mdd = curve[0], 0.0
    for v in curve:
        peak = max(peak, v)
        mdd = max(mdd, 1.0 - v / peak)
    return {"total": total, "cagr": cagr, "sharpe": sharpe, "mdd": mdd, "curve": curve}


def hist(values, bins=11, width=46):
    """Sharpe 分布的横向直方图。零线用 | 标出。"""
    lo, hi = min(values), max(values)
    if hi - lo < 1e-9:
        hi = lo + 1e-9
    edges = [lo + (hi - lo) * i / bins for i in range(bins + 1)]
    counts = [0] * bins
    for v in values:
        k = min(bins - 1, int((v - lo) / (hi - lo) * bins))
        counts[k] += 1
    top = max(counts) or 1
    rows = []
    for i in range(bins):
        mid = (edges[i] + edges[i + 1]) / 2
        bar = "#" * int(round(counts[i] / top * width))
        mark = " <- 0" if edges[i] <= 0 < edges[i + 1] else ""
        rows.append(f"  {mid:+5.2f} |{bar}{mark}")
    return "\n".join(rows)


def spark(curve, width=64, height=9):
    """无第三方库的净值图。纵轴是净值，横轴是时间。"""
    lo, hi = min(curve), max(curve)
    if hi - lo < 1e-9:
        hi = lo + 1e-9
    step = max(1, len(curve) // width)
    pts = curve[::step]
    rows = []
    for h in range(height - 1, -1, -1):
        band_hi = lo + (hi - lo) * (h + 1) / height
        band_lo = lo + (hi - lo) * h / height
        line = "".join("█" if band_lo <= v < band_hi or (h == height - 1 and v >= band_hi)
                       else " " for v in pts)
        label = f"{band_lo:5.2f} |"
        rows.append(label + line)
    rows.append("      +" + "-" * len(pts))
    return "\n".join(rows)


# --------------------------------------------------------------------------
# 5. 手算断言：这些必须过，否则回测框架本身是坏的
# --------------------------------------------------------------------------
def self_checks(rets):
    n_assets = len(rets[0])
    checks = []

    # (a) 未来数据不能影响过去决策
    m = 60
    w_before = decide(rets, m, n_assets)
    tampered = [row[:] for row in rets]
    rng = random.Random(999)
    for t in range(m, len(tampered)):                    # 把 m 及以后全部改掉
        tampered[t] = [rng.gauss(0, 0.2) for _ in range(n_assets)]
    w_after = decide(tampered, m, n_assets)
    ok = all(abs(a - b) < 1e-12 for a, b in zip(w_before, w_after))
    checks.append(("改掉月 60 及以后的全部数据，月 60 的决策不变（无未来函数）", ok))

    # (b) 权重是资产维度、多空对冲、总敞口为 1；两端选取数量相同
    w = decide(rets, 120, n_assets)
    n_long = sum(1 for x in w if x > 0)
    n_short = sum(1 for x in w if x < 0)
    ok = (len(w) == n_assets
          and abs(sum(w)) < 1e-12
          and abs(sum(abs(x) for x in w) - 1.0) < 1e-12
          and n_long == n_short)
    checks.append((f"权重长度=资产数，净敞口=0，总敞口=1，多头 {n_long} 只 = 空头 {n_short} 只", ok))

    # (c) 成本越高，净结果不可能越好
    r0 = stats(backtest(rets, 0))["total"]
    r10 = stats(backtest(rets, 10))["total"]
    r30 = stats(backtest(rets, 30))["total"]
    ok = r0 >= r10 - 1e-12 >= r30 - 2e-12
    checks.append((f"成本单调性 0bp {r0:+.2%} ≥ 10bp {r10:+.2%} ≥ 30bp {r30:+.2%}", ok))

    # (d) 把收益按时间打乱，动量结构被破坏，策略应显著退化
    shuffled = [row[:] for row in rets]
    random.Random(7).shuffle(shuffled)
    r_shuf = stats(backtest(shuffled, 0))["sharpe"]
    checks.append((f"打乱时间顺序后 Sharpe = {r_shuf:+.2f}（应接近 0）",
                   abs(r_shuf) < 0.75))

    # (e) 真正反转权重后重跑，零成本下**逐期毛收益**必须互为相反数。
    #     注意：复利总收益并不反号 —— [+10%,-10%] 与 [-10%,+10%] 都是 -1%，
    #     所以不能拿总收益做这个不变量。
    g_base = backtest_gross(rets, invert=False)
    g_flip = backtest_gross(rets, invert=True)
    worst = max((abs(a + b) for a, b in zip(g_base, g_flip)), default=0.0)
    checks.append((f"反转权重重跑，逐期毛收益互为相反数（最大偏差 {worst:.2e}）",
                   worst < 1e-12))

    # (f) 手算：真正的买入持有不会因为中途涨跌而凭空生出收益
    #     A 先 +100% 再 −50%、B 不动，各买一半 → 应当正好回到 0%
    hand = [[0.0, 0.0], [1.0, 0.0], [-0.5, 0.0]]
    bh = stats(buy_and_hold(hand, 0.0))["total"]
    checks.append((f"买入持有手算：A +100% 再 −50%、B 不动 → {bh:+.2%}（应为 0.00%）",
                   abs(bh) < 1e-12))

    # (g) 手算：目标权重不变、但价格动了，仍然需要再平衡交易
    w0 = [0.5, -0.5]
    drifted = drift(w0, [0.20, -0.10])
    need = sum(abs(w0[i] - drifted[i]) for i in range(2))
    checks.append((f"目标不变、价格变动仍产生换手 {need:.4f}（应 > 0）", need > 1e-6))

    return checks


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--signal", action="store_true",
                    help="在合成数据里注入真实动量（默认不注入）")
    ap.add_argument("--cost", type=float, default=10.0,
                    help="每单位换手的成本，单位 bp（默认 10）")
    ap.add_argument("--sweep", type=int, default=40,
                    help="用多少个随机种子重跑，观察结果分布（默认 40）")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    rets = make_returns(N_ASSETS, N_MONTHS, args.seed, args.signal)
    mode = "注入了动量" if args.signal else "没有动量（纯噪声 + 共同因子）"

    print("=" * 72)
    print(f"截面动量最小实验 · 合成数据 · {N_ASSETS} 个资产 × {N_MONTHS} 个月")
    print(f"数据模式：{mode}    成本：{args.cost:.0f} bp / 单位换手    种子：{args.seed}")
    print("=" * 72)

    print("\n【一】自检（框架坏了的话，下面的数字就没有意义）")
    all_ok = True
    for name, ok in self_checks(rets):
        all_ok &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print("\n【二】成本敏感性")
    print(f"  {'成本':>8} {'总收益':>10} {'年化':>9} {'Sharpe':>8} {'最大回撤':>10}")
    for c in (0.0, args.cost, args.cost * 3):
        s = stats(backtest(rets, c))
        print(f"  {c:6.0f}bp {s['total']:>10.2%} {s['cagr']:>9.2%} "
              f"{s['sharpe']:>8.2f} {s['mdd']:>10.2%}")

    print("\n【三】与同区间、同成本口径的买入持有基线对比")
    s_mom = stats(backtest(rets, args.cost))
    s_bh = stats(buy_and_hold(rets, args.cost))
    print(f"  {'策略':>10} {'总收益':>10} {'年化':>9} {'Sharpe':>8} {'最大回撤':>10}")
    print(f"  {'截面动量':>8} {s_mom['total']:>10.2%} {s_mom['cagr']:>9.2%} "
          f"{s_mom['sharpe']:>8.2f} {s_mom['mdd']:>10.2%}")
    print(f"  {'买入持有':>8} {s_bh['total']:>10.2%} {s_bh['cagr']:>9.2%} "
          f"{s_bh['sharpe']:>8.2f} {s_bh['mdd']:>10.2%}")

    print(f"\n【四】动量策略净值曲线（成本 {args.cost:.0f}bp）")
    print(spark(s_mom["curve"]))

    print(f"\n【五】换 {args.sweep} 个随机种子重跑 —— 单次结果到底说明了什么")

    def sweep(months):
        out = []
        for k in range(args.sweep):
            r_k = make_returns(N_ASSETS, months, args.seed + 1000 * (k + 1), args.signal)
            out.append(stats(backtest(r_k, args.cost))["sharpe"])
        return sorted(out)

    long_s = sweep(N_MONTHS)
    short_s = sweep(60)

    def line(tag, xs):
        n = len(xs)
        pos = sum(1 for x in xs if x > 0) / n
        return (f"  {tag:<14} 最差 {xs[0]:+.2f} | 中位 {xs[n // 2]:+.2f} | "
                f"最好 {xs[-1]:+.2f} | 为正的比例 {pos:.0%}")

    print(line(f"{N_MONTHS} 个月", long_s))
    print(line("60 个月", short_s))
    pct = 100 * sum(1 for x in long_s if x < s_mom["sharpe"]) // len(long_s)
    print(f"  本次单跑 Sharpe = {s_mom['sharpe']:+.2f}，在长样本分布里约第 {pct} 百分位")
    print(f"\n  长样本（{N_MONTHS} 个月）的 Sharpe 分布：")
    print(hist(long_s))
    print("\n  短样本（60 个月）的 Sharpe 分布 —— 注意横轴范围宽了多少：")
    print(hist(short_s))

    print("\n【六】怎么读这个结果")
    if not args.signal:
        best_l, best_s = long_s[-1], short_s[-1]
        print("  数据里**没有**任何动量结构，策略的真实期望收益是 0。")
        print(f"  但单跑做出了 {s_mom['total']:+.2%}，Sharpe {s_mom['sharpe']:+.2f}。这不是 bug，")
        print("  这就是噪声本来的样子 —— 【五】的两个分布是它的证据：")
        print(f"    · 真实 Sharpe = 0，长样本里最幸运的一个种子仍跑出 {best_l:+.2f}；")
        print(f"    · 样本缩到 60 个月，最幸运的种子跑到 {best_s:+.2f}，分布明显更宽。")
        print("  把「种子」换成「你调过的参数」，这就是学习页第 09 步那条")
        print("  「5 年数据 + 45 次尝试 = 一个假 Sharpe 1」的机制，在你自己的机器上重现。")
        print("  两条直接可用的推论：**样本越短，你越容易骗到自己**；")
        print("  **单次回测结果不是证据，分布才是**。")
        print("  下一步：加 --signal 再跑，看同一套代码能不能把真信号和这团噪声分开。")
    else:
        print("  数据里注入了真实动量，两个分布应该整体右移 —— 对照默认模式看差别。")
        print("  但请注意三件事：")
        print("  ① 合成数据的生成规则已知，这不构成任何样本外证据；")
        print("  ② 单个种子的结果没有意义，要看【五】的整个分布；")
        print("  ③ 你现在已经看过结果了 —— 再回去调参数，这段数据就变成开发集了。")
    print()
    if not all_ok:
        raise SystemExit("自检未全部通过，请勿相信上面的数字。")


if __name__ == "__main__":
    main()
