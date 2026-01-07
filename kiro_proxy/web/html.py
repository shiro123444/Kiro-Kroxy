"""Web UI - 组件化单文件结构"""

# ==================== CSS 样式 ====================
CSS_BASE = '''
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --bg: #fafafa; --card: #fff; --border: #e5e5e5; --text: #1a1a1a; --muted: #666; --accent: #000; --success: #22c55e; --error: #ef4444; --warn: #f59e0b; --info: #3b82f6; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #0a0a0a; --card: #141414; --border: #262626; --text: #fafafa; --muted: #a3a3a3; --accent: #fff; }
}
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
.container { max-width: 1100px; margin: 0 auto; padding: 2rem 1rem; }
'''

CSS_LAYOUT = '''
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); }
h1 { font-size: 1.5rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }
h1 img { width: 28px; height: 28px; }
.status { font-size: 0.875rem; color: var(--muted); display: flex; align-items: center; gap: 1rem; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot.ok { background: var(--success); }
.status-dot.err { background: var(--error); }
.tabs { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.tab { padding: 0.5rem 1rem; border: 1px solid var(--border); background: var(--card); cursor: pointer; font-size: 0.875rem; transition: all 0.2s; border-radius: 6px; }
.tab.active { background: var(--accent); color: var(--bg); border-color: var(--accent); }
.panel { display: none; }
.panel.active { display: block; }
.footer { text-align: center; color: var(--muted); font-size: 0.75rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border); }
'''

CSS_COMPONENTS = '''
.card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; }
.card h3 { font-size: 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.stat-item { text-align: center; padding: 1rem; background: var(--bg); border-radius: 6px; }
.stat-value { font-size: 1.5rem; font-weight: 600; }
.stat-label { font-size: 0.75rem; color: var(--muted); }
.badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500; }
.badge.success { background: #dcfce7; color: #166534; }
.badge.error { background: #fee2e2; color: #991b1b; }
.badge.warn { background: #fef3c7; color: #92400e; }
.badge.info { background: #dbeafe; color: #1e40af; }
@media (prefers-color-scheme: dark) {
  .badge.success { background: #14532d; color: #86efac; }
  .badge.error { background: #7f1d1d; color: #fca5a5; }
  .badge.warn { background: #78350f; color: #fde68a; }
  .badge.info { background: #1e3a5f; color: #93c5fd; }
}
'''

CSS_FORMS = '''
.input-row { display: flex; gap: 0.5rem; }
.input-row input, .input-row select { flex: 1; padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: 6px; background: var(--card); color: var(--text); font-size: 1rem; }
button { padding: 0.75rem 1.5rem; background: var(--accent); color: var(--bg); border: none; border-radius: 6px; cursor: pointer; font-size: 0.875rem; font-weight: 500; transition: opacity 0.2s; }
button:hover { opacity: 0.8; }
button:disabled { opacity: 0.5; cursor: not-allowed; }
button.secondary { background: var(--card); color: var(--text); border: 1px solid var(--border); }
button.small { padding: 0.25rem 0.5rem; font-size: 0.75rem; }
select { padding: 0.5rem; border: 1px solid var(--border); border-radius: 6px; background: var(--card); color: var(--text); }
pre { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 1rem; overflow-x: auto; font-size: 0.8rem; }
table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }
th { font-weight: 500; color: var(--muted); }
'''

CSS_CHAT = '''
.chat-box { height: 350px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; padding: 1rem; margin-bottom: 1rem; background: var(--bg); }
.msg { margin-bottom: 1rem; }
.msg.user { text-align: right; }
.msg span { display: inline-block; max-width: 80%; padding: 0.75rem 1rem; border-radius: 12px; white-space: pre-wrap; word-break: break-word; }
.msg.user span { background: var(--accent); color: var(--bg); }
.msg.ai span { background: var(--card); border: 1px solid var(--border); }
'''

CSS_ACCOUNTS = '''
.account-card { border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; background: var(--card); }
.account-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.account-name { font-weight: 500; display: flex; align-items: center; gap: 0.5rem; }
.account-meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.5rem; font-size: 0.8rem; color: var(--muted); }
.account-meta-item { display: flex; justify-content: space-between; padding: 0.25rem 0; }
.account-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border); }
'''

