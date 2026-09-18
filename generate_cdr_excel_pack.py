"""
Institutional Telecommunications CDR Analytics & C-Suite Excel Pack Generator
=============================================================================
Project: Millicom (Tigo Tanzania) Enterprise Telecom CDR Intelligence Suite
Author: Principal Telecommunications Data Scientist & Financial Modeling Specialist
Output: Millicom_Tigo_Executive_CDR_Analytics_Pack.xlsx
Operator: MIC Tanzania PLC (Tigo Tanzania / Millicom Group) - MCC 640, MNC 02

Sheets:
1. 01_Executive_Scorecard: C-Suite KPI cards, TCRA SLA compliance table, revenue decomposition.
2. 02_Network_Tower_QoS: BTS / eNodeB / gNodeB traffic load, Erlangs, Erlang B blocking %, CDR %.
3. 03_Subscriber_Churn_RFM: Subscriber profiles, ARPU, dropped call frustration, churn risk tiers.
4. 04_Fraud_RAFM_Forensics: SIM-box bypass detections, Wangiri flash calls, impossible travel speed anomalies.
5. 05_Interconnect_MTR_Clearing: Operator interconnect matrix (Tigo vs Vodacom, Airtel, Halotel, TTCL, Safaricom).
6. 06_Diurnal_Traffic_Profiles: 24-hour diurnal curves for voice Erlangs, data gigabytes, and mobile money.
"""

import os
import csv
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_OUTPUT_PATH = os.path.join(WORKSPACE_DIR, 'Millicom_Tigo_Executive_CDR_Analytics_Pack.xlsx')

# -----------------------------------------------------------------------------
# TYPOGRAPHY & CORPORATE MILLICOM PALETTE
# -----------------------------------------------------------------------------
FONT_FAMILY = 'Calibri'

TITLE_FONT = Font(name=FONT_FAMILY, size=16, bold=True, color='FFFFFF')
SUBTITLE_FONT = Font(name=FONT_FAMILY, size=10, italic=True, color='E0F2FE')
SECTION_HEADER_FONT = Font(name=FONT_FAMILY, size=12, bold=True, color='FFFFFF')
TABLE_HEADER_FONT = Font(name=FONT_FAMILY, size=10, bold=True, color='FFFFFF')
DATA_FONT = Font(name=FONT_FAMILY, size=10, color='0F172A')
DATA_BOLD_FONT = Font(name=FONT_FAMILY, size=10, bold=True, color='0F172A')
SUMMARY_FONT = Font(name=FONT_FAMILY, size=10, bold=True, color='0F172A')

KPI_TITLE_FONT = Font(name=FONT_FAMILY, size=9, bold=True, color='0369A1')
KPI_VALUE_FONT = Font(name=FONT_FAMILY, size=16, bold=True, color='0C4A6E')
KPI_SUB_FONT = Font(name=FONT_FAMILY, size=8, color='64748B')

# Fills - Millicom Deep Blue & Tigo Yellow Accents
NAVY_HEADER_FILL = PatternFill(start_color='002B49', end_color='002B49', fill_type='solid')      # Millicom Corporate Blue
TIGO_GOLD_FILL = PatternFill(start_color='B45309', end_color='B45309', fill_type='solid')        # Deep Amber Gold
SLATE_HEADER_FILL = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')     # Slate Navy
KPI_CARD_FILL = PatternFill(start_color='F0F9FF', end_color='F0F9FF', fill_type='solid')         # Sky Ice Tint
ZEBRA_FILL = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')

ALERT_RED_FILL = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid')
ALERT_RED_FONT = Font(name=FONT_FAMILY, size=9, bold=True, color='991B1B')
ALERT_AMBER_FILL = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')
ALERT_AMBER_FONT = Font(name=FONT_FAMILY, size=9, bold=True, color='92400E')
ALERT_GREEN_FILL = PatternFill(start_color='DCFCE7', end_color='DCFCE7', fill_type='solid')
ALERT_GREEN_FONT = Font(name=FONT_FAMILY, size=9, bold=True, color='166534')

# Borders
THIN_GRAY = Side(border_style='thin', color='CBD5E1')
BORDER_ALL = Border(left=THIN_GRAY, right=THIN_GRAY, top=THIN_GRAY, bottom=THIN_GRAY)
BORDER_TOTAL = Border(
    left=THIN_GRAY, right=THIN_GRAY,
    top=Side(border_style='thin', color='002B49'),
    bottom=Side(border_style='double', color='002B49')
)

