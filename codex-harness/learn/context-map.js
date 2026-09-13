// A teaching projection of the pinned source snapshot, not captured request data.
(() => {
  const stage = document.getElementById('history-stage');
  const wire = document.getElementById('wire-mode');
  const records = {
    developerBundle: ['聚合 developer 消息', 'rule', 'I0/I1 · 槽位 1', 'developer', '每个 content 保留 kind；例如 skills.catalog / model_switch.instructions', '扩展贡献 + WorldState 的 developer fragments', '存在 ModelSwitchInstructions 时提到本组最前；其余内容在同一消息内聚合。基础 instructions 不应无条件在这里再复制一遍。'],
    separateDeveloper: ['独立 developer 片段（条件性）', 'rule', 'I0/I1 · 槽位 2，可有多条', 'developer', 'token_budget.context_window / multi_agent.role_instructions 等', '窗口提示 + WorldState 中要求独立的片段', '每个片段各建一条消息；TokenBudgetContext 需要对应 feature 和已知窗口。角色相同并不意味着必然合并。'],
    multiAgentMode: ['Multi-agent mode（条件性）', 'rule', 'I0/I1 · 槽位 3', 'developer', 'multi_agent.mode_instructions', 'WorldState 暂存后单独输出', '放在独立 developer 片段之后、contextual user 之前；与 MultiAgentRole 是不同片段。'],
    contextualUser: ['聚合 contextual user 消息', 'rule', 'I0/I1 · 槽位 4', 'user', '例如 agents_md.instructions / plugins.recommendations', '项目规则、推荐插件及 WorldState 的 user fragments', '本例 I0 含 R0，重建 I1 含当前 R1。user role 不代表真实用户输入；显式选中 Skill 正文另走注入路径，不固定属于本组。'],
    guardian: ['Guardian policy（条件性）', 'rule', 'I0/I1 · 槽位 5', 'developer', 'guardian.policy', '符合 session source 条件且非空的 developer instructions', '源码在 contextual user 消息之后追加本项；不能用“所有 developer 都排在 user 前面”概括。'],
    managed: ['Managed developer instructions（条件性）', 'rule', 'I0/I1 · 槽位 6', 'developer', 'managed_config.developer_instructions', 'WorldState 暂存的托管 developer 指令', '存在时最后追加到初始上下文组。后续真实用户消息、历史位置和 compaction 尾部产物另由外层装配决定。'],
    selectedSkill: ['类别探针：选中的 Skill 正文', 'rule', '独立注入路径；不固定属于 I0/I1', 'user', 'skills.selected_skill_instructions', 'Skills extension 读取显式选择的技能正文', '此按钮用于对照目录与正文，不额外插入示例 history。目录是 developer / skills.catalog；正文经 SkillInstructions 注入，模型自主读取则还要看实际工具输出。'],
    base: ['基础行为指令', 'rule', '顶层 instructions', '无 message.role 字段', '基础指令字段，不是 history content_kind', '显式配置 → 会话继承 → 模型目录', '通常独立于历史装配；不是把它混入摘要。'],
    schema: ['模型可见工具定义', 'call', '顶层 tools', '非消息', '工具 schema，不是 function_call', 'StepContext 的 ToolRouter.model_visible_specs()', '工具能力目录和一次工具的执行结果是不同对象；延迟工具不必全部常驻。'],
    liteBase: ['基础指令前缀', 'rule', 'input 前缀', 'developer', 'model.base_instructions', 'Responses Lite 请求转换', '这是客户端的 wire 装配分支，不能由此推导服务端 system prompt。'],
    liteTools: ['AdditionalTools 前缀', 'call', 'input 前缀', 'developer（AdditionalTools 自带 role）', 'AdditionalTools', 'Responses Lite 工具转换', '工具定义移到 input 前缀；不变成一次工具调用或一次工具结果。'],
    i0: ['I0 · 初始规则与目录', 'rule', 'input 的初始上下文分组', '分组内各片段不同', '例如 agents_md.instructions / skills.catalog', 'WorldState 与 extension 的初始上下文贡献', '图中折叠了多项：AGENTS R0 是 user role；Skills 目录片段是 developer role。I0 不是一种协议 item，也没有单一 role。'],
    i1: ['I1 · 按当前 R1 重建', 'rule', '回合中压缩：最后保留用户消息之前', '分组内各片段不同', '当前规则、权限、环境及其他 initial context', '当前 canonical state，不由摘要模型编写', '规则从程序状态源重建，让摘要不必独自承担规则保真。具体刷新仍受管理器缓存条件约束。'],
    reset: ['I1 · 新窗口初始上下文', 'rule', '新 input 窗口', '分组内各片段不同', '当前 initial context，含可用的窗口提示', 'start_new_context_window', 'TokenBudget 不自动产生摘要，也不自动保留 U1/U2。已有 notes 和 history 能否使用另有条件。'],
    u1: ['U1 · 满 100 免运费；API 不变', 'user', '历史中的真实用户消息', 'user', 'user.text', '用户输入', '本例在预算内原文保留。同为 user role 的 AGENTS、Skill 正文和 Local 摘要不等于真实用户请求。'],
    u2: ['U2 · 验证 99 / 100 / 101', 'user', '本例最后一条真实用户消息', 'user', 'user.text', '追加的用户输入', '回合中 Local/V2 的 initial context 插在它前面，摘要／压缩项仍位于历史尾部。'],
    call: ['c2 · 运行 ShippingCostTest', 'call', '历史中的调用项', '非 message；模型生成', 'function_call · call_id=c2', '模型输出，经工具路由执行', '不能因为一般聊天 API 把工具调用放在 assistant 消息内，就给 Responses 的独立 function_call 强行补一个 role。'],
    result: ['output c2 · amount=100 → FAIL', 'call', '历史中的结果项', '非普通 message', 'function_call_output · call_id=c2', '实际工具执行结果', '通过 call_id 与调用配对；Local/V2 的本例原文保留不留下这个 item。部分信息可能进摘要，完整原文能否取回另看存储路径。'],
    delta: ['ΔR · 新规则 R1 替代 R0', 'rule', '更新时追加到历史', 'user（本例 AGENTS 更新）', 'agents_md.instructions', 'WorldState 差异渲染', '它不是在原地改写旧消息。新片段声明替换旧规则；压缩后再从当前状态重建 I1。'],
    edit: ['c3 / output · 已把 > 改为 >=', 'call', '成对调用／结果的视觉分组', '非普通 message', 'function_call + function_call_output', '模型动作与工具结果', '只是已修改，不是已验证。图中合并展示一对 item，不代表 wire 上只有一个对象。'],
    summary: ['S · 已改比较符，仍待验证', 'summary', '新历史尾部', 'user', 'compaction.summary', 'Local 模型生成总结，再由客户端包装', '此处是教学摘要，非实测。它是进度交接，不升级成新的 system 规则。'],
    compact: ['Compaction · encrypted_content', 'summary', '新历史尾部', '非 message，无普通 role', 'compaction', 'Remote V2 返回的压缩项', '客户端可保存并重新发送，无法读懂内部语义，不能画出密文里究竟保留了哪些事实。']
  };
  const stages = {
    initial: [['i0','u1'], '初始请求：当前规则进入 input；基础 instructions 与工具定义另行装配。'],
    tools: [['i0','u1','call','result'], '新增工具调用与结果。call_id=c2 把这两项配对；规则和用户要求还留在历史前部。'],
    updated: [['i0','u1','call','result','delta','u2','edit'], '追加 R1 替换通知与 U2，再记录修改结果。旧 R0 文本仍在历史里，但更新片段声明它被替代。'],
    local: [['u1','i1','u2','summary'], '原始工具项退出活跃历史；预算内用户原文保留；规则从当前状态重建；尾部追加可读摘要。'],
    v2: [['u1','i1','u2','compact'], '布局与 Local 有相似处，尾部产物却是不可读的 compaction item。不能用 Local 摘要内容替代解释它。'],
    reset: [['reset'], '无自动摘要、无自动 U1/U2 保留。需要时依赖此前写好的 notes 或有条件可用的历史检索。']
  };
  function inspect(key, button) {
    const [name,,position,role,kind,source,meaning] = records[key];
    document.querySelectorAll('.history-item').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.getElementById('item-title').textContent = name;
    const fields = document.getElementById('item-fields');
    fields.replaceChildren();
    [['位置',position],['role',role],['类别 / type',kind],['来源',source]].forEach(([label,value]) => {
      const dt=document.createElement('dt');dt.textContent=label;
      const dd=document.createElement('dd');dd.textContent=value;fields.append(dt,dd);
    });
    document.getElementById('item-explanation').textContent = meaning;
  }
  function item(key, index) {
    const record=records[key];const button=document.createElement('button');
    button.type='button';button.className='history-item kind-'+record[1];button.dataset.item=key;
    button.setAttribute('aria-pressed','false');
    const name=document.createElement('strong');name.textContent=index+record[0];
    const badge=document.createElement('span');badge.textContent=record[3]+' · '+record[4];
    button.append(name,badge);button.addEventListener('click',()=>inspect(key,button));return button;
  }
  function breakdown(key) {
    const detail=document.createElement('details');detail.className='context-breakdown';
    const summary=document.createElement('summary');summary.textContent=`展开 ${key==='i0'?'I0':'I1'}：内部位置与类别`;
    const note=document.createElement('p');note.textContent='下面是构造器的有序槽位。无内容的槽位省略；条件项不表示同时启用，编号不是实际 wire index。';
    const slots=document.createElement('ol');
    ['developerBundle','separateDeveloper','multiAgentMode','contextualUser','guardian','managed'].forEach((name,i)=>{
      const li=document.createElement('li');li.append(item(name,`${i+1}. `));slots.append(li);
    });
    const skillNote=document.createElement('p');skillNote.textContent='分组外的注入类别（不占上面六个槽位）：';
    detail.append(summary,note,slots,skillNote,item('selectedSkill',''));return detail;
  }
  function render() {
    const [keys,note]=stages[stage.value];const top=document.getElementById('request-top');
    const list=document.getElementById('history-items');top.replaceChildren();list.replaceChildren();
    if(wire.value==='responses')top.append(item('base',''),item('schema',''));
    const prefix=wire.value==='lite'?['liteTools','liteBase']:[];
    [...prefix,...keys].forEach((key,i)=>{const li=document.createElement('li');li.append(item(key,`${i+1}. `));if(['i0','i1','reset'].includes(key))li.append(breakdown(key));list.append(li);});
    document.getElementById('history-change').textContent=note;
    const first=list.querySelector('button');inspect(first.dataset.item,first);
  }
  stage.addEventListener('change',render);wire.addEventListener('change',render);render();
})();