CSS_API = '''
.endpoint { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
.method { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.method.get { background: #dcfce7; color: #166534; }
.method.post { background: #fef3c7; color: #92400e; }
@media (prefers-color-scheme: dark) {
  .method.get { background: #14532d; color: #86efac; }
  .method.post { background: #78350f; color: #fde68a; }
}
.copy-btn { padding: 0.25rem 0.5rem; font-size: 0.75rem; background: var(--card); border: 1px solid var(--border); color: var(--text); }
'''

CSS_STYLES = CSS_BASE + CSS_LAYOUT + CSS_COMPONENTS + CSS_FORMS + CSS_CHAT + CSS_ACCOUNTS + CSS_API


# ==================== HTML 模板 ====================
HTML_HEADER = '''
<header>
  <h1><img src="/assets/icon.svg" alt="Kiro">Kiro API Proxy</h1>
  <div class="status">
    <span class="status-dot" id="statusDot"></span>
    <span id="statusText">检查中...</span>
    <span id="uptime"></span>
  </div>
</header>

<div class="tabs">
  <div class="tab active" data-tab="chat">对话</div>
  <div class="tab" data-tab="monitor">监控</div>
  <div class="tab" data-tab="accounts">账号</div>
  <div class="tab" data-tab="logs">日志</div>
  <div class="tab" data-tab="api">API</div>
  <div class="tab" data-tab="docs">文档</div>
</div>
'''

HTML_CHAT = '''
<div class="panel active" id="chat">
  <div class="card">
    <div style="display:flex;gap:0.5rem;margin-bottom:1rem">
      <select id="model" style="flex:1"></select>
      <button class="secondary" onclick="clearChat()">清空</button>
    </div>
    <div class="chat-box" id="chatBox"></div>
    <div class="input-row">
      <input type="text" id="input" placeholder="输入消息..." onkeydown="if(event.key==='Enter')send()">
      <button onclick="send()" id="sendBtn">发送</button>
    </div>
  </div>
</div>
'''

HTML_MONITOR = '''
<div class="panel" id="monitor">
  <div class="card">
    <h3>服务状态 <button class="secondary small" onclick="loadStats()">刷新</button></h3>
    <div class="stats-grid" id="statsGrid"></div>
  </div>
  <div class="card">
    <h3>配额状态</h3>
    <div id="quotaStatus"></div>
  </div>
  <div class="card">
    <h3>速度测试</h3>
    <button onclick="runSpeedtest()" id="speedtestBtn">开始测试</button>
    <span id="speedtestResult" style="margin-left:1rem"></span>
  </div>
</div>
'''

HTML_ACCOUNTS = '''
<div class="panel" id="accounts">
  <div class="card">
    <h3>账号管理</h3>
    <div style="display:flex;gap:0.5rem;margin-bottom:1rem;flex-wrap:wrap">
      <button class="secondary" onclick="scanTokens()">扫描 Token</button>
      <button class="secondary" onclick="showAddAccount()">手动添加</button>
      <button class="secondary" onclick="refreshAllTokens()">刷新所有 Token</button>
      <button class="secondary" onclick="checkTokens()">检查有效期</button>
    </div>
    <div id="accountList"></div>
  </div>
  <div class="card" id="scanResults" style="display:none">
    <h3>扫描结果</h3>
    <div id="scanList"></div>
  </div>
  <div class="card">
    <h3>Kiro 登录说明</h3>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:0.5rem">
      Kiro 使用 AWS Identity Center 认证，需要通过 Kiro IDE 登录：
    </p>
    <ol style="color:var(--muted);font-size:0.875rem;padding-left:1.5rem">
      <li>打开 Kiro IDE</li>
      <li>点击登录，使用 Google/GitHub 账号</li>
      <li>登录成功后 token 自动保存</li>
      <li>点击上方"扫描 Token"添加账号</li>
    </ol>
  </div>
</div>
'''

HTML_LOGS = '''
<div class="panel" id="logs">
  <div class="card">
    <h3>请求日志 <button class="secondary small" onclick="loadLogs()">刷新</button></h3>
    <table>
      <thead><tr><th>时间</th><th>路径</th><th>模型</th><th>账号</th><th>状态</th><th>耗时</th></tr></thead>
      <tbody id="logTable"></tbody>
    </table>
  </div>
</div>
'''