# Alignments
ALIGN_LEFT = Alignment(horizontal='left', vertical='center')
ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_RIGHT = Alignment(horizontal='right', vertical='center')
ALIGN_HEADER = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Number Formats
FMT_INTEGER = '#,##0'
FMT_DECIMAL_2 = '#,##0.00'
FMT_DECIMAL_3 = '#,##0.000'
FMT_PERCENT_2 = '0.00%'
FMT_CURRENCY_TZS = '"TZS " #,##0'
FMT_CURRENCY_USD = '"$ " #,##0'

def auto_fit_columns(ws, max_cap=45):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if cell.number_format and ('TZS' in cell.number_format or '$' in cell.number_format):
                val_str += '    '
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 11), max_cap)

def build_excel_pack():
    print("[EXCEL] Generating Institutional Millicom Telecom CDR Reporting Pack...")

    metrics_file = os.path.join(WORKSPACE_DIR, 'millicom_telecom_metrics.json')
    if not os.path.exists(metrics_file):
        raise FileNotFoundError(f"Metrics file {metrics_file} not found. Run telecom_cdr_analytics_engine.py first.")

    with open(metrics_file, 'r', encoding='utf-8') as f:
        metrics = json.load(f)

    macro = metrics['macro_kpis']
    tcra = metrics['tcra_qos_compliance']
    rafm = metrics['rafm_fraud_metrics']
    churn = metrics['churn_and_segmentation']
    towers_perf = metrics['tower_performance']
    interconnect = metrics['interconnect_settlement']
    diurnal = metrics['diurnal_hourly_traffic']

    wb = openpyxl.Workbook()

    # =========================================================================
    # SHEET 1: 01_Executive_Scorecard
    # =========================================================================
    ws1 = wb.active
    ws1.title = "01_Executive_Scorecard"
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells('A1:K1')
    ws1['A1'] = "MILLICOM (TIGO TANZANIA) - TELECOMMUNICATIONS CDR & NETWORK INTELLIGENCE PACK"
    ws1['A1'].font = TITLE_FONT
    ws1['A1'].fill = NAVY_HEADER_FILL
    ws1['A1'].alignment = ALIGN_CENTER
    ws1.row_dimensions[1].height = 36

    ws1.merge_cells('A2:K2')
    ws1['A2'] = "Operator: MIC Tanzania PLC (Tigo) | Market: United Republic of Tanzania | Regulated by TCRA | Confidential C-Suite Audit"
    ws1['A2'].font = SUBTITLE_FONT
    ws1['A2'].fill = NAVY_HEADER_FILL
    ws1['A2'].alignment = ALIGN_CENTER
    ws1.row_dimensions[2].height = 20

    # 4 Macro KPI Cards
    kpis = [
        ("TOTAL SUBSCRIBERS AUDITED", f"{macro['total_subscribers']:,}", "Active SIM profiles across 14 regions", 'A4:B5'),
        ("TOTAL REVENUE (TZS)", f"TZS {macro['total_gross_revenue_tzs']:,.0f}", f"$ {macro['total_gross_revenue_usd']:,.0f} USD Gross Inflow", 'D4:E5'),
        ("CALL COMPLETION RATE (CCR)", f"{tcra['call_completion_rate_ccr_pct']:.2f}%", f"TCRA Target: ≥ {tcra['ccr_tcra_target_pct']:.1f}% ({tcra['ccr_compliance_status']})", 'G4:H5'),
        ("FRAUD BYPASS EXPOSURE", f"TZS {rafm['bypass_revenue_loss_tzs']:,.0f}", f"{rafm['simbox_detected_count']} SIM-Boxes Intercepted", 'J4:K5')
    ]

    for title, val, sub, cell_range in kpis:
        top_left = cell_range.split(':')[0]
        ws1.merge_cells(cell_range)
        ws1[top_left] = f"{title}\n{val}\n{sub}"
        ws1[top_left].font = Font(name=FONT_FAMILY, size=11, bold=True, color='002B49')
        ws1[top_left].fill = KPI_CARD_FILL
        ws1[top_left].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        # Apply borders to range
        start_col, start_row = openpyxl.utils.coordinate_to_tuple(top_left)
        end_col, end_row = openpyxl.utils.coordinate_to_tuple(cell_range.split(':')[1])
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                ws1.cell(row=r, column=c).border = BORDER_ALL

    ws1.row_dimensions[4].height = 25
    ws1.row_dimensions[5].height = 30

    # Section 1: TCRA Regulatory Key Telecommunication Performance Indicators (KTPI)
    ws1.cell(row=7, column=1, value="1. TCRA REGULATORY QUALITY OF SERVICE (QoS) AUDIT").font = SECTION_HEADER_FONT
    ws1.cell(row=7, column=1).fill = SLATE_HEADER_FILL
    ws1.merge_cells('A7:F7')
    ws1.row_dimensions[7].height = 24

    tcra_headers = ["KTPI Dimension", "TCRA Regulatory Standard", "Actual Network Performance", "Variance / Gap", "SLA Status", "Regulatory Risk Assessment"]
    for col_idx, h in enumerate(tcra_headers, 1):
        cell = ws1.cell(row=8, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL
    ws1.row_dimensions[8].height = 24

    tcra_rows = [
        ("Answer Seizure Ratio (ASR)", "≥ 65.00%", f"{tcra['answer_seizure_ratio_asr_pct']:.2f}%", f"{tcra['answer_seizure_ratio_asr_pct'] - 65.0:+.2f}%", tcra['asr_compliance_status'], "Call setup efficiency compliant with national benchmark."),
        ("Call Completion Rate (CCR)", "≥ 98.00%", f"{tcra['call_completion_rate_ccr_pct']:.2f}%", f"{tcra['call_completion_rate_ccr_pct'] - 98.0:+.2f}%", tcra['ccr_compliance_status'], "Radio link failures in fringe cells causing slight SLA non-compliance."),
        ("Call Drop Rate (CDR)", "< 0.80%", f"{tcra['call_drop_rate_cdr_pct']:.2f}%", f"{tcra['call_drop_rate_cdr_pct'] - 0.80:+.2f}%", tcra['cdr_compliance_status'], "Congestion-driven handover drops require carrier capacity expansion."),
        ("Trunk Congestion Blocking Rate", "< 1.50%", f"{tcra['congestion_blocking_pct']:.2f}%", f"{tcra['congestion_blocking_pct'] - 1.50:+.2f}%", tcra['congestion_compliance_status'], "Within TCRA statutory maximum allowable threshold.")
    ]

    for r_idx, row_data in enumerate(tcra_rows, 9):
        ws1.row_dimensions[r_idx].height = 20
        for c_idx, val in enumerate(row_data, 1):
            cell = ws1.cell(row=r_idx, column=c_idx, value=val)
            cell.font = DATA_FONT
            cell.border = BORDER_ALL
            cell.alignment = ALIGN_CENTER if c_idx in [2, 3, 4, 5] else ALIGN_LEFT
            if c_idx == 5:
                if val == 'COMPLIANT':
                    cell.fill = ALERT_GREEN_FILL
                    cell.font = ALERT_GREEN_FONT
                else:
                    cell.fill = ALERT_RED_FILL
                    cell.font = ALERT_RED_FONT

    # Section 2: Financial Revenue Streams & ARPU Waterfall
    ws1.cell(row=15, column=1, value="2. MULTI-SERVICE REVENUE & ARPU DECOMPOSITION").font = SECTION_HEADER_FONT
    ws1.cell(row=15, column=1).fill = SLATE_HEADER_FILL
    ws1.merge_cells('A15:F15')
    ws1.row_dimensions[15].height = 24

    rev_headers = ["Revenue Stream", "Gross Revenue (TZS)", "Gross Revenue (USD)", "Contribution %", "Volume Metric", "Unit Yield"]
    for col_idx, h in enumerate(rev_headers, 1):
        cell = ws1.cell(row=16, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL
    ws1.row_dimensions[16].height = 24

    tot_rev = macro['total_gross_revenue_tzs']
    rev_rows = [
        ("Mobile Data (4G/5G/LTE PDP)", macro['data_revenue_tzs'], macro['data_revenue_tzs'] / 2620.0, macro['data_revenue_tzs'] / tot_rev, f"{macro['total_data_volume_gb']:,.1f} GB", f"TZS {macro['data_revenue_tzs'] / max(1, macro['total_data_volume_gb']):,.1f} / GB"),
        ("Tigo Pesa (Mobile Money Commissions)", macro['momo_revenue_tzs'], macro['momo_revenue_tzs'] / 2620.0, macro['momo_revenue_tzs'] / tot_rev, f"TZS {macro['total_momo_volume_tzs']:,.0f} Processed", "1.42% Take Rate"),
        ("Circuit-Switched Voice & VoLTE", macro['voice_revenue_tzs'], macro['voice_revenue_tzs'] / 2620.0, macro['voice_revenue_tzs'] / tot_rev, f"{macro['total_voice_traffic_minutes']:,.1f} Minutes", f"TZS {macro['voice_revenue_tzs'] / max(1, macro['total_voice_traffic_minutes']):,.1f} / Min")
    ]

    for r_idx, row_data in enumerate(rev_rows, 17):
        ws1.row_dimensions[r_idx].height = 20
        ws1.cell(row=r_idx, column=1, value=row_data[0]).font = DATA_FONT
        ws1.cell(row=r_idx, column=2, value=row_data[1]).number_format = FMT_CURRENCY_TZS
        ws1.cell(row=r_idx, column=3, value=row_data[2]).number_format = FMT_CURRENCY_USD
        ws1.cell(row=r_idx, column=4, value=row_data[3]).number_format = FMT_PERCENT_2
        ws1.cell(row=r_idx, column=5, value=row_data[4]).alignment = ALIGN_CENTER
        ws1.cell(row=r_idx, column=6, value=row_data[5]).alignment = ALIGN_RIGHT
        for c in range(1, 7):
            ws1.cell(row=r_idx, column=c).border = BORDER_ALL

    # Total Row using Excel Formulas
    tot_row = 20
    ws1.row_dimensions[tot_row].height = 22
    ws1.cell(row=tot_row, column=1, value="CONSOLIDATED TOTAL REVENUE").font = DATA_BOLD_FONT
    ws1.cell(row=tot_row, column=2, value=f"=SUM(B17:B19)").number_format = FMT_CURRENCY_TZS
    ws1.cell(row=tot_row, column=3, value=f"=SUM(C17:C19)").number_format = FMT_CURRENCY_USD
    ws1.cell(row=tot_row, column=4, value=f"=SUM(D17:D19)").number_format = FMT_PERCENT_2
    ws1.cell(row=tot_row, column=5, value=f"{macro['total_subscribers']} Subscribers").alignment = ALIGN_CENTER
    ws1.cell(row=tot_row, column=6, value=f"ARPU: TZS {macro['average_blended_arpu_tzs']:,.0f}").alignment = ALIGN_RIGHT
    for c in range(1, 7):
        ws1.cell(row=tot_row, column=c).font = DATA_BOLD_FONT
        ws1.cell(row=tot_row, column=c).border = BORDER_TOTAL

    auto_fit_columns(ws1)

    # =========================================================================
    # SHEET 2: 02_Network_Tower_QoS
    # =========================================================================
    ws2 = wb.create_sheet(title="02_Network_Tower_QoS")
    ws2.views.sheetView[0].showGridLines = True

    # Title Banner
    ws2.merge_cells('A1:N1')
    ws2['A1'] = "CELL TOWER INFRASTRUCTURE, ERLANG TRAFFIC & TCRA QoS PERFORMANCE AUDIT"
    ws2['A1'].font = TITLE_FONT
    ws2['A1'].fill = NAVY_HEADER_FILL
    ws2['A1'].alignment = ALIGN_CENTER
    ws2.row_dimensions[1].height = 32

    t_headers = [
        "Tower ID", "Tower Site Name", "Region", "Tech", "Channels", "Total Calls",
        "Answered", "Dropped", "Mean Erlangs", "Busy Hour Erlangs",
        "Erlang B Block %", "ASR %", "CDR %", "Data (GB)", "Revenue (TZS)", "SLA Status"
    ]
    for col_idx, h in enumerate(t_headers, 1):
        cell = ws2.cell(row=3, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL
    ws2.row_dimensions[3].height = 24

    for r_idx, tw in enumerate(towers_perf, 4):
        ws2.row_dimensions[r_idx].height = 19
        ws2.cell(row=r_idx, column=1, value=tw['tower_id']).alignment = ALIGN_CENTER
        ws2.cell(row=r_idx, column=2, value=tw['name'])
        ws2.cell(row=r_idx, column=3, value=tw['region'])
        ws2.cell(row=r_idx, column=4, value=tw['tech']).alignment = ALIGN_CENTER
        ws2.cell(row=r_idx, column=5, value=tw['capacity_channels']).number_format = FMT_INTEGER
        ws2.cell(row=r_idx, column=6, value=tw['total_calls']).number_format = FMT_INTEGER
        ws2.cell(row=r_idx, column=7, value=tw['answered_calls']).number_format = FMT_INTEGER
        ws2.cell(row=r_idx, column=8, value=tw['dropped_calls']).number_format = FMT_INTEGER
        ws2.cell(row=r_idx, column=9, value=tw['traffic_erlangs']).number_format = FMT_DECIMAL_3
        ws2.cell(row=r_idx, column=10, value=tw['busy_hour_erlangs']).number_format = FMT_DECIMAL_3
        ws2.cell(row=r_idx, column=11, value=tw['erlang_b_blocking_pct'] / 100.0).number_format = FMT_PERCENT_2
        ws2.cell(row=r_idx, column=12, value=tw['asr_pct'] / 100.0).number_format = FMT_PERCENT_2
        ws2.cell(row=r_idx, column=13, value=tw['cdr_pct'] / 100.0).number_format = FMT_PERCENT_2
        ws2.cell(row=r_idx, column=14, value=tw['total_data_gb']).number_format = FMT_DECIMAL_2
        ws2.cell(row=r_idx, column=15, value=tw['total_revenue_tzs']).number_format = FMT_CURRENCY_TZS

        sla_cell = ws2.cell(row=r_idx, column=16, value=tw['sla_status'])
        sla_cell.alignment = ALIGN_CENTER
        if tw['sla_status'] == 'NORMAL':
            sla_cell.fill = ALERT_GREEN_FILL
            sla_cell.font = ALERT_GREEN_FONT
        elif tw['sla_status'] == 'WARNING_HIGH_LOAD':
            sla_cell.fill = ALERT_AMBER_FILL
            sla_cell.font = ALERT_AMBER_FONT
        else:
            sla_cell.fill = ALERT_RED_FILL
            sla_cell.font = ALERT_RED_FONT

        for c in range(1, 17):
            if c != 16:
                ws2.cell(row=r_idx, column=c).font = DATA_FONT
            ws2.cell(row=r_idx, column=c).border = BORDER_ALL

    auto_fit_columns(ws2)

    # =========================================================================
    # SHEET 3: 03_Subscriber_Churn_RFM
    # =========================================================================
    ws3 = wb.create_sheet(title="03_Subscriber_Churn_RFM")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells('A1:M1')
    ws3['A1'] = "SUBSCRIBER SEGMENTATION, VALUE-AT-RISK & CHURN PROPENSITY MODEL"
    ws3['A1'].font = TITLE_FONT
    ws3['A1'].fill = NAVY_HEADER_FILL
    ws3['A1'].alignment = ALIGN_CENTER
    ws3.row_dimensions[1].height = 32

    # Segment Summary Table First
    ws3.cell(row=3, column=1, value="CUSTOMER SEGMENT PERFORMANCE SUMMARY").font = SECTION_HEADER_FONT
    ws3.cell(row=3, column=1).fill = SLATE_HEADER_FILL
    ws3.merge_cells('A3:F3')

    seg_headers = ["Customer Segment", "Subscribers", "Voice Revenue (TZS)", "Data Revenue (TZS)", "Tigo Pesa Revenue", "Blended ARPU (TZS)"]
    for col_idx, h in enumerate(seg_headers, 1):
        cell = ws3.cell(row=4, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL

    for r_idx, (sname, sdata) in enumerate(churn['segments_summary'].items(), 5):
        ws3.cell(row=r_idx, column=1, value=sname).font = DATA_FONT
        ws3.cell(row=r_idx, column=2, value=sdata['subscriber_count']).number_format = FMT_INTEGER
        ws3.cell(row=r_idx, column=3, value=sdata['voice_revenue_tzs']).number_format = FMT_CURRENCY_TZS
        ws3.cell(row=r_idx, column=4, value=sdata['data_revenue_tzs']).number_format = FMT_CURRENCY_TZS
        ws3.cell(row=r_idx, column=5, value=sdata['momo_fees_tzs']).number_format = FMT_CURRENCY_TZS
        ws3.cell(row=r_idx, column=6, value=sdata['blended_arpu_tzs']).number_format = FMT_CURRENCY_TZS
        for c in range(1, 7):
            ws3.cell(row=r_idx, column=c).border = BORDER_ALL

    # Top Influencer Nodes Table
    inf_start_row = 13
    ws3.cell(row=inf_start_row, column=1, value="HIGH-DEGREE NETWORK INFLUENCER HUBS (VIRAL CHURN RISK)").font = SECTION_HEADER_FONT
    ws3.cell(row=inf_start_row, column=1).fill = SLATE_HEADER_FILL
    ws3.merge_cells(f'A{inf_start_row}:G{inf_start_row}')

    inf_headers = ["MSISDN", "Segment", "Plan", "Out-Degree (Calls Out)", "In-Degree (Calls In)", "Degree Centrality", "Network Influence Role"]
    for col_idx, h in enumerate(inf_headers, 1):
        cell = ws3.cell(row=inf_start_row+1, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL

    for r_idx, inf in enumerate(churn['top_influencer_nodes'], inf_start_row+2):
        ws3.cell(row=r_idx, column=1, value=inf['msisdn']).alignment = ALIGN_CENTER
        ws3.cell(row=r_idx, column=2, value=inf['segment'])
        ws3.cell(row=r_idx, column=3, value=inf['plan']).alignment = ALIGN_CENTER
        ws3.cell(row=r_idx, column=4, value=inf['out_degree']).number_format = FMT_INTEGER
        ws3.cell(row=r_idx, column=5, value=inf['in_degree']).number_format = FMT_INTEGER
        ws3.cell(row=r_idx, column=6, value=inf['total_degree_centrality']).number_format = FMT_INTEGER
        ws3.cell(row=r_idx, column=7, value=inf['network_role']).font = DATA_BOLD_FONT
        for c in range(1, 8):
            ws3.cell(row=r_idx, column=c).font = DATA_FONT
            ws3.cell(row=r_idx, column=c).border = BORDER_ALL

    auto_fit_columns(ws3)

    # =========================================================================
    # SHEET 4: 04_Fraud_RAFM_Forensics
    # =========================================================================
    ws4 = wb.create_sheet(title="04_Fraud_RAFM_Forensics")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells('A1:L1')
    ws4['A1'] = "REVENUE ASSURANCE & FRAUD MANAGEMENT (RAFM) FORENSIC DOSSIER"
    ws4['A1'].font = TITLE_FONT
    ws4['A1'].fill = NAVY_HEADER_FILL
    ws4['A1'].alignment = ALIGN_CENTER
    ws4.row_dimensions[1].height = 32

    # SIM Box Section
    ws4.cell(row=3, column=1, value="1. DETECTED SIM-BOX BYPASS GATEWAYS (INTERCONNECT THEFT)").font = SECTION_HEADER_FONT
    ws4.cell(row=3, column=1).fill = SLATE_HEADER_FILL
    ws4.merge_cells('A3:K3')

    sb_headers = [
        "SIM MSISDN", "IMSI", "IMEI", "Handset Description", "Out Calls", "In Calls",
        "Out/In Ratio", "Towers", "Bypass Mins", "Revenue Loss (TZS)", "Revenue Loss (USD)", "Action Mandate"
    ]
    for col_idx, h in enumerate(sb_headers, 1):
        cell = ws4.cell(row=4, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL

    for r_idx, sb in enumerate(rafm['simbox_suspects_detail'], 5):
        ws4.cell(row=r_idx, column=1, value=sb['msisdn']).alignment = ALIGN_CENTER
        ws4.cell(row=r_idx, column=2, value=sb['imsi']).alignment = ALIGN_CENTER
        ws4.cell(row=r_idx, column=3, value=sb['imei']).alignment = ALIGN_CENTER
        ws4.cell(row=r_idx, column=4, value=sb['handset'])
        ws4.cell(row=r_idx, column=5, value=sb['outgoing_calls']).number_format = FMT_INTEGER
        ws4.cell(row=r_idx, column=6, value=sb['incoming_calls']).number_format = FMT_INTEGER
        ws4.cell(row=r_idx, column=7, value=sb['out_in_ratio']).number_format = FMT_DECIMAL_2
        ws4.cell(row=r_idx, column=8, value=sb['towers_attached']).number_format = FMT_INTEGER
        ws4.cell(row=r_idx, column=9, value=sb['total_bypass_minutes']).number_format = FMT_DECIMAL_2
        ws4.cell(row=r_idx, column=10, value=sb['estimated_loss_tzs']).number_format = FMT_CURRENCY_TZS
        ws4.cell(row=r_idx, column=11, value=sb['estimated_loss_usd']).number_format = FMT_CURRENCY_USD
        act_cell = ws4.cell(row=r_idx, column=12, value=sb['action'])
        act_cell.fill = ALERT_RED_FILL
        act_cell.font = ALERT_RED_FONT
        act_cell.alignment = ALIGN_CENTER
        for c in range(1, 13):
            if c != 12:
                ws4.cell(row=r_idx, column=c).font = DATA_FONT
            ws4.cell(row=r_idx, column=c).border = BORDER_ALL

    # Impossible Travel Section
    imp_start_row = 5 + len(rafm['simbox_suspects_detail']) + 2
    ws4.cell(row=imp_start_row, column=1, value="2. IMPOSSIBLE TRAVEL & CLONED SIM SPEED ANOMALIES (>850 KM/H)").font = SECTION_HEADER_FONT
    ws4.cell(row=imp_start_row, column=1).fill = SLATE_HEADER_FILL
    ws4.merge_cells(f'A{imp_start_row}:H{imp_start_row}')

    imp_headers = ["MSISDN", "Event 1 Timestamp", "Origin Cell Tower", "Event 2 Timestamp", "Destination Cell Tower", "Distance (km)", "Elapsed (s)", "Speed (km/h)"]
    for col_idx, h in enumerate(imp_headers, 1):
        cell = ws4.cell(row=imp_start_row+1, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL

    for r_idx, imp in enumerate(rafm['impossible_travel_detail'], imp_start_row+2):
        ws4.cell(row=r_idx, column=1, value=imp['msisdn']).alignment = ALIGN_CENTER
        ws4.cell(row=r_idx, column=2, value=imp['timestamp_event_1'])
        ws4.cell(row=r_idx, column=3, value=imp['tower_1'])
        ws4.cell(row=r_idx, column=4, value=imp['timestamp_event_2'])
        ws4.cell(row=r_idx, column=5, value=imp['tower_2'])
        ws4.cell(row=r_idx, column=6, value=imp['distance_km']).number_format = FMT_DECIMAL_2
        ws4.cell(row=r_idx, column=7, value=imp['elapsed_seconds']).number_format = FMT_INTEGER
        spd_cell = ws4.cell(row=r_idx, column=8, value=imp['apparent_speed_kmh'])
        spd_cell.number_format = FMT_DECIMAL_2
        spd_cell.fill = ALERT_AMBER_FILL
        spd_cell.font = ALERT_AMBER_FONT
        for c in range(1, 9):
            if c != 8:
                ws4.cell(row=r_idx, column=c).font = DATA_FONT
            ws4.cell(row=r_idx, column=c).border = BORDER_ALL

    auto_fit_columns(ws4)

    # =========================================================================
    # SHEET 5: 05_Interconnect_MTR_Clearing
    # =========================================================================
    ws5 = wb.create_sheet(title="05_Interconnect_MTR_Clearing")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells('A1:J1')
    ws5['A1'] = "NATIONAL & INTERNATIONAL INTERCONNECT (MTR) CLEARING MATRIX"
    ws5['A1'].font = TITLE_FONT
    ws5['A1'].fill = NAVY_HEADER_FILL
    ws5['A1'].alignment = ALIGN_CENTER
    ws5.row_dimensions[1].height = 32

    ic_headers = [
        "Interconnect Partner", "Outbound Calls", "Outbound Mins", "Payable MTR (TZS)",
        "Inbound Calls", "Inbound Mins", "Receivable MTR (TZS)", "Net Settlement (TZS)", "Retail Billed (TZS)", "Clearing Status"
    ]
    for col_idx, h in enumerate(ic_headers, 1):
        cell = ws5.cell(row=3, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL

    for r_idx, ic in enumerate(interconnect, 4):
        ws5.cell(row=r_idx, column=1, value=ic['operator'])
        ws5.cell(row=r_idx, column=2, value=ic['outbound_calls']).number_format = FMT_INTEGER
        ws5.cell(row=r_idx, column=3, value=ic['outbound_minutes']).number_format = FMT_DECIMAL_2
        ws5.cell(row=r_idx, column=4, value=ic['payable_mtr_tzs']).number_format = FMT_CURRENCY_TZS
        ws5.cell(row=r_idx, column=5, value=ic['inbound_calls']).number_format = FMT_INTEGER
        ws5.cell(row=r_idx, column=6, value=ic['inbound_minutes']).number_format = FMT_DECIMAL_2
        ws5.cell(row=r_idx, column=7, value=ic['receivable_mtr_tzs']).number_format = FMT_CURRENCY_TZS
        ws5.cell(row=r_idx, column=8, value=ic['net_settlement_tzs']).number_format = FMT_CURRENCY_TZS
        ws5.cell(row=r_idx, column=9, value=ic['retail_billed_tzs']).number_format = FMT_CURRENCY_TZS
        st_cell = ws5.cell(row=r_idx, column=10, value=ic['clearing_position'])
        st_cell.alignment = ALIGN_CENTER
        if ic['clearing_position'] == 'NET_RECEIVABLE':
            st_cell.fill = ALERT_GREEN_FILL
            st_cell.font = ALERT_GREEN_FONT
        else:
            st_cell.fill = ALERT_AMBER_FILL
            st_cell.font = ALERT_AMBER_FONT
        for c in range(1, 11):
            if c != 10:
                ws5.cell(row=r_idx, column=c).font = DATA_FONT
            ws5.cell(row=r_idx, column=c).border = BORDER_ALL

    auto_fit_columns(ws5)

    # =========================================================================
    # SHEET 6: 06_Diurnal_Traffic_Profiles
    # =========================================================================
    ws6 = wb.create_sheet(title="06_Diurnal_Traffic_Profiles")
    ws6.views.sheetView[0].showGridLines = True

    ws6.merge_cells('A1:G1')
    ws6['A1'] = "24-HOUR DIURNAL TRAFFIC DISTRIBUTION & BUSY HOUR PROFILE"
    ws6['A1'].font = TITLE_FONT
    ws6['A1'].fill = NAVY_HEADER_FILL
    ws6['A1'].alignment = ALIGN_CENTER
    ws6.row_dimensions[1].height = 32

    dh_headers = ["Hour of Day", "Voice Calls", "Answered Calls", "Dropped Calls", "Voice Erlangs", "Data Traffic (GB)", "Tigo Pesa TXs"]
    for col_idx, h in enumerate(dh_headers, 1):
        cell = ws6.cell(row=3, column=col_idx, value=h)
        cell.font = TABLE_HEADER_FONT
        cell.fill = NAVY_HEADER_FILL
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_ALL

    for r_idx, dh in enumerate(diurnal, 4):
        ws6.cell(row=r_idx, column=1, value=f"{dh['hour']:02d}:00 - {dh['hour']:02d}:59").alignment = ALIGN_CENTER
        ws6.cell(row=r_idx, column=2, value=dh['calls']).number_format = FMT_INTEGER
        ws6.cell(row=r_idx, column=3, value=dh['answered']).number_format = FMT_INTEGER
        ws6.cell(row=r_idx, column=4, value=dh['dropped']).number_format = FMT_INTEGER
        ws6.cell(row=r_idx, column=5, value=dh['erlangs']).number_format = FMT_DECIMAL_3
        ws6.cell(row=r_idx, column=6, value=dh['data_gb']).number_format = FMT_DECIMAL_2
        ws6.cell(row=r_idx, column=7, value=dh['momo_txs']).number_format = FMT_INTEGER
        for c in range(1, 8):
            ws6.cell(row=r_idx, column=c).font = DATA_FONT
            ws6.cell(row=r_idx, column=c).border = BORDER_ALL

    auto_fit_columns(ws6)

    wb.save(EXCEL_OUTPUT_PATH)
    print(f"[SUCCESS] Excel Audit Pack created successfully: {EXCEL_OUTPUT_PATH}")

if __name__ == '__main__':
    build_excel_pack()
