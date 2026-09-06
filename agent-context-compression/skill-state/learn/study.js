'use strict';
// All charts are local SVG. No analytics, remote fonts, model calls, or CDN dependencies.
const PAPER = 'https://arxiv.org/html/2608.26263v3#';
const SERIES = [
  { name: 'ReAct', color: '#ffbc81', dash: '' },
  { name: 'Memory', color: '#c2a2fa', dash: '7 4' },
  { name: 'Stateful', color: '#8dbbff', dash: '2 4' },
  { name: 'SKILL.state', color: '#82edc3', dash: '' }
];
const PUBLIC_DATA = {
  ctf: { score: [43.2,46.4,41.8,54.2], prompt: [1909,1797,1946,813], tokens: [977000,1030000,1130000,387000], insight: 'CTF：54.2%，比最强对照 Memory 高 7.8 个百分点；累计 token 比 ReAct 少 60.4%。不是“提高 7.8%”的相对增幅。' },
  retail: { score: [48.2,29.9,51.7,58.3], prompt: [2819,2737,3065,3325], tokens: [4480000,4240000,3920000,3470000], insight: 'Retail：SKILL.state 成功率最高（58.3%），总 token 最低（3.47M），但平均 prompt 数值最大（3,325）。平均大小、调用次数与总消耗要分开看。' },
  airline: { score: [21.8,23.6,28.1,32.4], prompt: [5100,4700,5400,2800], tokens: [4850000,4650000,5280000,2880000], insight: 'Airline：32.4%，比最强对照 Stateful 高 4.3 个百分点；累计 token 比 ReAct 少约 40.6%（按表中舍入值计算，正文写 40.5%）。绝对成功率仍不足三分之一。' }
};
const LAYERS = [
 ['L1 / 还要测量，但不只盯历史长度','使用 provider usage、估算或 tokenizer 判断上下文有多大。','核心循环不依赖“历史快满了”的判断；但真实系统仍要测状态、最新观察、输出与重试成本。','固定字段数不保证固定 token；应监控 Σ 的增长。'],
 ['L2 / 从阈值触发变成逐步维护','百分比、绝对余量、事件数、cadence 或溢出后触发压缩。','每一个执行步都生成状态补丁，不等窗口满了再交接。','更新频率变了，但什么时候归档大状态仍需设计。'],
 ['L3 / 从切历史片段变成挑未来信息','保护头尾、用户消息、未闭合 tool pair，寻找合法切点。','从当前状态与新观察提取后续执行需要的变化，旧对话不进入下一轮。','决策更早：当下没识别出来的重要信息，之后可能无法恢复。'],
 ['L4 / 从摘要文本变成状态转移','通过摘要、剪裁、去重或服务端压缩缩小历史。','模型提出 ΔΣ；runtime 校验、合并和删除键。状态是下一轮决策的直接输入。','最大变化是更新语义与执行依赖，不是把 Markdown 换成 JSON。'],
 ['L5 / 从拼接历史变成重建三元输入','摘要与保留消息重新拼接，修复角色交替与工具配对。','下一轮重新构造 P + Σ + O；不携带前轮推理与历史消息。','本文以文本 prompt 展示。实际 provider 的工具调用协议仍须合法，不能因本设计而跳过。'],
 ['L6 / 把“模型看什么”和“证据存哪里”拆开','原研究区分存储可恢复、UI 可查看、模型可检索三层。','论文保留更新后的状态并丢弃中间推理；基本循环没有通用历史回捞机制。','研究型 agent 可另留原始观察与动作日志、添加 recall；这是混合扩展，需重新评测。']
];
const STEPS = [
 {title:'01 / 先看当前账本',description:'item_12 在 42 号架，item_7 在 12 号架。无需重读它们如何入库。规则 P 始终保留。',input:'等待最新事件…',output:'尚未生成补丁',applied:false,shipped:false},
 {title:'02 / 收到一条新观察',description:'订单是本轮新信息；其他无关遥测不必写进持久状态。',input:'Customer ordered item_12.\n背景：温度 22°C（与发货无关）',output:'尚未生成补丁',applied:false,shipped:false},
 {title:'03 / 提出变化和动作',description:'删除 42 号架这一项，并发出 Ship 动作。12 号架没被提到，应原样保留。',input:'Customer ordered item_12.',output:'{\n  "state_patch": {"shelf_42": null},\n  "action": "Ship item_12 shelf_42"\n}',applied:false,shipped:false},
 {title:'04 / 程序校验并合并',description:'在论文算法顺序中，合法 patch 先更新模型状态，此时真实货物尚未发出。格式检查不保证动作一定成功。',input:'校验通过：允许的键与值类型。\n未出现的 shelf_12 保留。',output:'Σ_next = Σ ⊕ {"shelf_42": null}\n待执行：Ship item_12 shelf_42',applied:true,shipped:false},
 {title:'05 / 执行动作，获得结果',description:'此例假定发货成功，真实货架现在也空了。若动作失败，需用失败观察修正状态；生产实现还需事务设计。',input:'Success: Shipped item_12 from shelf_42.',output:'动作已成功。\n上一轮推理不再进入后续 prompt。',applied:true,shipped:true},
 {title:'06 / 下一轮只带这三样',description:'规则 P、更新后的状态 Σ、新观察 O。没有重读旧订单和旧推理；必须留下的信息已进入状态。',input:'P：仓库操作规则\nΣ：{"shelf_12":"item_7"}\nO：发货成功',output:'下一轮等待新任务。\n这不是删除所有外部审计日志的指令。',applied:true,shipped:true}
];
const $ = id => document.getElementById(id);
const fmt = n => n.toLocaleString('en-US',{maximumFractionDigits:2});
const escapeHTML = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function mergePatch(state, patch) {
  const next = {...state};
  for (const [key,value] of Object.entries(patch)) {
    if (!/^shelf_\d+$/.test(key) || (value !== null && typeof value !== 'string')) throw new Error('Invalid teaching-schema patch');
    if (value === null) delete next[key]; else next[key] = value;
  }
  return next;
}
let simStep=0;
function renderSim() {
 const step=STEPS[simStep];
 const initial={shelf_12:'item_7',shelf_42:'item_12'};
 $('sim-state').textContent=JSON.stringify(step.applied ? mergePatch(initial,{shelf_42:null}) : initial,null,2);
 $('sim-title').textContent=step.title;
 $('sim-description').textContent=step.description;
 $('sim-input').textContent=step.input;
 $('sim-input-label').textContent=simStep===5?'下一轮完整输入':'O / 最新观察与执行反馈';
 $('sim-output').textContent=step.output;
 $('sim-count').textContent=`${simStep+1} / ${STEPS.length}`;
 $('sim-prev').disabled=simStep===0;
 $('sim-next').disabled=simStep===STEPS.length-1;
 $('step-track').innerHTML=STEPS.map((_,i)=>`<span class="${i<=simStep?'active':''}"></span>`).join('');
 $('warehouse').innerHTML=[12,21,31,42,48,55].map(n=>`<div class="shelf ${n===12||(n===42&&!step.shipped)?'occupied':''} ${n===42&&simStep>0&&simStep<5?'active':''}">${n} 号架</div>`).join('');
 const occupancy=step.shipped?'12 号架有 item_7，42 号架已空。':'12 号架有 item_7，42 号架有 item_12。';
 $('warehouse').parentElement.setAttribute('aria-label','真实仓库示意：'+occupancy);
}
function lineChart({xs,series,maxY,yLabel,width=850,height=330,markX}) {
 const left=65,right=25,top=18,bottom=48;
 const plotW=width-left-right,plotH=height-top-bottom;
 const minX=Math.min(...xs),maxX=Math.max(...xs);
 const X=n=>left+(n-minX)/(maxX-minX)*plotW;
 const Y=n=>top+(1-n/maxY)*plotH;
 let out='';
 for(let i=0;i<=4;i++) {
  const n=maxY*i/4,y=Y(n);
  out+=`<line class="gridline" x1="${left}" y1="${y}" x2="${width-right}" y2="${y}"/><text x="${left-10}" y="${y+5}" text-anchor="end">${yLabel(n)}</text>`;
 }
 const ticks=xs.length>8?[0,50,100,150,200]:width<500?xs.filter(x=>x!==25):xs;
 for(const x of ticks) out+=`<text x="${X(x)}" y="${height-20}" text-anchor="middle">${x}</text>`;
 out+=`<text x="${width-right}" y="${height-1}" text-anchor="end">执行步数 T</text>`;
 if(markX!==undefined) out+=`<line x1="${X(markX)}" y1="${top}" x2="${X(markX)}" y2="${height-bottom}" stroke="#eef3f8" stroke-dasharray="3 5" opacity=".5"/>`;
 for(const s of series) {
  const path=s.values.map((v,i)=>`${i?'L':'M'}${X(xs[i]).toFixed(2)},${Y(v).toFixed(2)}`).join(' ');
  out+=`<path d="${path}" fill="none" stroke="${s.color}" stroke-width="${s.name==='SKILL.state'?3.5:2.2}" stroke-dasharray="${s.dash||''}"/>`;
  if(xs.length<=8) s.values.forEach((v,i)=>{
   const x=X(xs[i]),y=Y(v),sd=s.sd?s.sd[i]:0;
   if(sd){const y1=Y(Math.min(maxY,v+sd)),y2=Y(Math.max(0,v-sd));out+=`<path d="M${x},${y1}V${y2}M${x-4},${y1}H${x+4}M${x-4},${y2}H${x+4}" stroke="${s.color}" opacity=".5" fill="none"/>`;}
   out+=`<circle cx="${x}" cy="${y}" r="4" fill="${s.color}"><title>${escapeHTML(s.name)} · T=${xs[i]}: ${fmt(v)}${sd?' ± '+fmt(sd):''}</title></circle>`;
  });
 }
 return out;
}
function theoreticalCost(t) {return {history:1000*t+100*t*(t+1),state:2000*t};}
function chartSize(id) {
 const width=window.innerWidth<=650?360:850,height=330;
 $(id).setAttribute('viewBox',`0 0 ${width} ${height}`);
 return {width,height};
}
function renderCost() {
 const t=Number($('turns').value),cost=theoreticalCost(t),xs=Array.from({length:41},(_,i)=>i*5);
 $('turns-value').textContent=`${t} 步`;
 $('history-cost').textContent=fmt(cost.history)+' tok';
 $('state-cost').textContent=fmt(cost.state)+' tok';
 $('cost-ratio').textContent=(cost.history/cost.state).toFixed(2)+'×';
 $('cost-chart').innerHTML=lineChart({xs,...chartSize('cost-chart'),maxY:4500000,yLabel:n=>(n/10000).toFixed(0),markX:t,series:[{name:'历史累加',color:SERIES[0].color,values:xs.map(x=>theoreticalCost(x).history)},{name:'固定状态',color:SERIES[3].color,values:xs.map(x=>theoreticalCost(x).state)}]});
}
function renderScaling() {
 const domain=$('scaling-domain').value,metric=$('scaling-metric').value,data=SCALE_DATA[domain];
 const xs=[...new Set(data.rows.map(r=>r.t))];
 const unit=metric==='score'?'Score · 0–1':metric==='prompt'?'平均 prompt · 字符（按 §4.3）':'累计 token · 百万';
 const series=SERIES.map((s,i)=>{const rows=data.rows.filter(r=>r.series===i);return {...s,values:rows.map(r=>r[metric]),sd:metric==='score'?rows.map(r=>r.scoreSD):null};});
 const maxY=metric==='score'?1:Math.ceil(Math.max(...series.flatMap(s=>s.values))*1.05/(metric==='prompt'?10000:1000000))*(metric==='prompt'?10000:1000000);
 $('scaling-unit').textContent=unit;
 $('scaling-legend').innerHTML=SERIES.map(s=>`<span style="--series:${s.color}">${s.name}</span>`).join('');
 $('scaling-chart').innerHTML=lineChart({xs,series,...chartSize('scaling-chart'),maxY,yLabel:n=>metric==='score'?n.toFixed(2):metric==='tokens'?(n/1e6).toFixed(1):fmt(n)});
 $('scaling-chart').setAttribute('aria-label',`${domain==='warehouse'?'仓库':'软件仓库'}：${unit}随执行步数的变化；精确数据在下方表格。`);
 const insights={warehouse:{score:'Warehouse：T=200，SKILL.state 的 Score 为 0.94 ± 0.02；它在这组任务里保住了较高的正确动作比例。',prompt:'Warehouse：SKILL.state 的均值保持在约 1,700–1,900 字符；Memory 到 T=200 增长为 84,364 字符。这个摘要对照没有保持有界。',tokens:'Warehouse：T=100，Stateful 1,062,387 ÷ SKILL.state 65,408 ≈ 16.2 倍。这是特定模型与任务的累计 token 比值，不是通用省钱倍数。'},software:{score:'反例也要看：Software 的 T=25，SKILL.state 为 0.88，低于 Stateful 的 0.94；T=100 则为 0.78，高于其他对照。并非每个场景都占优。',prompt:'Software：SKILL.state 在 T=25–100 的平均 prompt 都是 2,545；Stateful 在 T=100 达 62,330。单位按 §4.3 的字符定义读取。',tokens:'Software：T=100，SKILL.state 累计 90,200 token，Stateful 为 2,308,000；省 token 的幅度需要连同任务得分一起看。'}};
 $('scaling-insight').textContent=insights[domain][metric];
 $('scaling-source').href=PAPER+data.source;
 $('scaling-table').innerHTML=`<table><caption>${domain==='warehouse'?'Table 1 · Warehouse':'Table 6 · Software Repository'} · Gemini-3-Flash · 均值 ± SD</caption><thead><tr><th>T</th><th>Runtime</th><th>Score</th><th>Prompt（字符）</th><th>Tokens</th></tr></thead><tbody>${data.rows.map(r=>`<tr><td>${r.t}</td><td>${SERIES[r.series].name}</td><td>${r.score.toFixed(2)} ± ${r.scoreSD.toFixed(2)}</td><td>${fmt(r.prompt)} ± ${fmt(r.promptSD)}</td><td>${fmt(r.tokens)} ± ${fmt(r.tokensSD)}</td></tr>`).join('')}</tbody></table>`;
}
function bars(rows,max,label) {
 return rows.map(r=>`<div class="bar-row"><span>${escapeHTML(r.name)}</span><div class="bar-track"><div class="bar-fill" style="width:${r.value/max*100}%;--series:${r.color}"></div></div><span class="bar-value">${label(r.value)}</span></div>`).join('');
}
function renderPublic() {
 const data=PUBLIC_DATA[$('public-domain').value],metric=$('public-metric').value,values=data[metric];
 const max=metric==='score'?100:Math.max(...values)*1.08;
 $('public-bars').innerHTML=bars(SERIES.map((s,i)=>({...s,value:values[i]})),max,n=>metric==='score'?n.toFixed(1)+'%':metric==='tokens'?(n/1e6).toFixed(3)+'M':fmt(n));
 $('public-insight').textContent=data.insight;
}
function renderLayer(index) {
 const [title,old,current,implication]=LAYERS[index];
 document.querySelectorAll('[data-layer]').forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
 $('layer-detail').innerHTML=`<h3>${title}</h3><div class="compare-pair"><div><small>原研究 / 历史压缩</small><p>${old}</p></div><div><small>SKILL.state / 执行状态</small><p>${current}</p></div></div><div class="callout">${implication}</div>`;
}
$('sim-prev').addEventListener('click',()=>{simStep=Math.max(0,simStep-1);renderSim();});
$('sim-next').addEventListener('click',()=>{simStep=Math.min(STEPS.length-1,simStep+1);renderSim();});
$('sim-reset').addEventListener('click',()=>{simStep=0;renderSim();});
$('turns').addEventListener('input',renderCost);
['scaling-domain','scaling-metric'].forEach(id=>$(id).addEventListener('change',renderScaling));
['public-domain','public-metric'].forEach(id=>$(id).addEventListener('change',renderPublic));
document.querySelectorAll('[data-layer]').forEach(button=>button.addEventListener('click',()=>renderLayer(Number(button.dataset.layer))));
document.querySelectorAll('[data-answer]').forEach(button=>button.addEventListener('click',()=>{
 document.querySelectorAll('[data-answer]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 const answers={right:'答对了。固定字段数不等于固定信息量。all_findings 持续增长，|Σ| 就会增长，O(1) 的前提不成立。',wrong:'再想一步：一个字段也能装下一整本书。要有界的是序列化后的状态大小，而不是字段数量。',partial:'JSON 只限定表示形式。内容仍可能遗漏事实、覆盖错误，或者无限增长。可靠性还需要语义检查和任务评测。'};
 $('quiz-result').textContent=answers[button.dataset.answer];
}));
renderSim();renderCost();renderScaling();renderPublic();renderLayer(0);
window.addEventListener('resize',()=>{renderCost();renderScaling();});
$('budget-bars').innerHTML=bars([{name:'Full ReAct',value:.84,color:SERIES[0].color},{name:'Sliding Window',value:.18,color:'#8496ac'},{name:'Summary-capped',value:.52,color:SERIES[1].color},{name:'LLMLingua',value:.22,color:SERIES[2].color},{name:'SKILL.state',value:.94,color:SERIES[3].color}],1,n=>n.toFixed(2));
