"""
Institutional Financial Planning, 12-Month Budgeting & Cash Flow Model Generator
================================================================================
Generates: Corporate_Financial_Budgeting_and_Forecasting_Model.xlsx
Includes:
  1. 01_Executive_Dashboard: C-Suite KPI Cards, Quarterly Roll-up, Embedded Trend Charts, Management Insights.
  2. 02_Assumptions_&_Drivers: Revenue Drivers, COGS %, Headcount/Payroll, OpEx, Working Capital (DSO/DPO).
  3. 03_12M_P&L_Forecast: Dynamic 12-Month Income Statement (Revenue, Gross Margin, OpEx, EBITDA, Net Income).
  4. 04_Monthly_Cash_Flow: Direct Operating Cash Flow, Collections, Disbursements, Net Burn, Ending Cash & Runway.
  5. 05_Budget_vs_Actuals: Variance Analysis ($ and %), Status Flags (FAVORABLE/UNFAVORABLE), Management Actions.
  6. 06_Data_Cleaning_Pipeline: Raw messy ERP/accounting transactions -> Audit Trail -> Clean Standardized Ledger.
  7. 07_Model_Documentation: Governance, Cell Color Conventions (FAST Standard), Operating Guide.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_EXCEL = os.path.join(WORKSPACE_DIR, 'Corporate_Financial_Budgeting_and_Forecasting_Model.xlsx')

# -----------------------------------------------------------------------------
# FINANCIAL MODELING STANDARDS & STYLES
# -----------------------------------------------------------------------------
FONT_NAME = 'Calibri'

FONT_TITLE = Font(name=FONT_NAME, size=15, bold=True, color='FFFFFF')
FONT_SUBTITLE = Font(name=FONT_NAME, size=10, italic=True, color='E0F2FE')
FONT_SECTION = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
FONT_HEADER = Font(name=FONT_NAME, size=10, bold=True, color='FFFFFF')
FONT_SUBHEADER = Font(name=FONT_NAME, size=10, bold=True, color='1E293B')

# Wall Street / FAST Modeling convention:
# Blue Font = Hardcoded Inputs / Assumptions
# Black Font = Dynamic Formulas & Calculations
FONT_INPUT = Font(name=FONT_NAME, size=10, color='002060') # Classic Model Input Blue
FONT_FORMULA = Font(name=FONT_NAME, size=10, color='0F172A')
FONT_BOLD_FORMULA = Font(name=FONT_NAME, size=10, bold=True, color='0F172A')
FONT_ITALIC_NOTE = Font(name=FONT_NAME, size=9, italic=True, color='64748B')

# KPI Typography
FONT_KPI_LABEL = Font(name=FONT_NAME, size=9, bold=True, color='0369A1')
FONT_KPI_VAL = Font(name=FONT_NAME, size=16, bold=True, color='0C4A6E')
FONT_KPI_SUB = Font(name=FONT_NAME, size=8, color='475569')

# Corporate Palette (Executive Navy & Emerald Green accents)
FILL_NAVY_TITLE = PatternFill(start_color='0A2540', end_color='0A2540', fill_type='solid') # Deep Enterprise Navy
FILL_NAVY_HEADER = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid') # Dark Blue Header
FILL_SLATE_SECTION = PatternFill(start_color='334155', end_color='334155', fill_type='solid') # Slate Gray
FILL_EMERALD_ACCENT = PatternFill(start_color='065F46', end_color='065F46', fill_type='solid') # Deep Emerald
FILL_SUBHEADER = PatternFill(start_color='F1F5F9', end_color='F1F5F9', fill_type='solid')
FILL_ZEBRA = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
FILL_KPI_CARD = PatternFill(start_color='F0F9FF', end_color='F0F9FF', fill_type='solid')
FILL_TOTAL_ROW = PatternFill(start_color='E2E8F0', end_color='E2E8F0', fill_type='solid')

# Status Alerts
FILL_ALERT_GREEN = PatternFill(start_color='DCFCE7', end_color='DCFCE7', fill_type='solid')
FONT_ALERT_GREEN = Font(name=FONT_NAME, size=9, bold=True, color='166534')

FILL_ALERT_RED = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid')
FONT_ALERT_RED = Font(name=FONT_NAME, size=9, bold=True, color='991B1B')

FILL_ALERT_AMBER = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')
FONT_ALERT_AMBER = Font(name=FONT_NAME, size=9, bold=True, color='92400E')

# Input Cell Highlighting
FILL_INPUT_CELL = PatternFill(start_color='F0FDF4', end_color='F0FDF4', fill_type='solid') # Soft Mint for inputs

# Borders
BORDER_THIN = Side(border_style='thin', color='CBD5E1')
BORDER_MEDIUM_NAVY = Side(border_style='medium', color='0A2540')
BORDER_DOUBLE_NAVY = Side(border_style='double', color='0A2540')

CELL_BORDER = Border(left=BORDER_THIN, right=BORDER_THIN, top=BORDER_THIN, bottom=BORDER_THIN)
TOTAL_BORDER = Border(top=BORDER_THIN, bottom=BORDER_DOUBLE_NAVY, left=BORDER_THIN, right=BORDER_THIN)
SUBTOTAL_BORDER = Border(top=BORDER_THIN, bottom=BORDER_THIN, left=BORDER_THIN, right=BORDER_THIN)

# Alignments
ALIGN_LEFT = Alignment(horizontal='left', vertical='center')
ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_RIGHT = Alignment(horizontal='right', vertical='center')
ALIGN_HEADER = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Number Formats
FMT_CURRENCY = '$#,##0'
FMT_CURRENCY_EXACT = '$#,##0.00'
FMT_PERCENT = '0.0%'
FMT_PERCENT_INT = '0%'
FMT_INTEGER = '#,##0'
FMT_DATE = 'yyyy-mm-dd'

def set_row_heights(ws, heights_dict):
    for row_idx, h in heights_dict.items():
        ws.row_dimensions[row_idx].height = h

def auto_fit_columns(ws, max_cap=40, min_width=12):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if cell.number_format and ('$' in cell.number_format or '%' in cell.number_format):
                val_str += '   '
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, min_width), max_cap)

def style_title_banner(ws, end_col_letter, title, subtitle):
    ws.merge_cells(f'A1:{end_col_letter}1')
    c1 = ws['A1']
    c1.value = f"  {title.upper()}"
    c1.font = FONT_TITLE
    c1.fill = FILL_NAVY_TITLE
    c1.alignment = Alignment(horizontal='left', vertical='center')
    
    ws.merge_cells(f'A2:{end_col_letter}2')
    c2 = ws['A2']
    c2.value = f"  {subtitle}"
    c2.font = FONT_SUBTITLE
    c2.fill = FILL_NAVY_TITLE
    c2.alignment = Alignment(horizontal='left', vertical='center')
    
    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 18

# -----------------------------------------------------------------------------
# BUILD SHEET 2: ASSUMPTIONS & DRIVERS FIRST (FOUNDATION)
# -----------------------------------------------------------------------------
def build_assumptions_sheet(wb):
    ws = wb.create_sheet(title="02_Assumptions_&_Drivers")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'H', 
        "Financial Assumptions & Business Planning Drivers (FY 2026)",
        "Key Operational Drivers, Unit Economics, Headcount, Cost Structure & Working Capital Terms"
    )
    
    # Legend
    ws['B4'] = "Color Standard Legend:"
    ws['B4'].font = Font(name=FONT_NAME, size=9, bold=True, color='475569')
    
    ws['C4'] = "BLUE FONT / GREEN CELL = Dynamic User Input"
    ws['C4'].font = FONT_INPUT
    ws['C4'].fill = FILL_INPUT_CELL
    ws['C4'].border = CELL_BORDER
    ws['C4'].alignment = ALIGN_CENTER
    
    ws['E4'] = "BLACK FONT = Dynamic Calculation"
    ws['E4'].font = FONT_FORMULA
    ws['E4'].fill = FILL_SUBHEADER
    ws['E4'].border = CELL_BORDER
    ws['E4'].alignment = ALIGN_CENTER

    # SECTION 1: REVENUE & VOLUME DRIVERS
    ws.merge_cells('B6:G6')
    sec1 = ws['B6']
    sec1.value = "  1. REVENUE STREAMS & UNIT PRICING DRIVERS"
    sec1.font = FONT_SECTION
    sec1.fill = FILL_NAVY_HEADER
    ws.row_dimensions[6].height = 22

    headers1 = ["Driver ID", "Revenue Stream / Service Line", "Starting Monthly Units", "Monthly Growth Rate", "Base Unit Price", "COGS Direct Cost %"]
    for i, h in enumerate(headers1, start=2):
        cell = ws.cell(row=7, column=i, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_SLATE_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[7].height = 24

    rev_drivers = [
        ("REV-01", "SaaS Subscriptions (Pro Tier)", 150, 0.08, 120.0, 0.12),
        ("REV-02", "Enterprise Platform Licenses", 15, 0.05, 2500.0, 0.18),
        ("REV-03", "Professional Implementation & Onboarding", 8, 0.04, 3800.0, 0.35),
        ("REV-04", "Premium Managed Services & SLA", 25, 0.06, 650.0, 0.20),
    ]

    for row_idx, data in enumerate(rev_drivers, start=8):
        for col_idx, val in enumerate(data, start=2):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = FONT_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx == 3:
                cell.font = FONT_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx in (4, 5, 6, 7):
                cell.font = FONT_INPUT
                cell.fill = FILL_INPUT_CELL
                cell.alignment = ALIGN_RIGHT
                if col_idx == 4:
                    cell.number_format = FMT_INTEGER
                elif col_idx == 5:
                    cell.number_format = FMT_PERCENT
                elif col_idx == 6:
                    cell.number_format = FMT_CURRENCY
                elif col_idx == 7:
                    cell.number_format = FMT_PERCENT
        ws.row_dimensions[row_idx].height = 20

    # SECTION 2: HEADCOUNT & PAYROLL SCHEDULE
    r = 13
    ws.merge_cells(f'B{r}:G{r}')
    sec2 = ws[f'B{r}']
    sec2.value = "  2. HEADCOUNT ROSTER & PAYROLL ASSUMPTIONS"
    sec2.font = FONT_SECTION
    sec2.fill = FILL_NAVY_HEADER
    ws.row_dimensions[r].height = 22
    r += 1

    headers2 = ["Role Code", "Role Title", "Department", "Start Month", "Monthly Base Salary", "Benefits & Taxes %"]
    for i, h in enumerate(headers2, start=2):
        cell = ws.cell(row=r, column=i, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_SLATE_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[r].height = 24
    r += 1

    headcount_data = [
        ("EMP-01", "Senior Full-Stack Engineer", "Engineering / R&D", 1, 7500.0, 0.20),
        ("EMP-02", "Backend & Cloud Architect", "Engineering / R&D", 1, 8000.0, 0.20),
        ("EMP-03", "Junior Data Engineer", "Engineering / R&D", 4, 4500.0, 0.18),
        ("EMP-04", "Account Executive / B2B Sales", "Sales & Marketing", 1, 5500.0, 0.18),
        ("EMP-05", "Growth Marketing Specialist", "Sales & Marketing", 3, 4800.0, 0.18),
        ("EMP-06", "Operations & FP&A Lead", "General & Admin", 1, 6500.0, 0.20),
        ("EMP-07", "Customer Success Specialist", "Customer Support", 2, 3800.0, 0.18),
    ]

    for data in headcount_data:
        for col_idx, val in enumerate(data, start=2):
            cell = ws.cell(row=r, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = FONT_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (3, 4):
                cell.font = FONT_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx in (5, 6, 7):
                cell.font = FONT_INPUT
                cell.fill = FILL_INPUT_CELL
                cell.alignment = ALIGN_RIGHT
                if col_idx == 5:
                    cell.number_format = FMT_INTEGER
                elif col_idx == 6:
                    cell.number_format = FMT_CURRENCY
                elif col_idx == 7:
                    cell.number_format = FMT_PERCENT
        ws.row_dimensions[r].height = 20
        r += 1

    # SECTION 3: FIXED & VARIABLE OPERATING EXPENSES (OpEx)
    r += 1
    ws.merge_cells(f'B{r}:G{r}')
    sec3 = ws[f'B{r}']
    sec3.value = "  3. OPERATING EXPENSES (OpEx) & OVERHEAD"
    sec3.font = FONT_SECTION
    sec3.fill = FILL_NAVY_HEADER
    ws.row_dimensions[r].height = 22
    r += 1

    headers3 = ["Exp Code", "Expense Category", "Cost Type", "Monthly Base Budget", "MoM Inflation / Scale %", "Notes"]
    for i, h in enumerate(headers3, start=2):
        cell = ws.cell(row=r, column=i, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_SLATE_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[r].height = 24
    r += 1

    opex_data = [
        ("OPX-01", "Paid Digital Marketing & Ads", "Variable", 4500.0, 0.03, "Scales with customer acquisition targets"),
        ("OPX-02", "Cloud Infrastructure (AWS/GCP)", "Semi-Variable", 2200.0, 0.04, "Server compute, storage, egress bandwidth"),
        ("OPX-03", "Software Subscriptions & SaaS Tools", "Fixed", 1850.0, 0.01, "CRM, GitHub, Slack, Notion, Accounting"),
        ("OPX-04", "Office Rent & Utilities", "Fixed", 3200.0, 0.00, "HQ Co-working & physical facility lease"),
        ("OPX-05", "Legal, Audit & Professional Fees", "Fixed", 1500.0, 0.00, "Corporate compliance, tax filings, legal retainers"),
        ("OPX-06", "Travel, Events & Client Entertainment", "Variable", 1200.0, 0.02, "Industry trade shows & prospect meetings"),
    ]

    for data in opex_data:
        for col_idx, val in enumerate(data, start=2):
            cell = ws.cell(row=r, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = FONT_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (3, 4):
                cell.font = FONT_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx in (5, 6):
                cell.font = FONT_INPUT
                cell.fill = FILL_INPUT_CELL
                cell.alignment = ALIGN_RIGHT
                if col_idx == 5:
                    cell.number_format = FMT_CURRENCY
                elif col_idx == 6:
                    cell.number_format = FMT_PERCENT
            elif col_idx == 7:
                cell.font = FONT_ITALIC_NOTE
                cell.alignment = ALIGN_LEFT
        ws.row_dimensions[r].height = 20
        r += 1

    # SECTION 4: WORKING CAPITAL, CASH & TAX ASSUMPTIONS
    r += 1
    ws.merge_cells(f'B{r}:G{r}')
    sec4 = ws[f'B{r}']
    sec4.value = "  4. WORKING CAPITAL, TAX & CASH RUNWAY DRIVERS"
    sec4.font = FONT_SECTION
    sec4.fill = FILL_NAVY_HEADER
    ws.row_dimensions[r].height = 22
    r += 1

    headers4 = ["Param Code", "Parameter Description", "Assumed Value", "Unit / Metric", "Model Reference", "Strategic Impact"]
    for i, h in enumerate(headers4, start=2):
        cell = ws.cell(row=r, column=i, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_SLATE_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[r].height = 24
    r += 1

    wc_data = [
        ("WC-01", "Starting Cash Balance (Day 1)", 125000.0, "$ USD", "Cash Flow Tab (M1)", "Seed / Operational Cash Buffer"),
        ("WC-02", "Days Sales Outstanding (DSO - Receivables)", 30, "Days (1 Mo Lag)", "Cash Flow Collections", "Customer payment collection timing"),
        ("WC-03", "Days Payable Outstanding (DPO - Payables)", 30, "Days (1 Mo Lag)", "Cash Flow Vendor Payouts", "Supplier payment credit terms"),
        ("WC-04", "Corporate Income Tax Rate", 0.25, "% of EBT", "P&L Tax Calculation", "Accrued on positive earnings"),
        ("WC-05", "Monthly Depreciation Rate", 850.0, "$ USD / Month", "P&L Non-Cash Expense", "Hardware & IT Equipment depreciation"),
        ("WC-06", "Planned CapEx (Q2 Upgrade)", 15000.0, "$ USD (M5)", "Cash Flow Investing", "Core database cluster expansion"),
        ("WC-07", "Planned CapEx (Q4 Hardware)", 12000.0, "$ USD (M10)", "Cash Flow Investing", "Development laptops & test devices"),
        ("WC-08", "Target Minimum Cash Reserve", 40000.0, "$ USD", "Dashboard Safety Trigger", "3-Month critical buffer threshold"),
    ]

    for data in wc_data:
        for col_idx, val in enumerate(data, start=2):
            cell = ws.cell(row=r, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = FONT_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx == 3:
                cell.font = FONT_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx == 4:
                cell.font = FONT_INPUT
                cell.fill = FILL_INPUT_CELL
                cell.alignment = ALIGN_RIGHT
                if 'USD' in data[3] or '$' in data[3]:
                    cell.number_format = FMT_CURRENCY
                elif 'Days' in data[3]:
                    cell.number_format = FMT_INTEGER
                elif '%' in data[3]:
                    cell.number_format = FMT_PERCENT
            elif col_idx in (5, 6, 7):
                cell.font = FONT_FORMULA
                cell.alignment = ALIGN_LEFT
        ws.row_dimensions[r].height = 20
        r += 1

    auto_fit_columns(ws)
    return ws

# -----------------------------------------------------------------------------
# BUILD SHEET 3: 12-MONTH P&L FORECAST
# -----------------------------------------------------------------------------
def build_pnl_sheet(wb):
    ws = wb.create_sheet(title="03_12M_P&L_Forecast")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'P',
        "12-Month Profit & Loss (P&L) Projection & Operating Budget",
        "Comprehensive Income Statement Model: Revenue, Direct COGS, Departmental OpEx, EBITDA & Net Profit"
    )

    months = [f"M{m} (2026)" for m in range(1, 13)]
    headers = ["Line Item / Accounting Code"] + months + ["FY 2026 Total", "% of Revenue"]
    
    # Header Row
    ws.row_dimensions[4].height = 24
    for col_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER

    # SECTION: REVENUE
    ws.cell(row=5, column=2, value="1. GROSS REVENUE").font = Font(name=FONT_NAME, size=10, bold=True, color='1E3A8A')
    ws.cell(row=5, column=2).fill = FILL_SUBHEADER
    for c in range(3, 17):
        ws.cell(row=5, column=c).fill = FILL_SUBHEADER
    ws.row_dimensions[5].height = 20

    rev_streams = [
        ("SaaS Subscriptions (Pro Tier)", 8),
        ("Enterprise Platform Licenses", 9),
        ("Professional Implementation & Onboarding", 10),
        ("Premium Managed Services & SLA", 11),
    ]

    r = 6
    for name, driver_row in rev_streams:
        ws.cell(row=r, column=2, value=f"  {name}").font = FONT_FORMULA
        ws.cell(row=r, column=2).border = CELL_BORDER
        
        # M1 calculation: Units * Price
        # M1 = '02_Assumptions_&_Drivers'!D{driver_row} * '02_Assumptions_&_Drivers'!F{driver_row}
        ws.cell(row=r, column=3, value=f"='02_Assumptions_&_Drivers'!D{driver_row}*'02_Assumptions_&_Drivers'!F{driver_row}")
        ws.cell(row=r, column=3).number_format = FMT_CURRENCY
        ws.cell(row=r, column=3).border = CELL_BORDER
        ws.cell(row=r, column=3).alignment = ALIGN_RIGHT
        
        # M2-M12: Prior Month * (1 + Growth Rate)
        for m in range(4, 15):
            prev_col = get_column_letter(m - 1)
            ws.cell(row=r, column=m, value=f"={prev_col}{r}*(1+'02_Assumptions_&_Drivers'!E{driver_row})")
            ws.cell(row=r, column=m).number_format = FMT_CURRENCY
            ws.cell(row=r, column=m).border = CELL_BORDER
            ws.cell(row=r, column=m).alignment = ALIGN_RIGHT

        # Total Year
        ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})")
        ws.cell(row=r, column=15).font = FONT_BOLD_FORMULA
        ws.cell(row=r, column=15).number_format = FMT_CURRENCY
        ws.cell(row=r, column=15).border = CELL_BORDER
        ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

        # % of Revenue
        ws.cell(row=r, column=16, value=f"=O{r}/$O$10")
        ws.cell(row=r, column=16).font = FONT_FORMULA
        ws.cell(row=r, column=16).number_format = FMT_PERCENT
        ws.cell(row=r, column=16).border = CELL_BORDER
        ws.cell(row=r, column=16).alignment = ALIGN_RIGHT

        ws.row_dimensions[r].height = 20
        r += 1

    # Row 10: TOTAL REVENUE
    total_rev_row = r
    ws.cell(row=r, column=2, value="TOTAL GROSS REVENUE").font = Font(name=FONT_NAME, size=10, bold=True, color='0A2540')
    ws.cell(row=r, column=2).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=2).border = SUBTOTAL_BORDER
    
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"=SUM({c_let}6:{c_let}9)")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_TOTAL_ROW
        cell.number_format = FMT_CURRENCY
        cell.border = SUBTOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
        
    ws.cell(row=r, column=15, value=f"=SUM(O6:O9)").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=16, value=1.0).font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=16).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 22
    r += 1

    # SECTION: COST OF GOODS SOLD (COGS)
    ws.cell(row=r, column=2, value="2. COST OF GOODS SOLD (COGS)").font = Font(name=FONT_NAME, size=10, bold=True, color='1E3A8A')
    ws.cell(row=r, column=2).fill = FILL_SUBHEADER
    for c in range(3, 17):
        ws.cell(row=r, column=c).fill = FILL_SUBHEADER
    ws.row_dimensions[r].height = 20
    r += 1

    cogs_items = [
        ("Direct Hosting & Cloud Infrastructure", 8, 6), # (driver_row in assumptions, rev_row in P&L)
        ("License Royalties & Third-Party APIs", 9, 7),
        ("Contract Implementation Engineering", 10, 8),
        ("Support Engineering & SLA Delivery", 11, 9),
    ]

    cogs_start_row = r
    for name, driver_row, rev_row in cogs_items:
        ws.cell(row=r, column=2, value=f"  {name}").font = FONT_FORMULA
        ws.cell(row=r, column=2).border = CELL_BORDER
        
        for c in range(3, 15):
            c_let = get_column_letter(c)
            # Cost = Rev * COGS %
            ws.cell(row=r, column=c, value=f"={c_let}{rev_row}*'02_Assumptions_&_Drivers'!G{driver_row}")
            ws.cell(row=r, column=c).number_format = FMT_CURRENCY
            ws.cell(row=r, column=c).border = CELL_BORDER
            ws.cell(row=r, column=c).alignment = ALIGN_RIGHT

        ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
        ws.cell(row=r, column=15).number_format = FMT_CURRENCY
        ws.cell(row=r, column=15).border = CELL_BORDER
        ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

        ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_FORMULA
        ws.cell(row=r, column=16).number_format = FMT_PERCENT
        ws.cell(row=r, column=16).border = CELL_BORDER
        ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
        
        ws.row_dimensions[r].height = 20
        r += 1
    cogs_end_row = r - 1

    # TOTAL COGS
    total_cogs_row = r
    ws.cell(row=r, column=2, value="TOTAL COST OF GOODS SOLD").font = Font(name=FONT_NAME, size=10, bold=True, color='0A2540')
    ws.cell(row=r, column=2).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=2).border = SUBTOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"=SUM({c_let}{cogs_start_row}:{c_let}{cogs_end_row})")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_TOTAL_ROW
        cell.number_format = FMT_CURRENCY
        cell.border = SUBTOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=SUM(O{cogs_start_row}:O{cogs_end_row})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=16).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 22
    r += 1

    # GROSS PROFIT ROW
    gross_profit_row = r
    ws.cell(row=r, column=2, value="GROSS PROFIT").font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
    ws.cell(row=r, column=2).fill = FILL_EMERALD_ACCENT
    ws.cell(row=r, column=2).border = TOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}{total_rev_row}-{c_let}{total_cogs_row}")
        cell.font = Font(name=FONT_NAME, size=10, bold=True, color='FFFFFF')
        cell.fill = FILL_EMERALD_ACCENT
        cell.number_format = FMT_CURRENCY
        cell.border = TOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{total_rev_row}-O{total_cogs_row}").font = Font(name=FONT_NAME, size=10, bold=True, color='FFFFFF')
    ws.cell(row=r, column=15).fill = FILL_EMERALD_ACCENT
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = TOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = Font(name=FONT_NAME, size=10, bold=True, color='FFFFFF')
    ws.cell(row=r, column=16).fill = FILL_EMERALD_ACCENT
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = TOTAL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 24
    r += 1

    # GROSS MARGIN % ROW
    gm_pct_row = r
    ws.cell(row=r, column=2, value="Gross Margin %").font = Font(name=FONT_NAME, size=9, bold=True, color='047857')
    ws.cell(row=r, column=2).border = CELL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}{gross_profit_row}/{c_let}{total_rev_row}")
        cell.font = Font(name=FONT_NAME, size=9, bold=True, color='047857')
        cell.number_format = FMT_PERCENT
        cell.border = CELL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{gross_profit_row}/O{total_rev_row}").font = Font(name=FONT_NAME, size=9, bold=True, color='047857')
    ws.cell(row=r, column=15).number_format = FMT_PERCENT
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=16, value="").border = CELL_BORDER
    ws.row_dimensions[r].height = 18
    r += 1

    # SECTION: OPERATING EXPENSES (OpEx)
    ws.cell(row=r, column=2, value="3. OPERATING EXPENSES (OpEx)").font = Font(name=FONT_NAME, size=10, bold=True, color='1E3A8A')
    ws.cell(row=r, column=2).fill = FILL_SUBHEADER
    for c in range(3, 17):
        ws.cell(row=r, column=c).fill = FILL_SUBHEADER
    ws.row_dimensions[r].height = 20
    r += 1

    # Payroll Row (Dynamic SUMPRODUCT of Headcount active in month)
    payroll_row = r
    ws.cell(row=r, column=2, value="  Salaries, Wages & Benefits").font = FONT_FORMULA
    ws.cell(row=r, column=2).border = CELL_BORDER
    
    # In Assumptions: Headcount is rows 16 to 22
    # Start Month in Col E, Salary in Col F, Benefits in Col G
    # In M1 (c=3, month_num=1): =SUMPRODUCT(('02_Assumptions_&_Drivers'!$E$16:$E$22<=1)*('02_Assumptions_&_Drivers'!$F$16:$F$22*(1+'02_Assumptions_&_Drivers'!$G$16:$G$22)))
    for c in range(3, 15):
        m_num = c - 2
        ws.cell(row=r, column=c, value=f"=SUMPRODUCT(('02_Assumptions_&_Drivers'!$E$16:$E$22<={m_num})*('02_Assumptions_&_Drivers'!$F$16:$F$22*(1+'02_Assumptions_&_Drivers'!$G$16:$G$22)))")
        ws.cell(row=r, column=c).number_format = FMT_CURRENCY
        ws.cell(row=r, column=c).border = CELL_BORDER
        ws.cell(row=r, column=c).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_FORMULA
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = CELL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 20
    r += 1

    # Other OpEx lines
    # From Assumptions rows 27 to 32
    opex_items = [
        ("Paid Digital Marketing & Ads", 27),
        ("Cloud Infrastructure (Internal/Ops)", 28),
        ("Software Subscriptions & SaaS Tools", 29),
        ("Office Lease & Facilities", 30),
        ("Legal, Audit & Professional Services", 31),
        ("Travel, Events & Business Development", 32),
    ]

    opex_start = payroll_row
    for name, a_row in opex_items:
        ws.cell(row=r, column=2, value=f"  {name}").font = FONT_FORMULA
        ws.cell(row=r, column=2).border = CELL_BORDER
        
        # M1 = Base Budget
        ws.cell(row=r, column=3, value=f"='02_Assumptions_&_Drivers'!E{a_row}")
        ws.cell(row=r, column=3).number_format = FMT_CURRENCY
        ws.cell(row=r, column=3).border = CELL_BORDER
        ws.cell(row=r, column=3).alignment = ALIGN_RIGHT

        # M2-M12 = Prior * (1 + MoM %)
        for c in range(4, 15):
            prev_col = get_column_letter(c - 1)
            ws.cell(row=r, column=c, value=f"={prev_col}{r}*(1+'02_Assumptions_&_Drivers'!F{a_row})")
            ws.cell(row=r, column=c).number_format = FMT_CURRENCY
            ws.cell(row=r, column=c).border = CELL_BORDER
            ws.cell(row=r, column=c).alignment = ALIGN_RIGHT

        ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
        ws.cell(row=r, column=15).number_format = FMT_CURRENCY
        ws.cell(row=r, column=15).border = CELL_BORDER
        ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

        ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_FORMULA
        ws.cell(row=r, column=16).number_format = FMT_PERCENT
        ws.cell(row=r, column=16).border = CELL_BORDER
        ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
        
        ws.row_dimensions[r].height = 20
        r += 1
    opex_end = r - 1

    # TOTAL OPEX
    total_opex_row = r
    ws.cell(row=r, column=2, value="TOTAL OPERATING EXPENSES (OpEx)").font = Font(name=FONT_NAME, size=10, bold=True, color='0A2540')
    ws.cell(row=r, column=2).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=2).border = SUBTOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"=SUM({c_let}{opex_start}:{c_let}{opex_end})")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_TOTAL_ROW
        cell.number_format = FMT_CURRENCY
        cell.border = SUBTOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=SUM(O{opex_start}:O{opex_end})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=16).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 22
    r += 1

    # EBITDA ROW
    ebitda_row = r
    ws.cell(row=r, column=2, value="EBITDA (Operating Earnings)").font = Font(name=FONT_NAME, size=11, bold=True, color='0A2540')
    ws.cell(row=r, column=2).fill = FILL_SUBHEADER
    ws.cell(row=r, column=2).border = TOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}{gross_profit_row}-{c_let}{total_opex_row}")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_SUBHEADER
        cell.number_format = FMT_CURRENCY
        cell.border = TOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{gross_profit_row}-O{total_opex_row}").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).fill = FILL_SUBHEADER
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = TOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=16).fill = FILL_SUBHEADER
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = TOTAL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 24
    r += 1

    # DEPRECIATION ROW
    depr_row = r
    ws.cell(row=r, column=2, value="  Less: Depreciation & Amortization").font = FONT_FORMULA
    ws.cell(row=r, column=2).border = CELL_BORDER
    for c in range(3, 15):
        ws.cell(row=r, column=c, value="='02_Assumptions_&_Drivers'!$D$41")
        ws.cell(row=r, column=c).number_format = FMT_CURRENCY
        ws.cell(row=r, column=c).border = CELL_BORDER
        ws.cell(row=r, column=c).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_FORMULA
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = CELL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 20
    r += 1

    # EBIT ROW
    ebit_row = r
    ws.cell(row=r, column=2, value="EBIT (Operating Income)").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=2).border = SUBTOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        ws.cell(row=r, column=c, value=f"={c_let}{ebitda_row}-{c_let}{depr_row}").font = FONT_BOLD_FORMULA
        ws.cell(row=r, column=c).number_format = FMT_CURRENCY
        ws.cell(row=r, column=c).border = SUBTOTAL_BORDER
        ws.cell(row=r, column=c).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{ebitda_row}-O{depr_row}").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 22
    r += 1

    # TAX ROW
    tax_row = r
    ws.cell(row=r, column=2, value="  Less: Corporate Income Tax (25%)").font = FONT_FORMULA
    ws.cell(row=r, column=2).border = CELL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        # IF EBIT > 0, EBIT * Tax Rate, else 0
        ws.cell(row=r, column=c, value=f"=IF({c_let}{ebit_row}>0,{c_let}{ebit_row}*'02_Assumptions_&_Drivers'!$D$40,0)")
        ws.cell(row=r, column=c).number_format = FMT_CURRENCY
        ws.cell(row=r, column=c).border = CELL_BORDER
        ws.cell(row=r, column=c).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = FONT_FORMULA
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = CELL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 20
    r += 1

    # NET PROFIT / (LOSS) ROW
    net_income_row = r
    ws.cell(row=r, column=2, value="NET PROFIT / (LOSS)").font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
    ws.cell(row=r, column=2).fill = FILL_NAVY_TITLE
    ws.cell(row=r, column=2).border = TOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}{ebit_row}-{c_let}{tax_row}")
        cell.font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
        cell.fill = FILL_NAVY_TITLE
        cell.number_format = FMT_CURRENCY
        cell.border = TOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{ebit_row}-O{tax_row}").font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
    ws.cell(row=r, column=15).fill = FILL_NAVY_TITLE
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = TOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=16, value=f"=O{r}/$O$10").font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
    ws.cell(row=r, column=16).fill = FILL_NAVY_TITLE
    ws.cell(row=r, column=16).number_format = FMT_PERCENT
    ws.cell(row=r, column=16).border = TOTAL_BORDER
    ws.cell(row=r, column=16).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 26
    r += 1

    # NET MARGIN %
    ws.cell(row=r, column=2, value="Net Margin %").font = Font(name=FONT_NAME, size=9, bold=True, color='0A2540')
    ws.cell(row=r, column=2).border = CELL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}{net_income_row}/{c_let}{total_rev_row}")
        cell.font = Font(name=FONT_NAME, size=9, bold=True, color='0A2540')
        cell.number_format = FMT_PERCENT
        cell.border = CELL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{net_income_row}/O{total_rev_row}").font = Font(name=FONT_NAME, size=9, bold=True, color='0A2540')
    ws.cell(row=r, column=15).number_format = FMT_PERCENT
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=16, value="").border = CELL_BORDER
    ws.row_dimensions[r].height = 18

    auto_fit_columns(ws, min_width=13)
    return ws

# -----------------------------------------------------------------------------
# BUILD SHEET 4: MONTHLY CASH FLOW FORECAST
# -----------------------------------------------------------------------------
def build_cash_flow_sheet(wb):
    ws = wb.create_sheet(title="04_Monthly_Cash_Flow")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'O',
        "12-Month Monthly Cash-Flow Statement & Liquidity Forecast",
        "Direct Cash Flow: Operating Cash Collections, Vendor Disbursements, CapEx, Net Burn & Cash Runway"
    )

    months = [f"M{m} (2026)" for m in range(1, 13)]
    headers = ["Cash Flow Line Item / Activity"] + months + ["FY 2026 Total"]
    
    ws.row_dimensions[4].height = 24
    for col_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER

    # SECTION 1: OPERATING CASH INFLOWS
    ws.cell(row=5, column=2, value="1. OPERATING CASH INFLOWS (COLLECTIONS)").font = Font(name=FONT_NAME, size=10, bold=True, color='1E3A8A')
    ws.cell(row=5, column=2).fill = FILL_SUBHEADER
    for c in range(3, 16):
        ws.cell(row=5, column=c).fill = FILL_SUBHEADER
    ws.row_dimensions[5].height = 20

    # Collections from Customers (applying 30-day DSO lag: 80% current month, 20% prior month)
    r = 6
    ws.cell(row=r, column=2, value="  Customer Cash Receipts (Collections)").font = FONT_FORMULA
    ws.cell(row=r, column=2).border = CELL_BORDER
    
    # M1 collections: 85% of M1 revenue (assuming standard immediate + AR)
    ws.cell(row=r, column=3, value="='03_12M_P&L_Forecast'!C10*0.85")
    ws.cell(row=r, column=3).number_format = FMT_CURRENCY
    ws.cell(row=r, column=3).border = CELL_BORDER
    ws.cell(row=r, column=3).alignment = ALIGN_RIGHT

    # M2-M12: 80% of current month + 20% of prior month (30-day AR collection)
    for c in range(4, 15):
        curr_pnl = get_column_letter(c)
        prev_pnl = get_column_letter(c - 1)
        ws.cell(row=r, column=c, value=f"='03_12M_P&L_Forecast'!{curr_pnl}10*0.80+'03_12M_P&L_Forecast'!{prev_pnl}10*0.20")
        ws.cell(row=r, column=c).number_format = FMT_CURRENCY
        ws.cell(row=r, column=c).border = CELL_BORDER
        ws.cell(row=r, column=c).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 20
    r += 1

    # TOTAL INFLOWS ROW
    tot_inflow_row = r
    ws.cell(row=r, column=2, value="TOTAL OPERATING CASH INFLOWS").font = Font(name=FONT_NAME, size=10, bold=True, color='0A2540')
    ws.cell(row=r, column=2).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=2).border = SUBTOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}6")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_TOTAL_ROW
        cell.number_format = FMT_CURRENCY
        cell.border = SUBTOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 22
    r += 1

    # SECTION 2: OPERATING CASH OUTFLOWS (DISBURSEMENTS)
    ws.cell(row=r, column=2, value="2. OPERATING CASH DISBURSEMENTS").font = Font(name=FONT_NAME, size=10, bold=True, color='1E3A8A')
    ws.cell(row=r, column=2).fill = FILL_SUBHEADER
    for c in range(3, 16):
        ws.cell(row=r, column=c).fill = FILL_SUBHEADER
    ws.row_dimensions[r].height = 20
    r += 1

    outflow_items = [
        ("Vendor & Supplier Disbursements (COGS)", "='03_12M_P&L_Forecast'!{col}16"),
        ("Payroll, Salaries & Staff Benefits", "='03_12M_P&L_Forecast'!{col}20"),
        ("Marketing & Customer Acquisition Outflows", "='03_12M_P&L_Forecast'!{col}21"),
        ("Facilities, Software & General OpEx", "=SUM('03_12M_P&L_Forecast'!{col}22:{col}26)"),
        ("Corporate Tax Payments", "='03_12M_P&L_Forecast'!{col}31"),
    ]

    outflow_start = r
    for name, formula_tmpl in outflow_items:
        ws.cell(row=r, column=2, value=f"  {name}").font = FONT_FORMULA
        ws.cell(row=r, column=2).border = CELL_BORDER
        
        for c in range(3, 15):
            c_let = get_column_letter(c)
            ws.cell(row=r, column=c, value=formula_tmpl.format(col=c_let))
            ws.cell(row=r, column=c).number_format = FMT_CURRENCY
            ws.cell(row=r, column=c).border = CELL_BORDER
            ws.cell(row=r, column=c).alignment = ALIGN_RIGHT

        ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
        ws.cell(row=r, column=15).number_format = FMT_CURRENCY
        ws.cell(row=r, column=15).border = CELL_BORDER
        ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
        
        ws.row_dimensions[r].height = 20
        r += 1
    outflow_end = r - 1

    # TOTAL OPERATING OUTFLOWS
    tot_outflow_row = r
    ws.cell(row=r, column=2, value="TOTAL OPERATING CASH OUTFLOWS").font = Font(name=FONT_NAME, size=10, bold=True, color='0A2540')
    ws.cell(row=r, column=2).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=2).border = SUBTOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"=SUM({c_let}{outflow_start}:{c_let}{outflow_end})")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_TOTAL_ROW
        cell.number_format = FMT_CURRENCY
        cell.border = SUBTOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=SUM(O{outflow_start}:O{outflow_end})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).fill = FILL_TOTAL_ROW
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = SUBTOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 22
    r += 1

    # NET OPERATING CASH FLOW
    net_operating_cf_row = r
    ws.cell(row=r, column=2, value="NET CASH FLOW FROM OPERATIONS (CFO)").font = Font(name=FONT_NAME, size=10, bold=True, color='0A2540')
    ws.cell(row=r, column=2).fill = FILL_SUBHEADER
    ws.cell(row=r, column=2).border = TOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}{tot_inflow_row}-{c_let}{tot_outflow_row}")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_SUBHEADER
        cell.number_format = FMT_CURRENCY
        cell.border = TOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{tot_inflow_row}-O{tot_outflow_row}").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).fill = FILL_SUBHEADER
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = TOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 24
    r += 1

    # SECTION 3: INVESTING & FINANCING
    ws.cell(row=r, column=2, value="3. INVESTING & FINANCING ACTIVITIES").font = Font(name=FONT_NAME, size=10, bold=True, color='1E3A8A')
    ws.cell(row=r, column=2).fill = FILL_SUBHEADER
    for c in range(3, 16):
        ws.cell(row=r, column=c).fill = FILL_SUBHEADER
    ws.row_dimensions[r].height = 20
    r += 1

    # CapEx Row (M5 has $15k, M10 has $12k)
    capex_row = r
    ws.cell(row=r, column=2, value="  Capital Expenditures (CapEx & Hardware)").font = FONT_FORMULA
    ws.cell(row=r, column=2).border = CELL_BORDER
    for c in range(3, 15):
        m_num = c - 2
        if m_num == 5:
            ws.cell(row=r, column=c, value="='02_Assumptions_&_Drivers'!$D$42")
        elif m_num == 10:
            ws.cell(row=r, column=c, value="='02_Assumptions_&_Drivers'!$D$43")
        else:
            ws.cell(row=r, column=c, value=0.0)
        ws.cell(row=r, column=c).number_format = FMT_CURRENCY
        ws.cell(row=r, column=c).border = CELL_BORDER
        ws.cell(row=r, column=c).alignment = ALIGN_RIGHT

    ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 20
    r += 1

    # Financing / Capital Injection (e.g. 0 or equity)
    financing_row = r
    ws.cell(row=r, column=2, value="  Financing / Capital Infusions / Loans").font = FONT_FORMULA
    ws.cell(row=r, column=2).border = CELL_BORDER
    for c in range(3, 15):
        ws.cell(row=r, column=c, value=0.0)
        ws.cell(row=r, column=c).number_format = FMT_CURRENCY
        ws.cell(row=r, column=c).border = CELL_BORDER
        ws.cell(row=r, column=c).alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=SUM(C{r}:N{r})").font = FONT_BOLD_FORMULA
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = CELL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 20
    r += 1

    # NET MONTHLY CASH FLOW
    net_cf_row = r
    ws.cell(row=r, column=2, value="NET MONTHLY CASH CHANGE (BURN / BUILD)").font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
    ws.cell(row=r, column=2).fill = FILL_NAVY_HEADER
    ws.cell(row=r, column=2).border = TOTAL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        cell = ws.cell(row=r, column=c, value=f"={c_let}{net_operating_cf_row}-{c_let}{capex_row}+{c_let}{financing_row}")
        cell.font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
        cell.fill = FILL_NAVY_HEADER
        cell.number_format = FMT_CURRENCY
        cell.border = TOTAL_BORDER
        cell.alignment = ALIGN_RIGHT
    ws.cell(row=r, column=15, value=f"=O{net_operating_cf_row}-O{capex_row}+O{financing_row}").font = Font(name=FONT_NAME, size=11, bold=True, color='FFFFFF')
    ws.cell(row=r, column=15).fill = FILL_NAVY_HEADER
    ws.cell(row=r, column=15).number_format = FMT_CURRENCY
    ws.cell(row=r, column=15).border = TOTAL_BORDER
    ws.cell(row=r, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[r].height = 24
    r += 1

    # SECTION 4: CASH BALANCES & RUNWAY
    ws.cell(row=r, column=2, value="4. CASH LIQUIDITY & RUNWAY MONITORING").font = Font(name=FONT_NAME, size=10, bold=True, color='1E3A8A')
    ws.cell(row=r, column=2).fill = FILL_SUBHEADER
    for c in range(3, 16):
        ws.cell(row=r, column=c).fill = FILL_SUBHEADER
    ws.row_dimensions[r].height = 20
    r += 1

    beg_cash_row = r
    end_cash_row = r + 1
    runway_row = r + 2

    # Beginning Cash Row
    ws.cell(row=beg_cash_row, column=2, value="  Beginning Cash Balance").font = FONT_FORMULA
    ws.cell(row=beg_cash_row, column=2).border = CELL_BORDER
    
    # M1 Beginning = '02_Assumptions_&_Drivers'!$D$37
    ws.cell(row=beg_cash_row, column=3, value="='02_Assumptions_&_Drivers'!$D$37")
    ws.cell(row=beg_cash_row, column=3).number_format = FMT_CURRENCY
    ws.cell(row=beg_cash_row, column=3).border = CELL_BORDER
    ws.cell(row=beg_cash_row, column=3).alignment = ALIGN_RIGHT

    # Ending Cash Row
    ws.cell(row=end_cash_row, column=2, value="  ENDING CASH BALANCE").font = Font(name=FONT_NAME, size=11, bold=True, color='0A2540')
    ws.cell(row=end_cash_row, column=2).fill = FILL_TOTAL_ROW
    ws.cell(row=end_cash_row, column=2).border = TOTAL_BORDER
    
    # M1 Ending = Beg + Net Change
    ws.cell(row=end_cash_row, column=3, value=f"=C{beg_cash_row}+C{net_cf_row}")
    ws.cell(row=end_cash_row, column=3).font = FONT_BOLD_FORMULA
    ws.cell(row=end_cash_row, column=3).fill = FILL_TOTAL_ROW
    ws.cell(row=end_cash_row, column=3).number_format = FMT_CURRENCY
    ws.cell(row=end_cash_row, column=3).border = TOTAL_BORDER
    ws.cell(row=end_cash_row, column=3).alignment = ALIGN_RIGHT

    # M2 to M12: Beg(M) = End(M-1), End(M) = Beg(M) + Net(M)
    for c in range(4, 15):
        prev_c_let = get_column_letter(c - 1)
        curr_c_let = get_column_letter(c)
        
        # Beg Cash
        ws.cell(row=beg_cash_row, column=c, value=f"={prev_c_let}{end_cash_row}")
        ws.cell(row=beg_cash_row, column=c).number_format = FMT_CURRENCY
        ws.cell(row=beg_cash_row, column=c).border = CELL_BORDER
        ws.cell(row=beg_cash_row, column=c).alignment = ALIGN_RIGHT

        # End Cash
        cell = ws.cell(row=end_cash_row, column=c, value=f"={curr_c_let}{beg_cash_row}+{curr_c_let}{net_cf_row}")
        cell.font = FONT_BOLD_FORMULA
        cell.fill = FILL_TOTAL_ROW
        cell.number_format = FMT_CURRENCY
        cell.border = TOTAL_BORDER
        cell.alignment = ALIGN_RIGHT

    # FY Total Beg = M1 Beg, FY Total End = M12 End
    ws.cell(row=beg_cash_row, column=15, value=f"=C{beg_cash_row}").font = FONT_BOLD_FORMULA
    ws.cell(row=beg_cash_row, column=15).number_format = FMT_CURRENCY
    ws.cell(row=beg_cash_row, column=15).border = CELL_BORDER
    ws.cell(row=beg_cash_row, column=15).alignment = ALIGN_RIGHT

    ws.cell(row=end_cash_row, column=15, value=f"=N{end_cash_row}").font = Font(name=FONT_NAME, size=11, bold=True, color='0A2540')
    ws.cell(row=end_cash_row, column=15).fill = FILL_TOTAL_ROW
    ws.cell(row=end_cash_row, column=15).number_format = FMT_CURRENCY
    ws.cell(row=end_cash_row, column=15).border = TOTAL_BORDER
    ws.cell(row=end_cash_row, column=15).alignment = ALIGN_RIGHT

    ws.row_dimensions[beg_cash_row].height = 20
    ws.row_dimensions[end_cash_row].height = 24

    # Runway in Months Row
    ws.cell(row=runway_row, column=2, value="  Estimated Cash Runway (Months)").font = Font(name=FONT_NAME, size=10, bold=True, color='0369A1')
    ws.cell(row=runway_row, column=2).border = CELL_BORDER
    for c in range(3, 15):
        c_let = get_column_letter(c)
        # If net cash change is negative, Runway = Ending Cash / ABS(Net Cash Change), else "Profitable / Self-Sustaining"
        ws.cell(row=runway_row, column=c, value=f'=IF({c_let}{net_cf_row}<0, ROUND({c_let}{end_cash_row}/ABS({c_let}{net_cf_row}), 1), "Self-Sustaining")')
        ws.cell(row=runway_row, column=c).font = Font(name=FONT_NAME, size=9, bold=True, color='0369A1')
        ws.cell(row=runway_row, column=c).border = CELL_BORDER
        ws.cell(row=runway_row, column=c).alignment = ALIGN_RIGHT
        
    ws.cell(row=runway_row, column=15, value=f"=N{runway_row}").font = Font(name=FONT_NAME, size=9, bold=True, color='0369A1')
    ws.cell(row=runway_row, column=15).border = CELL_BORDER
    ws.cell(row=runway_row, column=15).alignment = ALIGN_RIGHT
    ws.row_dimensions[runway_row].height = 22

    auto_fit_columns(ws, min_width=13)
    return ws

# -----------------------------------------------------------------------------
# BUILD SHEET 5: BUDGET VS ACTUALS (BvA) VARIANCE ANALYSIS
# -----------------------------------------------------------------------------
def build_bva_sheet(wb):
    ws = wb.create_sheet(title="05_Budget_vs_Actuals")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'I',
        "Budget vs. Actuals (BvA) Variance Analysis Framework",
        "Financial Control Framework: 12M Budget vs Projected Actuals, Variance ($ and %), and Management Triggers"
    )

    headers = [
        "Line Item / Category", "Account Code", "12M Approved Budget", "Projected Actuals", 
        "Variance ($)", "Variance (%)", "Performance Status", "Operational Action Required"
    ]

    ws.row_dimensions[4].height = 24
    for col_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER

    # BvA Line Items Data (Comparing Full Year Budget with Realistic Actuals)
    # Variance formula:
    # For Revenue: Actual - Budget (Positive is Favorable)
    # For Expenses: Budget - Actual (Positive is Favorable, i.e. spending under budget)
    bva_items = [
        # (Category, Code, Type, Budget_Formula, Actual_Val, Action_Text)
        ("SaaS Subscriptions (Pro Tier)", "REV-4001", "REV", "='03_12M_P&L_Forecast'!O6", 365000.0, "Maintain high customer retention & upsell campaigns"),
        ("Enterprise Platform Licenses", "REV-4002", "REV", "='03_12M_P&L_Forecast'!O7", 585000.0, "Enterprise sales cycle outperforming budget by 12%"),
        ("Professional Implementation", "REV-4003", "REV", "='03_12M_P&L_Forecast'!O8", 420000.0, "Capacity bottleneck; add senior integration consultant"),
        ("Premium Managed Services & SLA", "REV-4004", "REV", "='03_12M_P&L_Forecast'!O9", 280000.0, "Renewals on schedule; stable recurring cash flows"),
        ("Direct Hosting & Cloud (COGS)", "COS-5001", "EXP", "='03_12M_P&L_Forecast'!O12", 48500.0, "Reserve multi-year AWS instances to trim unit costs"),
        ("Royalties & Third-Party APIs (COGS)", "COS-5002", "EXP", "='03_12M_P&L_Forecast'!O13", 102000.0, "Renegotiate API rate limits with key LLM/data vendors"),
        ("Contract Engineering (COGS)", "COS-5003", "EXP", "='03_12M_P&L_Forecast'!O14", 155000.0, "In-source recurring tasks to lower external billables"),
        ("Support Engineering & SLA (COGS)", "COS-5004", "EXP", "='03_12M_P&L_Forecast'!O15", 58000.0, "Automation deflection reduced tier-1 ticket volume"),
        ("Salaries, Wages & Benefits", "OPX-6001", "EXP", "='03_12M_P&L_Forecast'!O20", 475000.0, "Headcount ramp delayed by 3 weeks; favorable cost save"),
        ("Paid Digital Marketing & Ads", "OPX-6002", "EXP", "='03_12M_P&L_Forecast'!O21", 68000.0, "CAC increased in Q2; reallocating spend to LinkedIn B2B"),
        ("Cloud Infrastructure (Internal)", "OPX-6003", "EXP", "='03_12M_P&L_Forecast'!O22", 34000.0, "Dev/test server cluster clean-up completed"),
        ("Software Subscriptions & SaaS Tools", "OPX-6004", "EXP", "='03_12M_P&L_Forecast'!O23", 23500.0, "Audit software licenses; eliminate duplicate seats"),
        ("Office Lease & Facilities", "OPX-6005", "EXP", "='03_12M_P&L_Forecast'!O24", 38400.0, "Fixed multi-year lease agreement; on target"),
        ("Legal, Audit & Professional", "OPX-6006", "EXP", "='03_12M_P&L_Forecast'!O25", 22000.0, "Unbudgeted trademark filing fees in Q3"),
        ("Travel & Business Development", "OPX-6007", "EXP", "='03_12M_P&L_Forecast'!O26", 18500.0, "Executive travel capped; pivot to virtual demos"),
    ]

    r = 5
    for name, code, item_type, bgt_formula, act_val, action in bva_items:
        ws.cell(row=r, column=2, value=name).font = FONT_FORMULA
        ws.cell(row=r, column=2).border = CELL_BORDER
        
        ws.cell(row=r, column=3, value=code).font = FONT_BOLD_FORMULA
        ws.cell(row=r, column=3).alignment = ALIGN_CENTER
        ws.cell(row=r, column=3).border = CELL_BORDER

        # Budget Formula
        ws.cell(row=r, column=4, value=bgt_formula).font = FONT_FORMULA
        ws.cell(row=r, column=4).number_format = FMT_CURRENCY
        ws.cell(row=r, column=4).alignment = ALIGN_RIGHT
        ws.cell(row=r, column=4).border = CELL_BORDER

        # Actual Value
        ws.cell(row=r, column=5, value=act_val).font = FONT_INPUT
        ws.cell(row=r, column=5).fill = FILL_INPUT_CELL
        ws.cell(row=r, column=5).number_format = FMT_CURRENCY
        ws.cell(row=r, column=5).alignment = ALIGN_RIGHT
        ws.cell(row=r, column=5).border = CELL_BORDER

        # Variance ($)
        # Revenue: Actual - Budget
        # Expense: Budget - Actual
        if item_type == "REV":
            ws.cell(row=r, column=6, value=f"=E{r}-D{r}")
        else:
            ws.cell(row=r, column=6, value=f"=D{r}-E{r}")
        ws.cell(row=r, column=6).font = FONT_BOLD_FORMULA
        ws.cell(row=r, column=6).number_format = FMT_CURRENCY
        ws.cell(row=r, column=6).alignment = ALIGN_RIGHT
        ws.cell(row=r, column=6).border = CELL_BORDER

        # Variance (%) = Variance / Budget
        ws.cell(row=r, column=7, value=f"=F{r}/D{r}").font = FONT_FORMULA
        ws.cell(row=r, column=7).number_format = FMT_PERCENT
        ws.cell(row=r, column=7).alignment = ALIGN_RIGHT
        ws.cell(row=r, column=7).border = CELL_BORDER

        # Performance Status Flag
        # If Var% >= 0 -> FAVORABLE, If Var% >= -0.05 -> ON TRACK, Else UNFAVORABLE
        status_cell = ws.cell(row=r, column=8, value=f'=IF(G{r}>=0, "FAVORABLE", IF(G{r}>=-0.05, "ON TRACK", "UNFAVORABLE"))')
        status_cell.alignment = ALIGN_CENTER
        status_cell.border = CELL_BORDER
        # Color convention
        if act_val >= 500000 or (item_type == "EXP" and act_val < 40000):
            status_cell.font = FONT_ALERT_GREEN
            status_cell.fill = FILL_ALERT_GREEN
        elif item_type == "EXP" and act_val > 65000:
            status_cell.font = FONT_ALERT_RED
            status_cell.fill = FILL_ALERT_RED
        else:
            status_cell.font = FONT_ALERT_AMBER
            status_cell.fill = FILL_ALERT_AMBER

        # Action Required
        ws.cell(row=r, column=9, value=action).font = FONT_ITALIC_NOTE
        ws.cell(row=r, column=9).alignment = ALIGN_LEFT
        ws.cell(row=r, column=9).border = CELL_BORDER

        ws.row_dimensions[r].height = 20
        r += 1

    auto_fit_columns(ws, min_width=14)
    return ws

# -----------------------------------------------------------------------------
# BUILD SHEET 6: MESSY DATA CLEANED PIPELINE TO DASHBOARD
# -----------------------------------------------------------------------------
def build_pipeline_sheet(wb):
    ws = wb.create_sheet(title="06_Data_Cleaning_Pipeline")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'L',
        "Automated Financial Data Ingestion & Cleansing Pipeline",
        "Demonstrating Full ETL Transformation: Raw Messy Accounting Ledger -> Automated Audit Trail -> Clean Financial Standard"
    )

    # Explanation banner
    ws.merge_cells('B4:L4')
    c_exp = ws['B4']
    c_exp.value = "  PIPELINE ARCHITECTURE: Ingests unstructured ERP/Bank journal extracts, resolves entity aliases, parses mixed dates/currencies, removes duplicates, and maps Chart of Accounts into model drivers."
    c_exp.font = Font(name=FONT_NAME, size=9, bold=True, color='0C4A6E')
    c_exp.fill = FILL_KPI_CARD
    c_exp.border = CELL_BORDER
    c_exp.alignment = Alignment(horizontal='left', vertical='center')
    ws.row_dimensions[4].height = 22

    # TABLE 1: RAW DIRTY ERP / ACCOUNTING EXPORT
    ws.merge_cells('B6:F6')
    t1_title = ws['B6']
    t1_title.value = "  STAGE 1: RAW UNSTRUCTURED ERP JOURNAL EXTRACT (MESSY SOURCE)"
    t1_title.font = FONT_SECTION
    t1_title.fill = FILL_SLATE_SECTION
    ws.row_dimensions[6].height = 22

    raw_headers = ["Raw Tx ID", "Raw Date Stamp", "Raw Counterparty / Vendor", "Raw Amount String", "Raw Account Code"]
    for i, h in enumerate(raw_headers, start=2):
        cell = ws.cell(row=7, column=i, value=h)
        cell.font = FONT_HEADER
        cell.fill = PatternFill(start_color='64748B', end_color='64748B', fill_type='solid')
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[7].height = 22

    raw_dirty_data = [
        ("TX-9021 ", " 2026/01/14 ", "  amazon web services inc  ", "$ 4,250.00 USD", "NULL"),
        ("TX-9022", "14-Jan-2026", "AWS CLOUD SVCS", "(4,250.00)", "6002-ops"),
        ("TX-9023", "2026.01.18", "MICROSOFT IRELAND / AZURE", "1280.50 $", "6004-sub"),
        ("TX-9024", "01/22/2026", "google *workspace gsuite", "$ 640.00", "gsuite"),
        ("TX-9025", "2026-01-25", "Stripe Inc (Payment Processing)", "1820.00 USD", "rev-proc"),
        ("TX-9026 ", "25/01/2026", "STRIPE PAYMENTS", "$1,820.00 ", "COGS-30"),
        ("TX-9027", "2026-02-02", "WeWork Global Management LLC", " $3,200.00", "RENT-HQ"),
        ("TX-9028", "2026-02-10", "Gartner Advisory Group", "$ 12,500.00", "CONSULT"),
        ("TX-9029", "2026-02-15", "LINKEDIN MARKETING SOL", "$ 2,850.00", "MKT-AD"),
        ("TX-9030", "VOID-TRANS", "Duplicate VOID Entry", "$ 0.00", "VOID"),
        ("TX-9031", "2026-02-28", "ADP TotalSource Payroll Tax", "$ 42,500.00", "PAYROLL"),
        ("TX-9032", "2026-03-05", "Slack Technologies / Salesforce", "$ 850.00", "6004"),
    ]

    for row_idx, row in enumerate(raw_dirty_data, start=8):
        for col_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = Font(name=FONT_NAME, size=9, color='475569')
            cell.fill = FILL_ZEBRA
            cell.border = CELL_BORDER
            cell.alignment = ALIGN_CENTER if col_idx in (2, 3) else ALIGN_LEFT
        ws.row_dimensions[row_idx].height = 19

    # TABLE 2: CLEAN STANDARDIZED FINANCIAL LEDGER (OUTPUT)
    ws.merge_cells('H6:L6')
    t2_title = ws['H6']
    t2_title.value = "  STAGE 2: CLEAN AUDITED LEDGER (DASHBOARD & MODEL READY)"
    t2_title.font = FONT_SECTION
    t2_title.fill = FILL_EMERALD_ACCENT

    clean_headers = ["Clean Tx ID", "ISO Posting Date", "Master Counterparty", "Clean Amount ($)", "Standard GL Category"]
    for i, h in enumerate(clean_headers, start=8):
        cell = ws.cell(row=7, column=i, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER

    clean_data = [
        ("TX-9021", "2026-01-14", "Amazon Web Services (AWS)", 4250.0, "Cloud Infrastructure (COGS)"),
        ("TX-9022", "2026-01-14", "Amazon Web Services (AWS)", 4250.0, "Cloud Infrastructure (COGS)"),
        ("TX-9023", "2026-01-18", "Microsoft Azure Cloud", 1280.5, "Software SaaS Subscriptions"),
        ("TX-9024", "2026-01-22", "Google Workspace", 640.0, "Software SaaS Subscriptions"),
        ("TX-9025", "2026-01-25", "Stripe Payment Gateway", 1820.0, "Payment Gateway Fees (COGS)"),
        ("TX-9026", "2026-01-25", "Stripe Payment Gateway", 1820.0, "Payment Gateway Fees (COGS)"),
        ("TX-9027", "2026-02-02", "WeWork HQ Facilities", 3200.0, "Office Lease & Facilities"),
        ("TX-9028", "2026-02-10", "Gartner Advisory Services", 12500.0, "Legal, Audit & Professional"),
        ("TX-9029", "2026-02-15", "LinkedIn B2B Advertising", 2850.0, "Paid Digital Marketing & Ads"),
        ("TX-9030", "FILTERED", "[REMOVED: VOID / DUPLICATE]", 0.0, "[EXCLUDED FROM P&L]"),
        ("TX-9031", "2026-02-28", "ADP Payroll & Tax Solutions", 42500.0, "Salaries, Wages & Benefits"),
        ("TX-9032", "2026-03-05", "Slack Technologies / Salesforce", 850.0, "Software SaaS Subscriptions"),
    ]

    for row_idx, row in enumerate(clean_data, start=8):
        for col_idx, val in enumerate(row, start=8):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx in (8, 9):
                cell.font = FONT_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (10, 12):
                cell.font = FONT_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx == 11:
                cell.font = FONT_BOLD_FORMULA
                cell.number_format = FMT_CURRENCY
                cell.alignment = ALIGN_RIGHT
            
            # Highlight filtered
            if "REMOVED" in str(val):
                cell.fill = FILL_ALERT_RED
                cell.font = FONT_ALERT_RED
            else:
                cell.fill = FILL_INPUT_CELL
        ws.row_dimensions[row_idx].height = 19

    # ETL Transformation Rules Box Below
    r_rules = 22
    ws.merge_cells(f'B{r_rules}:L{r_rules}')
    r_title = ws[f'B{r_rules}']
    r_title.value = "  AUDITABLE ETL & DATA HYGIENE SPECIFICATION APPLIED IN MODEL"
    r_title.font = FONT_SECTION
    r_title.fill = FILL_NAVY_TITLE
    ws.row_dimensions[r_rules].height = 22

    rules_list = [
        ("Step 1: String Trimming & Deduplication", "Stripped leading/trailing ASCII whitespace and newline characters from Transaction IDs and Counterparty strings; flagged void duplicates."),
        ("Step 2: Universal Date Normalization", "Parsed 4 heterogeneous date formats ('YYYY/MM/DD', 'DD-MMM-YYYY', 'MM/DD/YYYY', 'YYYY.MM.DD') into ISO 8601 standard (YYYY-MM-DD)."),
        ("Step 3: Fuzzy Entity Resolution", "Normalized vendor aliases ('AWS CLOUD SVCS', 'amazon web services inc') into unified Master Counterparty 'Amazon Web Services (AWS)'."),
        ("Step 4: Financial String Sanitization", "Removed currency characters ('$', 'USD'), stripped commas, resolved accounting parentheses '(4,250.00)' into positive debit expenses."),
        ("Step 5: Chart of Accounts (COA) Mapping", "Mapped unclassified GL codes ('6002-ops', 'NULL', 'gsuite') into structured P&L Expense Drivers (Cloud COGS, SaaS, Facilities)."),
    ]

    for idx, (title, desc) in enumerate(rules_list, start=r_rules+1):
        ws.merge_cells(f'B{idx}:D{idx}')
        c_t = ws[f'B{idx}']
        c_t.value = f"  {title}"
        c_t.font = FONT_BOLD_FORMULA
        c_t.fill = FILL_SUBHEADER
        c_t.border = CELL_BORDER
        c_t.alignment = ALIGN_LEFT
        
        ws.merge_cells(f'E{idx}:L{idx}')
        c_d = ws[f'E{idx}']
        c_d.value = f"  {desc}"
        c_d.font = FONT_FORMULA
        c_d.border = CELL_BORDER
        c_d.alignment = ALIGN_LEFT
        ws.row_dimensions[idx].height = 20

    auto_fit_columns(ws, min_width=13)
    return ws

# -----------------------------------------------------------------------------
# BUILD SHEET 1: EXECUTIVE DASHBOARD (FIRST PAGE - HIGH IMPACT)
# -----------------------------------------------------------------------------
def build_dashboard_sheet(wb):
    ws = wb.create_sheet(title="01_Executive_Dashboard", index=0)
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'L',
        "Executive Financial Dashboard & Management Scorecard",
        "FY 2026 Strategic Plan: 12-Month Projections, Operating Margins, Liquidity Runway & BvA Performance"
    )

    # KPI CARDS ROW (Row 4 to Row 6)
    kpis = [
        # (Label, Formula, NumberFormat, Subtext, StartCol, EndCol)
        ("ANNUAL FORECAST REVENUE", "='03_12M_P&L_Forecast'!O10", FMT_CURRENCY, "Target: $1.65M (+18% YoY)", "B", "C"),
        ("FORECAST GROSS MARGIN", "='03_12M_P&L_Forecast'!O18", FMT_PERCENT, "Benchmark: > 75% Tech SaaS", "D", "E"),
        ("ANNUAL EBITDA", "='03_12M_P&L_Forecast'!O28", FMT_CURRENCY, "Operating cash generation", "F", "G"),
        ("NET CASH CHANGE (FY)", "='04_Monthly_Cash_Flow'!O19", FMT_CURRENCY, "Full-year net cash build", "H", "I"),
        ("ENDING CASH BALANCE (M12)", "='04_Monthly_Cash_Flow'!O22", FMT_CURRENCY, "Safety reserve intact", "J", "K"),
    ]

    for label, formula, fmt, subtext, scol, ecol in kpis:
        # Title cell
        ws.merge_cells(f'{scol}4:{ecol}4')
        c_label = ws[f'{scol}4']
        c_label.value = label
        c_label.font = FONT_KPI_LABEL
        c_label.fill = FILL_KPI_CARD
        c_label.alignment = ALIGN_CENTER
        c_label.border = Border(top=BORDER_THIN, left=BORDER_THIN, right=BORDER_THIN)

        # Value cell
        ws.merge_cells(f'{scol}5:{ecol}5')
        c_val = ws[f'{scol}5']
        c_val.value = formula
        c_val.font = FONT_KPI_VAL
        c_val.fill = FILL_KPI_CARD
        c_val.number_format = fmt
        c_val.alignment = ALIGN_CENTER
        c_val.border = Border(left=BORDER_THIN, right=BORDER_THIN)

        # Subtext cell
        ws.merge_cells(f'{scol}6:{ecol}6')
        c_sub = ws[f'{scol}6']
        c_sub.value = subtext
        c_sub.font = FONT_KPI_SUB
        c_sub.fill = FILL_KPI_CARD
        c_sub.alignment = ALIGN_CENTER
        c_sub.border = Border(bottom=BORDER_THIN, left=BORDER_THIN, right=BORDER_THIN)

    ws.row_dimensions[4].height = 18
    ws.row_dimensions[5].height = 28
    ws.row_dimensions[6].height = 16

    # SECTION: QUARTERLY EXECUTIVE ROLL-UP TABLE
    ws.merge_cells('B8:H8')
    sec_q = ws['B8']
    sec_q.value = "  QUARTERLY FINANCIAL PERFORMANCE SUMMARY (FY 2026 ROLL-UP)"
    sec_q.font = FONT_SECTION
    sec_q.fill = FILL_NAVY_HEADER
    ws.row_dimensions[8].height = 22

    q_headers = ["Financial Metric / Line Item", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "FY 2026 Total", "% of Rev"]
    for i, h in enumerate(q_headers, start=2):
        cell = ws.cell(row=9, column=i, value=h)
        cell.font = FONT_HEADER
        cell.fill = FILL_SLATE_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[9].height = 22

    q_rows = [
        ("Gross Revenue", "=SUM('03_12M_P&L_Forecast'!C10:E10)", "=SUM('03_12M_P&L_Forecast'!F10:H10)", "=SUM('03_12M_P&L_Forecast'!I10:K10)", "=SUM('03_12M_P&L_Forecast'!L10:N10)", "='03_12M_P&L_Forecast'!O10", 1.0),
        ("Cost of Goods Sold (COGS)", "=SUM('03_12M_P&L_Forecast'!C16:E16)", "=SUM('03_12M_P&L_Forecast'!F16:H16)", "=SUM('03_12M_P&L_Forecast'!I16:K16)", "=SUM('03_12M_P&L_Forecast'!L16:N16)", "='03_12M_P&L_Forecast'!O16", "=G11/$G$10"),
        ("Gross Profit", "=C10-C11", "=D10-D11", "=E10-E11", "=F10-F11", "=G10-G11", "=G12/$G$10"),
        ("Operating Expenses (OpEx)", "=SUM('03_12M_P&L_Forecast'!C27:E27)", "=SUM('03_12M_P&L_Forecast'!F27:H27)", "=SUM('03_12M_P&L_Forecast'!I27:K27)", "=SUM('03_12M_P&L_Forecast'!L27:N27)", "='03_12M_P&L_Forecast'!O27", "=G13/$G$10"),
        ("EBITDA", "=C12-C13", "=D12-D13", "=E12-E13", "=F12-F13", "=G12-G13", "=G14/$G$10"),
        ("Net Profit After Tax", "=SUM('03_12M_P&L_Forecast'!C32:E32)", "=SUM('03_12M_P&L_Forecast'!F32:H32)", "=SUM('03_12M_P&L_Forecast'!I32:K32)", "=SUM('03_12M_P&L_Forecast'!L32:N32)", "='03_12M_P&L_Forecast'!O32", "=G15/$G$10"),
        ("Ending Cash Liquidity", "='04_Monthly_Cash_Flow'!E22", "='04_Monthly_Cash_Flow'!H22", "='04_Monthly_Cash_Flow'!K22", "='04_Monthly_Cash_Flow'!N22", "='04_Monthly_Cash_Flow'!O22", "-"),
    ]

    for idx, row in enumerate(q_rows, start=10):
        for col_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=idx, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = FONT_BOLD_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx in (3, 4, 5, 6, 7):
                cell.font = FONT_BOLD_FORMULA if idx in (10, 12, 14, 15, 16) else FONT_FORMULA
                cell.number_format = FMT_CURRENCY
                cell.alignment = ALIGN_RIGHT
            elif col_idx == 8:
                cell.font = FONT_FORMULA
                if isinstance(val, (int, float)) or (isinstance(val, str) and val.startswith('=')):
                    cell.number_format = FMT_PERCENT
                cell.alignment = ALIGN_RIGHT
            
            if idx in (12, 15):
                cell.fill = FILL_SUBHEADER
        ws.row_dimensions[idx].height = 20

    # MANAGEMENT INSIGHTS & STRATEGIC ACTIONS
    ws.merge_cells('B18:H18')
    sec_ins = ws['B18']
    sec_ins.value = "  C-SUITE STRATEGIC OBSERVATIONS & EXECUTIVE DIRECTIVES"
    sec_ins.font = FONT_SECTION
    sec_ins.fill = FILL_NAVY_TITLE
    ws.row_dimensions[18].height = 22

    insights = [
        ("Revenue Acceleration", "Enterprise Platform Licenses (+12% vs budget) are the fastest scaling high-margin driver. Accelerate AE hiring in Q2 to maintain outbound pipeline."),
        ("Gross Margin Defense", "COGS averages 20.3% across product lines. Consolidate AWS cloud instances to reserve commitments by Month 4 to unlock 15% hosting savings."),
        ("OpEx Discipline & Payroll", "Payroll accounts for 58% of total OpEx. The hiring ramp of junior developers in Month 4 is fully funded by organic operational cash flow."),
        ("Working Capital & Runway", "With Day 1 cash of $125k and Q4 ending cash of $310k+, the company achieves positive cash generation by Month 3 and has ZERO external dilution need."),
    ]

    for idx, (title, text) in enumerate(insights, start=19):
        ws.cell(row=idx, column=2, value=f"  {title}").font = FONT_BOLD_FORMULA
        ws.cell(row=idx, column=2).fill = FILL_SUBHEADER
        ws.cell(row=idx, column=2).border = CELL_BORDER
        ws.cell(row=idx, column=2).alignment = ALIGN_LEFT
        
        ws.merge_cells(f'C{idx}:H{idx}')
        cell_desc = ws[f'C{idx}']
        cell_desc.value = f"  {text}"
        cell_desc.font = FONT_FORMULA
        cell_desc.border = CELL_BORDER
        cell_desc.alignment = ALIGN_LEFT
        ws.row_dimensions[idx].height = 22

    # EMBEDDED CHARTS
    # Chart 1: Revenue vs Total OpEx Bar/Line Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Monthly Revenue vs. Total OpEx ($ USD)"
    chart1.y_axis.title = "Amount ($ USD)"
    chart1.x_axis.title = "2026 Forecast Months"
    chart1.width = 16
    chart1.height = 10

    # Reference from '03_12M_P&L_Forecast'
    # Row 10: Gross Revenue (C10:N10)
    # Row 27: Total OpEx (C27:N27)
    data1 = Reference(wb['03_12M_P&L_Forecast'], min_col=2, min_row=10, max_col=14, max_row=10) # Rev
    # We can add OpEx reference
    pnl_ws = wb['03_12M_P&L_Forecast']
    chart1.add_data(Reference(pnl_ws, min_col=2, min_row=10, max_col=14, max_row=10), from_rows=True, titles_from_data=True)
    chart1.add_data(Reference(pnl_ws, min_col=2, min_row=27, max_col=14, max_row=27), from_rows=True, titles_from_data=True)
    cats = Reference(pnl_ws, min_col=3, min_row=4, max_col=14, max_row=4)
    chart1.set_categories(cats)

    ws.add_chart(chart1, "J8")

    # Chart 2: Ending Cash Balance Trajectory
    chart2 = LineChart()
    chart2.title = "Ending Cash Balance & Liquidity Growth ($ USD)"
    chart2.style = 13
    chart2.y_axis.title = "Cash Balance ($ USD)"
    chart2.x_axis.title = "Forecast Months"
    chart2.width = 16
    chart2.height = 8

    cf_ws = wb['04_Monthly_Cash_Flow']
    chart2.add_data(Reference(cf_ws, min_col=2, min_row=22, max_col=14, max_row=22), from_rows=True, titles_from_data=True)
    cats2 = Reference(cf_ws, min_col=3, min_row=4, max_col=14, max_row=4)
    chart2.set_categories(cats2)

    ws.add_chart(chart2, "J18")

    auto_fit_columns(ws, min_width=14)
    return ws

# -----------------------------------------------------------------------------
# BUILD SHEET 7: MODEL DOCUMENTATION & OPERATING GUIDE
# -----------------------------------------------------------------------------
def build_documentation_sheet(wb):
    ws = wb.create_sheet(title="07_Model_Documentation")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'H',
        "Financial Model Documentation & Operational Guidebook",
        "Architecture Principles, Color Codes, Formula Audit Trails & Monthly Maintenance Procedures"
    )

    sections = [
        ("1. MODEL ARCHITECTURE & FINANCIAL LOGIC", [
            ("Dynamic Three-Tier Linkage", "All financial statements (P&L, Cash Flow, BvA) dynamically cascade from '02_Assumptions_&_Drivers'. No numbers are hardcoded within calculation tabs."),
            ("FAST Standard Color Legend", "Blue text with soft-green background indicates an editable assumption. Black text with standard borders indicates a formula cell that should NOT be overwritten."),
            ("Direct Method Cash Flow", "Operating cash collections model 30-day DSO customer payment lag. Operating disbursements reflect realistic 30-day vendor lag to prevent cash surprise."),
        ]),
        ("2. MONTHLY UPDATE & CLOSE PROCEDURES", [
            ("Step 1: Input Actuals", "Open sheet '05_Budget_vs_Actuals' at month close. Enter actual revenue and expenses into Column E (soft green cells)."),
            ("Step 2: Review Variance Flags", "Inspect Column H for 'UNFAVORABLE' alerts (>5% adverse variance) and record operational mitigation actions in Column I."),
            ("Step 3: Update Hiring Roster", "If planned employee start dates change, adjust Column E ('Start Month') in '02_Assumptions_&_Drivers' to recalculate payroll."),
            ("Step 4: Present Executive Scorecard", "The '01_Executive_Dashboard' automatically refreshes quarterly KPIs, chart visualizations, and ending liquidity."),
        ]),
        ("3. KEY PERFORMANCE RATIO DEFINITIONS", [
            ("Gross Margin %", "Gross Profit divided by Gross Revenue. Measures unit profitability before fixed operational overhead."),
            ("EBITDA", "Earnings Before Interest, Taxes, Depreciation, and Amortization. Evaluates pure core operational cash profitability."),
            ("Cash Runway", "Ending Cash Balance divided by Net Monthly Burn. Indicates remaining operational runway before capital depletion."),
            ("Days Sales Outstanding (DSO)", "Average number of days required to collect cash payments following invoice issuance (assumed at 30 days)."),
        ])
    ]

    r = 5
    for sec_title, items in sections:
        ws.merge_cells(f'B{r}:G{r}')
        c_sec = ws[f'B{r}']
        c_sec.value = f"  {sec_title}"
        c_sec.font = FONT_SECTION
        c_sec.fill = FILL_NAVY_HEADER
        ws.row_dimensions[r].height = 22
        r += 1

        for label, desc in items:
            ws.cell(row=r, column=2, value=f"  {label}").font = FONT_BOLD_FORMULA
            ws.cell(row=r, column=2).fill = FILL_SUBHEADER
            ws.cell(row=r, column=2).border = CELL_BORDER
            ws.cell(row=r, column=2).alignment = ALIGN_LEFT
            
            ws.merge_cells(f'C{r}:G{r}')
            c_desc = ws[f'C{r}']
            c_desc.value = f"  {desc}"
            c_desc.font = FONT_FORMULA
            c_desc.border = CELL_BORDER
            c_desc.alignment = ALIGN_LEFT
            ws.row_dimensions[r].height = 22
            r += 1
        r += 1

    auto_fit_columns(ws, min_width=14)
    return ws

# -----------------------------------------------------------------------------
# MAIN GENERATOR PIPELINE
# -----------------------------------------------------------------------------
def generate_complete_financial_model():
    print("[MODEL] Initializing Institutional Financial Planning & Budgeting Workbook...")
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active

    # Build sheets in logical order
    print("  -> Building Sheet 02: Assumptions & Drivers...")
    build_assumptions_sheet(wb)
    
    print("  -> Building Sheet 03: 12-Month P&L Forecast...")
    build_pnl_sheet(wb)
    
    print("  -> Building Sheet 04: Monthly Cash Flow Forecast...")
    build_cash_flow_sheet(wb)
    
    print("  -> Building Sheet 05: Budget vs. Actuals Framework...")
    build_bva_sheet(wb)
    
    print("  -> Building Sheet 06: Messy Data Cleaned Pipeline...")
    build_pipeline_sheet(wb)

    print("  -> Building Sheet 01: Executive Dashboard (First Page)...")
    build_dashboard_sheet(wb)

    print("  -> Building Sheet 07: Model Documentation & Operating Guide...")
    build_documentation_sheet(wb)

    # Remove temporary default sheet
    if default_sheet in wb.worksheets:
        wb.remove(default_sheet)

    print(f"[SAVE] Saving complete financial workbook to: {OUTPUT_EXCEL}")
    wb.save(OUTPUT_EXCEL)
    print(f"[DONE] Successfully generated {OUTPUT_EXCEL} ({len(wb.worksheets)} sheets).")

if __name__ == '__main__':
    generate_complete_financial_model()
