"""
Greater Washington, D.C. Real Estate Transition & Scope Estimator Engine
========================================================================
Project: Proprietary Real Estate Decision & Scope-Estimating Engine
Market: Greater Washington, D.C. Metropolitan Area (DC, Northern Virginia, Suburban Maryland)
Output: Greater_DC_Property_Transition_Master_Estimator.xlsx

Sheets:
  1. 01_Field_Estimator_UI: Front-End Field Scope & Instant Estimate Generator.
     - Property Inputs: Target ZIP Code, Square Footage, Asset Tier (Good/Better/Best).
     - 21-Day Transition Parametric Scope Matrix (Decluttering, Paint, Flooring, Hardware, Lighting).
     - Automated Executive Outputs: Total Scope Cost, Operational Speed Zone (Alpha/Beta/Gamma), Value-Add Equity Lift, Projected ROI Multiple.
     - Protected sheet with Data Validation drop-downs; only input cells are unlocked.
  2. 02_Master_SKU_Database: Backend Catalog (Home Depot, Floor & Decor, Amazon).
     - Standardized SKUs, Unit Costs ($/SF, $/EA), Material Specifications.
  3. 03_Parametric_Rules_Multipliers: Central Formula Logic & Regional Multipliers.
     - Regional Tier Multipliers (1.00x - 1.55x) based on D.C. Metro submarket labor & Median Days on Market (MDOM).
     - Asset Tier Grade adjustments.
     - Scope Value-Add & ROI factors based on D.C. transition historical comps.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(WORKSPACE_DIR, 'Greater_DC_Property_Transition_Master_Estimator.xlsx')

FONT_FAMILY = 'Segoe UI' # Clean modern UI font

# Typography
F_TITLE = Font(name=FONT_FAMILY, size=15, bold=True, color='FFFFFF')
F_SUBTITLE = Font(name=FONT_FAMILY, size=10, italic=True, color='E2E8F0')
F_SECTION = Font(name=FONT_FAMILY, size=11, bold=True, color='FFFFFF')
F_HEADER = Font(name=FONT_FAMILY, size=10, bold=True, color='FFFFFF')
F_SUBHEADER = Font(name=FONT_FAMILY, size=10, bold=True, color='0F172A')

F_INPUT = Font(name=FONT_FAMILY, size=11, bold=True, color='002060') # Field Input
F_FORMULA = Font(name=FONT_FAMILY, size=10, color='1E293B')
F_BOLD_FORMULA = Font(name=FONT_FAMILY, size=10, bold=True, color='0F172A')
F_ITALIC = Font(name=FONT_FAMILY, size=9, italic=True, color='64748B')

# KPI Typography
F_KPI_TITLE = Font(name=FONT_FAMILY, size=9, bold=True, color='475569')
F_KPI_VAL = Font(name=FONT_FAMILY, size=17, bold=True, color='0A2540')
F_KPI_SUB = Font(name=FONT_FAMILY, size=8, color='64748B')

# Palette (Muted Executive Palette: D.C. Federal Slate Navy & Warm Gold Accents)
FILL_NAVY_BANNER = PatternFill(start_color='0F172A', end_color='0F172A', fill_type='solid') # Deep Slate Navy
FILL_NAVY_HEADER = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid') # Slate 800
FILL_SECTION = PatternFill(start_color='334155', end_color='334155', fill_type='solid')     # Slate 700
FILL_GOLD_ACCENT = PatternFill(start_color='D97706', end_color='D97706', fill_type='solid') # Amber 600
FILL_SUBHEADER = PatternFill(start_color='F1F5F9', end_color='F1F5F9', fill_type='solid')   # Slate 100
FILL_ZEBRA = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')       # Slate 50
FILL_KPI_CARD = PatternFill(start_color='F1F5F9', end_color='F1F5F9', fill_type='solid')

# Interactive Field Input Highlighting (Soft Mint / White with Medium Border)
FILL_INPUT_ACTIVE = PatternFill(start_color='ECFDF5', end_color='ECFDF5', fill_type='solid') # Emerald-50 tint
FILL_INPUT_WHITE = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
FILL_TOTAL_ROW = PatternFill(start_color='E2E8F0', end_color='E2E8F0', fill_type='solid')

# Status Alerts
FILL_ALPHA_SPEED = PatternFill(start_color='DCFCE7', end_color='DCFCE7', fill_type='solid') # Green
FONT_ALPHA_SPEED = Font(name=FONT_FAMILY, size=10, bold=True, color='166534')

FILL_BETA_SPEED = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid') # Amber
FONT_BETA_SPEED = Font(name=FONT_FAMILY, size=10, bold=True, color='92400E')

FILL_GAMMA_SPEED = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid') # Red
FONT_GAMMA_SPEED = Font(name=FONT_FAMILY, size=10, bold=True, color='991B1B')

# Borders
BORDER_THIN = Side(border_style='thin', color='CBD5E1')
BORDER_MEDIUM_NAVY = Side(border_style='medium', color='1E293B')
BORDER_DOUBLE_NAVY = Side(border_style='double', color='0F172A')

CELL_BORDER = Border(left=BORDER_THIN, right=BORDER_THIN, top=BORDER_THIN, bottom=BORDER_THIN)
INPUT_BORDER = Border(left=BORDER_MEDIUM_NAVY, right=BORDER_MEDIUM_NAVY, top=BORDER_MEDIUM_NAVY, bottom=BORDER_MEDIUM_NAVY)
TOTAL_BORDER = Border(top=BORDER_THIN, bottom=BORDER_DOUBLE_NAVY, left=BORDER_THIN, right=BORDER_THIN)

# Alignments
ALIGN_LEFT = Alignment(horizontal='left', vertical='center')
ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_RIGHT = Alignment(horizontal='right', vertical='center')
ALIGN_HEADER = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Formats
FMT_CURRENCY = '$#,##0'
FMT_CURRENCY_EXACT = '$#,##0.00'
FMT_PERCENT = '0.0%'
FMT_INTEGER = '#,##0'
FMT_MULTIPLE = '0.00"x"'

def auto_fit_columns(ws, min_width=13, max_cap=45):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or '')
            if cell.number_format and ('$' in cell.number_format or '%' in cell.number_format):
                val += '   '
            if len(val) > max_len:
                max_len = len(val)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, min_width), max_cap)

def style_title_banner(ws, end_col_letter, title, subtitle):
    ws.merge_cells(f'A1:{end_col_letter}1')
    c1 = ws['A1']
    c1.value = f"  {title.upper()}"
    c1.font = F_TITLE
    c1.fill = FILL_NAVY_BANNER
    c1.alignment = Alignment(horizontal='left', vertical='center')
    
    ws.merge_cells(f'A2:{end_col_letter}2')
    c2 = ws['A2']
    c2.value = f"  {subtitle}"
    c2.font = F_SUBTITLE
    c2.fill = FILL_NAVY_BANNER
    c2.alignment = Alignment(horizontal='left', vertical='center')
    
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 20

# -----------------------------------------------------------------------------
# TAB 3: PARAMETRIC RULES & REGIONAL MULTIPLIERS (LOGIC ENGINE)
# -----------------------------------------------------------------------------
def build_rules_sheet(wb):
    ws = wb.create_sheet(title="03_Parametric_Rules_Multipliers")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'I',
        "Parametric Rules & Regional Tier Multipliers (Engine Logic)",
        "Centralized Formula Logic: Greater D.C. Submarket Multipliers, Speed Zones & ROI Benchmark Multiples"
    )

    # TABLE 1: D.C. METRO ZIP CODES & SPEED ZONES
    ws.merge_cells('B5:G5')
    t1 = ws['B5']
    t1.value = "  1. GREATER D.C. SUBMARKET MATRIX & REGIONAL MULTIPLIERS"
    t1.font = F_SECTION
    t1.fill = FILL_NAVY_HEADER
    ws.row_dimensions[5].height = 24

    headers1 = ["Target ZIP Code", "Submarket / Neighborhood", "State / Jurisdiction", "Labor & Market Multiplier", "Historical MDOM (Days)", "Operational Speed Zone"]
    for i, h in enumerate(headers1, start=2):
        cell = ws.cell(row=6, column=i, value=h)
        cell.font = F_HEADER
        cell.fill = FILL_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[6].height = 24

    # D.C. Metro Data: Washington DC, Northern VA (Arlington, Alexandria, Fairfax, Loudoun), Suburban MD (Bethesda, Silver Spring, Chevy Chase)
    dc_zip_data = [
        ("20001", "Shaw / Logan Circle / Mt Vernon", "Washington, D.C.", 1.25, 12, "Alpha Zone (Ultra-Fast)"),
        ("20007", "Georgetown / Glover Park", "Washington, D.C.", 1.45, 11, "Alpha Zone (Ultra-Fast)"),
        ("20002", "Capitol Hill / H-Street Corridor", "Washington, D.C.", 1.20, 15, "Beta Zone (Standard)"),
        ("20009", "Dupont Circle / Adams Morgan", "Washington, D.C.", 1.35, 13, "Alpha Zone (Ultra-Fast)"),
        ("20016", "Tenleytown / AU Park / Spring Valley", "Washington, D.C.", 1.40, 14, "Alpha Zone (Ultra-Fast)"),
        ("22201", "Clarendon / Courthouse / Rosslyn", "Arlington, VA", 1.30, 9, "Alpha Zone (Ultra-Fast)"),
        ("22207", "North Arlington / Country Club", "Arlington, VA", 1.45, 10, "Alpha Zone (Ultra-Fast)"),
        ("22314", "Old Town Alexandria", "Alexandria, VA", 1.28, 16, "Beta Zone (Standard)"),
        ("22101", "McLean / Salona Village", "Fairfax County, VA", 1.55, 12, "Alpha Zone (Ultra-Fast)"),
        ("22182", "Vienna / Tysons Corner", "Fairfax County, VA", 1.25, 14, "Alpha Zone (Ultra-Fast)"),
        ("20190", "Reston Town Center / Dulles Corridor", "Fairfax County, VA", 1.15, 22, "Beta Zone (Standard)"),
        ("20814", "Bethesda / Downtown Arts District", "Montgomery Co, MD", 1.40, 11, "Alpha Zone (Ultra-Fast)"),
        ("20815", "Chevy Chase Village", "Montgomery Co, MD", 1.50, 8, "Alpha Zone (Ultra-Fast)"),
        ("20910", "Silver Spring / Woodside", "Montgomery Co, MD", 1.12, 24, "Beta Zone (Standard)"),
        ("20850", "Rockville Town Square", "Montgomery Co, MD", 1.10, 27, "Beta Zone (Standard)"),
        ("20782", "Hyattsville / Gateway Arts", "Prince George's, MD", 1.00, 38, "Gamma Zone (Extended)"),
    ]

    for row_idx, row in enumerate(dc_zip_data, start=7):
        for col_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = F_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (3, 4):
                cell.font = F_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx == 5:
                cell.font = F_BOLD_FORMULA
                cell.number_format = FMT_MULTIPLE
                cell.alignment = ALIGN_RIGHT
            elif col_idx == 6:
                cell.font = F_FORMULA
                cell.number_format = FMT_INTEGER
                cell.alignment = ALIGN_RIGHT
            elif col_idx == 7:
                cell.font = F_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
                if "Alpha" in val:
                    cell.fill = FILL_ALPHA_SPEED
                    cell.font = FONT_ALPHA_SPEED
                elif "Beta" in val:
                    cell.fill = FILL_BETA_SPEED
                    cell.font = FONT_BETA_SPEED
                else:
                    cell.fill = FILL_GAMMA_SPEED
                    cell.font = FONT_GAMMA_SPEED
        ws.row_dimensions[row_idx].height = 20

    # TABLE 2: ASSET TIER RULES
    r2 = 25
    ws.merge_cells(f'B{r2}:F{r2}')
    t2 = ws[f'B{r2}']
    t2.value = "  2. ASSET SPECIFICATION TIERS & GRADE MULTIPLIERS"
    t2.font = F_SECTION
    t2.fill = FILL_NAVY_HEADER
    ws.row_dimensions[r2].height = 24
    r2 += 1

    headers2 = ["Asset Tier Code", "Asset Tier Description", "Price Band Benchmark", "Specification Grade", "Finish Tier Multiplier"]
    for i, h in enumerate(headers2, start=2):
        cell = ws.cell(row=r2, column=i, value=h)
        cell.font = F_HEADER
        cell.fill = FILL_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[r2].height = 24
    r2 += 1

    asset_tier_data = [
        ("Good", "Good (< $500k Market Value)", "< $500,000 USD", "Clean Rental / Entry Spec (LVP, Builder Fixtures)", 1.00),
        ("Better", "Better ($500k - $799k Market Value)", "$500,000 - $799,999 USD", "Move-In Retail Spec (Wide Plank LVP, Matte Black)", 1.25),
        ("Best", "Best ($800k+ Executive Portfolio)", "$800,000+ USD", "Luxury Turnkey Spec (Engineered Oak, Designer Brass)", 1.60),
    ]

    for row in asset_tier_data:
        for col_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r2, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = F_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (3, 4, 5):
                cell.font = F_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx == 6:
                cell.font = F_BOLD_FORMULA
                cell.number_format = FMT_MULTIPLE
                cell.alignment = ALIGN_RIGHT
        ws.row_dimensions[r2].height = 20
        r2 += 1

    # TABLE 3: SCOPE VALUE-ADD & ROI MULTIPLES
    r3 = 31
    ws.merge_cells(f'B{r3}:F{r3}')
    t3 = ws[f'B{r3}']
    t3.value = "  3. 21-DAY COSMETIC VALUE-ADD & VALUE-CREATION ROI BENCHMARKS"
    t3.font = F_SECTION
    t3.fill = FILL_NAVY_HEADER
    ws.row_dimensions[r3].height = 24
    r3 += 1

    headers3 = ["Scope Category ID", "Scope Category Name", "Execution Window", "Typical Value-Add Multiple", "Market Strategic Rationale"]
    for i, h in enumerate(headers3, start=2):
        cell = ws.cell(row=r3, column=i, value=h)
        cell.font = F_HEADER
        cell.fill = FILL_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[r3].height = 24
    r3 += 1

    roi_data = [
        ("SCP-01", "Whole-Home Decluttering & Staging Prep", "Days 1 - 4", 2.15, "Highest direct ROI: eliminates visual friction; expands perceived SF"),
        ("SCP-02", "Interior Paint, Trim & Drywall Refinish", "Days 5 - 10", 1.95, "Neutral SW Alabaster/Agreeable Gray creates modern airy appeal"),
        ("SCP-03", "Flooring Modernization (LVP / Hardwood)", "Days 11 - 16", 1.80, "Removes dated carpet odor; unified continuous flooring visually doubles space"),
        ("SCP-04", "Cabinet Hardware & Modern Plumbing Fixtures", "Days 15 - 18", 1.85, "High-impact micro-refresh; elevates kitchens and baths at 1/10th remodel cost"),
        ("SCP-05", "Designer LED Lighting & Fixture Upgrade", "Days 18 - 21", 1.90, "Replaces 90s brass with 3000K warm LED lighting; photographs exceptionally"),
    ]

    for row in roi_data:
        for col_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r3, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = F_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (3, 4):
                cell.font = F_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx == 5:
                cell.font = F_BOLD_FORMULA
                cell.number_format = FMT_MULTIPLE
                cell.alignment = ALIGN_RIGHT
            elif col_idx == 6:
                cell.font = F_ITALIC
                cell.alignment = ALIGN_LEFT
        ws.row_dimensions[r3].height = 20
        r3 += 1

    ws.protection.sheet = True
    ws.protection.enable()
    ws.protection.set_password('dc2026')

    auto_fit_columns(ws, min_width=14)
    return ws

# -----------------------------------------------------------------------------
# TAB 2: MASTER SKU & MATERIAL PRICE DATABASE
# -----------------------------------------------------------------------------
def build_sku_sheet(wb):
    ws = wb.create_sheet(title="02_Master_SKU_Database")
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'J',
        "Master SKU & Material Price Database (Live Sourcing Feed)",
        "Structured Procurement Catalog: Home Depot, Floor & Decor, Amazon Commercial Rates ($/SF, $/EA)"
    )

    headers = [
        "SKU ID", "Scope Category", "Material / Item Description", "Preferred Sourcing Vendor", 
        "Unit Measure", "Good Spec ($)", "Better Spec ($)", "Best Spec ($)", "Labor Install Rate ($/Unit)", "Catalog Status"
    ]

    ws.row_dimensions[5].height = 24
    for i, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=i, value=h)
        cell.font = F_HEADER
        cell.fill = FILL_NAVY_HEADER
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER

    sku_catalog = [
        # (SKU, Category, Description, Vendor, UOM, Good, Better, Best, LaborRate, Status)
        ("SKU-DEC-101", "Decluttering", "Professional Junk Removal & 20-Yard Roll-off Dumpster", "1-800-Got-Junk / Local", "EA (Drop)", 450.0, 650.0, 950.0, 300.0, "ACTIVE"),
        ("SKU-DEC-102", "Decluttering", "Professional Staging Preparation, Deep Clean & Window Polish", "Commercial Clean Pro", "SF", 0.35, 0.55, 0.85, 0.20, "ACTIVE"),
        ("SKU-PNT-201", "Paint", "Interior Wall Paint (Sherwin Williams / Behr Premium)", "Home Depot Pro", "SF (Floor)", 1.20, 1.65, 2.40, 1.50, "ACTIVE"),
        ("SKU-PNT-202", "Paint", "Trim, Baseboard, Door & Ceiling Ultra-Pure White Enamel", "Sherwin Williams Comm", "SF (Floor)", 0.60, 0.85, 1.25, 0.75, "ACTIVE"),
        ("SKU-FLR-301", "Flooring", "Rigid Core Waterproof Luxury Vinyl Plank (LVP - 20mil Wear)", "Floor & Decor", "SF", 2.29, 3.49, 4.99, 2.25, "ACTIVE"),
        ("SKU-FLR-302", "Flooring", "Engineered European White Oak Hardwood Flooring", "Floor & Decor Pro", "SF", 3.99, 5.89, 8.99, 3.50, "ACTIVE"),
        ("SKU-FLR-303", "Flooring", "Premium Stain-Resistant Carpet & 8lb Memory Foam Pad", "Home Depot Comm", "SF", 1.85, 2.75, 4.10, 1.15, "ACTIVE"),
        ("SKU-HRD-401", "Hardware", "Modern Matte Black / Brushed Gold Cabinet Pulls (30-Pack)", "Amazon Business", "Set (Kitchen)", 65.0, 120.0, 220.0, 150.0, "ACTIVE"),
        ("SKU-HRD-402", "Hardware", "Contemporary High-Arc Pull-Down Commercial Kitchen Faucet", "Home Depot Pro", "EA", 119.0, 229.0, 399.0, 175.0, "ACTIVE"),
        ("SKU-HRD-403", "Hardware", "Single-Hole Matte Black Bathroom Faucets & Pop-Up Drains", "Amazon Commercial", "EA", 59.0, 115.0, 210.0, 120.0, "ACTIVE"),
        ("SKU-HRD-404", "Hardware", "Modern Interior Door Lever Handles & Privacy Latches", "Home Depot Pro", "EA (Door)", 18.5, 32.0, 58.0, 25.0, "ACTIVE"),
        ("SKU-LGT-501", "Lighting", "Ultra-Thin Dimmable 6-Inch Canless LED Recessed Lights (Pack of 12)", "Amazon Business", "Pack", 110.0, 185.0, 295.0, 180.0, "ACTIVE"),
        ("SKU-LGT-502", "Lighting", "Modern Architectural Dining Chandelier & Kitchen Island Pendants", "Wayfair / HD Comm", "Set", 140.0, 290.0, 580.0, 220.0, "ACTIVE"),
        ("SKU-LGT-503", "Lighting", "Contemporary Vanity 3-Light Bath Sconces (Brushed Gold/Black)", "Home Depot Pro", "EA", 65.0, 135.0, 245.0, 110.0, "ACTIVE"),
        ("SKU-LGT-504", "Lighting", "Smart Wi-Fi Rocker Light Switches & Decora Wall Plates", "Lutron / Amazon", "Set (Whole)", 85.0, 175.0, 320.0, 140.0, "ACTIVE"),
    ]

    for row_idx, row in enumerate(sku_catalog, start=6):
        for col_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.border = CELL_BORDER
            if col_idx == 2:
                cell.font = F_BOLD_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (3, 4, 5):
                cell.font = F_FORMULA
                cell.alignment = ALIGN_LEFT
            elif col_idx == 6:
                cell.font = F_FORMULA
                cell.alignment = ALIGN_CENTER
            elif col_idx in (7, 8, 9, 10):
                cell.font = F_FORMULA
                cell.number_format = FMT_CURRENCY_EXACT
                cell.alignment = ALIGN_RIGHT
            elif col_idx == 11:
                cell.font = F_BOLD_FORMULA
                cell.fill = FILL_ALPHA_SPEED
                cell.font = FONT_ALPHA_SPEED
                cell.alignment = ALIGN_CENTER
        ws.row_dimensions[row_idx].height = 20

    ws.protection.sheet = True
    ws.protection.enable()
    ws.protection.set_password('dc2026')

    auto_fit_columns(ws, min_width=14)
    return ws

# -----------------------------------------------------------------------------
# TAB 1: FRONT-END FIELD SCOPE & INSTANT ESTIMATE GENERATOR (THE USER INTERFACE)
# -----------------------------------------------------------------------------
def build_ui_sheet(wb):
    ws = wb.create_sheet(title="01_Field_Scope_Estimator", index=0)
    ws.views.sheetView[0].showGridLines = True
    
    style_title_banner(
        ws, 'K',
        "Greater D.C. Property Transition & Instant Scope Estimator",
        "Proprietary Decision Engine: On-Site Parametric Estimator, 21-Day Transition Budgets & Value-Add ROI"
    )

    # -------------------------------------------------------------------------
    # SECTION 1: PROJECT INPUTS & PROPERTY PROFILE (INTERACTIVE FIELD INPUTS)
    # -------------------------------------------------------------------------
    ws.merge_cells('B5:K5')
    s1 = ws['B5']
    s1.value = "  STEP 1: ON-SITE PROPERTY INPUTS & MARKET SELECTION"
    s1.font = F_SECTION
    s1.fill = FILL_NAVY_HEADER
    ws.row_dimensions[5].height = 24

    input_labels = [
        ("Target Property Address:", "B6", "1420 14th Street NW, Washington, D.C.", "C6:D6", "Text", False),
        ("Target ZIP Code (D.C. Metro):", "B7", "20001", "C7", "ZIP_Pick", True),
        ("Property Square Footage (SF):", "B8", 1850, "C8", "Integer", True),
        ("Selected Asset Tier:", "B9", "Better", "C9", "Tier_Pick", True),
    ]

    # Style Step 1 Inputs
    # B column: Label
    # C column: Input
    for label, b_cell, default_val, merge_target, input_type, is_unlocked in input_labels:
        r = int(b_cell[1:])
        cell_lbl = ws[b_cell]
        cell_lbl.value = label
        cell_lbl.font = F_SUBHEADER
        cell_lbl.fill = FILL_SUBHEADER
        cell_lbl.alignment = ALIGN_LEFT
        cell_lbl.border = CELL_BORDER

        if ':' in merge_target:
            ws.merge_cells(merge_target)
            top_left = merge_target.split(':')[0]
            val_cell = ws[top_left]
        else:
            val_cell = ws[merge_target]
        
        val_cell.value = default_val
        val_cell.font = F_INPUT
        val_cell.fill = FILL_INPUT_ACTIVE
        val_cell.border = INPUT_BORDER
        val_cell.alignment = ALIGN_CENTER if input_type != "Text" else ALIGN_LEFT
        
        if input_type == "Integer":
            val_cell.number_format = FMT_INTEGER
        
        # Unlock input cells for field users!
        if is_unlocked or input_type == "Text":
            val_cell.protection = Protection(locked=False)
            if ':' in merge_target:
                end_c = merge_target.split(':')[1]
                ws[end_c].protection = Protection(locked=False)
        
        ws.row_dimensions[r].height = 24

    # D.C. Regional Lookup Cards (Columns F to K, rows 6 to 9)
    # Submarket Display
    ws.merge_cells('F6:H6')
    c_sm_lbl = ws['F6']
    c_sm_lbl.value = "Identified Submarket:"
    c_sm_lbl.font = F_SUBHEADER
    c_sm_lbl.fill = FILL_SUBHEADER
    c_sm_lbl.border = CELL_BORDER
    
    ws.merge_cells('I6:K6')
    c_sm_val = ws['I6']
    # XLOOKUP Target ZIP in Tab 3
    c_sm_val.value = '=XLOOKUP(C7,\'03_Parametric_Rules_Multipliers\'!$B$7:$B$22,\'03_Parametric_Rules_Multipliers\'!$C$7:$C$22&" ("&\'03_Parametric_Rules_Multipliers\'!$D$7:$D$22&")","Unknown ZIP")'
    c_sm_val.font = F_BOLD_FORMULA
    c_sm_val.alignment = ALIGN_LEFT
    c_sm_val.border = CELL_BORDER

    # Regional Labor Multiplier
    ws.merge_cells('F7:H7')
    c_lm_lbl = ws['F7']
    c_lm_lbl.value = "Regional Labor Multiplier:"
    c_lm_lbl.font = F_SUBHEADER
    c_lm_lbl.fill = FILL_SUBHEADER
    c_lm_lbl.border = CELL_BORDER

    ws.merge_cells('I7:K7')
    c_lm_val = ws['I7']
    c_lm_val.value = '=XLOOKUP(C7,\'03_Parametric_Rules_Multipliers\'!$B$7:$B$22,\'03_Parametric_Rules_Multipliers\'!$E$7:$E$22,1.0)'
    c_lm_val.font = F_BOLD_FORMULA
    c_lm_val.number_format = FMT_MULTIPLE
    c_lm_val.alignment = ALIGN_CENTER
    c_lm_val.border = CELL_BORDER

    # Historical MDOM
    ws.merge_cells('F8:H8')
    c_mdom_lbl = ws['F8']
    c_mdom_lbl.value = "Median Days on Market (MDOM):"
    c_mdom_lbl.font = F_SUBHEADER
    c_mdom_lbl.fill = FILL_SUBHEADER
    c_mdom_lbl.border = CELL_BORDER

    ws.merge_cells('I8:K8')
    c_mdom_val = ws['I8']
    c_mdom_val.value = '=XLOOKUP(C7,\'03_Parametric_Rules_Multipliers\'!$B$7:$B$22,\'03_Parametric_Rules_Multipliers\'!$F$7:$F$22,21)&" Days"'
    c_mdom_val.font = F_BOLD_FORMULA
    c_mdom_val.alignment = ALIGN_CENTER
    c_mdom_val.border = CELL_BORDER

    # Operational Speed Zone
    ws.merge_cells('F9:H9')
    c_sz_lbl = ws['F9']
    c_sz_lbl.value = "Operational Speed Zone:"
    c_sz_lbl.font = F_SUBHEADER
    c_sz_lbl.fill = FILL_SUBHEADER
    c_sz_lbl.border = CELL_BORDER

    ws.merge_cells('I9:K9')
    c_sz_val = ws['I9']
    c_sz_val.value = '=XLOOKUP(C7,\'03_Parametric_Rules_Multipliers\'!$B$7:$B$22,\'03_Parametric_Rules_Multipliers\'!$G$7:$G$22,"Standard")'
    c_sz_val.font = F_BOLD_FORMULA
    c_sz_val.fill = FILL_ALPHA_SPEED
    c_sz_val.font = FONT_ALPHA_SPEED
    c_sz_val.alignment = ALIGN_CENTER
    c_sz_val.border = CELL_BORDER

    # -------------------------------------------------------------------------
    # EXECUTIVE KPI SUMMARY CARDS (ROW 11 TO 13)
    # -------------------------------------------------------------------------
    kpis = [
        # (Label, Formula, Format, Subtext, StartCol, EndCol)
        ("TOTAL ESTIMATED TRANSITION SCOPE", "=I22", FMT_CURRENCY, "Includes Labor, Materials & Multipliers", "B", "C"),
        ("AVERAGE COST PER SQUARE FOOT", "=I22/C8", FMT_CURRENCY_EXACT, "Comprehensive $/SF investment", "D", "E"),
        ("ESTIMATED VALUE-ADD EQUITY LIFT", "=K23", FMT_CURRENCY, "Projected Net Equity Spread", "F", "G"),
        ("PROJECTED VALUE-ADD / ROI MULTIPLE", "=K24", FMT_MULTIPLE, "Benchmark: 1.8x - 2.0x target", "H", "I"),
        ("ESTIMATED TARGET COMPLETION", '="21 Business Days"', "@", "Guaranteed 21-Day Cosmetic Turn", "J", "K"),
    ]

    for label, formula, fmt, subtext, scol, ecol in kpis:
        # Title
        ws.merge_cells(f'{scol}11:{ecol}11')
        c_l = ws[f'{scol}11']
        c_l.value = label
        c_l.font = F_KPI_TITLE
        c_l.fill = FILL_KPI_CARD
        c_l.alignment = ALIGN_CENTER
        c_l.border = Border(top=BORDER_THIN, left=BORDER_THIN, right=BORDER_THIN)

        # Val
        ws.merge_cells(f'{scol}12:{ecol}12')
        c_v = ws[f'{scol}12']
        c_v.value = formula
        c_v.font = F_KPI_VAL
        c_v.fill = FILL_KPI_CARD
        c_v.number_format = fmt
        c_v.alignment = ALIGN_CENTER
        c_v.border = Border(left=BORDER_THIN, right=BORDER_THIN)

        # Sub
        ws.merge_cells(f'{scol}13:{ecol}13')
        c_s = ws[f'{scol}13']
        c_s.value = subtext
        c_s.font = F_KPI_SUB
        c_s.fill = FILL_KPI_CARD
        c_s.alignment = ALIGN_CENTER
        c_s.border = Border(bottom=BORDER_THIN, left=BORDER_THIN, right=BORDER_THIN)

    ws.row_dimensions[11].height = 18
    ws.row_dimensions[12].height = 28
    ws.row_dimensions[13].height = 16

    # -------------------------------------------------------------------------
    # SECTION 2: 21-DAY COSMETIC PARAMETRIC SCOPE SELECTOR
    # -------------------------------------------------------------------------
    ws.merge_cells('B15:K15')
    s2 = ws['B15']
    s2.value = "  STEP 2: 21-DAY COSMETIC TRANSITION SCOPE BUILDER (PARAMETRIC SELECTOR)"
    s2.font = F_SECTION
    s2.fill = FILL_NAVY_HEADER
    ws.row_dimensions[15].height = 24

    scope_headers = [
        "Include in Scope?", "Scope Line Item / Package", "Execution Category", "Base Scope Qty / Unit", 
        "Selected SKU Code", "Material Unit Rate", "Labor Unit Rate", "Regional Scope Cost", "Target ROI Multiple", "Projected Value-Add ($)"
    ]

    for i, h in enumerate(scope_headers, start=2):
        cell = ws.cell(row=16, column=i, value=h)
        cell.font = F_HEADER
        cell.fill = FILL_SECTION
        cell.alignment = ALIGN_HEADER
        cell.border = CELL_BORDER
    ws.row_dimensions[16].height = 24

    # 5 Scope Lines
    scope_rows = [
        # (Include, Name, Category, DefaultQtyFormula, DefaultSKU, ROIMultipleFormula)
        ("YES", "Whole-Home Decluttering & Staging Prep", "Decluttering", "=C8", "SKU-DEC-102", "='03_Parametric_Rules_Multipliers'!$E$35"),
        ("YES", "Interior Paint, Drywall & Trim Modernization", "Paint", "=C8", "SKU-PNT-201", "='03_Parametric_Rules_Multipliers'!$E$36"),
        ("YES", "Continuous Waterproof LVP / Hardwood Flooring", "Flooring", "=C8*0.75", "SKU-FLR-301", "='03_Parametric_Rules_Multipliers'!$E$37"),
        ("YES", "Cabinet Pulls & Contemporary Plumbing Fixtures", "Hardware", 1, "SKU-HRD-401", "='03_Parametric_Rules_Multipliers'!$E$38"),
        ("YES", "Designer 3000K LED Recessed & Accent Lighting", "Lighting", 1, "SKU-LGT-501", "='03_Parametric_Rules_Multipliers'!$E$39"),
    ]

    r_scope = 17
    for inc, name, cat, qty, sku, roi_f in scope_rows:
        # Col B: Include Toggle (Unlocked!)
        c_inc = ws.cell(row=r_scope, column=2, value=inc)
        c_inc.font = F_INPUT
        c_inc.fill = FILL_INPUT_ACTIVE
        c_inc.alignment = ALIGN_CENTER
        c_inc.border = INPUT_BORDER
        c_inc.protection = Protection(locked=False)

        # Col C: Line Item Name
        c_name = ws.cell(row=r_scope, column=3, value=name)
        c_name.font = F_BOLD_FORMULA
        c_name.alignment = ALIGN_LEFT
        c_name.border = CELL_BORDER

        # Col D: Execution Category
        c_cat = ws.cell(row=r_scope, column=4, value=cat)
        c_cat.font = F_FORMULA
        c_cat.alignment = ALIGN_LEFT
        c_cat.border = CELL_BORDER

        # Col E: Base Scope Qty (Unlocked for field adjustments!)
        c_qty = ws.cell(row=r_scope, column=5, value=qty)
        c_qty.font = F_INPUT
        c_qty.fill = FILL_INPUT_ACTIVE
        c_qty.alignment = ALIGN_RIGHT
        c_qty.number_format = FMT_INTEGER
        c_qty.border = INPUT_BORDER
        c_qty.protection = Protection(locked=False)

        # Col F: Selected SKU Code (Unlocked drop-down!)
        c_sku = ws.cell(row=r_scope, column=6, value=sku)
        c_sku.font = F_INPUT
        c_sku.fill = FILL_INPUT_ACTIVE
        c_sku.alignment = ALIGN_CENTER
        c_sku.border = INPUT_BORDER
        c_sku.protection = Protection(locked=False)

        # Col G: Material Unit Rate ($/Unit) based on Asset Tier (Good/Better/Best)
        # Dynamic XLOOKUP: Looks up SKU in Tab 2, retrieves column based on Asset Tier in C9
        # In Tab 2: Good is Col G (7), Better is Col H (8), Best is Col I (9)
        # Using IFS: =IF(C9="Good", XLOOKUP(F{r},'02_Master_SKU_Database'!$B$6:$B$20,'02_Master_SKU_Database'!$G$6:$G$20), IF(C9="Best", XLOOKUP(F{r},'02_Master_SKU_Database'!$B$6:$B$20,'02_Master_SKU_Database'!$I$6:$I$20), XLOOKUP(F{r},'02_Master_SKU_Database'!$B$6:$B$20,'02_Master_SKU_Database'!$H$6:$H$20)))
        c_mat = ws.cell(row=r_scope, column=7)
        c_mat.value = f'=IF($C$9="Good", XLOOKUP(F{r_scope},\'02_Master_SKU_Database\'!$B$6:$B$20,\'02_Master_SKU_Database\'!$G$6:$G$20,0), IF($C$9="Best", XLOOKUP(F{r_scope},\'02_Master_SKU_Database\'!$B$6:$B$20,\'02_Master_SKU_Database\'!$I$6:$I$20,0), XLOOKUP(F{r_scope},\'02_Master_SKU_Database\'!$B$6:$B$20,\'02_Master_SKU_Database\'!$H$6:$H$20,0)))'
        c_mat.font = F_FORMULA
        c_mat.number_format = FMT_CURRENCY_EXACT
        c_mat.alignment = ALIGN_RIGHT
        c_mat.border = CELL_BORDER

        # Col H: Labor Unit Rate ($/Unit)
        # =XLOOKUP(F{r},'02_Master_SKU_Database'!$B$6:$B$20,'02_Master_SKU_Database'!$J$6:$J$20,0)*$I$7
        # Multiplies baseline labor rate by regional labor multiplier in I7
        c_lab = ws.cell(row=r_scope, column=8)
        c_lab.value = f'=XLOOKUP(F{r_scope},\'02_Master_SKU_Database\'!$B$6:$B$20,\'02_Master_SKU_Database\'!$J$6:$J$20,0)*$I$7'
        c_lab.font = F_FORMULA
        c_lab.number_format = FMT_CURRENCY_EXACT
        c_lab.alignment = ALIGN_RIGHT
        c_lab.border = CELL_BORDER

        # Col I: Regional Scope Cost ($)
        # =IF(B{r}="YES", E{r}*(G{r}+H{r}), 0)
        c_cost = ws.cell(row=r_scope, column=9)
        c_cost.value = f'=IF(B{r_scope}="YES", E{r_scope}*(G{r_scope}+H{r_scope}), 0)'
        c_cost.font = F_BOLD_FORMULA
        c_cost.number_format = FMT_CURRENCY
        c_cost.alignment = ALIGN_RIGHT
        c_cost.border = CELL_BORDER

        # Col J: Target ROI Multiple
        c_roi = ws.cell(row=r_scope, column=10, value=roi_f)
        c_roi.font = F_BOLD_FORMULA
        c_roi.number_format = FMT_MULTIPLE
        c_roi.alignment = ALIGN_RIGHT
        c_roi.border = CELL_BORDER

        # Col K: Projected Value-Add ($)
        # =I{r}*J{r}
        c_va = ws.cell(row=r_scope, column=11)
        c_va.value = f'=I{r_scope}*J{r_scope}'
        c_va.font = F_BOLD_FORMULA
        c_va.number_format = FMT_CURRENCY
        c_va.alignment = ALIGN_RIGHT
        c_va.border = CELL_BORDER

        ws.row_dimensions[r_scope].height = 22
        r_scope += 1

    # TOTAL ROW (Row 22)
    tot_row = r_scope
    ws.merge_cells(f'B{tot_row}:H{tot_row}')
    c_tot_lbl = ws[f'B{tot_row}']
    c_tot_lbl.value = "TOTAL 21-DAY ESTIMATED TRANSITION SCOPE INVESTMENT"
    c_tot_lbl.font = Font(name=FONT_FAMILY, size=11, bold=True, color='0F172A')
    c_tot_lbl.fill = FILL_TOTAL_ROW
    c_tot_lbl.alignment = Alignment(horizontal='right', vertical='center')
    c_tot_lbl.border = TOTAL_BORDER

    c_tot_cost = ws.cell(row=tot_row, column=9, value=f"=SUM(I17:I21)")
    c_tot_cost.font = Font(name=FONT_FAMILY, size=11, bold=True, color='0F172A')
    c_tot_cost.fill = FILL_TOTAL_ROW
    c_tot_cost.number_format = FMT_CURRENCY
    c_tot_cost.alignment = ALIGN_RIGHT
    c_tot_cost.border = TOTAL_BORDER

    c_tot_roi = ws.cell(row=tot_row, column=10, value=f"=K{tot_row+1}/I{tot_row}")
    c_tot_roi.font = Font(name=FONT_FAMILY, size=11, bold=True, color='0F172A')
    c_tot_roi.fill = FILL_TOTAL_ROW
    c_tot_roi.number_format = FMT_MULTIPLE
    c_tot_roi.alignment = ALIGN_RIGHT
    c_tot_roi.border = TOTAL_BORDER

    c_tot_va = ws.cell(row=tot_row, column=11, value=f"=SUM(K17:K21)")
    c_tot_va.font = Font(name=FONT_FAMILY, size=11, bold=True, color='166534')
    c_tot_va.fill = FILL_ALPHA_SPEED
    c_tot_va.number_format = FMT_CURRENCY
    c_tot_va.alignment = ALIGN_RIGHT
    c_tot_va.border = TOTAL_BORDER
    ws.row_dimensions[tot_row].height = 24

    # NET EQUITY CREATION SUMMARY ROW (Row 23)
    eq_row = tot_row + 1
    ws.merge_cells(f'B{eq_row}:J{eq_row}')
    c_eq_lbl = ws[f'B{eq_row}']
    c_eq_lbl.value = "NET PROJECTED EQUITY CREATION / PROFIT SPREAD (VALUE-ADD MINUS SCOPE COST)"
    c_eq_lbl.font = Font(name=FONT_FAMILY, size=10, bold=True, color='0369A1')
    c_eq_lbl.fill = FILL_SUBHEADER
    c_eq_lbl.alignment = Alignment(horizontal='right', vertical='center')
    c_eq_lbl.border = CELL_BORDER

    c_eq_val = ws.cell(row=eq_row, column=11, value=f"=K{tot_row}-I{tot_row}")
    c_eq_val.font = Font(name=FONT_FAMILY, size=11, bold=True, color='0369A1')
    c_eq_val.fill = FILL_KPI_CARD
    c_eq_val.number_format = FMT_CURRENCY
    c_eq_val.alignment = ALIGN_RIGHT
    c_eq_val.border = CELL_BORDER
    ws.row_dimensions[eq_row].height = 22

    # ROI Multiple Row (Row 24)
    roi_row = eq_row + 1
    ws.merge_cells(f'B{roi_row}:J{roi_row}')
    c_roi_lbl = ws[f'B{roi_row}']
    c_roi_lbl.value = "BLENDED PORTFOLIO VALUE-ADD MULTIPLE (ARV LIFT ÷ SCOPE INVESTMENT)"
    c_roi_lbl.font = Font(name=FONT_FAMILY, size=10, bold=True, color='0F172A')
    c_roi_lbl.fill = FILL_SUBHEADER
    c_roi_lbl.alignment = Alignment(horizontal='right', vertical='center')
    c_roi_lbl.border = CELL_BORDER

    c_roi_val = ws.cell(row=roi_row, column=11, value=f"=K{tot_row}/I{tot_row}")
    c_roi_val.font = Font(name=FONT_FAMILY, size=11, bold=True, color='0F172A')
    c_roi_val.fill = FILL_SUBHEADER
    c_roi_val.number_format = FMT_MULTIPLE
    c_roi_val.alignment = ALIGN_RIGHT
    c_roi_val.border = CELL_BORDER
    ws.row_dimensions[roi_row].height = 22

    # -------------------------------------------------------------------------
    # DATA VALIDATION DROP-DOWNS
    # -------------------------------------------------------------------------
    # 1. ZIP Code Validation (Referencing Tab 3 B7:B22)
    dv_zip = DataValidation(type="list", formula1="'03_Parametric_Rules_Multipliers'!$B$7:$B$22", allow_blank=False)
    dv_zip.error ='Please select a valid D.C. Metropolitan ZIP code from the drop-down list.'
    dv_zip.errorTitle = 'Invalid D.C. ZIP Code'
    ws.add_data_validation(dv_zip)
    dv_zip.add(ws['C7'])

    # 2. Asset Tier Validation (Good, Better, Best)
    dv_tier = DataValidation(type="list", formula1='"Good,Better,Best"', allow_blank=False)
    dv_tier.error = 'Please select Good, Better, or Best.'
    dv_tier.errorTitle = 'Invalid Asset Tier'
    ws.add_data_validation(dv_tier)
    dv_tier.add(ws['C9'])

    # 3. Include Toggle (YES, NO) for Scope Rows 17 to 21
    dv_inc = DataValidation(type="list", formula1='"YES,NO"', allow_blank=False)
    dv_inc.error = 'Please choose YES or NO.'
    dv_inc.errorTitle = 'Invalid Scope Toggle'
    ws.add_data_validation(dv_inc)
    for r in range(17, 22):
        dv_inc.add(ws[f'B{r}'])

    # 4. SKU Validation (Referencing Tab 2 B6:B20)
    dv_sku = DataValidation(type="list", formula1="'02_Master_SKU_Database'!$B$6:$B$20", allow_blank=False)
    dv_sku.error = 'Please select an approved catalog SKU from the list.'
    dv_sku.errorTitle = 'Invalid Material SKU'
    ws.add_data_validation(dv_sku)
    for r in range(17, 22):
        dv_sku.add(ws[f'F{r}'])

    # -------------------------------------------------------------------------
    # FIELD PROTECTION & LOCKING GUIDELINES
    # -------------------------------------------------------------------------
    # Protect sheet so non-technical users cannot break formulas
    ws.protection.sheet = True
    ws.protection.enable()
    ws.protection.set_password('dc2026') # Standard unlocked or known admin key

    auto_fit_columns(ws, min_width=14)
    return ws

# -----------------------------------------------------------------------------
# MAIN COMPILER PIPELINE
# -----------------------------------------------------------------------------
def build_master_estimator():
    print("[ESTIMATOR] Initializing Greater D.C. Real Estate Transition Engine...")
    wb = openpyxl.Workbook()
    default_sheet = wb.active

    print("  -> Generating Tab 3: Parametric Rules & Regional Multipliers...")
    build_rules_sheet(wb)

    print("  -> Generating Tab 2: Master SKU & Material Price Database...")
    build_sku_sheet(wb)

    print("  -> Generating Tab 1: Front-End Field Scope & Estimate Generator (UI)...")
    build_ui_sheet(wb)

    if default_sheet in wb.worksheets:
        wb.remove(default_sheet)

    # Order sheets exactly as requested: Tab 1, Tab 2, Tab 3
    wb._sheets = [
        wb['01_Field_Scope_Estimator'],
        wb['02_Master_SKU_Database'],
        wb['03_Parametric_Rules_Multipliers']
    ]

    print(f"[SAVE] Saving Master Estimator to: {OUTPUT_FILE}")
    wb.save(OUTPUT_FILE)
    print(f"[DONE] Successfully generated {OUTPUT_FILE} (3 interconnected tabs in exact order).")

if __name__ == '__main__':
    build_master_estimator()