HTML_API = '''
<div class="panel" id="api">
  <div class="card">
    <h3>API 端点</h3>
    <p style="color:var(--muted);font-size:0.875rem;margin-bottom:1rem">支持 OpenAI、Anthropic、Gemini 三种协议</p>
    <h4 style="color:var(--muted);margin-bottom:0.5rem">OpenAI 协议</h4>
    <div class="endpoint"><span class="method post">POST</span><code>/v1/chat/completions</code></div>
    <div class="endpoint"><span class="method get">GET</span><code>/v1/models</code></div>
    <h4 style="color:var(--muted);margin-top:1rem;margin-bottom:0.5rem">Anthropic 协议</h4>
    <div class="endpoint"><span class="method post">POST</span><code>/v1/messages</code></div>
    <div class="endpoint"><span class="method post">POST</span><code>/v1/messages/count_tokens</code></div>
    <h4 style="color:var(--muted);margin-top:1rem;margin-bottom:0.5rem">Gemini 协议</h4>
    <div class="endpoint"><span class="method post">POST</span><code>/v1/models/{model}:generateContent</code></div>
    <h4 style="margin-top:1rem;color:var(--muted)">Base URL</h4>
    <pre><code id="baseUrl"></code></pre>
    <button class="copy-btn" onclick="copy(location.origin)" style="margin-top:0.5rem">复制</button>
  </div>
  <div class="card">
    <h3>配置示例</h3>
    <h4 style="color:var(--muted);margin-bottom:0.5rem">Claude Code</h4>
    <pre><code>Base URL: <span class="pyUrl"></span>
API Key: any
模型: claude-sonnet-4</code></pre>
    <h4 style="color:var(--muted);margin-top:1rem;margin-bottom:0.5rem">Codex CLI</h4>
    <pre><code>Endpoint: <span class="pyUrl"></span>/v1
API Key: any
模型: gpt-4o</code></pre>
  </div>
</div>
'''

HTML_DOCS = '''
<div class="panel" id="docs">
  <div class="card">
    <h3>模型对照表</h3>
    <table>
      <thead><tr><th>Kiro 模型</th><th>能力</th><th>Claude Code</th><th>Codex</th></tr></thead>
      <tbody>
        <tr><td><code>claude-sonnet-4</code></td><td>⭐⭐⭐ 推荐</td><td><code>claude-sonnet-4</code></td><td><code>gpt-4o</code></td></tr>
        <tr><td><code>claude-sonnet-4.5</code></td><td>⭐⭐⭐⭐ 更强</td><td><code>claude-sonnet-4.5</code></td><td><code>gpt-4o</code></td></tr>
        <tr><td><code>claude-haiku-4.5</code></td><td>⚡ 快速</td><td><code>claude-haiku-4.5</code></td><td><code>gpt-4o-mini</code></td></tr>
        <tr><td><code>claude-opus-4.5</code></td><td>⭐⭐⭐⭐⭐ 最强</td><td><code>claude-opus-4.5</code></td><td><code>o1</code></td></tr>
      </tbody>
    </table>
  </div>
  <div class="card">
    <h3>新功能 v1.3.0</h3>
    <ul style="color:var(--muted);font-size:0.875rem;padding-left:1.5rem">
      <li><strong>Token 自动刷新</strong> - 检测过期自动刷新</li>
      <li><strong>动态 Machine ID</strong> - 每个账号独立指纹</li>
      <li><strong>配额管理</strong> - 429 自动冷却和恢复</li>
      <li><strong>自动账号切换</strong> - 配额超限自动切换</li>
    </ul>
  </div>
</div>
'''

HTML_BODY = HTML_HEADER + HTML_CHAT + HTML_MONITOR + HTML_ACCOUNTS + HTML_LOGS + HTML_API + HTML_DOCS


# ==================== JavaScript ====================
JS_UTILS = '''
const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);

function copy(text){
  navigator.clipboard.writeText(text).then(()=>{
    const toast=document.createElement('div');
    toast.textContent='已复制';
    toast.style.cssText='position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);background:var(--accent);color:var(--bg);padding:0.5rem 1rem;border-radius:6px;font-size:0.875rem;z-index:1000';
    document.body.appendChild(toast);
    setTimeout(()=>toast.remove(),1500);
  });
}

function formatUptime(s){
  if(s<60)return s+'秒';
  if(s<3600)return Math.floor(s/60)+'分钟';
  return Math.floor(s/3600)+'小时'+Math.floor((s%3600)/60)+'分钟';
}
'''

JS_TABS = '''
// Tabs
$$('.tab').forEach(t=>t.onclick=()=>{
  $$('.tab').forEach(x=>x.classList.remove('active'));
  $$('.panel').forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  $('#'+t.dataset.tab).classList.add('active');
  if(t.dataset.tab==='monitor'){loadStats();loadQuota();}
  if(t.dataset.tab==='logs')loadLogs();
  if(t.dataset.tab==='accounts')loadAccounts();
});
'''

