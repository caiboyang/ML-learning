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
  ctf: { score: [43.2,46.4,41.8,54.2], prompt: [1909,1797,1946,813], tokens: [977000,1030000,1130000,387000], insight: 'CTF 评测：SKILL.state 成功率达 54.2%（pass@1），较次优基线 Memory 高出 7.8 个百分点；累计 Token 消耗相较 ReAct 降低 60.4%（此为绝对百分点差值，而非相对提升幅度）。' },
  retail: { score: [48.2,29.9,51.7,58.3], prompt: [2819,2737,3065,3325], tokens: [4480000,4240000,3920000,3470000], insight: 'Retail 场景：SKILL.state 成功率最高（58.3%），累计 Token 消耗最低（3.47M），但平均单步 Prompt 字符数却为各组最大（3,325）。需注意区分单步上下文规模、调用轮次与全局总消耗的不同维度。' },
  airline: { score: [21.8,23.6,28.1,32.4], prompt: [5100,4700,5400,2800], tokens: [4850000,4650000,5280000,2880000], insight: 'Airline 场景：成功率为 32.4%，较次优基线 Stateful 高出 4.3 个百分点；累计 Token 较 ReAct 减少约 40.6%（按表中标称值计算，正文描述为 40.5%）。但整体绝对成功率仍不足三分之一，挑战依然严峻。' }
};
const LAYERS = [
 ['L1 / 测量监控：从关注历史长度转向评估状态体量','依赖 Provider Usage 统计、字符粗算或分词器（Tokenizer）监控上下文占用。','核心循环不再依赖“上下文即将溢出”的被动判断；但生产系统仍需对状态规模、单步观测及重试开销建立严密监控。','固定的字段数量绝不代表实际 Token 规模有界；必须持续追踪状态字典 Σ 的膨胀情况。'],
 ['L2 / 触发范式：从被动阈值触发演进为单步增量维护','基于 Token 比例阈值、绝对余量窗口、固定步长（Cadence）或溢出异常触发压缩。','每个执行步均直接生成状态补丁（Patch），彻底摒弃等待上下文满载再行交接的模式。','更新时机被前移至每轮单步，但庞大状态的归档与淘汰生命周期仍需显式工程设计。'],
 ['L3 / 信息选点：从截断历史片段转向提炼未来决策增量','保护系统 Prompt、首尾轮对话及工具调用对（Tool Pair）原子性，确定安全截断切点。','直接从当前状态与最新观测中提炼未来执行所需的有效增量，历史流水不再传递至下轮。','信息保留决策被大幅前移：当前步若未能提炼出有效状态，后续轮次将彻底无法恢复。'],
 ['L4 / 减法本质：从非结构化摘要转为确定性状态转移','运用大模型摘要、规则裁剪、语义去重或提示词压缩手段精简历史。','模型仅提议状态补丁 ΔΣ；运行时负责校验、键合并与显式 null 删除。状态直接作为下步输入真源。','核心跃迁在于状态契约与执行依赖，而非仅仅把 Markdown 纯文本替换为 JSON 格式。'],
 ['L5 / 上下文重组：从历史流拼接转为三元组确定性装配','将保留的消息与摘要重新缝合，严格修复多轮角色交替（Role Alternation）与工具调用配对。','每轮以确定性规则重新组装 P + Σ + O 三元组；完全不携带前轮推理轨迹与对话记录。','论文以纯文本 Prompt 展示。工程落地的工具调用协议仍需严守 Provider 规范，不可因极简设计而破坏合规性。'],
 ['L6 / 持久化解耦：分离“模型当前视图”与“历史审计存证”','前序研究明确区分：全量存储可恢复、控制台交互可见、模型推理可检索三层边界。','论文仅持久化更新后的当前状态，中间推理轨迹即刻丢弃；原生循环未提供通用历史回捞检索通道。','研发型 Agent 需外置环境观测流水与动作日志，并构建按引用回溯（Recall）通道；这是必要的混合增强架构。']
];
const STEPS = [
 {title:'01 / 读取当前状态账本',description:'状态记录：item_12 位于 42 号货架，item_7 位于 12 号货架。执行动作无需回溯货物的入库与搬运历史。操作规程 P 保持静态不变。',input:'等待最新环境事件…',output:'尚未生成状态补丁',applied:false,shipped:false},
 {title:'02 / 接收最新环境观测',description:'客户订单为当前步的新增输入；与之交织的无关遥测（如温度读数）无需写入持久化状态。',input:'Customer ordered item_12.\n背景遥测：温度 22°C（与发货任务无关）',output:'尚未生成状态补丁',applied:false,shipped:false},
 {title:'03 / 生成状态补丁与执行动作',description:'提议将 42 号货架置为 null（移出库存），并下发 Ship 动作。未被提及的 12 号货架严格保持原样。',input:'Customer ordered item_12.',output:'{\n  "state_patch": {"shelf_42": null},\n  "action": "Ship item_12 shelf_42"\n}',applied:false,shipped:false},
 {title:'04 / 运行时校验与状态合并',description:'在论文算法时序中，合规补丁先行合并进状态，此时物理发货动作尚未执行。格式校验无法保证动作一定成功。',input:'校验通过：字段名与取值类型均合规。\n未出现的 shelf_12 保持原值保留。',output:'Σ_next = Σ ⊕ {"shelf_42": null}\n待执行动作：Ship item_12 shelf_42',applied:true,shipped:false},
 {title:'05 / 下发执行动作并获取反馈',description:'本例设定物理发货成功，真实货架同步清空。若动作失败，需依赖后续观测纠正状态；生产级实现必须配套事务一致性机制。',input:'Success: Shipped item_12 from shelf_42.',output:'动作执行成功。\n本轮步内推理完成使命，不再回填至后续 Prompt。',applied:true,shipped:true},
 {title:'06 / 装配下轮极简三元组输入',description:'下一轮仅携带：静态规程 P、更新后的状态 Σ、最新反馈 O。无需重复加载历史订单与推理；关键信息已完整固化于状态中。',input:'P：仓储调度操作规程\nΣ：{"shelf_12":"item_7"}\nO：发货执行成功',output:'就绪并等待新任务输入。\n注：这并不等同于物理删除底层的全量审计日志。',applied:true,shipped:true}
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
 $('sim-input-label').textContent=simStep===5?'下一轮完整输入三元组':'O / 最新环境观测与执行反馈';
 $('sim-output').textContent=step.output;
 $('sim-count').textContent=`${simStep+1} / ${STEPS.length}`;
 $('sim-prev').disabled=simStep===0;
 $('sim-next').disabled=simStep===STEPS.length-1;
 $('step-track').innerHTML=STEPS.map((_,i)=>`<span class="${i<=simStep?'active':''}"></span>`).join('');
 $('warehouse').innerHTML=[12,21,31,42,48,55].map(n=>`<div class="shelf ${n===12||(n===42&&!step.shipped)?'occupied':''} ${n===42&&simStep>0&&simStep<5?'active':''}">${n} 号架</div>`).join('');
 const occupancy=step.shipped?'12 号架存放 item_7，42 号架已清空。':'12 号架存放 item_7，42 号架存放 item_12。';
 $('warehouse').parentElement.setAttribute('aria-label','真实仓储货架状态：'+occupancy);
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
 const ticks=xs.length>8?[0,50,100,150,200]:width<500&&maxX-minX>100?xs.filter(x=>x!==25):xs;
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
 $('cost-chart').innerHTML=lineChart({xs,...chartSize('cost-chart'),maxY:4500000,yLabel:n=>(n/10000).toFixed(0),markX:t,series:[{name:'全量历史追加',color:SERIES[0].color,values:xs.map(x=>theoreticalCost(x).history)},{name:'固定状态维护',color:SERIES[3].color,values:xs.map(x=>theoreticalCost(x).state)}]});
}
function renderScaling() {
 const domain=$('scaling-domain').value,metric=$('scaling-metric').value,data=SCALE_DATA[domain];
 const xs=[...new Set(data.rows.map(r=>r.t))];
 const unit=metric==='score'?'动作准确率 Score · 0–1':metric==='prompt'?'平均 Prompt 规模 · 字符（依据 §4.3）':'累计 Token 消耗 · 百万 (M)';
 const series=SERIES.map((s,i)=>{const rows=data.rows.filter(r=>r.series===i);return {...s,values:rows.map(r=>r[metric]),sd:metric==='score'?rows.map(r=>r.scoreSD):null};});
 const maxY=metric==='score'?1:Math.ceil(Math.max(...series.flatMap(s=>s.values))*1.05/(metric==='prompt'?10000:1000000))*(metric==='prompt'?10000:1000000);
 $('scaling-unit').textContent=unit;
 $('scaling-legend').innerHTML=SERIES.map(s=>`<span style="--series:${s.color}">${s.name}</span>`).join('');
 $('scaling-chart').innerHTML=lineChart({xs,series,...chartSize('scaling-chart'),maxY,yLabel:n=>metric==='score'?n.toFixed(2):metric==='tokens'?(n/1e6).toFixed(1):fmt(n)});
 $('scaling-chart').setAttribute('aria-label',`${domain==='warehouse'?'Warehouse 仓储':'Software Repository 软件仓库'}：${unit}随执行步数的变化趋势；精确数据见下方数据表。`);
 const insights={
  warehouse:{
   score:'Warehouse 评测：T=200 步时，SKILL.state 的 Score 保持在 0.94 ± 0.02；在长程交互下成功维持了极高的正确动作比例。',
   prompt:'Warehouse 评测：SKILL.state 的单步 Prompt 均值恒定在约 1,700–1,900 字符；而 Memory 基线至 T=200 步时增长至 84,364 字符，表明该摘要对照组未能有效约束上下文膨胀。',
   tokens:'Warehouse 评测：T=100 步时，Stateful（1,062,387）÷ SKILL.state（65,408）≈ 16.2 倍。此为特定模型与受控任务下的累计 Token 比值，不能简单等同于通用的商业降本倍率。'
  },
  software:{
   score:'Software 评测：T=25 步时，SKILL.state 均值为 0.88 ± 0.08，Stateful 基线为 0.94 ± 0.03；此为全篇唯一均值偏低点，结合 SD 误差棒可知两者存在重叠，不能轻率断定显著落败。在 T=100 步时，SKILL.state 均值达 0.78，显著超越各基线。',
   prompt:'Software 评测：SKILL.state 在 T=25 至 100 步各阶段单步 Prompt 均保持为 2,545 字符；而 Stateful 在 T=100 步达 62,330 字符（依 §4.3 字符口径统计）。',
   tokens:'Software 评测：T=100 步时，SKILL.state 累计消耗 90,200 Token，Stateful 为 2,308,000 Token；Token 压缩收益需结合具体任务准确率进行审慎评估。'
  }
 };
 $('scaling-insight').textContent=insights[domain][metric];
 $('scaling-source').href=PAPER+data.source;
 $('scaling-table').innerHTML=`<table><caption>${domain==='warehouse'?'Table 1 · Warehouse 仓储':'Table 6 · Software Repository 软件仓库'} · Gemini-3-Flash · 均值 ± SD</caption><thead><tr><th>T 步数</th><th>运行时架构</th><th>动作准确率 Score</th><th>Prompt 规模（字符）</th><th>累计 Tokens</th></tr></thead><tbody>${data.rows.map(r=>`<tr><td>${r.t}</td><td>${SERIES[r.series].name}</td><td>${r.score.toFixed(2)} ± ${r.scoreSD.toFixed(2)}</td><td>${fmt(r.prompt)} ± ${fmt(r.promptSD)}</td><td>${fmt(r.tokens)} ± ${fmt(r.tokensSD)}</td></tr>`).join('')}</tbody></table>`;
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
 $('layer-detail').innerHTML=`<h3>${title}</h3><div class="compare-pair"><div><small>前序系统调研 / 历史压缩范式</small><p>${old}</p></div><div><small>SKILL.state / 状态驱动范式</small><p>${current}</p></div></div><div class="callout">${implication}</div>`;
}
$('sim-prev').addEventListener('click',()=>{simStep=Math.max(0,simStep-1);renderSim();});
$('sim-next').addEventListener('click',()=>{simStep=Math.min(STEPS.length-1,simStep+1);renderSim();});
$('sim-reset').addEventListener('click',()=>{simStep=0;renderSim();});
$('turns').addEventListener('input',renderCost);
['scaling-domain','scaling-metric'].forEach(id=>$(id).addEventListener('change',renderScaling));
['public-domain','public-metric'].forEach(id=>$(id).addEventListener('change',renderPublic));
document.querySelectorAll('[data-layer]').forEach(button=>button.addEventListener('click',()=>renderLayer(Number(button.dataset.layer))));
const QUIZZES = [
 {question:'若预设了 5 个固定 JSON 字段，但其中某个探索日志字段每轮追加千字文本，单步输入仍是 O(1) 吗？',
  options:['是，字段数量固定即满足要求','并非如此，内容体量仍在持续膨胀'],correct:1,
  explanation:'字段数量固定不代表数据体积有界。单步 O(1) 推导成立的前提是序列化后的状态与观测体积严格有界；单个字段同样能够线性累加长文。'},
 {question:'状态补丁格式完全合法且通过了类型 Schema 校验，真实系统的业务状态是否必然正确？',
  options:['不一定，合法补丁同样可能误删关键状态','是，运行时校验已确保业务正确性'],correct:0,
  explanation:'Schema 校验仅能防范数据结构与类型格式错误。对于“格式完全合法却意外删除了错误货架”等语义失真问题，必须依赖业务不变量断言与真实环境反馈进行兜底。'},
 {question:'某组对照实验显示累计 Token 降低了 16 倍，实际商业 API 账单是否必然节省 16 倍？',
  options:['是，同模型单价一致即等比例节约','不一定，需考量输入/输出定价差异与缓存机制'],correct:1,
  explanation:'实际账单取决于输入输出配比、Prompt Cache（前缀缓存）门槛与命中率以及重试成本等复合因素。裸 Token 计数不能直接等同于最终账单倍率。'},
 {question:'在构建研发型 Agent 时，某段早期原文在后续步骤突然变得至关重要，但此前未被提取至状态中，该如何应对？',
  options:['仅凭当前状态即可反向重建全量细节','在系统架构中为原始证据保留可寻址的回捞通道'],correct:1,
  explanation:'纯状态机无法恢复未曾显式保留的隐式信息。在状态中保留证据索引、在外置存储中沉淀全量流水并配合按需检索，是解决长程迟滞相关性的关键混合设计。'}
];
$('quiz-list').innerHTML=QUIZZES.map((q,i)=>`<div class="panel"><span class="label-chip">${i+1} / ${QUIZZES.length}</span><h3 id="question-${i}">${escapeHTML(q.question)}</h3><div class="quiz-options" role="group" aria-labelledby="question-${i}">${q.options.map((option,j)=>`<button type="button" data-quiz="${i}" data-option="${j}" aria-pressed="false">${escapeHTML(option)}</button>`).join('')}</div><p class="quiz-result" id="quiz-result-${i}" aria-live="polite">完成判断后查看深度解析。</p></div>`).join('');
document.querySelectorAll('[data-quiz]').forEach(button=>button.addEventListener('click',()=>{
 const index=Number(button.dataset.quiz),quiz=QUIZZES[index];
 document.querySelectorAll(`[data-quiz="${index}"]`).forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 $(`quiz-result-${index}`).textContent=(Number(button.dataset.option)===quiz.correct?'判断准确。':'推演有误。')+quiz.explanation;
}));
document.querySelectorAll('[data-reading]').forEach(button=>button.addEventListener('click',()=>{
 const preset=button.dataset.reading;
 let target;
 if(preset==='retail') {
  $('public-domain').value='retail';$('public-metric').value='prompt';renderPublic();
  target=$('public-experiment');
 } else {
  $('scaling-domain').value=preset==='tokens'?'warehouse':'software';
  $('scaling-metric').value=preset;renderScaling();
  target=$('scaling-experiment');
 }
 target.focus({preventScroll:true});target.scrollIntoView({block:'start'});
}));
renderSim();renderCost();renderScaling();renderPublic();renderLayer(0);
window.addEventListener('resize',()=>{renderCost();renderScaling();});
$('budget-bars').innerHTML=bars([{name:'Full ReAct（不限预算）',value:.84,color:SERIES[0].color},{name:'Sliding Window（滑动窗口）',value:.18,color:'#8496ac'},{name:'Summary-capped（硬顶摘要）',value:.52,color:SERIES[1].color},{name:'LLMLingua（困惑度压缩）',value:.22,color:SERIES[2].color},{name:'SKILL.state（结构化状态）',value:.94,color:SERIES[3].color}],1,n=>n.toFixed(2));
