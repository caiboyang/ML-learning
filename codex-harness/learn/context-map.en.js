// A teaching projection of the pinned source snapshot, not captured request data.
(() => {
  const stage = document.getElementById('history-stage');
  const wire = document.getElementById('wire-mode');
  const records = {
  "developerBundle": [
    "Aggregated developer message",
    "rule",
    "I0/I1 · slot 1",
    "developer",
    "Each content item keeps its kind, e.g. skills.catalog / model_switch.instructions",
    "Extension contributions + WorldState developer fragments",
    "ModelSwitchInstructions, when present, comes first within this group; other content is aggregated in the same message. Base instructions are not unconditionally copied here again."
  ],
  "separateDeveloper": [
    "Separate developer fragments (conditional)",
    "rule",
    "I0/I1 · slot 2, possibly multiple messages",
    "developer",
    "token_budget.context_window / multi_agent.role_instructions, etc.",
    "Window hints + WorldState fragments requiring separate messages",
    "Each fragment creates a separate message. TokenBudgetContext requires the feature and a known window. A shared role does not necessarily imply merging."
  ],
  "multiAgentMode": [
    "Multi-agent mode (conditional)",
    "rule",
    "I0/I1 · slot 3",
    "developer",
    "multi_agent.mode_instructions",
    "Buffered in WorldState, then emitted separately",
    "After separate developer fragments and before contextual user content. This differs from MultiAgentRole."
  ],
  "contextualUser": [
    "Aggregated contextual user message",
    "rule",
    "I0/I1 · slot 4",
    "user",
    "e.g. agents_md.instructions / plugins.recommendations",
    "Project rules, recommended plugins, and WorldState user fragments",
    "I0 contains R0; rebuilt I1 contains current R1. A user role does not establish actual user input. Explicitly selected Skill bodies have a separate injection path, not a fixed place in this group."
  ],
  "guardian": [
    "Guardian policy (conditional)",
    "rule",
    "I0/I1 · slot 5",
    "developer",
    "guardian.policy",
    "Nonempty developer instructions satisfying session-source conditions",
    "Appended after the contextual user message. It is incorrect to summarize the ordering as all developer messages preceding user messages."
  ],
  "managed": [
    "Managed developer instructions (conditional)",
    "rule",
    "I0/I1 · slot 6",
    "developer",
    "managed_config.developer_instructions",
    "Managed developer instructions buffered in WorldState",
    "Appended last in the initial-context group when present. Actual user messages, the group's history position, and compaction outputs at the tail are determined by outer assembly."
  ],
  "selectedSkill": [
    "Kind probe: selected Skill body",
    "rule",
    "Separate injection path; not fixed within I0/I1",
    "user",
    "skills.selected_skill_instructions",
    "Skills extension reads an explicitly selected body",
    "This button compares catalog and body; it does not add an item to the example history. The catalog is developer / skills.catalog; a body is injected through SkillInstructions. Model-initiated reading appears in actual tool outputs."
  ],
  "base": [
    "Base behavior instructions",
    "rule",
    "Top-level instructions",
    "No message.role field",
    "Base-instruction field, not a history content_kind",
    "Explicit configuration → inherited session → model catalog",
    "Normally assembled separately from history, not mixed into the summary."
  ],
  "schema": [
    "Model-visible tool definitions",
    "call",
    "Top-level tools",
    "Not a message",
    "Tool schema, not function_call",
    "StepContext's ToolRouter.model_visible_specs()",
    "A capability catalog and an individual execution result are different objects. Deferred tools need not all remain resident."
  ],
  "liteBase": [
    "Base-instruction prefix",
    "rule",
    "input prefix",
    "developer",
    "model.base_instructions",
    "Responses Lite request conversion",
    "A client wire-assembly branch; it does not reveal the server-side system prompt."
  ],
  "liteTools": [
    "AdditionalTools prefix",
    "call",
    "input prefix",
    "developer (carried by AdditionalTools)",
    "AdditionalTools",
    "Responses Lite tool conversion",
    "Definitions move into the input prefix; they do not become tool calls or results."
  ],
  "i0": [
    "I0 · Initial rules and catalogs",
    "rule",
    "Initial-context group in input",
    "Varies across fragments",
    "e.g. agents_md.instructions / skills.catalog",
    "WorldState and extension initial-context contributions",
    "Several items are collapsed here: AGENTS R0 uses user; the Skill catalog uses developer. I0 is not a protocol item and has no single role."
  ],
  "i1": [
    "I1 · Rebuilt from current R1",
    "rule",
    "Mid-turn compaction: before the last retained user message",
    "Varies across fragments",
    "Current rules, permissions, environment, and other initial context",
    "Current canonical state, not written by the summarizer",
    "Rules are reconstructed from program-owned sources so the summary is not solely responsible for rule fidelity. Refresh still depends on manager caching conditions."
  ],
  "reset": [
    "I1 · Initial context for a new window",
    "rule",
    "New input window",
    "Varies across fragments",
    "Current initial context, including available window hints",
    "start_new_context_window",
    "TokenBudget does not automatically summarize or retain U1/U2. Existing notes and history have separate availability conditions."
  ],
  "u1": [
    "U1 · Free shipping at 100+; preserve API",
    "user",
    "Actual user message in history",
    "user",
    "user.text",
    "User input",
    "Retained verbatim within this example's budget. AGENTS, Skill bodies, and Local summaries sharing the user role are not actual user requests."
  ],
  "u2": [
    "U2 · Verify 99 / 100 / 101",
    "user",
    "Last actual user message in this example",
    "user",
    "user.text",
    "Additional user input",
    "Mid-turn Local/V2 inserts initial context before this message; the summary/compaction item remains at the tail."
  ],
  "call": [
    "c2 · Run ShippingCostTest",
    "call",
    "Call item in history",
    "Not a message; model-generated",
    "function_call · call_id=c2",
    "Model output executed through tool routing",
    "Do not force a role onto a standalone Responses function_call simply because some chat APIs embed calls in assistant messages."
  ],
  "result": [
    "output c2 · amount=100 → FAIL",
    "call",
    "Result item in history",
    "Not an ordinary message",
    "function_call_output · call_id=c2",
    "Actual tool execution result",
    "Paired with its call through call_id. This example's Local/V2 verbatim retention does not keep this item. Some information may enter the summary; original-text retrieval depends on separate storage paths."
  ],
  "delta": [
    "ΔR · New R1 replaces R0",
    "rule",
    "Appended to history when updated",
    "user (AGENTS update in this example)",
    "agents_md.instructions",
    "WorldState diff rendering",
    "The old message is not edited in place. A new fragment declares replacement; after compaction, I1 is rebuilt from current state."
  ],
  "edit": [
    "c3 / output · Changed > to >=",
    "call",
    "Visual grouping of a call/result pair",
    "Not ordinary messages",
    "function_call + function_call_output",
    "Model action and tool result",
    "Edited does not mean verified. Grouping a pair in the diagram does not make it one wire object."
  ],
  "summary": [
    "S · Comparison changed; verification pending",
    "summary",
    "Tail of replacement history",
    "user",
    "compaction.summary",
    "Local model summary wrapped by the client",
    "A constructed teaching summary, not measured output. It is a progress handoff, not a new system rule."
  ],
  "compact": [
    "Compaction · encrypted_content",
    "summary",
    "Tail of replacement history",
    "Not a message; no ordinary role",
    "compaction",
    "Compaction item returned by Remote V2",
    "The client can save and resend it but cannot interpret its semantics. The diagram cannot claim which facts its ciphertext preserves."
  ]
};
  const stages = {
  "initial": [
    [
      "i0",
      "u1"
    ],
    "Initial request: current rules enter input; base instructions and tool definitions are assembled separately."
  ],
  "tools": [
    [
      "i0",
      "u1",
      "call",
      "result"
    ],
    "A tool call and result are added, paired by call_id=c2. Rules and user requirements remain earlier in history."
  ],
  "updated": [
    [
      "i0",
      "u1",
      "call",
      "result",
      "delta",
      "u2",
      "edit"
    ],
    "Append the R1 replacement notice and U2, then record the edit. Old R0 text remains, but the update declares it superseded."
  ],
  "local": [
    [
      "u1",
      "i1",
      "u2",
      "summary"
    ],
    "Original tool items leave active history. User text within budget remains, current rules are rebuilt, and a readable summary is appended."
  ],
  "v2": [
    [
      "u1",
      "i1",
      "u2",
      "compact"
    ],
    "The layout resembles Local, but the tail is an unreadable compaction item. A Local summary cannot explain its actual contents."
  ],
  "reset": [
    [
      "reset"
    ],
    "No automatic summary or U1/U2 retention. Continuation can depend on previously written notes or conditionally available history retrieval."
  ]
};
  function inspect(key, button) {
    const [name,,position,role,kind,source,meaning] = records[key];
    document.querySelectorAll('.history-item').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.getElementById('item-title').textContent = name;
    const fields = document.getElementById('item-fields');
    fields.replaceChildren();
    [['Position',position],['role',role],['Kind / type',kind],['Source',source]].forEach(([label,value]) => {
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
    const summary=document.createElement('summary');summary.textContent=`Expand ${key==='i0'?'I0':'I1'}: internal positions and kinds`;
    const note=document.createElement('p');note.textContent='Ordered constructor slots are shown below. Empty slots are omitted; conditional items are not necessarily enabled together, and numbering is not the actual wire index.';
    const slots=document.createElement('ol');
    ['developerBundle','separateDeveloper','multiAgentMode','contextualUser','guardian','managed'].forEach((name,i)=>{
      const li=document.createElement('li');li.append(item(name,`${i+1}. `));slots.append(li);
    });
    const skillNote=document.createElement('p');skillNote.textContent='Injection kind outside the group (not one of the six slots above):';
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
