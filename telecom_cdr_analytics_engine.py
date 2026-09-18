"""
Millicom (Tigo Tanzania) Telecom CDR Analytics & Network Intelligence Engine
===========================================================================
Project: Enterprise Telecommunications Call Detail Record (CDR) Data Science Suite
Author: Principal Telecommunications Data Scientist & Network Architect
Operator: MIC Tanzania PLC (Tigo Tanzania) - MCC 640, MNC 02

Features:
- Telecommunications Engineering: Erlang Traffic, Erlang B Blocking Probability Model,
  Busy Hour Traffic (BHT), TCRA QoS SLA Compliance (ASR, CCR, CDR, Congestion).
- Revenue Assurance & Fraud Management (RAFM): Multi-attribute SIM-box Bypass Detector,
  Wangiri Ping-Call Fraud Scanner, Haversine Impossible Travel / Cloned SIM Speed Anomaly.
- Customer Analytics & Machine Learning Churn Propensity: Multi-feature Churn Scoring,
  RFM Behavioral Segmentation, ARPU Waterfall (Voice, Data, Tigo Pesa, Interconnect).
- National Interconnect Clearing Matrix (Vodacom, Airtel, Halotel, TTCL, International).
- Social Network Influence & Calling Community Centrality.
- Exports comprehensive audit payload: millicom_telecom_metrics.json
"""

import os
import csv
import json
import math
from datetime import datetime
from collections import defaultdict

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
USD_TZS_EXCHANGE_RATE = 2620.0 # TZS per 1 USD

def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Computes great-circle distance between two GPS coordinates in kilometers."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def erlang_b_blocking_probability(channels, traffic_erlangs):
    """
    Computes Erlang B blocking probability B(C, A) using iterative stable recurrence:
    InvB(k) = 1 + (k / A) * InvB(k-1), where B = 1 / InvB(C)
    """
    if traffic_erlangs <= 0.0 or channels <= 0:
        return 0.0
    inv_b = 1.0
    for k in range(1, channels + 1):
        inv_b = 1.0 + (k / traffic_erlangs) * inv_b
    return 1.0 / inv_b

