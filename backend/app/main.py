<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#0A0E14">
    <title>JARVIS - Cognitive Operations System</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        :root {
            --bg-primary: #0A0E14;
            --bg-secondary: #0F1419;
            --bg-panel: #151A22;
            --border: #232A34;
            --text-primary: #DDE4ED;
            --text-secondary: #8899AA;
            --text-muted: #4A5568;
            --accent-green: #00E676;
            --accent-blue: #448AFF;
            --accent-orange: #FF9100;
            --accent-purple: #B388FF;
            --accent-cyan: #40C4FF;
            --accent-pink: #FF80AB;
            --radius: 4px;
            --safe-bottom: env(safe-area-inset-bottom, 0px);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        html { -webkit-text-size-adjust: 100%; -webkit-tap-highlight-color: transparent; }
        
        body {
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            padding-bottom: calc(90px + var(--safe-bottom));
        }
        
        /* ===== HEADER ===== */
        .header {
            padding: 14px 12px 10px 12px;
            border-bottom: 1px solid var(--border);
        }
        .header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .logo h1 { font-size: 18px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.1; }
        .logo .sub { font-size: 9px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }
        .node { text-align: right; }
        .node .node-name { font-size: 10px; font-weight: 500; }
        .node .node-name span { color: var(--text-secondary); font-weight: 400; }
        .node .mode { font-size: 8px; color: var(--accent-green); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }
        
        /* ===== AGENT LIST ===== */
        .sec-title {
            padding: 10px 12px 6px 12px;
            font-size: 9px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-secondary);
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
        }
        .agent-list { background: var(--border); }
        .agent-row {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 9px 12px;
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border);
        }
        .agent-dot {
            width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
        }
        .dot-planning { background: var(--accent-blue); animation: pulse 2s infinite; }
        .dot-running { background: var(--accent-green); animation: pulse 1.2s infinite; }
        .dot-analyzing { background: var(--accent-orange); animation: pulse 1.5s infinite; }
        .dot-idle { background: var(--text-muted); }
        .dot-measuring { background: var(--accent-cyan); animation: pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }
        
        .agent-mid { flex: 1; display: flex; justify-content: space-between; align-items: center; }
        .agent-name { font-size: 10px; font-weight: 500; }
        .agent-status { font-size: 8px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .agent-act { font-size: 8px; color: var(--text-muted); text-align: right; max-width: 130px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        
        /* ===== SYSTEM FEED ===== */
        .feed-tabs {
            display: flex; overflow-x: auto; scrollbar-width: none;
            border-bottom: 1px solid var(--border); background: var(--bg-primary);
        }
        .feed-tabs::-webkit-scrollbar { display: none; }
        .feed-tab {
            flex: none; padding: 7px 11px;
            font-family: 'JetBrains Mono', monospace; font-size: 8px;
            text-transform: uppercase; letter-spacing: 1px;
            color: var(--text-muted); background: transparent; border: none;
            border-bottom: 2px solid transparent; cursor: pointer; white-space: nowrap;
        }
        .feed-tab.on { color: var(--text-primary); border-bottom-color: var(--accent-blue); }
        
        .feed-items { max-height: 240px; overflow-y: auto; }
        .feed-row {
            display: flex; gap: 7px; padding: 6px 12px;
            border-bottom: 1px solid var(--border); font-size: 9px; align-items: flex-start;
        }
        .feed-tm { color: var(--text-muted); font-size: 8px; min-width: 48px; white-space: nowrap; }
        .feed-tag {
            font-size: 7px; font-weight: 700; text-transform: uppercase;
            padding: 1px 4px; border-radius: 2px; white-space: nowrap; letter-spacing: 0.3px;
        }
        .tg-s { background: #1a2a3a; color: var(--accent-blue); }
        .tg-e { background: #1a2a1a; color: var(--accent-green); }
        .tg-m { background: #2a1a0a; color: var(--accent-orange); }
        .tg-i { background: #1a0a2a; color: var(--accent-purple); }
        .tg-a { background: #0a1a2a; color: var(--accent-cyan); }
        .tg-r { background: #2a0a1a; color: var(--accent-pink); }
        .feed-msg { color: var(--text-secondary); flex: 1; }
        .feed-more { text-align: center; padding: 8px; font-size: 8px; color: var(--text-muted); opacity: 0.5; font-style: italic; }
        
        /* ===== PANELS ===== */
        .panels { background: var(--border); }
        .panel {
            background: var(--bg-primary); padding: 10px 12px;
            border-bottom: 1px solid var(--border);
        }
        .panel h3 {
            font-size: 9px; text-transform: uppercase; letter-spacing: 2px;
            color: var(--text-secondary); margin-bottom: 6px; font-weight: 700;
        }
        .panel .empty { font-size: 9px; color: var(--text-muted); opacity: 0.7; }
        .stat-r { display: flex; justify-content: space-between; padding: 3px 0; font-size: 9px; }
        .stat-l { color: var(--text-muted); }
        .stat-v { color: var(--text-secondary); }
        
        /* ===== COMMAND ===== */
        .cmd-bar {
            position: fixed; bottom: 0; left: 0; right: 0;
            background: var(--bg-secondary); border-top: 1px solid var(--border);
            padding: 7px 12px; padding-bottom: max(7px, var(--safe-bottom));
            z-index: 100;
        }
        .cmd-wrap {
            display: flex; align-items: center;
            background: var(--bg-primary); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 0 9px; height: 32px; margin-bottom: 6px;
        }
        .cmd-pfx { color: var(--accent-blue); font-weight: 700; font-size: 12px; margin-right: 7px; }
        .cmd-wrap input {
            flex: 1; background: transparent; border: none; outline: none;
            color: var(--text-primary); font-family: 'JetBrains Mono', monospace; font-size: 10px;
        }
        .cmd-wrap input::placeholder { color: var(--text-muted); opacity: 0.5; }
        .chips { display: flex; gap: 5px; overflow-x: auto; scrollbar-width: none; }
        .chips::-webkit-scrollbar { display: none; }
        .chip {
            flex: none; padding: 5px 10px; border: 1px solid var(--border);
            border-radius: var(--radius); font-family: 'JetBrains Mono', monospace;
            font-size: 8px; color: var(--text-muted); cursor: pointer; white-space: nowrap;
            background: var(--bg-primary);
        }
        .chip:active { border-color: var(--accent-blue); color: var(--text-primary); }
    </style>
</head>
<body>

<!-- HEADER -->
<div class="header">
    <div class="header-row">
        <div class="logo">
            <h1>JARVIS</h1>
            <div class="sub">Mahedi Muktadir</div>
        </div>
        <div class="node">
            <div class="node-name"><span>Node:</span> Sakhipur</div>
            <div class="mode">Autonomous</div>
        </div>
    </div>
</div>

<!-- AGENTS -->
<div class="sec-title">Agents</div>
<div class="agent-list" id="agents"></div>

<!-- SYSTEM FEED -->
<div class="sec-title">System Feed</div>
<div class="feed-tabs" id="tabs"></div>
<div class="feed-items" id="feed"></div>

<!-- PANELS -->
<div class="panels">
    <div class="panel"><h3>Active Tasks</h3><div class="empty">No active tasks</div></div>
    <div class="panel"><h3>Knowledge Gaps</h3><div class="empty">No gaps identified</div></div>
    <div class="panel"><h3>Innovations</h3><div class="empty">No innovations generated</div></div>
    <div class="panel" id="metrics-panel"><h3>Performance Metrics</h3></div>
    <div class="panel" id="sys-panel"><h3>System Status</h3></div>
</div>

<!-- COMMAND -->
<div class="cmd-bar">
    <div class="cmd-wrap">
        <span class="cmd-pfx">&gt;</span>
        <input id="cmd" placeholder="Type a command for JARVIS..." onkeypress="if(event.key==='Enter')exec()" autocomplete="off">
    </div>
    <div class="chips">
        <span class="chip" onclick="sc('plan next 7 days')">plan next 7 days</span>
        <span class="chip" onclick="sc('analyze performance')">analyze performance</span>
        <span class="chip" onclick="sc('fix knowledge gaps')">fix knowledge gaps</span>
        <span class="chip" onclick="sc('generate innovations')">generate innovations</span>
    </div>
</div>

<script>
const agents = [
    {n:'Strategist',s:'PLANNING',a:'Generating 5 tasks...',c:'#448AFF',d:'dot-planning'},
    {n:'Executor',s:'RUNNING',a:'TSK-001',p:65,c:'#00E676',d:'dot-running'},
    {n:'Mentor',s:'ANALYZING',a:'Detecting gaps...',c:'#FF9100',d:'dot-analyzing'},
    {n:'Innovator',s:'IDLE',a:'Waiting for trigger...',c:'#B388FF',d:'dot-idle'},
    {n:'Amplifier',s:'MEASURING',a:'Updating metrics...',c:'#40C4FF',d:'dot-measuring'},
    {n:'Reflector',s:'IDLE',a:'System reflection...',c:'#FF80AB',d:'dot-idle'}
];

const feed = [
    {t:'10:32:14',a:'STRATEGIST',m:'Plan generated: "Sakhipur Growth Plan Q2"',g:'tg-s'},
    {t:'10:32:18',a:'EXECUTOR',m:'Started task TSK-001: Market Research',g:'tg-e'},
    {t:'10:32:45',a:'EXECUTOR',m:'Task TSK-001 progress: 65%',g:'tg-e'},
    {t:'10:33:01',a:'MENTOR',m:'Knowledge gap detected: Ad Copywriting Skill',g:'tg-m'},
    {t:'10:33:05',a:'MENTOR',m:'Knowledge gap detected: Funnel Optimization',g:'tg-m'},
    {t:'10:33:22',a:'INNOVATOR',m:'Generated idea: Content Repurposing Engine',g:'tg-i'},
    {t:'10:33:40',a:'AMPLIFIER',m:'Performance metrics updated',g:'tg-a'},
    {t:'10:34:02',a:'REFLECTOR',m:'System reflection cycle completed',g:'tg-r'}
];

const tabs=['ALL','TASKS','GAPS','INNOVATIONS','SYSTEM'];
let cur='ALL';

document.getElementById('agents').innerHTML=agents.map(a=>
    `<div class="agent-row">
        <div class="agent-dot ${a.d}"></div>
        <div class="agent-mid">
            <span class="agent-name">${a.n}</span>
            <span class="agent-status" style="color:${a.c}">${a.s}</span>
        </div>
        <div class="agent-act">${a.p?a.a+' '+a.p+'%':a.a}</div>
    </div>`
).join('');

function rTabs(){
    document.getElementById('tabs').innerHTML=tabs.map(t=>
        `<button class="feed-tab${t===cur?' on':''}" onclick="sw('${t}')">${t}</button>`
    ).join('');
}
function sw(t){cur=t;rTabs();rFeed();}
function rFeed(){
    const f=cur==='ALL'?feed:feed.filter(i=>{
        if(cur==='SYSTEM')return i.a==='AMPLIFIER'||i.a==='REFLECTOR';
        return i.a===cur.slice(0,-1);
    });
    document.getElementById('feed').innerHTML=f.map(i=>
        `<div class="feed-row">
            <span class="feed-tm">${i.t}</span>
            <span class="feed-tag ${i.g}">${i.a}</span>
            <span class="feed-msg">${i.m}</span>
        </div>`
    ).join('')+'<div class="feed-more">Swipe up to load more</div>';
}

document.getElementById('metrics-panel').innerHTML='<h3>Performance Metrics</h3>'+
    ['Plan Compliance','Tasks Today','Task Success Rate','System Efficiency'].map(l=>
        `<div class="stat-r"><span class="stat-l">${l}</span><span class="stat-v">—${l.includes('Rate')||l.includes('Compliance')||l.includes('Efficiency')?'%':''}</span></div>`
    ).join('');

document.getElementById('sys-panel').innerHTML='<h3>System Status</h3>'+
    ['Overall Health','Active Agents','Queue Length','Last Cycle'].map(l=>
        `<div class="stat-r"><span class="stat-l">${l}</span><span class="stat-v">${l==='Active Agents'?'— / 6':'—'}</span></div>`
    ).join('');

function sc(c){document.getElementById('cmd').value=c;document.getElementById('cmd').focus();}
function exec(){const c=document.getElementById('cmd').value.trim();if(c){alert('Executing: '+c);document.getElementById('cmd').value='';}}

rTabs();rFeed();
</script>
</body>
</html>