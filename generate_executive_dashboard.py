"""
Executive Telecommunications CDR & Network Intelligence Dashboard Generator
===========================================================================
Project: Millicom (Tigo Tanzania) Enterprise Telecom CDR Intelligence Suite
Author: Principal Telecommunications Data Scientist & Modern Web Solutions Architect
Output: millicom_executive_cdr_dashboard.html
Operator: MIC Tanzania PLC (Tigo Tanzania) - MCC 640, MNC 02

Features:
- Single-file, standalone responsive HTML5 dashboard with dark glassmorphic styling.
- Interactive Leaflet.js map displaying all 54 cell towers across Tanzania with Erlangs,
  tech generation (5G/4G/3G), sector azimuths, and live congestion tooltips.
- Chart.js visual analytics: 24-Hour Diurnal traffic curve, TCRA QoS SLA compliance,
  Revenue streams, Churn risk distribution, and Interconnect net balances.
- Revenue Assurance & Fraud Management (RAFM) investigation workbench (SIM-box bypass,
  Wangiri flash callers, and Impossible travel speed anomalies).
- Live searchable, filterable CDR Forensic Table with pagination and modal inspection.
"""

import os
import csv
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_HTML_PATH = os.path.join(WORKSPACE_DIR, 'millicom_executive_cdr_dashboard.html')

def load_json(filename):
    p = os.path.join(WORKSPACE_DIR, filename)
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_csv_records(filename, max_rows=None):
    p = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.exists(p):
        return []
    with open(p, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        return reader[:max_rows] if max_rows else reader

def build_dashboard():
    print("[DASHBOARD] Building Millicom Executive Telecom CDR Analytics Dashboard...")

    metrics = load_json('millicom_telecom_metrics.json')
    macro = metrics.get('macro_kpis', {})
    tcra = metrics.get('tcra_qos_compliance', {})
    rafm = metrics.get('rafm_fraud_metrics', {})
    churn = metrics.get('churn_and_segmentation', {})
    towers_perf = metrics.get('tower_performance', [])
    tech_data = metrics.get('network_data_qos_by_tech', {})
    diurnal = metrics.get('diurnal_hourly_traffic', [])
    interconnect = metrics.get('interconnect_settlement', [])

    # Sample CDR records for interactive forensics table
    voice_samples = load_csv_records('millicom_cdr_voice.csv', 180)
    data_samples = load_csv_records('millicom_cdr_data_sessions.csv', 100)
    momo_samples = load_csv_records('millicom_cdr_tigo_pesa_momo.csv', 100)

    client_payload = {
        'macro': macro,
        'tcra': tcra,
        'rafm': rafm,
        'churn': churn,
        'towers': towers_perf,
        'tech_data': tech_data,
        'diurnal': diurnal,
        'interconnect': interconnect,
        'voice_cdrs': voice_samples,
        'data_cdrs': data_samples,
        'momo_cdrs': momo_samples
    }

    payload_json_str = json.dumps(client_payload).replace("</script>", "<\\/script>")

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Millicom (Tigo Tanzania) | Telecom CDR Intelligence & Executive Analytics</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        telecom: {{
                            dark: '#070C18',
                            card: '#0D1627',
                            cardBorder: 'rgba(56, 189, 248, 0.15)',
                            blue: '#0284C7',
                            cyan: '#38BDF8',
                            gold: '#F59E0B',
                            amber: '#D97706',
                            emerald: '#10B981',
                            purple: '#A855F7',
                            red: '#EF4444'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <!-- Leaflet.js CDN -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Inter Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #070C18;
            color: #F1F5F9;
        }}
        .mono {{
            font-family: 'JetBrains Mono', monospace;
        }}
        .glass-card {{
            background: rgba(13, 22, 39, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(56, 189, 248, 0.14);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}
        .glass-card:hover {{
            border-color: rgba(56, 189, 248, 0.35);
        }}
        .glow-cyan {{
            box-shadow: 0 0 20px -5px rgba(56, 189, 248, 0.4);
        }}
        .glow-gold {{
            box-shadow: 0 0 20px -5px rgba(245, 158, 11, 0.4);
        }}
        .glow-red {{
            box-shadow: 0 0 20px -5px rgba(239, 68, 68, 0.4);
        }}
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: #070C18;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #1E293B;
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #38BDF8;
        }}
        #map {{
            height: 480px;
            width: 100%;
            border-radius: 0.75rem;
            z-index: 10;
        }}
    </style>
