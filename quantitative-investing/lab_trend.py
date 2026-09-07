"""A synthetic, long/cash timing lab. Python standard library only.

Run from the repository root: python3 quantitative-investing/lab_trend.py
This is an accounting exercise, not a replication or investment performance test.
Signal after close d; fill at close d+1; first earn return from d+1 to d+2.
"""

import math
import random


def synthetic_prices():
    """A fixed artificial path, including trends and oscillation; not market data."""
    rng = random.Random(20260907)
    prices = [100.0]
    for day in range(630):
        if day < 210:
            drift = 0.0007
        elif day < 420:
            drift = 0.005 * math.sin(day * 0.7)
        else:
            drift = -0.0004
        prices.append(prices[-1] * math.exp(drift + rng.gauss(0, 0.009)))
    return prices


def signals(prices, lookback=20):
    """End-of-day decisions; the window includes only that close and earlier."""
    return [
        int(price > sum(prices[day - lookback + 1 : day + 1]) / lookback)
        if day >= lookback - 1 else 0
        for day, price in enumerate(prices)
    ]


def backtest(prices, decisions, start, stop, cost_bp):
    """Earn close[t-1] -> close[t] using decisions[t-2].

    Every subperiod starts with NAV 1 in cash. The first permitted fill occurs
    at close[start-1], from an already available decision at close[start-2].
    Pay proportional cost before that interval's return; cash earns zero.
    Liquidate at the final close, paying exit cost. Positions are always 0 or 1.
    Turnover is sum of one-way traded notional / contemporaneous NAV, incl. exit.
    """
    cost = cost_bp / 10000
    nav, peak, max_drawdown, held, turnover = 1.0, 1.0, 0.0, 0, 0.0
    path = [nav]
    for t in range(start, stop):
        target = decisions[t - 2] if t >= 2 else 0
        trade = abs(target - held)
        turnover += trade
        nav *= 1 - cost * trade
        peak = max(peak, nav)
        max_drawdown = max(max_drawdown, 1 - nav / peak)
        held = target
        nav *= 1 + held * (prices[t] / prices[t - 1] - 1)
        peak = max(peak, nav)
        max_drawdown = max(max_drawdown, 1 - nav / peak)
        path.append(nav)
    turnover += held
    nav *= 1 - cost * held
    max_drawdown = max(max_drawdown, 1 - nav / peak)
    path[-1] = nav
    return {"total": nav - 1, "drawdown": max_drawdown,
            "turnover": turnover, "nav": path}


def verify_accounting():
    """Small hand-computable examples test latency, costs, and return intervals."""
    prices = [100, 110, 120, 108, 108]
    decisions = signals(prices, 2)
    # First positive decision after close 1; fill close 2; first earn t=3 loss.
    result = backtest(prices, decisions, 1, len(prices), 0)
    assert result["nav"][:3] == [1.0, 1.0, 1.0]
    assert math.isclose(result["total"], -0.1, abs_tol=1e-12)
    assert math.isclose(result["drawdown"], 0.1, abs_tol=1e-12)
    # Flat market: one entry and one exit, at 1% per side => 0.99 squared.
    flat = backtest([100] * 5, [1] * 5, 2, 5, 100)
    assert math.isclose(1 + flat["total"], 0.99 ** 2, abs_tol=1e-12)
    assert flat["turnover"] == 2
    # Cash stays at 1; buy-and-hold captures exactly the chosen close interval.
    assert backtest(prices, [0] * 5, 2, 5, 100)["total"] == 0
    buy = backtest(prices, [1] * 5, 2, 5, 0)
    assert math.isclose(1 + buy["total"], prices[4] / prices[1], abs_tol=1e-12)


def main():
    verify_accounting()
    prices = synthetic_prices()
    fixed = signals(prices)
    buy_hold = [1] * len(prices)
    print("SYNTHETIC DATA — accounting lesson, not market or paper results")
    print("20-day SMA; long/cash; no leverage; zero cash return; costs per side.")
    print("After close d signal -> close d+1 fill -> d+1 to d+2 first return.")
    print("Each segment starts in cash; costs include initial entry/final exit.")
    print("First 420 generated returns: development; last 210: fixed-rule check.")
    print("No parameter search. The synthetic check is not real out-of-sample proof.")
    print("Hand-computable accounting checks: passed.\n")
    for name, start, stop in [("DEVELOPMENT (after warm-up)", 21, 421),
                              ("SYNTHETIC FIXED-RULE CHECK", 421, len(prices))]:
        print(name, "| close", start - 1, "to close", stop - 1)
        print(f"{'Rule':<26} {'Total':>9} {'Max DD':>9} {'1-way turnover':>15}")
        results = []
        for label, decisions, bp in [("Trend / 0 bp", fixed, 0),
                                     ("Trend / 10 bp", fixed, 10),
                                     ("Trend / 40 bp", fixed, 40),
                                     ("Buy-and-hold / 10 bp", buy_hold, 10)]:
            r = backtest(prices, decisions, start, stop, bp)
            print(f"{label:<26} {r['total']:>8.2%} {r['drawdown']:>8.2%} {r['turnover']:>14.1f}x")
            results.append(r)
        assert results[0]["total"] >= results[1]["total"] >= results[2]["total"]
        print()
    print("Try one change only. Record it; reused check data becomes development data.")


if __name__ == "__main__":
    main()