JS_STATUS = '''
// Status
async function checkStatus(){
  try{
    const r=await fetch('/api/status');
    const d=await r.json();
    $('#statusDot').className='status-dot '+(d.ok?'ok':'err');
    $('#statusText').textContent=d.ok?'已连接':'未连接';
    if(d.stats)$('#uptime').textContent='运行 '+formatUptime(d.stats.uptime_seconds);
  }catch(e){
    $('#statusDot').className='status-dot err';
    $('#statusText').textContent='连接失败';
  }
}
checkStatus();
setInterval(checkStatus,30000);

// URLs
$('#baseUrl').textContent=location.origin;
$$('.pyUrl').forEach(e=>e.textContent=location.origin);
'''

JS_MODELS = '''
// Models
async function loadModels(){
  try{
    const r=await fetch('/v1/models');
    const d=await r.json();
    const select=$('#model');
    select.innerHTML='';
    (d.data||[]).forEach(m=>{
      const opt=document.createElement('option');
      opt.value=m.id;
      opt.textContent=m.name||m.id;
      if(m.id==='claude-sonnet-4')opt.selected=true;
      select.appendChild(opt);
    });
  }catch(e){console.error(e)}
}
loadModels();
'''

JS_CHAT = '''
// Chat
let messages=[];
function addMsg(role,text){
  const box=$('#chatBox');
  const div=document.createElement('div');
  div.className='msg '+(role==='user'?'user':'ai');
  div.innerHTML='<span>'+text.replace(/</g,'&lt;').replace(/\\n/g,'<br>')+'</span>';
  box.appendChild(div);
  box.scrollTop=box.scrollHeight;
}
function clearChat(){messages=[];$('#chatBox').innerHTML='';}
async function send(){
  const input=$('#input');
  const text=input.value.trim();
  if(!text)return;
  input.value='';
  addMsg('user',text);
  messages.push({role:'user',content:text});
  $('#sendBtn').disabled=true;
  $('#sendBtn').textContent='...';
  try{
    const res=await fetch('/v1/chat/completions',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({model:$('#model').value,messages})
    });
    const data=await res.json();
    if(data.choices&&data.choices[0]){
      const reply=data.choices[0].message.content;
      addMsg('ai',reply);
      messages.push({role:'assistant',content:reply});
    }else if(data.detail){
      addMsg('ai','错误: '+data.detail);
    }
  }catch(e){addMsg('ai','请求失败: '+e.message)}
  $('#sendBtn').disabled=false;
  $('#sendBtn').textContent='发送';
}
'''

JS_STATS = '''
// Stats
async function loadStats(){
  try{
    const r=await fetch('/api/stats');
    const d=await r.json();
    $('#statsGrid').innerHTML=`
      <div class="stat-item"><div class="stat-value">${d.total_requests}</div><div class="stat-label">总请求</div></div>
      <div class="stat-item"><div class="stat-value">${d.total_errors}</div><div class="stat-label">错误数</div></div>
      <div class="stat-item"><div class="stat-value">${d.error_rate}</div><div class="stat-label">错误率</div></div>
      <div class="stat-item"><div class="stat-value">${d.accounts_available}/${d.accounts_total}</div><div class="stat-label">可用账号</div></div>
      <div class="stat-item"><div class="stat-value">${d.accounts_cooldown||0}</div><div class="stat-label">冷却中</div></div>
    `;
  }catch(e){console.error(e)}
}

// Quota
async function loadQuota(){
  try{
    const r=await fetch('/api/quota');
    const d=await r.json();
    if(d.exceeded_credentials&&d.exceeded_credentials.length>0){
      $('#quotaStatus').innerHTML=d.exceeded_credentials.map(c=>`
        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.5rem;background:var(--bg);border-radius:4px;margin-bottom:0.5rem">
          <span><span class="badge warn">冷却中</span> ${c.credential_id}</span>
          <span style="color:var(--muted);font-size:0.8rem">剩余 ${c.remaining_seconds}秒</span>
          <button class="secondary small" onclick="restoreAccount('${c.credential_id}')">恢复</button>
        </div>
      `).join('');
    }else{
      $('#quotaStatus').innerHTML='<p style="color:var(--muted)">无冷却中的账号</p>';
    }
  }catch(e){console.error(e)}
}

// Speedtest
async function runSpeedtest(){
  $('#speedtestBtn').disabled=true;
  $('#speedtestResult').textContent='测试中...';
  try{
    const r=await fetch('/api/speedtest',{method:'POST'});
    const d=await r.json();
    $('#speedtestResult').textContent=d.ok?`延迟: ${d.latency_ms.toFixed(0)}ms (${d.account_id})`:'测试失败: '+d.error;
  }catch(e){$('#speedtestResult').textContent='测试失败'}
  $('#speedtestBtn').disabled=false;
}
'''

