<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#0A0E14">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
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
            --accent-red: #FF5252;
            --radius: 4px;
            --safe-bottom: env(safe-area-inset-bottom, 0px);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        html {
            -webkit-text-size-adjust: 100%;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            line-height: 1.4;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
            padding-bottom: calc(96px + var(--safe-bottom));
        }
        
        /* ============================================
           MOBILE-FIRST BASE (320px+)
           ============================================ */
        
        /* TOP BAR - Compact Sticky */
        .topbar {
            height: 40px;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 8px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }
        
        .topbar-left { display: flex; align-items: center; gap: 8px; }
        
        .logo {
            width: 24px;
            height: 24px;
            background: var(--accent-blue);
            border-radius: var(--radius);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: bold;
            color: #FFF;
            flex-shrink: 0;
        }
        
        .system-title { font-size: 15px; font-weight: bold; }
        .system-subtitle, .topbar-center, .node-info { display: none; }
        
        .topbar-right {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 9px;
        }
        
        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--accent-green);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        
        .uptime { color: var(--accent-cyan); font-size: 9px; }
        .label { display: none; }
        
        /* AGENT STRIP - Swipe Carousel */
        .agent-strip {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch;
            gap: 6px;
            padding: 6px 8px;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            margin-top: 40px;
            height: 52px;
            align-items: center;
            scrollbar-width: none;
        }
        .agent-strip::-webkit-scrollbar { display: none; }
        
        .agent-card {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 6px 10px;
            min-width: 105px;
            flex-shrink: 0;
            scroll-snap-align: start;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        
        .agent-card-header { display: flex; align-items: center; gap: 5px; }
        
        .agent-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        .agent-dot.active { background: var(--accent-green); }
        .agent-dot.running { background: var(--accent-blue); animation: pulse 1.5s infinite; }
        .agent-dot.analyzing { background: var(--accent-orange); animation: pulse 1.5s infinite; }
        .agent-dot.idle { background: var(--text-muted); }
        .agent-dot.measuring { background: var(--accent-cyan); }
        .agent-dot.reflecting { background: var(--accent-purple); }
        
        .agent-name {
            font-size: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
        }
        .agent-status {
            font-size: 9px;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 0.3px;
        }
        .agent-action { display: none; }
        
        /* MAIN CONTENT - Single Column */
        .main-content {
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding: 6px;
        }
        
        /* SYSTEM FEED - Full Width */
        .feed-panel {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            display: flex;
            flex-direction: column;
            max-height: 45vh;
            overflow: hidden;
        }
        
        .feed-tabs {
            display: flex;
            overflow-x: auto;
            white-space: nowrap;
            scrollbar-width: none;
            border-bottom: 1px solid var(--border);
            flex-shrink: 0;
        }
        .feed-tabs::-webkit-scrollbar { display: none; }
        
        .feed-tab {
            flex: none;
            min-width: auto;
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            color: var(--text-muted);
            padding: 7px 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 9px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            white-space: nowrap;
            min-height: 32px;
            -webkit-tap-highlight-color: transparent;
        }
        .feed-tab.active {
            background: var(--bg-secondary);
            border-bottom: 2px solid var(--accent-blue);
            color: var(--text-primary);
        }
        
        .feed-items {
            flex: 1;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        .feed-item {
            display: flex;
            align-items: flex-start;
            gap: 6px;
            padding: 5px 8px;
            border-bottom: 1px solid var(--border);
            font-size: 9px;
        }
        .feed-time { color: var(--text-muted); font-size: 8px; white-space: nowrap; min-width: 48px; }
        .feed-agent { text-transform: uppercase; font-size: 8px; font-weight: bold; min-width: 55px; letter-spacing: 0.3px; }
        .feed-message { color: var(--text-secondary); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .feed-status {
            font-size: 7px;
            text-transform: uppercase;
            background: var(--bg-secondary);
            padding: 1px 4px;
            border-radius: 2px;
            white-space: nowrap;
            flex-shrink: 0;
        }
        
        /* RIGHT PANELS - Accordion */
        .right-panel {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .card {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
        }
        
        .card-header {
            padding: 10px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            -webkit-tap-highlight-color: transparent;
            min-height: 40px;
            user-select: none;
        }
        .card-header:active { background: var(--bg-secondary); }
        
        .card-title {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-secondary);
            font-weight: bold;
        }
        
        .card-arrow {
            font-size: 8px;
            color: var(--text-muted);
            transition: transform 0.2s;
        }
        .card.collapsed .card-arrow { transform: rotate(-90deg); }
        
        .card-body {
            padding: 0 10px 10px 10px;
            display: block;
        }
        .card.collapsed .card-body { display: none; }
        
        /* Task rows */
        .task-row {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 5px 0;
            border-bottom: 1px solid var(--border);
            font-size: 9px;
        }
        .task-id { color: var(--accent-blue); font-weight: bold; min-width: 45px; font-size: 8px; }
        .task-title { flex: 1; color: var(--text-primary); font-size: 9px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .progress-bar { width: 40px; height: 3px; background: var(--border); border-radius: 2px; overflow: hidden; flex-shrink: 0; }
        .progress-fill { height: 100%; border-radius: 2px; }
        .progress-fill.high { background: var(--accent-green); }
        .progress-fill.medium { background: var(--accent-blue); }
        .progress-fill.low { background: var(--accent-orange); }
        .task-pct { color: var(--text-muted); font-size: 8px; min-width: 25px; text-align: right; }
        
        /* Gap rows */
        .gap-row {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 0;
            font-size: 9px;
        }
        .gap-icon { color: var(--accent-orange); font-size: 11px; flex-shrink: 0; }
        .gap-category {
            font-size: 7px;
            text-transform: uppercase;
            padding: 1px 4px;
            border-radius: 2px;
            background: var(--bg-secondary);
            color: var(--text-muted);
            flex-shrink: 0;
        }
        .gap-title { color: var(--text-secondary); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        
        /* Innovation rows */
        .innovation-row {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 0;
            font-size: 9px;
        }
        .innovation-icon { color: var(--accent-purple); flex-shrink: 0; }
        .innovation-title { color: var(--text-primary); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .innovation-feasibility {
            font-size: 7px;
            text-transform: uppercase;
            padding: 1px 4px;
            border-radius: 2px;
            flex-shrink: 0;
        }
        .feasibility-high { background: #1a3a2a; color: var(--accent-green); }
        .feasibility-medium { background: #2a2a1a; color: var(--accent-orange); }
        
        /* Metric rows */
        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 0;
            border-bottom: 1px solid var(--border);
            font-size: 9px;
        }
        .metric-name { color: var(--text-secondary); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .metric-value { font-weight: bold; margin: 0 6px; }
        .metric-trend { font-size: 7px; min-width: 50px; text-align: right; flex-shrink: 0; }
        .trend-up { color: var(--accent-green); }
        .trend-down { color: var(--accent-red); }
        
        /* FOOTER */
        .footer {
            text-align: center;
            padding: 4px;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            font-size: 7px;
            color: var(--text-muted);
            position: fixed;
            bottom: 48px;
            left: 0;
            right: 0;
            z-index: 80;
        }
        
        /* BOTTOM NAV - Mobile Only */
        .bottom-nav {
            display: flex;
            position: fixed;
            bottom: 48px;
            left: 0;
            right: 0;
            height: 40px;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            z-index: 90;
        }
        .bottom-nav-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 1px;
            color: var(--text-muted);
            font-size: 7px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
            border: none;
            background: transparent;
            font-family: 'JetBrains Mono', monospace;
            min-height: 40px;
        }
        .bottom-nav-item.active { color: var(--accent-blue); }
        .bottom-nav-icon { font-size: 12px; }
        
        /* COMMAND BAR - Fixed Bottom */
        .command-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 48px;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            padding: 0 8px;
            gap: 6px;
            z-index: 100;
            padding-bottom: var(--safe-bottom);
        }
        
        .command-input {
            flex: 1;
            display: flex;
            align-items: center;
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0 8px;
            height: 30px;
        }
        .command-prefix {
            color: var(--accent-blue);
            font-weight: bold;
            font-size: 12px;
            flex-shrink: 0;
        }
        .command-input input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            margin-left: 6px;
        }
        .command-input input::placeholder { color: var(--text-muted); opacity: 0.6; }
        
        .execute-btn {
            background: var(--accent-blue);
            color: #FFF;
            border: none;
            border-radius: var(--radius);
            padding: 6px 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 9px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
            white-space: nowrap;
            min-height: 30px;
        }
        .execute-btn:active { opacity: 0.8; }
        
        .suggestions { display: none; }
        
        /* ============================================
           TABLET: 768px+
           ============================================ */
        @media (min-width: 768px) {
            body { padding-bottom: calc(56px + var(--safe-bottom)); font-size: 12px; }
            
            .topbar { height: 44px; padding: 0 12px; }
            .logo { width: 26px; height: 26px; font-size: 14px; }
            .system-title { font-size: 17px; }
            .topbar-center { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-secondary); }
            .node-info { display: flex; align-items: center; gap: 4px; }
            .label { display: inline; color: var(--text-muted); font-size: 8px; }
            .uptime { font-size: 10px; }
            
            .agent-strip { height: 56px; gap: 8px; padding: 8px 12px; margin-top: 44px; }
            .agent-card { min-width: 120px; padding: 8px 10px; }
            .agent-name { font-size: 9px; }
            .agent-status { font-size: 10px; }
            .agent-action { display: block; font-size: 8px; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            
            .main-content { flex-direction: row; gap: 8px; padding: 8px; }
            .feed-panel { flex: 0.55; max-height: none; }
            .right-panel { flex: 0.45; }
            
            .feed-tab { padding: 8px 12px; font-size: 10px; }
            .feed-item { padding: 5px 10px; font-size: 10px; }
            .feed-time { font-size: 9px; min-width: 55px; }
            .feed-agent { font-size: 9px; min-width: 65px; }
            .feed-status { font-size: 8px; padding: 2px 5px; }
            
            .card-header { padding: 10px 12px; }
            .card-body { padding: 0 12px 12px 12px; }
            .card-title { font-size: 10px; }
            
            .task-row { font-size: 10px; }
            .gap-row { font-size: 10px; }
            .innovation-row { font-size: 10px; }
            .metric-row { font-size: 9px; }
            
            .command-bar { height: 48px; padding: 0 10px; gap: 8px; }
            .command-input { height: 32px; }
            .command-input input { font-size: 11px; }
            .execute-btn { padding: 6px 14px; font-size: 10px; }
            .suggestions { display: flex; gap: 5px; }
            .suggestion-chip {
                background: var(--bg-panel);
                border: 1px solid var(--border);
                border-radius: var(--radius);
                color: var(--text-muted);
                padding: 4px 8px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 8px;
                cursor: pointer;
                white-space: nowrap;
                -webkit-tap-highlight-color: transparent;
            }
            .suggestion-chip:active { border-color: var(--accent-blue); }
            
            .bottom-nav { display: none; }
            .footer { bottom: 48px; font-size: 8px; }
        }
        
        /* ============================================
           DESKTOP: 1440px+
           ============================================ */
        @media (min-width: 1440px) {
            body { padding-bottom: calc(60px + var(--safe-bottom)); }
            
            .topbar { height: 48px; padding: 0 16px; }
            .logo { width: 28px; height: 28px; font-size: 16px; }
            .system-title { font-size: 20px; }
            .system-subtitle { display: block; font-size: 9px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }
            .topbar-center { font-size: 14px; letter-spacing: 2px; }
            .uptime { font-size: 11px; }
            
            .agent-strip { height: 72px; gap: 10px; padding: 10px 16px; margin-top: 48px; }
            .agent-card { min-width: 140px; padding: 10px 14px; }
            .agent-name { font-size: 10px; letter-spacing: 1px; }
            .agent-status { font-size: 11px; }
            .agent-action { font-size: 10px; }
            
            .main-content { gap: 10px; padding: 10px; }
            .feed-panel { flex: 0.6; }
            .right-panel { flex: 0.4; gap: 6px; }
            
            .feed-tab { padding: 8px 12px; font-size: 10px; letter-spacing: 1px; }
            .feed-item { padding: 6px 12px; font-size: 11px; }
            .feed-time { font-size: 10px; min-width: 65px; }
            .feed-agent { font-size: 10px; min-width: 80px; }
            .feed-message { white-space: normal; }
            .feed-status { font-size: 9px; }
            
            .card-header { padding: 12px; }
            .card-body { padding: 0 12px 12px 12px; }
            .card-title { font-size: 11px; }
            
            .task-row { font-size: 10px; }
            .gap-row { font-size: 10px; }
            .innovation-row { font-size: 10px; }
            .metric-row { font-size: 10px; }
            
            .command-bar { height: 56px; padding: 0 16px; gap: 10px; }
            .command-input { height: 36px; padding: 0 12px; }
            .command-input input { font-size: 12px; }
            .execute-btn { padding: 8px 20px; font-size: 11px; letter-spacing: 1px; }
            .suggestion-chip { font-size: 10px; padding: 4px 10px; }
            
            .footer { bottom: 56px; font-size: 9px; }
        }
        
        /* Touch-friendly: no hover on mobile */
        @media (hover: none) {
            .card:hover { transform: none; border-color: var(--border); }
            .card:active { background: var(--bg-secondary); }
            .suggestion-chip:hover { border-color: var(--border); }
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 3px; height: 3px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
    </style>
</head>
<body>
    <!-- TOP BAR -->
    <div class="topbar">
        <div class="topbar-left">
            <div class="logo">J</div>
            <div>
                <div class="system-title">JARVIS</div>
                <div class="system-subtitle">Cognitive Operations System</div>
            </div>
        </div>
        <div class="topbar-center">COMMAND CENTER</div>
        <div class="topbar-right">
            <span class="node-info"><span class="label">NODE</span> Sakhipur</span>
            <div class="status-dot"></div>
            <span class="label">UPTIME</span>
            <span class="uptime">14h 32m</span>
        </div>
    </div>
    
    <!-- AGENT STRIP - Swipe Carousel -->
    <div class="agent-strip" id="agent-strip"></div>
    
    <!-- MAIN CONTENT -->
    <div class="main-content">
        <!-- LEFT: System Feed -->
        <div class="feed-panel">
            <div class="feed-tabs" id="feed-tabs"></div>
            <div class="feed-items" id="feed-items"></div>
        </div>
        
        <!-- RIGHT: Accordion Panels -->
        <div class="right-panel">
            <!-- Active Tasks -->
            <div class="card collapsed" id="card-tasks">
                <div class="card-header" onclick="toggleCard('card-tasks')">
                    <span class="card-title">ACTIVE TASKS</span>
                    <span class="card-arrow">▼</span>
                </div>
                <div class="card-body" id="active-tasks"></div>
            </div>
            
            <!-- Knowledge Gaps -->
            <div class="card collapsed" id="card-gaps">
                <div class="card-header" onclick="toggleCard('card-gaps')">
                    <span class="card-title">KNOWLEDGE GAPS</span>
                    <span class="card-arrow">▼</span>
                </div>
                <div class="card-body" id="knowledge-gaps"></div>
            </div>
            
            <!-- Innovations -->
            <div class="card collapsed" id="card-innovations">
                <div class="card-header" onclick="toggleCard('card-innovations')">
                    <span class="card-title">INNOVATIONS</span>
                    <span class="card-arrow">▼</span>
                </div>
                <div class="card-body" id="innovations"></div>
            </div>
            
            <!-- Performance Metrics -->
            <div class="card" id="card-metrics">
                <div class="card-header" onclick="toggleCard('card-metrics')">
                    <span class="card-title">METRICS</span>
                    <span class="card-arrow">▼</span>
                </div>
                <div class="card-body" id="metrics"></div>
            </div>
        </div>
    </div>
    
    <!-- BOTTOM NAVIGATION (Mobile Only) -->
    <nav class="bottom-nav">
        <button class="bottom-nav-item active" onclick="scrollToFeed()">
            <span class="bottom-nav-icon">📋</span>
            <span>Feed</span>
        </button>
        <button class="bottom-nav-item" onclick="toggleCard('card-tasks')">
            <span class="bottom-nav-icon">📝</span>
            <span>Tasks</span>
        </button>
        <button class="bottom-nav-item" onclick="toggleCard('card-gaps')">
            <span class="bottom-nav-icon">⚠️</span>
            <span>Gaps</span>
        </button>
        <button class="bottom-nav-item" onclick="toggleCard('card-metrics')">
            <span class="bottom-nav-icon">📊</span>
            <span>Metrics</span>
        </button>
    </nav>
    
    <!-- FOOTER -->
    <div class="footer">
        JARVIS v1.0.0 | All systems operational | <span id="sync-time">--:--:--</span>
    </div>
    
    <!-- COMMAND BAR -->
    <div class="command-bar">
        <div class="command-input">
            <span class="command-prefix">&gt;</span>
            <input type="text" id="command" placeholder="Command..." onkeypress="handleCommand(event)" autocomplete="off">
        </div>
        <button class="execute-btn" onclick="executeCommand()">EXEC</button>
        <div class="suggestions">
            <span class="suggestion-chip" onclick="setCommand('plan today')">plan today</span>
            <span class="suggestion-chip" onclick="setCommand('analyze')">analyze</span>
            <span class="suggestion-chip" onclick="setCommand('fix gaps')">fix gaps</span>
            <span class="suggestion-chip" onclick="setCommand('run loop')">run loop</span>
        </div>
    </div>
    
    <script>
        // ============================================
        // DATA
        // ============================================
        const agents = [
            { name: 'STRATEGIST', status: 'planning', action: 'Generating plan & tasks...', color: '#448AFF', dotClass: 'active' },
            { name: 'EXECUTOR', status: 'running', action: 'TSK-023 (65%)', color: '#00E676', dotClass: 'running' },
            { name: 'MENTOR', status: 'analyzing', action: 'Detecting knowledge gaps...', color: '#FF9100', dotClass: 'analyzing' },
            { name: 'INNOVATOR', status: 'idle', action: 'Waiting for trigger...', color: '#B388FF', dotClass: 'idle' },
            { name: 'AMPLIFIER', status: 'measuring', action: 'Performance metrics updated...', color: '#40C4FF', dotClass: 'measuring' },
            { name: 'REFLECTOR', status: 'reflecting', action: 'System reflection cycle...', color: '#FF80AB', dotClass: 'reflecting' },
        ];
        
        const feedData = [
            { time: '10:33:42', agent: 'AMPLIFIER', message: 'Performance metrics updated successfully.', category: 'SYSTEM', status: 'SYSTEM', color: '#40C4FF' },
            { time: '10:33:38', agent: 'MENTOR', message: 'Knowledge gap: "Advanced Ad Copy Techniques".', category: 'GAPS', status: 'GAP', color: '#FF9100' },
            { time: '10:33:34', agent: 'STRATEGIST', message: 'Plan: Weekly Growth Plan v2.1 generated.', category: 'TASKS', status: 'PLAN', color: '#448AFF' },
            { time: '10:33:29', agent: 'EXECUTOR', message: 'Completed TSK-022: Content Research.', category: 'TASKS', status: 'DONE', color: '#00E676' },
            { time: '10:33:25', agent: 'EXECUTOR', message: 'Started TSK-023: Facebook Ad Campaign.', category: 'TASKS', status: 'RUNNING', color: '#00E676' },
            { time: '10:33:20', agent: 'INNOVATOR', message: 'Idea: AI-Powered Ad Creative Generator.', category: 'INNOVATIONS', status: 'IDEA', color: '#B388FF' },
            { time: '10:33:15', agent: 'MENTOR', message: 'Analyzing gap: Ad Copywriting.', category: 'GAPS', status: 'ANALYSIS', color: '#FF9100' },
            { time: '10:33:10', agent: 'AMPLIFIER', message: 'Data collected from 12 sources.', category: 'SYSTEM', status: 'DATA', color: '#40C4FF' },
            { time: '10:33:05', agent: 'STRATEGIST', message: 'Generated 5 tasks from objectives.', category: 'TASKS', status: 'PLAN', color: '#448AFF' },
            { time: '10:32:58', agent: 'SYSTEM', message: 'Cognitive loop iteration started.', category: 'SYSTEM', status: 'LOOP', color: '#FF80AB' },
        ];
        
        const tasks = [
            { id: 'TSK-023', title: 'Facebook Ad Campaign', progress: 65 },
            { id: 'TSK-024', title: 'Content Writing', progress: 28 },
            { id: 'TSK-025', title: 'Competitor Analysis', progress: 0 },
        ];
        
        const gaps = [
            { category: 'SKILL', title: 'Ad Copywriting Skill' },
            { category: 'RESEARCH', title: 'Advanced Audience Research' },
            { category: 'TOOL', title: 'AI Ad Creative Generator' },
            { category: 'TOOL', title: 'Dynamic Budget Optimizer' },
            { category: 'STRATEGY', title: 'Smart Audience Segmentation' },
        ];
        
        const innovations = [
            { title: 'AI Ad Creative Generator', feasibility: 'high' },
            { title: 'Dynamic Budget Optimizer', feasibility: 'medium' },
            { title: 'Smart Audience Segmentation', feasibility: 'medium' },
        ];
        
        const metrics = [
            { name: 'Plan Compliance', value: '85%', trend: 'up', change: '12%' },
            { name: 'Tasks Completed Today', value: '12', trend: 'up', change: '28%' },
            { name: 'Active Tasks', value: '3', trend: 'down', change: '-25%' },
            { name: 'Knowledge Gaps', value: '2', trend: 'up', change: '33%' },
            { name: 'Innovations Generated', value: '3', trend: 'up', change: '50%' },
            { name: 'System Efficiency', value: '91%', trend: 'up', change: '8%' },
        ];
        
        // ============================================
        // RENDER FUNCTIONS
        // ============================================
        
        // Agent Strip
        function renderAgents() {
            const container = document.getElementById('agent-strip');
            container.innerHTML = agents.map(a => `
                <div class="agent-card" style="border-left: 3px solid ${a.color};">
                    <div class="agent-card-header">
                        <div class="agent-dot ${a.dotClass}"></div>
                        <span class="agent-name">${a.name}</span>
                    </div>
                    <div class="agent-status" style="color: ${a.color};">${a.status.toUpperCase()}</div>
                    <div class="agent-action">${a.action}</div>
                </div>
            `).join('');
        }
        
        // Feed Tabs
        const feedTabs = ['ALL', 'TASKS', 'GAPS', 'INNOVATIONS', 'SYSTEM'];
        let activeFeedTab = 'ALL';
        
        function renderFeedTabs() {
            const container = document.getElementById('feed-tabs');
            container.innerHTML = feedTabs.map(tab => `
                <button class="feed-tab ${tab === activeFeedTab ? 'active' : ''}" onclick="setFeedTab('${tab}')">${tab}</button>
            `).join('');
        }
        
        function setFeedTab(tab) {
            activeFeedTab = tab;
            renderFeedTabs();
            renderFeed();
        }
        
        function renderFeed() {
            const container = document.getElementById('feed-items');
            const items = activeFeedTab === 'ALL' ? feedData : feedData.filter(i => i.category === activeFeedTab);
            container.innerHTML = items.map(item => `
                <div class="feed-item" style="border-left: 3px solid ${item.color};">
                    <span class="feed-time">${item.time}</span>
                    <span class="feed-agent" style="color: ${item.color};">${item.agent}</span>
                    <span class="feed-message">${item.message}</span>
                    <span class="feed-status" style="color: ${item.color};">${item.status}</span>
                </div>
            `).join('');
        }
        
        // Tasks
        function renderTasks() {
            const container = document.getElementById('active-tasks');
            container.innerHTML = tasks.map(task => `
                <div class="task-row">
                    <span class="task-id">${task.id}</span>
                    <span class="task-title">${task.title}</span>
                    <div class="progress-bar">
                        <div class="progress-fill ${task.progress > 50 ? 'high' : task.progress > 25 ? 'medium' : 'low'}" style="width: ${task.progress}%;"></div>
                    </div>
                    <span class="task-pct">${task.progress}%</span>
                </div>
            `).join('');
        }
        
        // Gaps
        function renderGaps() {
            const container = document.getElementById('knowledge-gaps');
            container.innerHTML = gaps.map(gap => `
                <div class="gap-row">
                    <span class="gap-icon">⚠</span>
                    <span class="gap-category">${gap.category}</span>
                    <span class="gap-title">${gap.title}</span>
                </div>
            `).join('');
        }
        
        // Innovations
        function renderInnovations() {
            const container = document.getElementById('innovations');
            container.innerHTML = innovations.map(idea => `
                <div class="innovation-row">
                    <span class="innovation-icon">💡</span>
                    <span class="innovation-title">${idea.title}</span>
                    <span class="innovation-feasibility feasibility-${idea.feasibility}">${idea.feasibility.toUpperCase()}</span>
                </div>
            `).join('');
        }
        
        // Metrics
        function renderMetrics() {
            const container = document.getElementById('metrics');
            container.innerHTML = metrics.map(metric => `
                <div class="metric-row">
                    <span class="metric-name">${metric.name}</span>
                    <span class="metric-value">${metric.value}</span>
                    <span class="metric-trend trend-${metric.trend}">${metric.trend === 'up' ? '↑' : '↓'} ${metric.change}</span>
                </div>
            `).join('');
        }
        
        // ============================================
        // INTERACTIONS
        // ============================================
        
        // Accordion Toggle
        function toggleCard(id) {
            const card = document.getElementById(id);
            card.classList.toggle('collapsed');
            
            // Update bottom nav active state
            document.querySelectorAll('.bottom-nav-item').forEach(btn => btn.classList.remove('active'));
        }
        
        // Scroll to Feed (mobile)
        function scrollToFeed() {
            document.querySelector('.feed-panel').scrollIntoView({ behavior: 'smooth' });
            document.querySelectorAll('.bottom-nav-item').forEach(btn => btn.classList.remove('active'));
            document.querySelector('.bottom-nav-item').classList.add('active');
        }
        
        // Command
        function setCommand(cmd) {
            document.getElementById('command').value = cmd;
            document.getElementById('command').focus();
        }
        
        function executeCommand() {
            const cmd = document.getElementById('command').value.trim();
            if (cmd) {
                const now = new Date().toLocaleTimeString('en-US', { hour12: false });
                feedData.unshift({
                    time: now,
                    agent: 'SYSTEM',
                    message: `Command executed: ${cmd}`,
                    category: 'SYSTEM',
                    status: 'CMD',
                    color: '#448AFF'
                });
                renderFeed();
                document.getElementById('command').value = '';
                document.getElementById('command').blur();
            }
        }
        
        function handleCommand(event) {
            if (event.key === 'Enter') executeCommand();
        }
        
        // Clock
        function updateClock() {
            document.getElementById('sync-time').textContent = new Date().toLocaleTimeString('en-US', { hour12: true });
        }
        
        // ============================================
        // INIT
        // ============================================
        renderAgents();
        renderFeedTabs();
        renderFeed();
        renderTasks();
        renderGaps();
        renderInnovations();
        renderMetrics();
        updateClock();
        setInterval(updateClock, 1000);
        
        // Auto-update uptime
        setInterval(() => {
            const el = document.querySelector('.uptime');
            if (el) {
                const parts = el.textContent.split(' ');
                if (parts.length === 3) {
                    let h = parseInt(parts[0]), m = parseInt(parts[1]), s = parseInt(parts[2]) + 1;
                    if (s >= 60) { s = 0; m++; }
                    if (m >= 60) { m = 0; h++; }
                    el.textContent = `${h}h ${m}m ${s}s`;
                }
            }
        }, 1000);
    </script>
</body>
</html>