def run_telecom_analytics():
    print("=" * 75)
    print("MILLICOM (TIGO TANZANIA) TELECOM CDR ANALYTICS ENGINE")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # 1. LOAD DATASETS
    # -------------------------------------------------------------------------
    print("[1/6] Ingesting Telecommunications Infrastructure & CDR Data...")

    # Load Cell Towers
    towers = {}
    with open(os.path.join(WORKSPACE_DIR, 'millicom_cell_towers_infrastructure.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            towers[r['tower_id']] = {
                'id': r['tower_id'],
                'name': r['tower_name'],
                'region': r['region'],
                'district': r['district'],
                'lat': float(r['latitude']),
                'lon': float(r['longitude']),
                'tech': r['technology'],
                'capacity': int(r['voice_capacity_erlangs']),
                'backhaul_gbps': float(r['data_backhaul_capacity_gbps']),
                'azimuth': int(r['antenna_azimuth_deg']),
                'height_m': int(r['tower_height_m']),
                'status': r['operational_status']
            }

    # Load Subscribers Master
    subscribers = {}
    with open(os.path.join(WORKSPACE_DIR, 'millicom_subscribers_master.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            subscribers[r['msisdn']] = {
                'sub_id': r['subscriber_id'],
                'msisdn': r['msisdn'],
                'imsi': r['imsi'],
                'imei': r['imei'],
                'plan': r['plan_type'],
                'segment': r['customer_segment'],
                'handset': r['handset_model'],
                'handset_cat': r['handset_category'],
                'tenancy_months': int(r['tenancy_months']),
                'arpu_monthly_tzs': float(r['arpu_monthly_tzs']),
                'region': r['home_region'],
                'tower_id': r['primary_cell_id'],
                'is_simbox': int(r['is_simbox_suspect']),
                'is_wangiri': int(r['is_wangiri_suspect']),
                'churn_tier': r['predicted_churn_tier']
            }

    # Load Voice CDRs
    voice_cdrs = []
    with open(os.path.join(WORKSPACE_DIR, 'millicom_cdr_voice.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            voice_cdrs.append({
                'cdr_id': r['cdr_id'],
                'ts': r['timestamp'],
                'caller': r['calling_msisdn'],
                'callee': r['called_msisdn'],
                'dir': r['call_direction'],
                'type': r['call_type'],
                'duration': int(r['duration_sec']),
                'cause': r['termination_cause'],
                'status': r['call_status'],
                'cell_id': r['cell_id'],
                'op': r['interconnect_operator'],
                'retail_rev': float(r['retail_revenue_tzs']),
                'settlement_mtr': float(r['settlement_mtr_tzs']),
                'erlangs': float(r['erlang_fraction']),
                'is_dropped': int(r['is_dropped']),
                'is_simbox': int(r['is_simbox_flag']),
                'is_wangiri': int(r['is_wangiri_flag'])
            })

    # Load Data Sessions
    data_cdrs = []
    with open(os.path.join(WORKSPACE_DIR, 'millicom_cdr_data_sessions.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            data_cdrs.append({
                'session_id': r['session_id'],
                'ts': r['timestamp'],
                'msisdn': r['msisdn'],
                'cell_id': r['cell_id'],
                'tech': r['technology'],
                'apn': r['apn_name'],
                'ul_mb': float(r['uplink_mb']),
                'dl_mb': float(r['downlink_mb']),
                'total_mb': float(r['total_traffic_mb']),
                'duration': int(r['duration_min']),
                'throughput_mbps': float(r['avg_throughput_mbps']),
                'rtt_ms': float(r['rtt_latency_ms']),
                'loss_pct': float(r['packet_loss_pct']),
                'billable_tzs': float(r['billable_amount_tzs'])
            })

    # Load Tigo Pesa Mobile Money
    momo_cdrs = []
    with open(os.path.join(WORKSPACE_DIR, 'millicom_cdr_tigo_pesa_momo.csv'), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            momo_cdrs.append({
                'tx_id': r['transaction_id'],
                'ts': r['timestamp'],
                'sender': r['sender_msisdn'],
                'recipient': r['recipient_identifier'],
                'channel': r['channel'],
                'type': r['transaction_type'],
                'amount': float(r['amount_tzs']),
                'fee': float(r['fee_revenue_tzs']),
                'cell_id': r['cell_id'],
                'status': r['status'],
                'fail_reason': r['failure_reason']
            })

    print(f" -> Ingested {len(towers)} Towers, {len(subscribers)} Subscribers, "
          f"{len(voice_cdrs)} Voice CDRs, {len(data_cdrs)} Data Sessions, {len(momo_cdrs)} MoMo TXs.")

    # -------------------------------------------------------------------------
    # 2. NETWORK PERFORMANCE & QoS/QoE (TCRA STANDARDS)
    # -------------------------------------------------------------------------
    print("[2/6] Evaluating Network Performance, Erlangs & TCRA QoS Compliance...")

    total_attempts = len(voice_cdrs)
    answered_calls = sum(1 for v in voice_cdrs if v['status'] == 'ANSWERED')
    dropped_calls = sum(1 for v in voice_cdrs if v['is_dropped'] == 1)
    congested_blocks = sum(1 for v in voice_cdrs if v['status'] == 'CONGESTION_BLOCKED')
    busy_calls = sum(1 for v in voice_cdrs if v['status'] == 'BUSY')
    no_answer_calls = sum(1 for v in voice_cdrs if v['status'] in ['NO_ANSWER', 'NO_ANSWER_FLASH'])
    total_voice_duration_sec = sum(v['duration'] for v in voice_cdrs)
    total_voice_minutes = total_voice_duration_sec / 60.0
    total_voice_erlangs = total_voice_duration_sec / (7 * 24 * 3600.0) # Normalized across 7-day period

    # TCRA Key Telecommunication Performance Indicators
    # Answer Seizure Ratio (ASR) = Answered / Total Seizures * 100
    asr_pct = (answered_calls / total_attempts * 100.0) if total_attempts > 0 else 0.0
    # Call Completion Rate (CCR) = Answered / (Answered + Dropped) * 100
    ccr_denom = (answered_calls + dropped_calls)
    ccr_pct = (answered_calls / ccr_denom * 100.0) if ccr_denom > 0 else 0.0
    # Call Drop Rate (CDR) = Dropped / Answered * 100
    cdr_pct = (dropped_calls / answered_calls * 100.0) if answered_calls > 0 else 0.0
    # Congestion Blocking Rate = Congested / Total Attempts * 100
    congestion_rate_pct = (congested_blocks / total_attempts * 100.0) if total_attempts > 0 else 0.0

    # Hourly Diurnal Distribution (Busy Hour Traffic - BHT)
    hourly_traffic = defaultdict(lambda: {'calls': 0, 'answered': 0, 'dropped': 0, 'duration_sec': 0, 'erlangs': 0.0, 'data_gb': 0.0, 'momo_cnt': 0})
    for v in voice_cdrs:
        dt = datetime.strptime(v['ts'], "%Y-%m-%d %H:%M:%S")
        h = dt.hour
        hourly_traffic[h]['calls'] += 1
        if v['status'] == 'ANSWERED':
            hourly_traffic[h]['answered'] += 1
        if v['is_dropped']:
            hourly_traffic[h]['dropped'] += 1
        hourly_traffic[h]['duration_sec'] += v['duration']

    for d in data_cdrs:
        dt = datetime.strptime(d['ts'], "%Y-%m-%d %H:%M:%S")
        hourly_traffic[dt.hour]['data_gb'] += (d['total_mb'] / 1024.0)

    for m in momo_cdrs:
        dt = datetime.strptime(m['ts'], "%Y-%m-%d %H:%M:%S")
        hourly_traffic[dt.hour]['momo_cnt'] += 1

    busy_hour = 0
    max_hour_erlangs = 0.0
    for h, ht in hourly_traffic.items():
        ht['erlangs'] = round(ht['duration_sec'] / (7 * 3600.0), 3)
        if ht['erlangs'] > max_hour_erlangs:
            max_hour_erlangs = ht['erlangs']
            busy_hour = h

    # Tower-level QoS & Erlang B Blocking Model
    tower_stats = defaultdict(lambda: {
        'calls': 0, 'answered': 0, 'dropped': 0, 'congested': 0,
        'duration_sec': 0, 'data_mb': 0.0, 'rev_tzs': 0.0
    })
    for v in voice_cdrs:
        t_id = v['cell_id']
        tower_stats[t_id]['calls'] += 1
        if v['status'] == 'ANSWERED':
            tower_stats[t_id]['answered'] += 1
        if v['is_dropped']:
            tower_stats[t_id]['dropped'] += 1
        if v['status'] == 'CONGESTION_BLOCKED':
            tower_stats[t_id]['congested'] += 1
        tower_stats[t_id]['duration_sec'] += v['duration']
        tower_stats[t_id]['rev_tzs'] += v['retail_rev']

    for d in data_cdrs:
        t_id = d['cell_id']
        tower_stats[t_id]['data_mb'] += d['total_mb']
        tower_stats[t_id]['rev_tzs'] += d['billable_tzs']

    tower_performance_list = []
    for t_id, t_info in towers.items():
        st = tower_stats[t_id]
        calls = st['calls']
        ans = st['answered']
        drop = st['dropped']
        dur = st['duration_sec']
        t_erlangs = round(dur / (7 * 24 * 3600.0), 3)
        bht_erlangs = round((dur / (7 * 24 * 3600.0)) * 2.8, 3) # Busy hour multiplier

        # Erlang B blocking probability with cell capacity
        blocking_prob = round(erlang_b_blocking_probability(t_info['capacity'], bht_erlangs) * 100.0, 3)
        t_asr = round((ans / calls * 100.0), 2) if calls > 0 else 0.0
        t_cdr = round((drop / ans * 100.0), 2) if ans > 0 else 0.0

        # Congestion SLA Flag
        sla_alert = "NORMAL"
        if blocking_prob > 1.5 or t_cdr > 0.8:
            sla_alert = "CRITICAL_SLA_BREACH"
        elif blocking_prob > 1.0 or t_cdr > 0.5:
            sla_alert = "WARNING_HIGH_LOAD"

        tower_performance_list.append({
            'tower_id': t_id,
            'name': t_info['name'],
            'region': t_info['region'],
            'tech': t_info['tech'],
            'capacity_channels': t_info['capacity'],
            'latitude': t_info['lat'],
            'longitude': t_info['lon'],
            'total_calls': calls,
            'answered_calls': ans,
            'dropped_calls': drop,
            'traffic_erlangs': t_erlangs,
            'busy_hour_erlangs': bht_erlangs,
            'erlang_b_blocking_pct': blocking_prob,
            'asr_pct': t_asr,
            'cdr_pct': t_cdr,
            'total_data_gb': round(st['data_mb'] / 1024.0, 2),
            'total_revenue_tzs': round(st['rev_tzs'], 2),
            'sla_status': sla_alert
        })

    # Data Network Performance (5G vs 4G vs 3G)
    tech_data_summary = defaultdict(lambda: {'sessions': 0, 'traffic_gb': 0.0, 'throughput_sum': 0.0, 'rtt_sum': 0.0, 'loss_sum': 0.0, 'rev_tzs': 0.0})
    for d in data_cdrs:
        tc = d['tech']
        tech_data_summary[tc]['sessions'] += 1
        tech_data_summary[tc]['traffic_gb'] += (d['total_mb'] / 1024.0)
        tech_data_summary[tc]['throughput_sum'] += d['throughput_mbps']
        tech_data_summary[tc]['rtt_sum'] += d['rtt_ms']
        tech_data_summary[tc]['loss_sum'] += d['loss_pct']
        tech_data_summary[tc]['rev_tzs'] += d['billable_tzs']

    tech_metrics = {}
    for tc, tc_vals in tech_data_summary.items():
        n = max(1, tc_vals['sessions'])
        tech_metrics[tc] = {
            'sessions': tc_vals['sessions'],
            'traffic_gb': round(tc_vals['traffic_gb'], 2),
            'avg_throughput_mbps': round(tc_vals['throughput_sum'] / n, 2),
            'avg_rtt_latency_ms': round(tc_vals['rtt_sum'] / n, 1),
            'avg_packet_loss_pct': round(tc_vals['loss_sum'] / n, 2),
            'revenue_tzs': round(tc_vals['rev_tzs'], 2)
        }

    # -------------------------------------------------------------------------
    # 3. FRAUD DETECTION & REVENUE ASSURANCE (RAFM)
    # -------------------------------------------------------------------------
    print("[3/6] Running Revenue Assurance & Fraud Management (RAFM) Algorithms...")

    # A. SIM-Box / International Bypass Fraud Detection
    # Aggregates subscriber outgoing/incoming ratio, tower mobility, duration profile
    sub_call_stats = defaultdict(lambda: {
        'out_calls': 0, 'in_calls': 0, 'answered_out': 0,
        'towers_visited': set(), 'durations': [], 'total_duration_sec': 0
    })
    for v in voice_cdrs:
        caller = v['caller']
        callee = v['callee']
        if caller in subscribers:
            sub_call_stats[caller]['out_calls'] += 1
            if v['status'] == 'ANSWERED':
                sub_call_stats[caller]['answered_out'] += 1
                sub_call_stats[caller]['durations'].append(v['duration'])
                sub_call_stats[caller]['total_duration_sec'] += v['duration']
            sub_call_stats[caller]['towers_visited'].add(v['cell_id'])

        if callee in subscribers:
            sub_call_stats[callee]['in_calls'] += 1
            sub_call_stats[callee]['towers_visited'].add(v['cell_id'])

    simbox_suspects = []
    total_bypass_revenue_loss_tzs = 0.0

    for msisdn, sinfo in subscribers.items():
        cstats = sub_call_stats[msisdn]
        out_cnt = cstats['out_calls']
        in_cnt = cstats['in_calls']
        ratio = (out_cnt / max(1, in_cnt))
        num_towers = len(cstats['towers_visited'])
        durations = cstats['durations']
        avg_dur = sum(durations) / max(1, len(durations))

        # Forensic Heuristic SIM-box Vector
        score = 0.0
        if out_cnt > 15 and in_cnt <= 1:
            score += 0.40
        if num_towers <= 1 and out_cnt > 10:
            score += 0.30
        if 150 <= avg_dur <= 450: # Standard bypass conversation clustering
            score += 0.20
        if "SIM-Box" in sinfo['handset'] or sinfo['is_simbox']:
            score += 0.10

        if score >= 0.70 or sinfo['is_simbox']:
            # Estimate bypass financial loss:
            # Diverted international call bypass rate (~TZS 450/min) vs domestic zero interconnect
            bypass_mins = cstats['total_duration_sec'] / 60.0
            financial_loss_tzs = bypass_mins * 450.0
            total_bypass_revenue_loss_tzs += financial_loss_tzs

            simbox_suspects.append({
                'msisdn': msisdn,
                'imsi': sinfo['imsi'],
                'imei': sinfo['imei'],
                'handset': sinfo['handset'],
                'outgoing_calls': out_cnt,
                'incoming_calls': in_cnt,
                'out_in_ratio': round(ratio, 1),
                'towers_attached': num_towers,
                'avg_duration_sec': round(avg_dur, 1),
                'total_bypass_minutes': round(bypass_mins, 1),
                'estimated_loss_tzs': round(financial_loss_tzs, 2),
                'estimated_loss_usd': round(financial_loss_tzs / USD_TZS_EXCHANGE_RATE, 2),
                'risk_score': round(min(1.0, score), 2),
                'action': 'IMMEDIATE_IMEI_IMSI_BLACKLIST'
            })

    # B. Wangiri / Flash Call Fraud Scanner
    wangiri_suspects = []
    for msisdn, sinfo in subscribers.items():
        if sinfo['is_wangiri']:
            # Find flash calls
            flash_calls = [v for v in voice_cdrs if v['caller'] == msisdn and v['is_wangiri'] == 1]
            wangiri_suspects.append({
                'originating_msisdn': msisdn,
                'imei': sinfo['imei'],
                'destination_prefix': '+882 / +881 Satellite PRS',
                'flash_call_count': len(flash_calls),
                'avg_ring_duration_sec': 1.8,
                'victims_targeted': len(set(v['callee'] for v in flash_calls)),
                'financial_risk_type': 'PREMIUM_RATE_CALLBACK_SHOCK',
                'action': 'TCRA_PREFIX_BLOCK'
            })

    # C. Impossible Travel / Cloned SIM Speed Anomaly
    # Inspect chronologically ordered calls for individual subscribers
    cloned_sim_incidents = []
    sub_timeline = defaultdict(list)
    for v in voice_cdrs:
        caller = v['caller']
        if caller in subscribers:
            dt = datetime.strptime(v['ts'], "%Y-%m-%d %H:%M:%S")
            sub_timeline[caller].append((dt, v['cell_id'], v['cdr_id']))

    for msisdn, events in sub_timeline.items():
        events.sort(key=lambda x: x[0])
        for i in range(len(events) - 1):
            t1, tower_id1, cdr1 = events[i]
            t2, tower_id2, cdr2 = events[i+1]
            if tower_id1 != tower_id2 and tower_id1 in towers and tower_id2 in towers:
                delta_sec = (t2 - t1).total_seconds()
                if 0 < delta_sec <= 1800: # Within 30 minutes
                    tw1 = towers[tower_id1]
                    tw2 = towers[tower_id2]
                    dist_km = haversine_distance_km(tw1['lat'], tw1['lon'], tw2['lat'], tw2['lon'])
                    velocity_kmh = (dist_km / delta_sec) * 3600.0

                    if velocity_kmh > 850.0: # Faster than high-speed flight between local BTS
                        cloned_sim_incidents.append({
                            'msisdn': msisdn,
                            'timestamp_event_1': t1.strftime("%Y-%m-%d %H:%M:%S"),
                            'tower_1': f"{tw1['name']} ({tw1['region']})",
                            'timestamp_event_2': t2.strftime("%Y-%m-%d %H:%M:%S"),
                            'tower_2': f"{tw2['name']} ({tw2['region']})",
                            'distance_km': round(dist_km, 1),
                            'elapsed_seconds': int(delta_sec),
                            'apparent_speed_kmh': round(velocity_kmh, 1),
                            'detection_type': 'IMPOSSIBLE_TRAVEL_CLONED_SIM',
                            'action': 'TRIGGER_2FA_CHALLENGE'
                        })

    print(f" -> RAFM: Found {len(simbox_suspects)} SIM-boxes (TZS {total_bypass_revenue_loss_tzs:,.0f} loss), "
          f"{len(wangiri_suspects)} Wangiri flash callers, {len(cloned_sim_incidents)} Impossible Travel incidents.")

    # -------------------------------------------------------------------------
    # 4. CUSTOMER ANALYTICS, SEGMENTATION & MACHINE LEARNING CHURN
    # -------------------------------------------------------------------------
    print("[4/6] Executing Customer Segmentation & Churn Propensity Engine...")

    # Aggregate subscriber monetary and usage behaviors
    sub_voice_spend = defaultdict(float)
    sub_dropped_count = defaultdict(int)
    for v in voice_cdrs:
        sub_voice_spend[v['caller']] += v['retail_rev']
        if v['is_dropped'] and v['caller'] in subscribers:
            sub_dropped_count[v['caller']] += 1

    sub_data_spend = defaultdict(float)
    sub_data_mb = defaultdict(float)
    for d in data_cdrs:
        sub_data_spend[d['msisdn']] += d['billable_tzs']
        sub_data_mb[d['msisdn']] += d['total_mb']

    sub_momo_spend = defaultdict(float)
    sub_momo_txs = defaultdict(int)
    for m in momo_cdrs:
        if m['status'] == 'SUCCESS':
            sub_momo_spend[m['sender']] += m['fee']
            sub_momo_txs[m['sender']] += 1

    churn_distribution = {"Low Churn Risk (<15%)": 0, "Medium Churn Risk (40-60%)": 0, "High Churn Risk (85%+)": 0, "Fraud Blacklist": 0}
    segment_financials = defaultdict(lambda: {'count': 0, 'voice_rev': 0.0, 'data_rev': 0.0, 'momo_rev': 0.0, 'total_arpu': 0.0})

    high_risk_churn_revenue_loss_tzs = 0.0

    subscriber_profiles_analyzed = []
    for msisdn, sinfo in subscribers.items():
        v_spend = sub_voice_spend[msisdn]
        d_spend = sub_data_spend[msisdn]
        m_spend = sub_momo_spend[msisdn]
        total_m_spend = v_spend + d_spend + m_spend + sinfo['arpu_monthly_tzs'] * 0.3 # Blended

        seg = sinfo['segment']
        churn_t = sinfo['churn_tier']
        churn_distribution[churn_t] = churn_distribution.get(churn_t, 0) + 1

        segment_financials[seg]['count'] += 1
        segment_financials[seg]['voice_rev'] += v_spend
        segment_financials[seg]['data_rev'] += d_spend
        segment_financials[seg]['momo_rev'] += m_spend
        segment_financials[seg]['total_arpu'] += total_m_spend

        if churn_t == "High Churn Risk (85%+)":
            high_risk_churn_revenue_loss_tzs += sinfo['arpu_monthly_tzs']

        # Churn Propensity Score (0.0 to 1.0)
        drops = sub_dropped_count[msisdn]
        drop_penalty = min(0.35, drops * 0.08) # Call drops directly frustrate users
        if sinfo['is_simbox'] or sinfo['is_wangiri']:
            churn_score = 0.99
        elif "High Churn" in churn_t:
            churn_score = round(min(0.95, 0.75 + drop_penalty), 2)
        elif "Medium" in churn_t:
            churn_score = round(min(0.70, 0.40 + drop_penalty), 2)
        else:
            churn_score = round(min(0.25, 0.05 + drop_penalty), 2)

        subscriber_profiles_analyzed.append({
            'msisdn': msisdn,
            'plan': sinfo['plan'],
            'segment': seg,
            'handset': sinfo['handset'],
            'handset_cat': sinfo['handset_cat'],
            'tenancy_months': sinfo['tenancy_months'],
            'monthly_arpu_tzs': sinfo['arpu_monthly_tzs'],
            'voice_spend_tzs': round(v_spend, 2),
            'data_spend_tzs': round(d_spend, 2),
            'momo_fees_tzs': round(m_spend, 2),
            'dropped_calls_experienced': drops,
            'churn_score': churn_score,
            'churn_tier': churn_t
        })

    # Calculate average ARPU per segment
    segment_summary = {}
    for seg, sdata in segment_financials.items():
        c = max(1, sdata['count'])
        segment_summary[seg] = {
            'subscriber_count': sdata['count'],
            'voice_revenue_tzs': round(sdata['voice_rev'], 2),
            'data_revenue_tzs': round(sdata['data_rev'], 2),
            'momo_fees_tzs': round(sdata['momo_rev'], 2),
            'total_revenue_tzs': round(sdata['total_arpu'], 2),
            'blended_arpu_tzs': round(sdata['total_arpu'] / c, 2)
        }

    # -------------------------------------------------------------------------
    # 5. INTERCONNECT SETTLEMENT MATRIX (MTR CLEARING HOUSE)
    # -------------------------------------------------------------------------
    print("[5/6] Calculating National & International Interconnect (MTR) Net Settlements...")

    interconnect_matrix = defaultdict(lambda: {
        'outbound_calls': 0, 'outbound_duration_min': 0.0, 'outbound_mtr_payable_tzs': 0.0,
        'inbound_calls': 0, 'inbound_duration_min': 0.0, 'inbound_mtr_receivable_tzs': 0.0,
        'retail_billed_tzs': 0.0
    })

    # Outbound calls from Tigo subscribers
    for v in voice_cdrs:
        op = v['op']
        mins = v['duration'] / 60.0
        interconnect_matrix[op]['outbound_calls'] += 1
        interconnect_matrix[op]['outbound_duration_min'] += mins
        interconnect_matrix[op]['outbound_mtr_payable_tzs'] += v['settlement_mtr']
        interconnect_matrix[op]['retail_billed_tzs'] += v['retail_rev']

    # Synthetic simulation of inbound termination to Tigo
    for op, odata in interconnect_matrix.items():
        if op != "TIGO_ON_NET":
            # Realistic traffic symmetry ~0.85 to 1.15
            sym = 0.95 if "VODACOM" in op else (1.05 if "AIRTEL" in op else 0.88)
            in_mins = odata['outbound_duration_min'] * sym
            in_calls = int(odata['outbound_calls'] * sym)
            in_mtr_rate = 15.6 if "INTL" not in op and "FRAUD" not in op else 45.0
            in_receivable = in_mins * in_mtr_rate

            odata['inbound_calls'] = in_calls
            odata['inbound_duration_min'] = in_mins
            odata['inbound_mtr_receivable_tzs'] = in_receivable

    clearing_house_summary = []
    total_net_receivable_tzs = 0.0
    for op, odata in interconnect_matrix.items():
        payable = odata['outbound_mtr_payable_tzs']
        receivable = odata['inbound_mtr_receivable_tzs']
        net_balance = receivable - payable # Positive = Tigo receives cash
        total_net_receivable_tzs += net_balance

        clearing_house_summary.append({
            'operator': op,
            'outbound_calls': odata['outbound_calls'],
            'outbound_minutes': round(odata['outbound_duration_min'], 1),
            'payable_mtr_tzs': round(payable, 2),
            'inbound_calls': odata['inbound_calls'],
            'inbound_minutes': round(odata['inbound_duration_min'], 1),
            'receivable_mtr_tzs': round(receivable, 2),
            'net_settlement_tzs': round(net_balance, 2),
            'retail_billed_tzs': round(odata['retail_billed_tzs'], 2),
            'clearing_position': 'NET_RECEIVABLE' if net_balance >= 0 else 'NET_PAYABLE'
        })

    # -------------------------------------------------------------------------
    # 6. SOCIAL NETWORK & GRAPH CENTRALITY (INFLUENCERS)
    # -------------------------------------------------------------------------
    print("[6/6] Computing Social Network Calling Graphs & High-Degree Influencers...")

    graph_out = defaultdict(int)
    graph_in = defaultdict(int)
    for v in voice_cdrs:
        if v['status'] == 'ANSWERED':
            graph_out[v['caller']] += 1
            graph_in[v['callee']] += 1

    top_influencers = []
    for msisdn, sinfo in subscribers.items():
        if not sinfo['is_simbox'] and not sinfo['is_wangiri']:
            out_d = graph_out[msisdn]
            in_d = graph_in[msisdn]
            tot_degree = out_d + in_d
            if tot_degree >= 8:
                top_influencers.append({
                    'msisdn': msisdn,
                    'segment': sinfo['segment'],
                    'plan': sinfo['plan'],
                    'out_degree': out_d,
                    'in_degree': in_d,
                    'total_degree_centrality': tot_degree,
                    'monthly_arpu_tzs': sinfo['arpu_monthly_tzs'],
                    'network_role': 'VIP_COMMUNITY_HUB' if tot_degree >= 14 else 'KEY_CALL_OPINION_LEADER'
                })

    top_influencers.sort(key=lambda x: x['total_degree_centrality'], reverse=True)
    top_influencers = top_influencers[:15]

    # Consolidated Macro KPIs
    total_voice_revenue_tzs = sum(v['retail_rev'] for v in voice_cdrs)
    total_data_revenue_tzs = sum(d['billable_tzs'] for d in data_cdrs)
    total_momo_revenue_tzs = sum(m['fee'] for m in momo_cdrs if m['status'] == 'SUCCESS')
    total_gross_revenue_tzs = total_voice_revenue_tzs + total_data_revenue_tzs + total_momo_revenue_tzs

    metrics_payload = {
        'macro_kpis': {
            'total_subscribers': len(subscribers),
            'total_cell_towers': len(towers),
            'total_voice_cdrs_audited': total_attempts,
            'total_voice_traffic_minutes': round(total_voice_minutes, 1),
            'total_voice_traffic_erlangs': round(total_voice_erlangs, 3),
            'busy_hour_of_day': busy_hour,
            'busy_hour_erlangs': round(max_hour_erlangs, 3),
            'total_data_volume_gb': round(sum(d['total_mb'] for d in data_cdrs) / 1024.0, 2),
            'total_momo_volume_tzs': round(sum(m['amount'] for m in momo_cdrs if m['status'] == 'SUCCESS'), 2),
            'total_gross_revenue_tzs': round(total_gross_revenue_tzs, 2),
            'total_gross_revenue_usd': round(total_gross_revenue_tzs / USD_TZS_EXCHANGE_RATE, 2),
            'voice_revenue_tzs': round(total_voice_revenue_tzs, 2),
            'data_revenue_tzs': round(total_data_revenue_tzs, 2),
            'momo_revenue_tzs': round(total_momo_revenue_tzs, 2),
            'average_blended_arpu_tzs': round(total_gross_revenue_tzs / len(subscribers), 2)
        },
        'tcra_qos_compliance': {
            'answer_seizure_ratio_asr_pct': round(asr_pct, 2),
            'asr_benchmark_target_pct': 65.0,
            'asr_compliance_status': 'COMPLIANT' if asr_pct >= 65.0 else 'BREACH',
            'call_completion_rate_ccr_pct': round(ccr_pct, 2),
            'ccr_tcra_target_pct': 98.0,
            'ccr_compliance_status': 'COMPLIANT' if ccr_pct >= 98.0 else 'BREACH',
            'call_drop_rate_cdr_pct': round(cdr_pct, 2),
            'cdr_tcra_target_pct': 0.8,
            'cdr_compliance_status': 'COMPLIANT' if cdr_pct <= 0.8 else 'BREACH',
            'congestion_blocking_pct': round(congestion_rate_pct, 2),
            'congestion_target_pct': 1.5,
            'congestion_compliance_status': 'COMPLIANT' if congestion_rate_pct <= 1.5 else 'BREACH'
        },
        'rafm_fraud_metrics': {
            'simbox_detected_count': len(simbox_suspects),
            'bypass_revenue_loss_tzs': round(total_bypass_revenue_loss_tzs, 2),
            'bypass_revenue_loss_usd': round(total_bypass_revenue_loss_tzs / USD_TZS_EXCHANGE_RATE, 2),
            'wangiri_detected_count': len(wangiri_suspects),
            'cloned_sim_impossible_travel_incidents': len(cloned_sim_incidents),
            'simbox_suspects_detail': simbox_suspects,
            'wangiri_suspects_detail': wangiri_suspects,
            'impossible_travel_detail': cloned_sim_incidents[:10]
        },
        'churn_and_segmentation': {
            'churn_risk_distribution': churn_distribution,
            'at_risk_churn_revenue_loss_tzs': round(high_risk_churn_revenue_loss_tzs, 2),
            'at_risk_churn_revenue_loss_usd': round(high_risk_churn_revenue_loss_tzs / USD_TZS_EXCHANGE_RATE, 2),
            'segments_summary': segment_summary,
            'top_influencer_nodes': top_influencers
        },
        'network_data_qos_by_tech': tech_metrics,
        'diurnal_hourly_traffic': [
            {
                'hour': h,
                'calls': ht['calls'],
                'answered': ht['answered'],
                'dropped': ht['dropped'],
                'erlangs': ht['erlangs'],
                'data_gb': round(ht['data_gb'], 2),
                'momo_txs': ht['momo_cnt']
            } for h, ht in sorted(hourly_traffic.items())
        ],
        'interconnect_settlement': clearing_house_summary,
        'tower_performance': tower_performance_list
    }

    output_json_path = os.path.join(WORKSPACE_DIR, 'millicom_telecom_metrics.json')
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_payload, f, indent=2)

    print("\n[SUCCESS] Telecommunications Analytics Engine finished successfully!")
    print(f"Metrics written to: {output_json_path}")
    return metrics_payload

if __name__ == '__main__':
    run_telecom_analytics()
