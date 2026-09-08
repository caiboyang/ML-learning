#!/usr/bin/env python3
"""检查学习页里**实际展示的代码**能不能编译、能不能跑出正确结果。

    python3 quantitative-trading/check_page_code.py

为什么需要这个：这份材料里同一段算法会出现在主线和 deep dive 两处，
而且页面上的代码是带 HTML 高亮标签的字符串 —— 改动时既不会被语法检查
覆盖，也很容易只改一处。本脚本把代码从 HTML 里抽回来，做两件事：

  1. 对每个 Python 代码块做 compile()，抓语法错误；
  2. 把主线的选股片段真正执行一遍，在 N = 2/3/7/10/100 上断言
     多空只数相同、净敞口 0、总敞口 1。

历史上这两项各抓到过一个真实缺陷：顶层示例里出现 return，
以及分位阈值导致 10 只标的时选出「1 多 0 空」的纯多头仓位。
"""
import html
import os
import re
import sys

class Series:
    def __init__(self, data, index=None):
        if isinstance(data, dict):
            self.index = list(data); self.v = dict(data)
        elif isinstance(data, (int, float)):
            self.index = list(index); self.v = {k: float(data) for k in self.index}
        else:
            self.index = list(index); self.v = {k: float(x) for k, x in zip(self.index, data)}
    def dropna(self):
        keep = [k for k in self.index if self.v[k] == self.v[k]]
        return Series([self.v[k] for k in keep], index=keep)
    def sort_values(self):
        keep = sorted(self.index, key=lambda k: self.v[k])
        return Series([self.v[k] for k in keep], index=keep)
    def __len__(self): return len(self.index)
    def __setitem__(self, key, val):
        keys = key if isinstance(key, list) else [key]
        for k in keys: self.v[k] = float(val)
    def __getitem__(self, key): return self.v[key]
    def abs(self): return Series([abs(self.v[k]) for k in self.index], index=self.index)
    def sum(self): return sum(self.v[k] for k in self.index)
    def tolist(self): return [self.v[k] for k in self.index]

class PD:
    Series = staticmethod(lambda data, index=None: Series(data, index))

def extract_selection(path):
    s = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<pre><code>(.*?)</code></pre>', s, re.S):
        body = html.unescape(re.sub(r'</?span[^>]*>', '', m.group(1)))
        if 'valid = score.dropna()' in body:
            i = body.index('valid = score.dropna()')
            j = body.index('# ⑤') if '# ⑤' in body else len(body)
            return body[i:j]
    raise SystemExit('未找到选股片段')

ROOT = os.path.dirname(os.path.abspath(__file__))


def compile_all(paths):
    bad = 0
    for path in paths:
        s = open(path, encoding='utf-8').read()
        for m in re.finditer(r'<pre><code>(.*?)</code></pre>', s, re.S):
            body = html.unescape(re.sub(r'</?span[^>]*>', '', m.group(1)))
            line = s[:m.start()].count('\n') + 1
            if body.lstrip().startswith('python3 '):
                continue
            rel = os.path.relpath(path, ROOT)
            try:
                compile(body, f'{rel}:{line}', 'exec')
                print(f'  OK    {rel}:{line}')
            except SyntaxError as e:
                bad += 1
                print(f'  FAIL  {rel}:{line} -> {e.msg}（块内第 {e.lineno} 行）')
    return bad


PAGES = [os.path.join(ROOT, 'learn', p) for p in
         ('index.html', 'algorithms/index.html', 'validation/index.html', 'library/index.html')]

print('=== 1. 编译页面上的每个代码块 ===')
failures = compile_all(PAGES)

print('\n=== 2. 执行主线的选股片段 ===')
snippet = extract_selection(os.path.join(ROOT, 'learn', 'index.html'))
print('--- 从 HTML 抽出的实际展示代码 ---')
print(snippet.rstrip())
print('--- 执行结果 ---')
fail = 0
for N in (10, 100, 7, 3, 2):
    universe = [f'S{i}' for i in range(N)]
    score = Series([float(i) for i in range(N)], index=universe)   # 无并列
    ns = {'pd': PD, 'score': score, 'universe': universe, 'max': max, 'int': int,
          'round': round, 'len': len}
    exec(snippet, ns)
    w = ns['w']
    net, gross = w.sum(), w.abs().sum()
    nl = sum(1 for k in w.index if w[k] > 0); nsh = sum(1 for k in w.index if w[k] < 0)
    ok = abs(net) < 1e-12 and (abs(gross - 1.0) < 1e-12 or gross == 0.0) and nl == nsh
    fail += (not ok)
    print(f'  N={N:3d} → 多头 {nl} 只，空头 {nsh} 只 | 净敞口 {net:+.12f} | 总敞口 {gross:.12f} | {"OK" if ok else "FAIL"}')
failures += fail
print()
if failures:
    raise SystemExit(f'{failures} 项检查未通过')
print('全部通过。')