JS_LOGS = '''
// Logs
async function loadLogs(){
  try{
    const r=await fetch('/api/logs?limit=50');
    const d=await r.json();
    $('#logTable').innerHTML=(d.logs||[]).map(l=>`
      <tr>
        <td>${new Date(l.timestamp*1000).toLocaleTimeString()}</td>
        <td>${l.path}</td>
        <td>${l.model||'-'}</td>
        <td>${l.account_id||'-'}</td>
        <td><span class="badge ${l.status<400?'success':l.status<500?'warn':'error'}">${l.status}</span></td>
        <td>${l.duration_ms.toFixed(0)}ms</td>
      </tr>
    `).join('');
  }catch(e){console.error(e)}
}
'''


JS_ACCOUNTS = '''
// Accounts
async function loadAccounts(){
  try{
    const r=await fetch('/api/accounts');
    const d=await r.json();
    if(!d.accounts||d.accounts.length===0){
      $('#accountList').innerHTML='<p style="color:var(--muted)">暂无账号，请点击"扫描 Token"</p>';
      return;
    }
    $('#accountList').innerHTML=d.accounts.map(a=>{
      const statusBadge=a.status==='active'?'success':a.status==='cooldown'?'warn':'error';
      const statusText={active:'可用',cooldown:'冷却中',unhealthy:'不健康',disabled:'已禁用'}[a.status]||a.status;
      return `
        <div class="account-card">
          <div class="account-header">
            <div class="account-name">
              <span class="badge ${statusBadge}">${statusText}</span>
              <span>${a.name}</span>
            </div>
            <span style="color:var(--muted);font-size:0.75rem">${a.id}</span>
          </div>
          <div class="account-meta">
            <div class="account-meta-item"><span>请求数</span><span>${a.request_count}</span></div>
            <div class="account-meta-item"><span>错误数</span><span>${a.error_count}</span></div>
            <div class="account-meta-item"><span>Token</span><span class="badge ${a.token_expired?'error':a.token_expiring_soon?'warn':'success'}">${a.token_expired?'已过期':a.token_expiring_soon?'即将过期':'有效'}</span></div>
            ${a.cooldown_remaining?`<div class="account-meta-item"><span>冷却剩余</span><span>${a.cooldown_remaining}秒</span></div>`:''}
          </div>
          <div class="account-actions">
            <button class="secondary small" onclick="refreshToken('${a.id}')">刷新 Token</button>
            <button class="secondary small" onclick="viewAccountDetail('${a.id}')">详情</button>
            ${a.status==='cooldown'?`<button class="secondary small" onclick="restoreAccount('${a.id}')">恢复</button>`:''}
            <button class="secondary small" onclick="toggleAccount('${a.id}')">${a.enabled?'禁用':'启用'}</button>
            <button class="secondary small" onclick="deleteAccount('${a.id}')" style="color:var(--error)">删除</button>
          </div>
        </div>
      `;
    }).join('');
  }catch(e){console.error(e)}
}

async function refreshToken(id){
  try{
    const r=await fetch('/api/accounts/'+id+'/refresh',{method:'POST'});
    const d=await r.json();
    alert(d.ok?'刷新成功':'刷新失败: '+d.message);
    loadAccounts();
  }catch(e){alert('刷新失败: '+e.message)}
}

async function refreshAllTokens(){
  try{
    const r=await fetch('/api/accounts/refresh-all',{method:'POST'});
    const d=await r.json();
    alert(`刷新完成: ${d.refreshed} 个账号`);
    loadAccounts();
  }catch(e){alert('刷新失败: '+e.message)}
}

async function restoreAccount(id){
  try{
    await fetch('/api/accounts/'+id+'/restore',{method:'POST'});
    loadAccounts();
    loadQuota();
  }catch(e){alert('恢复失败: '+e.message)}
}

async function viewAccountDetail(id){
  try{
    const r=await fetch('/api/accounts/'+id);
    const d=await r.json();
    const info=`账号: ${d.name}
ID: ${d.id}
状态: ${d.status}
Machine ID: ${d.machine_id}

凭证信息:
- Access Token: ${d.credentials?.has_access_token?'有':'无'}
- Refresh Token: ${d.credentials?.has_refresh_token?'有':'无'}
- Client ID: ${d.credentials?.has_client_id?'有':'无'}
- 认证方式: ${d.credentials?.auth_method||'未知'}
- 区域: ${d.credentials?.region||'未知'}
- 过期时间: ${d.credentials?.expires_at||'未知'}
- Token 状态: ${d.credentials?.is_expired?'已过期':d.credentials?.is_expiring_soon?'即将过期':'有效'}

统计:
- 请求数: ${d.request_count}
- 错误数: ${d.error_count}`;
    alert(info);
  }catch(e){alert('获取详情失败: '+e.message)}
}

async function toggleAccount(id){
  await fetch('/api/accounts/'+id+'/toggle',{method:'POST'});
  loadAccounts();
}

async function deleteAccount(id){
  if(confirm('确定删除此账号?')){
    await fetch('/api/accounts/'+id,{method:'DELETE'});
    loadAccounts();
  }
}

function showAddAccount(){
  const path=prompt('输入 Token 文件路径:');
  if(path){
    const name=prompt('账号名称:','账号');
    fetch('/api/accounts',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({name,token_path:path})
    }).then(r=>r.json()).then(d=>{
      if(d.ok)loadAccounts();
      else alert(d.detail||'添加失败');
    });
  }
}

async function scanTokens(){
  try{
    const r=await fetch('/api/token/scan');
    const d=await r.json();
    const panel=$('#scanResults');
    const list=$('#scanList');
    if(d.tokens&&d.tokens.length>0){
      panel.style.display='block';
      list.innerHTML=d.tokens.map(t=>`
        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem;border:1px solid var(--border);border-radius:6px;margin-bottom:0.5rem">
          <div>
            <div>${t.name}</div>
            <div style="color:var(--muted);font-size:0.75rem">${t.path}</div>
            <div style="font-size:0.75rem;margin-top:0.25rem">
              <span class="badge ${t.has_refresh_token?'success':'warn'}">${t.has_refresh_token?'可刷新':'无刷新'}</span>
              <span style="color:var(--muted);margin-left:0.5rem">${t.auth_method}</span>
            </div>
          </div>
          ${t.already_added?'<span class="badge info">已添加</span>':`<button class="secondary small" onclick="addFromScan('${t.path}','${t.name}')">添加</button>`}
        </div>
      `).join('');
    }else{
      alert('未找到 Token 文件');
    }
  }catch(e){alert('扫描失败: '+e.message)}
}

async function addFromScan(path,name){
  try{
    const r=await fetch('/api/token/add-from-scan',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({path,name})
    });
    const d=await r.json();
    if(d.ok){
      loadAccounts();
      scanTokens();
    }else{
      alert(d.detail||'添加失败');
    }
  }catch(e){alert('添加失败: '+e.message)}
}

async function checkTokens(){
  try{
    const r=await fetch('/api/token/refresh-check',{method:'POST'});
    const d=await r.json();
    let msg='Token 状态:\\n\\n';
    (d.accounts||[]).forEach(a=>{
      const status=a.valid?'✅ 有效':'❌ 无效';
      const extra=a.expiring_soon?' (即将过期)':'';
      const refresh=a.has_refresh_token?' [可刷新]':' [无法刷新]';
      msg+=`${a.name}: ${status}${extra}${refresh}\\n`;
    });
    alert(msg);
  }catch(e){alert('检查失败: '+e.message)}
}
'''

JS_SCRIPTS = JS_UTILS + JS_TABS + JS_STATUS + JS_MODELS + JS_CHAT + JS_STATS + JS_LOGS + JS_ACCOUNTS


# ==================== 组装最终 HTML ====================
HTML_PAGE = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kiro API</title>
<link rel="icon" type="image/svg+xml" href="/assets/icon.svg">
<style>
{CSS_STYLES}
</style>
</head>
<body>
<div class="container">
{HTML_BODY}
<div class="footer">Kiro API Proxy v1.3.0 - Token 自动刷新 | 动态指纹 | 配额管理</div>
</div>
<script>
{JS_SCRIPTS}
</script>
</body>
</html>'''