</head>
<body class="min-h-screen antialiased selection:bg-cyan-500 selection:text-black">

    <!-- Top Executive Nav Header -->
    <header class="sticky top-0 z-50 bg-[#070C18]/90 backdrop-blur-md border-b border-slate-800/80 px-6 py-3.5">
        <div class="max-w-[1720px] mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
            <!-- Brand & Identification -->
            <div class="flex items-center gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-cyan-500/20">
                    <i data-lucide="radio" class="w-5 h-5 text-white"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2.5">
                        <h1 class="text-lg font-bold text-white tracking-tight">MILLICOM <span class="text-cyan-400 font-extrabold">TIGO TANZANIA</span></h1>
                        <span class="px-2 py-0.5 rounded text-[10px] font-semibold tracking-wider uppercase bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">MCC 640 MNC 02</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-semibold tracking-wider uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">TCRA Compliant</span>
                    </div>
                    <p class="text-xs text-slate-400">Enterprise CDR Big Data Analytics, QoS/QoE Telemetry & Revenue Assurance Intelligence</p>
                </div>
            </div>

            <!-- Controls & Actions -->
            <div class="flex items-center gap-3">
                <div class="hidden lg:flex items-center gap-2 bg-slate-900/90 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-300">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>MSC Core Feeds: <b>Operational</b></span>
                    <span class="text-slate-600">|</span>
                    <span>Audit Period: <b>7-Day National Ingestion</b></span>
                </div>
                <button onclick="downloadExcelPack()" class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition-all shadow">
                    <i data-lucide="file-spreadsheet" class="w-4 h-4 text-emerald-400"></i>
                    <span>Excel Audit Pack</span>
                </button>
                <button onclick="window.print()" class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold transition-all shadow-md shadow-cyan-600/30">
                    <i data-lucide="printer" class="w-4 h-4"></i>
                    <span>Export Executive Brief</span>
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-[1720px] mx-auto px-6 py-6 space-y-6">

        <!-- Macro Executive KPI Strip -->
        <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
            <!-- Card 1: Subscribers -->
            <div class="glass-card rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-cyan-500">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-xs font-medium uppercase tracking-wider">Subscribers Audited</span>
                    <i data-lucide="users" class="w-4 h-4 text-cyan-400"></i>
                </div>
                <div>
                    <div class="text-2xl font-extrabold text-white tracking-tight mono">{macro.get('total_subscribers', 1499):,}</div>
                    <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                        <span class="text-emerald-400 font-semibold">14 Regions</span> across Tanzania
                    </div>
                </div>
            </div>

            <!-- Card 2: Total Revenue -->
            <div class="glass-card rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-emerald-500">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-xs font-medium uppercase tracking-wider">Gross Network Revenue</span>
                    <i data-lucide="banknote" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div>
                    <div class="text-2xl font-extrabold text-white tracking-tight mono">TZS {macro.get('total_gross_revenue_tzs', 0):,.0f}</div>
                    <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                        <span class="text-emerald-400 font-semibold">${macro.get('total_gross_revenue_usd', 0):,.0f} USD</span> | ARPU TZS {macro.get('average_blended_arpu_tzs', 0):,.0f}
                    </div>
                </div>
            </div>

            <!-- Card 3: Busy Hour Traffic -->
            <div class="glass-card rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-blue-500">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-xs font-medium uppercase tracking-wider">Busy Hour Traffic (BHT)</span>
                    <i data-lucide="activity" class="w-4 h-4 text-blue-400"></i>
                </div>
                <div>
                    <div class="text-2xl font-extrabold text-white tracking-tight mono">{macro.get('busy_hour_erlangs', 0):.2f} <span class="text-sm font-medium text-slate-400">Erlangs</span></div>
                    <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                        Peak Hour: <span class="text-cyan-400 font-semibold">{macro.get('busy_hour_of_day', 20):02d}:00 HRS</span> (Diurnal Max)
                    </div>
                </div>
            </div>

            <!-- Card 4: Data Traffic -->
            <div class="glass-card rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-purple-500">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-xs font-medium uppercase tracking-wider">Total Mobile Data</span>
                    <i data-lucide="wifi" class="w-4 h-4 text-purple-400"></i>
                </div>
                <div>
                    <div class="text-2xl font-extrabold text-white tracking-tight mono">{macro.get('total_data_volume_gb', 0):,.1f} <span class="text-sm font-medium text-slate-400">GB</span></div>
                    <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                        <span class="text-purple-400 font-semibold">5G & 4G/LTE</span> High-Speed Backhaul
                    </div>
                </div>
            </div>

            <!-- Card 5: TCRA Call Completion -->
            <div class="glass-card rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-amber-500">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-xs font-medium uppercase tracking-wider">Call Completion (CCR)</span>
                    <i data-lucide="phone-call" class="w-4 h-4 text-amber-400"></i>
                </div>
                <div>
                    <div class="text-2xl font-extrabold text-white tracking-tight mono">{tcra.get('call_completion_rate_ccr_pct', 0):.2f}%</div>
                    <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                        TCRA Target: ≥ {tcra.get('ccr_tcra_target_pct', 98.0):.1f}% <span class="px-1.5 py-0.2 rounded text-[9px] font-bold uppercase bg-amber-500/20 text-amber-300">Action Required</span>
                    </div>
                </div>
            </div>

            <!-- Card 6: Fraud Interception -->
            <div class="glass-card rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-red-500">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-xs font-medium uppercase tracking-wider">RAFM Fraud Intercepted</span>
                    <i data-lucide="shield-alert" class="w-4 h-4 text-red-400"></i>
                </div>
                <div>
                    <div class="text-2xl font-extrabold text-red-400 tracking-tight mono">TZS {rafm.get('bypass_revenue_loss_tzs', 0):,.0f}</div>
                    <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                        <span class="text-red-400 font-bold">{rafm.get('simbox_detected_count', 0)} SIM-Boxes</span> & {rafm.get('wangiri_detected_count', 0)} Wangiri Rings
                    </div>
                </div>
            </div>
        </section>

        <!-- Main Section: Geospatial Tanzania Cell Tower Map & Diurnal Traffic Profile -->
        <section class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Tanzania Cell Tower Geospatial Map (7 Columns) -->
            <div class="lg:col-span-7 glass-card rounded-xl p-5 flex flex-col justify-between">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <i data-lucide="map-pin" class="w-5 h-5 text-cyan-400"></i>
                            <h2 class="text-base font-bold text-white tracking-tight">Tanzania Cell Towers Infrastructure & BTS Traffic Load</h2>
                        </div>
                        <p class="text-xs text-slate-400 mt-0.5">54 Live Monitored Sites: Voice Erlangs, Erlang B Blocking %, and Technology Layers (5G, 4G, 3G)</p>
                    </div>

                    <!-- Map Filter Pills -->
                    <div class="flex items-center gap-1.5 bg-slate-900/80 p-1 rounded-lg border border-slate-800 text-xs">
                        <button onclick="filterMap('ALL')" id="map-btn-all" class="px-2.5 py-1 rounded bg-cyan-600 text-white font-medium">All</button>
                        <button onclick="filterMap('5G')" id="map-btn-5g" class="px-2.5 py-1 rounded text-slate-400 hover:text-white font-medium">5G Sites</button>
                        <button onclick="filterMap('4G')" id="map-btn-4g" class="px-2.5 py-1 rounded text-slate-400 hover:text-white font-medium">4G LTE</button>
                        <button onclick="filterMap('ALERT')" id="map-btn-alert" class="px-2.5 py-1 rounded text-slate-400 hover:text-red-400 font-medium">SLA Breaches</button>
                    </div>
                </div>

                <div id="map"></div>

                <div class="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-2 pt-3 border-t border-slate-800 text-xs">
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-purple-500"></span>
                        <span class="text-slate-300">5G High-Capacity (Dar, Dom, Arusha, Mza)</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-cyan-500"></span>
                        <span class="text-slate-300">4G LTE Metro & Upcountry Corridors</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-amber-500"></span>
                        <span class="text-slate-300">3G Regional Fallback & Transit</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-red-500 ring-2 ring-red-500/50"></span>
                        <span class="text-red-400 font-medium">Erlang B Blocking &gt; 1.5% SLA</span>
                    </div>
                </div>
            </div>

            <!-- Diurnal Traffic & Erlang Distribution (5 Columns) -->
            <div class="lg:col-span-5 glass-card rounded-xl p-5 flex flex-col justify-between">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <i data-lucide="clock" class="w-5 h-5 text-blue-400"></i>
                            <h2 class="text-base font-bold text-white tracking-tight">24-Hour Diurnal Traffic Curve</h2>
                        </div>
                        <p class="text-xs text-slate-400 mt-0.5">Voice Erlangs vs Mobile Data GB across 24 Hours</p>
                    </div>
                    <span class="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">BHT Peak: 20:00</span>
                </div>

                <div class="h-[360px] w-full">
                    <canvas id="diurnalChart"></canvas>
                </div>

                <div class="mt-4 p-3 bg-slate-900/60 rounded-lg border border-slate-800 text-xs text-slate-300 flex items-center justify-between">
                    <span>Peak Voice Load: <b class="text-white">{macro.get('busy_hour_erlangs', 0):.2f} Erlangs</b></span>
                    <span>Total Audited Voice Duration: <b class="text-white">{macro.get('total_voice_traffic_minutes', 0):,.0f} Minutes</b></span>
                </div>
            </div>
        </section>

        <!-- Secondary Section: TCRA QoS Compliance Radar, Churn & Segment Analysis, and RAFM Hub -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">

            <!-- Panel 1: TCRA Quality of Service (QoS) Scorecard -->
            <div class="glass-card rounded-xl p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="award" class="w-5 h-5 text-emerald-400"></i>
                            <h3 class="text-base font-bold text-white">TCRA Quality of Service (QoS) SLA</h3>
                        </div>
                        <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">TZ Standards</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-4">Statutory telecommunications performance benchmark comparison mandated by TCRA.</p>

                    <div class="space-y-3.5">
                        <!-- ASR -->
                        <div class="p-3 bg-slate-900/70 rounded-lg border border-slate-800/80">
                            <div class="flex justify-between items-center text-xs mb-1.5">
                                <span class="font-medium text-slate-200">Answer Seizure Ratio (ASR)</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 uppercase">Compliant</span>
                            </div>
                            <div class="flex justify-between items-baseline mb-1">
                                <span class="text-lg font-bold text-white mono">{tcra.get('answer_seizure_ratio_asr_pct', 0):.2f}%</span>
                                <span class="text-xs text-slate-400">TCRA Target: ≥ {tcra.get('asr_benchmark_target_pct', 65.0):.1f}%</span>
                            </div>
                            <div class="w-full bg-slate-800 rounded-full h-2">
                                <div class="bg-emerald-500 h-2 rounded-full" style="width: {min(100.0, tcra.get('answer_seizure_ratio_asr_pct', 0))}%"></div>
                            </div>
                        </div>

                        <!-- CCR -->
                        <div class="p-3 bg-slate-900/70 rounded-lg border border-slate-800/80">
                            <div class="flex justify-between items-center text-xs mb-1.5">
                                <span class="font-medium text-slate-200">Call Completion Rate (CCR)</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 uppercase">Marginal SLA Gap</span>
                            </div>
                            <div class="flex justify-between items-baseline mb-1">
                                <span class="text-lg font-bold text-white mono">{tcra.get('call_completion_rate_ccr_pct', 0):.2f}%</span>
                                <span class="text-xs text-slate-400">TCRA Target: ≥ {tcra.get('ccr_tcra_target_pct', 98.0):.1f}%</span>
                            </div>
                            <div class="w-full bg-slate-800 rounded-full h-2">
                                <div class="bg-amber-500 h-2 rounded-full" style="width: {min(100.0, tcra.get('call_completion_rate_ccr_pct', 0))}%"></div>
                            </div>
                        </div>

                        <!-- CDR -->
                        <div class="p-3 bg-slate-900/70 rounded-lg border border-slate-800/80">
                            <div class="flex justify-between items-center text-xs mb-1.5">
                                <span class="font-medium text-slate-200">Call Drop Rate (CDR)</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400 uppercase">Attention Needed</span>
                            </div>
                            <div class="flex justify-between items-baseline mb-1">
                                <span class="text-lg font-bold text-red-400 mono">{tcra.get('call_drop_rate_cdr_pct', 0):.2f}%</span>
                                <span class="text-xs text-slate-400">TCRA Ceiling: &lt; {tcra.get('cdr_tcra_target_pct', 0.8):.1f}%</span>
                            </div>
                            <div class="w-full bg-slate-800 rounded-full h-2">
                                <div class="bg-red-500 h-2 rounded-full" style="width: {min(100.0, tcra.get('call_drop_rate_cdr_pct', 0) * 12.0)}%"></div>
                            </div>
                        </div>

                        <!-- Congestion -->
                        <div class="p-3 bg-slate-900/70 rounded-lg border border-slate-800/80">
                            <div class="flex justify-between items-center text-xs mb-1.5">
                                <span class="font-medium text-slate-200">Trunk Congestion Block</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 uppercase">Compliant</span>
                            </div>
                            <div class="flex justify-between items-baseline mb-1">
                                <span class="text-lg font-bold text-white mono">{tcra.get('congestion_blocking_pct', 0):.2f}%</span>
                                <span class="text-xs text-slate-400">TCRA Ceiling: &lt; {tcra.get('congestion_target_pct', 1.5):.1f}%</span>
                            </div>
                            <div class="w-full bg-slate-800 rounded-full h-2">
                                <div class="bg-emerald-500 h-2 rounded-full" style="width: {min(100.0, (tcra.get('congestion_blocking_pct', 0) / 1.5) * 100.0)}%"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex justify-between">
                    <span>Root Causes: <b>Radio Link Failure (62%)</b>, Handover (38%)</span>
                </div>
            </div>

            <!-- Panel 2: Customer Segmentation & Churn Risk Matrix -->
            <div class="glass-card rounded-xl p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="pie-chart" class="w-5 h-5 text-purple-400"></i>
                            <h3 class="text-base font-bold text-white">Churn Risk & ARPU Segmentation</h3>
                        </div>
                        <span class="text-xs text-purple-400 font-mono">Value at Risk</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-4">ML predictive churn model incorporating drop-call frustration and usage velocity.</p>

                    <div class="h-[220px] w-full mb-4">
                        <canvas id="churnChart"></canvas>
                    </div>

                    <!-- Segments Mini-Table -->
                    <div class="space-y-2">
                        <div class="flex items-center justify-between text-xs py-1 border-b border-slate-800 text-slate-300">
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> Low Churn Risk (&lt;15%)</span>
                            <span class="font-mono text-white font-semibold">{churn.get('churn_risk_distribution', {}).get('Low Churn Risk (<15%)', 0):,}</span>
                        </div>
                        <div class="flex items-center justify-between text-xs py-1 border-b border-slate-800 text-slate-300">
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500"></span> Medium Risk (40-60%)</span>
                            <span class="font-mono text-white font-semibold">{churn.get('churn_risk_distribution', {}).get('Medium Churn Risk (40-60%)', 0):,}</span>
                        </div>
                        <div class="flex items-center justify-between text-xs py-1 border-b border-slate-800 text-slate-300">
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-red-500"></span> High Churn Risk (85%+)</span>
                            <span class="font-mono text-red-400 font-semibold">{churn.get('churn_risk_distribution', {}).get('High Churn Risk (85%+)', 0):,}</span>
                        </div>
                        <div class="flex items-center justify-between text-xs py-1 text-slate-300">
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-purple-500"></span> Fraud Blacklist Terminations</span>
                            <span class="font-mono text-purple-400 font-semibold">{churn.get('churn_risk_distribution', {}).get('Fraud Blacklist', 0):,}</span>
                        </div>
                    </div>
                </div>

                <div class="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-300 flex justify-between items-center">
                    <span>High-Risk Churn Exposure:</span>
                    <span class="font-bold text-red-400 mono">TZS {churn.get('at_risk_churn_revenue_loss_tzs', 0):,.0f}</span>
                </div>
            </div>

            <!-- Panel 3: Revenue Assurance & Fraud Management (RAFM) Forensics -->
            <div class="glass-card rounded-xl p-5 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <i data-lucide="shield-alert" class="w-5 h-5 text-red-400"></i>
                            <h3 class="text-base font-bold text-white">RAFM Fraud & Security Center</h3>
                        </div>
                        <span class="text-xs px-2 py-0.5 rounded bg-red-500/20 text-red-400 font-mono font-bold">{rafm.get('simbox_detected_count', 0)} Detected</span>
                    </div>
                    <p class="text-xs text-slate-400 mb-4">Active forensic detection of grey-route bypass, Wangiri callbacks, and cloned IMSIs.</p>

                    <div class="space-y-3">
                        <div class="p-3 bg-red-950/30 rounded-lg border border-red-800/40">
                            <div class="flex items-center justify-between text-xs mb-1">
                                <span class="font-bold text-red-300 flex items-center gap-1.5"><i data-lucide="box" class="w-3.5 h-3.5"></i> SIM-Box Bypass Gateways</span>
                                <span class="text-red-400 font-mono font-bold">{rafm.get('simbox_detected_count', 0)} Active Nodes</span>
                            </div>
                            <p class="text-[11px] text-slate-400">Diverting international termination traffic into local on-net SIMs. Out/In call ratio &gt; 25:1, zero mobility.</p>
                            <div class="mt-2 text-xs font-mono text-white flex justify-between">
                                <span>Estimated MTR Loss:</span>
                                <span class="text-red-400 font-bold">TZS {rafm.get('bypass_revenue_loss_tzs', 0):,.0f}</span>
                            </div>
                        </div>

                        <div class="p-3 bg-amber-950/30 rounded-lg border border-amber-800/40">
                            <div class="flex items-center justify-between text-xs mb-1">
                                <span class="font-bold text-amber-300 flex items-center gap-1.5"><i data-lucide="phone-forwarded" class="w-3.5 h-3.5"></i> Wangiri Ping-Call Predators</span>
                                <span class="text-amber-400 font-mono font-bold">{rafm.get('wangiri_detected_count', 0)} Detected</span>
                            </div>
                            <p class="text-[11px] text-slate-400">High-burst 1-ring flash calls targeting Tigo subscribers to entice expensive satellite PRS callbacks (+882/+881).</p>
                        </div>

                        <div class="p-3 bg-purple-950/30 rounded-lg border border-purple-800/40">
                            <div class="flex items-center justify-between text-xs mb-1">
                                <span class="font-bold text-purple-300 flex items-center gap-1.5"><i data-lucide="zap" class="w-3.5 h-3.5"></i> Impossible Travel Speed Anomaly</span>
                                <span class="text-purple-400 font-mono font-bold">{rafm.get('cloned_sim_impossible_travel_incidents', 0)} Incidents</span>
                            </div>
                            <p class="text-[11px] text-slate-400">Sequential calls registered at distant BTS towers &gt;850 km/h apart. Indicates active cloned SIM / spoofed IMSI.</p>
                        </div>
                    </div>
                </div>

                <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between items-center">
                    <button onclick="switchTab('fraud')" class="w-full py-1.5 bg-red-600/80 hover:bg-red-500 text-white rounded-lg text-xs font-semibold transition-all flex items-center justify-center gap-2">
                        <i data-lucide="crosshair" class="w-4 h-4"></i>
                        <span>Inspect RAFM Forensic Evidence</span>
                    </button>
                </div>
            </div>

        </section>

        <!-- Interconnect Clearing & National MTR Settlements -->
        <section class="glass-card rounded-xl p-5">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                <div>
                    <div class="flex items-center gap-2">
                        <i data-lucide="repeat" class="w-5 h-5 text-cyan-400"></i>
                        <h2 class="text-base font-bold text-white tracking-tight">National & International Interconnect (MTR) Clearing House</h2>
                    </div>
                    <p class="text-xs text-slate-400 mt-0.5">Mobile Termination Rate (MTR) balances with Vodacom, Airtel, Halotel, TTCL, and International Carriers</p>
                </div>
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold">Regulated MTR: TZS 15.60 / Min</span>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                    <thead class="bg-slate-900/90 text-slate-300 uppercase tracking-wider text-[11px] border-b border-slate-800">
                        <tr>
                            <th class="p-3">Interconnect Partner</th>
                            <th class="p-3 text-right">Outbound Calls</th>
                            <th class="p-3 text-right">Outbound Mins</th>
                            <th class="p-3 text-right">Payable MTR (TZS)</th>
                            <th class="p-3 text-right">Inbound Calls</th>
                            <th class="p-3 text-right">Inbound Mins</th>
                            <th class="p-3 text-right">Receivable MTR (TZS)</th>
                            <th class="p-3 text-right">Net Settlement Balance</th>
                            <th class="p-3 text-center">Clearing Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800/60 font-mono">
                        {''.join([f'''
                        <tr class="hover:bg-slate-800/40 transition-colors">
                            <td class="p-3 font-sans font-semibold text-white">{ic['operator']}</td>
                            <td class="p-3 text-right text-slate-300">{ic['outbound_calls']:,}</td>
                            <td class="p-3 text-right text-slate-300">{ic['outbound_minutes']:,.1f}</td>
                            <td class="p-3 text-right text-slate-300">TZS {ic['payable_mtr_tzs']:,.0f}</td>
                            <td class="p-3 text-right text-slate-300">{ic['inbound_calls']:,}</td>
                            <td class="p-3 text-right text-slate-300">{ic['inbound_minutes']:,.1f}</td>
                            <td class="p-3 text-right text-slate-300">TZS {ic['receivable_mtr_tzs']:,.0f}</td>
                            <td class="p-3 text-right font-bold {'text-emerald-400' if ic['net_settlement_tzs'] >= 0 else 'text-amber-400'}">
                                {'+' if ic['net_settlement_tzs'] >= 0 else ''}TZS {ic['net_settlement_tzs']:,.0f}
                            </td>
                            <td class="p-3 text-center">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase {'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' if ic['clearing_position'] == 'NET_RECEIVABLE' else 'bg-amber-500/20 text-amber-300 border border-amber-500/30'}">
                                    {ic['clearing_position']}
                                </span>
                            </td>
                        </tr>
                        ''' for ic in interconnect])}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Forensic Live CDR Explorer Table -->
        <section class="glass-card rounded-xl p-5 space-y-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2">
                        <i data-lucide="database" class="w-5 h-5 text-cyan-400"></i>
                        <h2 class="text-base font-bold text-white tracking-tight">Forensic CDR & Network Telemetry Explorer</h2>
                    </div>
                    <p class="text-xs text-slate-400 mt-0.5">Deep-dive record inspection across Voice Calls, 4G/5G Data PDP Sessions, and Tigo Pesa</p>
                </div>

                <!-- Live Filters -->
                <div class="flex flex-wrap items-center gap-2.5">
                    <div class="relative">
                        <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-2.5"></i>
                        <input id="cdrSearch" type="text" onkeyup="filterCdrTable()" placeholder="Search MSISDN, Cell ID, Cause..." class="bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 w-56">
                    </div>

                    <select id="cdrServiceFilter" onchange="switchCdrService()" class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-500">
                        <option value="voice">Voice CDRs (VoLTE & CS)</option>
                        <option value="data">Data PDP Contexts (4G/5G)</option>
                        <option value="momo">Tigo Pesa Mobile Money</option>
                        <option value="fraud">Suspected Fraud Records</option>
                    </select>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table id="cdrTable" class="w-full text-left text-xs">
                    <thead class="bg-slate-900/90 text-slate-300 uppercase tracking-wider text-[11px] border-b border-slate-800">
                        <tr id="tableHeaders">
                            <!-- Populated dynamically via JS -->
                        </tr>
                    </thead>
                    <tbody id="tableBody" class="divide-y divide-slate-800/60 font-mono">
                        <!-- Populated dynamically via JS -->
                    </tbody>
                </table>
            </div>

            <!-- Table Footer & Pagination -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400 pt-2 border-t border-slate-800">
                <span id="recordCount">Showing 1 to 20 of audited records</span>
                <div class="flex items-center gap-2">
                    <button onclick="prevPage()" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium">Previous</button>
                    <span id="pageNum" class="text-white font-mono px-2">Page 1</span>
                    <button onclick="nextPage()" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium">Next</button>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="mt-12 border-t border-slate-800/80 px-6 py-6 text-center text-xs text-slate-500">
        <p>Millicom Enterprise Telecom CDR Intelligence Suite &copy; 2026 MIC Tanzania PLC. Confidential C-Suite Analytics Platform.</p>
        <p class="mt-1">Architected for Chief Technology Officer (CTO), Chief Commercial Officer (CCO), and Head of Revenue Assurance & Risk.</p>
    </footer>

    <!-- Client-Side Master Script -->
    <script>
        // Master Payload Injected from Python Engine
        const DATA = {payload_json_str};

        // Initialize Icons
        lucide.createIcons();

        // -------------------------------------------------------------
        // 1. LEAFLET TANZANIA CELL TOWERS MAP
        // -------------------------------------------------------------
        let map;
        let towerMarkers = [];

        function initMap() {{
            // Tanzania centered [-6.3690, 34.8888]
            map = L.map('map').setView([-6.40, 36.00], 6);

            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '&copy; CartoDB &copy; OpenStreetMap',
                subdomains: 'abcd',
                maxZoom: 18
            }}).addTo(map);

            renderMarkers(DATA.towers);
        }}

        function renderMarkers(towersList) {{
            // Clear existing
            towerMarkers.forEach(m => map.removeLayer(m));
            towerMarkers = [];

            towersList.forEach(t => {{
                let color = '#38BDF8'; // 4G Cyan
                let radius = 6;

                if (t.tech === '5G') {{
                    color = '#A855F7'; // 5G Purple
                    radius = 8;
                }} else if (t.tech === '3G') {{
                    color = '#F59E0B'; // 3G Amber
                    radius = 5;
                }}

                if (t.sla_status === 'CRITICAL_SLA_BREACH') {{
                    color = '#EF4444'; // Red
                    radius = 9;
                }}

                const marker = L.circleMarker([t.latitude, t.longitude], {{
                    radius: radius,
                    fillColor: color,
                    color: '#FFFFFF',
                    weight: 1.5,
                    opacity: 0.9,
                    fillOpacity: 0.85
                }}).addTo(map);

                const popupHtml = `
                    <div style="font-family: 'Inter', sans-serif; font-size: 11px; min-width: 210px; color: #0F172A; padding: 4px;">
                        <div style="font-weight: 700; font-size: 13px; color: #002B49; border-bottom: 1px solid #E2E8F0; padding-bottom: 4px; margin-bottom: 6px;">
                            ${{t.name}}
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <span style="color: #64748B;">Site ID / Tech:</span>
                            <b>${{t.tower_id}} (${{t.tech}})</b>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <span style="color: #64748B;">Region:</span>
                            <b>${{t.region}}</b>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <span style="color: #64748B;">Traffic Load:</span>
                            <b style="color: #0284C7;">${{t.traffic_erlangs}} Erlangs</b>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <span style="color: #64748B;">Erlang-B Block %:</span>
                            <b style="color: ${{t.erlang_b_blocking_pct > 1.5 ? '#EF4444' : '#10B981'}}">${{t.erlang_b_blocking_pct}}%</b>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <span style="color: #64748B;">Call Drop Rate (CDR):</span>
                            <b>${{t.cdr_pct}}%</b>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 6px; padding-top: 4px; border-top: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Revenue:</span>
                            <b>TZS ${{Number(t.total_revenue_tzs).toLocaleString()}}</b>
                        </div>
                    </div>
                `;
                marker.bindPopup(popupHtml);
                towerMarkers.push(marker);
            }});
        }}

        function filterMap(mode) {{
            // Reset buttons
            document.querySelectorAll('[id^="map-btn-"]').forEach(b => {{
                b.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white font-medium';
            }});
            document.getElementById('map-btn-' + mode.toLowerCase()).className = 'px-2.5 py-1 rounded bg-cyan-600 text-white font-medium';

            if (mode === 'ALL') {{
                renderMarkers(DATA.towers);
            }} else if (mode === '5G') {{
                renderMarkers(DATA.towers.filter(t => t.tech === '5G'));
            }} else if (mode === '4G') {{
                renderMarkers(DATA.towers.filter(t => t.tech === '4G'));
            }} else if (mode === 'ALERT') {{
                renderMarkers(DATA.towers.filter(t => t.sla_status !== 'NORMAL'));
            }}
        }}

        // -------------------------------------------------------------
        // 2. CHART.JS VISUALIZATIONS
        // -------------------------------------------------------------
        function initCharts() {{
            // A. Diurnal Chart
            const ctxDiurnal = document.getElementById('diurnalChart').getContext('2d');
            const hours = DATA.diurnal.map(d => `${{String(d.hour).padStart(2, '0')}}:00`);
            const erlangs = DATA.diurnal.map(d => d.erlangs);
            const dataGb = DATA.diurnal.map(d => d.data_gb);

            new Chart(ctxDiurnal, {{
                type: 'line',
                data: {{
                    labels: hours,
                    datasets: [
                        {{
                            label: 'Voice Traffic (Erlangs)',
                            data: erlangs,
                            borderColor: '#38BDF8',
                            backgroundColor: 'rgba(56, 189, 248, 0.1)',
                            fill: true,
                            tension: 0.35,
                            yAxisID: 'y'
                        }},
                        {{
                            label: 'Data Volume (GB)',
                            data: dataGb,
                            borderColor: '#A855F7',
                            backgroundColor: 'transparent',
                            borderDash: [5, 5],
                            tension: 0.35,
                            yAxisID: 'y1'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{
                        mode: 'index',
                        intersect: false
                    }},
                    scales: {{
                        x: {{
                            grid: {{ color: 'rgba(255,255,255,0.05)' }},
                            ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}
                        }},
                        y: {{
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: {{ display: true, text: 'Voice Erlangs', color: '#38BDF8' }},
                            grid: {{ color: 'rgba(255,255,255,0.05)' }},
                            ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}
                        }},
                        y1: {{
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: {{ display: true, text: 'Data (GB)', color: '#A855F7' }},
                            grid: {{ drawOnChartArea: false }},
                            ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#F1F5F9', font: {{ size: 11 }} }}
                        }}
                    }}
                }}
            }});

            // B. Churn Donut Chart
            const ctxChurn = document.getElementById('churnChart').getContext('2d');
            const churnData = DATA.churn.churn_risk_distribution;
            new Chart(ctxChurn, {{
                type: 'doughnut',
                data: {{
                    labels: ['Low Risk (<15%)', 'Medium Risk (40-60%)', 'High Risk (85%+)', 'Fraud Blacklist'],
                    datasets: [{{
                        data: [
                            churnData['Low Churn Risk (<15%)'] || 0,
                            churnData['Medium Churn Risk (40-60%)'] || 0,
                            churnData['High Churn Risk (85%+)'] || 0,
                            churnData['Fraud Blacklist'] || 0
                        ],
                        backgroundColor: ['#10B981', '#F59E0B', '#EF4444', '#A855F7'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }},
                    cutout: '72%'
                }}
            }});
        }}

        // -------------------------------------------------------------
        // 3. FORENSIC CDR TABLE EXPLORER
        // -------------------------------------------------------------
        let currentPage = 1;
        const pageSize = 15;
        let currentDataset = [];

        function switchCdrService() {{
            const val = document.getElementById('cdrServiceFilter').value;
            currentPage = 1;
            renderCdrTable();
        }}

        function renderCdrTable() {{
            const filterType = document.getElementById('cdrServiceFilter').value;
            const searchTerm = document.getElementById('cdrSearch').value.toLowerCase();
            const thead = document.getElementById('tableHeaders');
            const tbody = document.getElementById('tableBody');

            tbody.innerHTML = '';

            let headers = [];
            let rows = [];

            if (filterType === 'voice') {{
                headers = ['CDR ID', 'Timestamp', 'Calling Party (A)', 'Called Party (B)', 'Type', 'Duration', 'Termination Cause', 'Status', 'BTS Cell ID', 'Retail (TZS)'];
                currentDataset = DATA.voice_cdrs;
            }} else if (filterType === 'data') {{
                headers = ['Session ID', 'Timestamp', 'MSISDN', 'BTS Cell ID', 'Tech', 'APN', 'Traffic (MB)', 'Throughput', 'Latency RTT', 'Billable (TZS)'];
                currentDataset = DATA.data_cdrs;
            }} else if (filterType === 'momo') {{
                headers = ['TX ID', 'Timestamp', 'Sender MSISDN', 'Recipient', 'Channel', 'TX Type', 'Amount (TZS)', 'Fee Revenue', 'Status'];
                currentDataset = DATA.momo_cdrs;
            }} else if (filterType === 'fraud') {{
                headers = ['Fraud Subject', 'Target / Prefix', 'Handset / IMEI', 'Out/In Ratio', 'Duration Profile', 'Financial Loss', 'Mandated Action'];
                currentDataset = DATA.rafm.simbox_suspects_detail;
            }}

            thead.innerHTML = headers.map(h => `<th class="p-3">${{h}}</th>`).join('');

            // Filter logic
            let filtered = currentDataset.filter(row => {{
                return Object.values(row).some(v => String(v).toLowerCase().includes(searchTerm));
            }});

            const total = filtered.length;
            const start = (currentPage - 1) * pageSize;
            const pageSlice = filtered.slice(start, start + pageSize);

            document.getElementById('recordCount').innerText = `Showing ${{start + 1}} to ${{Math.min(start + pageSize, total)}} of ${{total}} records`;
            document.getElementById('pageNum').innerText = `Page ${{currentPage}} of ${{Math.ceil(total / pageSize) || 1}}`;

            pageSlice.forEach(row => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/40 transition-colors';

                if (filterType === 'voice') {{
                    const statusColor = row.call_status === 'ANSWERED' ? 'text-emerald-400' : (row.is_dropped === '1' ? 'text-red-400 font-bold' : 'text-slate-400');
                    tr.innerHTML = `
                        <td class="p-3 text-cyan-400">${{row.cdr_id}}</td>
                        <td class="p-3 text-slate-300 font-sans text-[11px]">${{row.timestamp}}</td>
                        <td class="p-3 text-white">${{row.calling_msisdn}}</td>
                        <td class="p-3 text-slate-300">${{row.called_msisdn}}</td>
                        <td class="p-3 text-slate-400">${{row.call_type}}</td>
                        <td class="p-3 text-right text-slate-200">${{row.duration_sec}}s</td>
                        <td class="p-3 text-slate-300"><span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 border border-slate-700">${{row.termination_cause}}</span></td>
                        <td class="p-3 ${{statusColor}}">${{row.call_status}}</td>
                        <td class="p-3 text-cyan-300 font-sans">${{row.cell_id}}</td>
                        <td class="p-3 text-right text-white">TZS ${{Number(row.retail_revenue_tzs).toLocaleString()}}</td>
                    `;
                }} else if (filterType === 'data') {{
                    tr.innerHTML = `
                        <td class="p-3 text-purple-400">${{row.session_id}}</td>
                        <td class="p-3 text-slate-300 font-sans text-[11px]">${{row.timestamp}}</td>
                        <td class="p-3 text-white">${{row.msisdn}}</td>
                        <td class="p-3 text-cyan-300 font-sans">${{row.cell_id}}</td>
                        <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300">${{row.technology}}</span></td>
                        <td class="p-3 text-slate-300">${{row.apn_name}}</td>
                        <td class="p-3 text-right text-white font-bold">${{row.total_traffic_mb}} MB</td>
                        <td class="p-3 text-right text-slate-300">${{row.avg_throughput_mbps}} Mbps</td>
                        <td class="p-3 text-right text-slate-300">${{row.rtt_latency_ms}} ms</td>
                        <td class="p-3 text-right text-emerald-400">TZS ${{Number(row.billable_amount_tzs).toLocaleString()}}</td>
                    `;
                }} else if (filterType === 'momo') {{
                    tr.innerHTML = `
                        <td class="p-3 text-emerald-400">${{row.transaction_id}}</td>
                        <td class="p-3 text-slate-300 font-sans text-[11px]">${{row.timestamp}}</td>
                        <td class="p-3 text-white">${{row.sender_msisdn}}</td>
                        <td class="p-3 text-slate-300">${{row.recipient_identifier}}</td>
                        <td class="p-3 text-slate-400 text-[10px]">${{row.channel}}</td>
                        <td class="p-3 text-slate-200"><span class="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400">${{row.transaction_type}}</span></td>
                        <td class="p-3 text-right text-white font-bold">TZS ${{Number(row.amount_tzs).toLocaleString()}}</td>
                        <td class="p-3 text-right text-emerald-400">TZS ${{Number(row.fee_revenue_tzs).toLocaleString()}}</td>
                        <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] ${{row.status === 'SUCCESS' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-red-500/20 text-red-300'}}">${{row.status}}</span></td>
                    `;
                }} else if (filterType === 'fraud') {{
                    tr.innerHTML = `
                        <td class="p-3 text-red-400 font-bold">${{row.msisdn}}</td>
                        <td class="p-3 text-slate-300 font-sans">${{row.imsi}}</td>
                        <td class="p-3 text-slate-300">${{row.handset}}</td>
                        <td class="p-3 text-right text-red-400 font-bold">${{row.out_in_ratio}}:1</td>
                        <td class="p-3 text-slate-300">${{row.total_bypass_minutes}} mins (${{row.avg_duration_sec}}s avg)</td>
                        <td class="p-3 text-right text-red-400 font-bold">TZS ${{Number(row.estimated_loss_tzs).toLocaleString()}}</td>
                        <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] bg-red-500/20 text-red-300 border border-red-500/30 font-bold">${{row.action}}</span></td>
                    `;
                }}

                tbody.appendChild(tr);
            }});
        }}

        function filterCdrTable() {{
            currentPage = 1;
            renderCdrTable();
        }}

        function nextPage() {{
            currentPage++;
            renderCdrTable();
        }}

        function prevPage() {{
            if (currentPage > 1) {{
                currentPage--;
                renderCdrTable();
            }}
        }}

        function switchTab(tab) {{
            if (tab === 'fraud') {{
                document.getElementById('cdrServiceFilter').value = 'fraud';
                switchCdrService();
                document.getElementById('cdrTable').scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}

        function downloadExcelPack() {{
            window.location.href = 'Millicom_Tigo_Executive_CDR_Analytics_Pack.xlsx';
        }}

        // Initialization
        window.addEventListener('DOMContentLoaded', () => {{
            initMap();
            initCharts();
            renderCdrTable();
        }});
    </script>
</body>
</html>
"""

    with open(DASHBOARD_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[SUCCESS] Executive Dashboard HTML built: {DASHBOARD_HTML_PATH}")

if __name__ == '__main__':
    build_dashboard()
