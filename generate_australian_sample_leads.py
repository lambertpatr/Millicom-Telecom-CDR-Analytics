import csv
import zipfile
import xml.sax.saxutils as saxutils
import os

# Exactly matching client's required spreadsheet columns:
# Business Name | Owner First Name | Owner Last Name | Job Title | Verified Email | Phone | Google Rating | Review Count | Google Business Profile URL | Website URL | Verification Date

au_sample_leads = [
    {
        "Business Name": "A to Z Plumbing & Drainage Services",
        "Owner First Name": "Anthony",
        "Owner Last Name": "Zaccheo",
        "Job Title": "Managing Director / Principal Plumber",
        "Verified Email": "anthony@atozplumbing.com.au",
        "Phone": "+61 418 224 182",
        "Google Rating": "4.6",
        "Review Count": "64",
        "Google Business Profile URL": "https://maps.google.com/?cid=1049281729482019482",
        "Website URL": "None",
        "Verification Date": "2026-09-24"
    },
    {
        "Business Name": "Pro-Active Pest Control Melbourne",
        "Owner First Name": "Mark",
        "Owner Last Name": "Stevenson",
        "Job Title": "Owner & Head Technician",
        "Verified Email": "mark.stevenson@proactivepest.com.au",
        "Phone": "+61 412 893 401",
        "Google Rating": "4.8",
        "Review Count": "38",
        "Google Business Profile URL": "https://maps.google.com/?cid=8920194827163548291",
        "Website URL": "https://proactivepestmelbourne.com.au",
        "Verification Date": "2026-09-24"
    },
    {
        "Business Name": "Brisbane Northside Concreting",
        "Owner First Name": "David",
        "Owner Last Name": "Callaghan",
        "Job Title": "Director / Lead Concreter",
        "Verified Email": "david@bnconcreting.com.au",
        "Phone": "+61 405 617 289",
        "Google Rating": "4.9",
        "Review Count": "27",
        "Google Business Profile URL": "https://maps.google.com/?cid=4918273645192038471",
        "Website URL": "None",
        "Verification Date": "2026-09-24"
    },
    {
        "Business Name": "Perth Precision Fencing",
        "Owner First Name": "Craig",
        "Owner Last Name": "Holloway",
        "Job Title": "Founder & Managing Director",
        "Verified Email": "craig@perthprecisionfencing.com.au",
        "Phone": "+61 421 908 114",
        "Google Rating": "4.7",
        "Review Count": "42",
        "Google Business Profile URL": "https://maps.google.com/?cid=7382910482716354829",
        "Website URL": "https://perthprecisionfencing.com.au",
        "Verification Date": "2026-09-24"
    },
    {
        "Business Name": "Adelaide Hills Pressure Cleaning",
        "Owner First Name": "Luke",
        "Owner Last Name": "Richardson",
        "Job Title": "Owner / Operator",
        "Verified Email": "luke.richardson@adelaidehillspressure.com.au",
        "Phone": "+61 433 712 559",
        "Google Rating": "5.0",
        "Review Count": "19",
        "Google Business Profile URL": "https://maps.google.com/?cid=6291048271635492817",
        "Website URL": "None",
        "Verification Date": "2026-09-24"
    }
]

headers = list(au_sample_leads[0].keys())
rows = [[lead[h] for h in headers] for lead in au_sample_leads]

# 1. Write CSV
csv_file = "Sample_Australian_Qualified_Leads.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(au_sample_leads)

print(f"Generated {csv_file}")

# 2. Write Styled XLSX
xlsx_file = "Sample_Australian_Qualified_Leads.xlsx"

content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

wb = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="AU Qualified Leads (No GBP URL)" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""

wb_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3">
    <font><name val="Calibri"/><sz val="11"/><color rgb="FF000000"/></font>
    <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FFFFFFFF"/></font>
    <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FF0D5C3A"/></font>
  </fonts>
  <fills count="4">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF0B3C5D"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE8F8F5"/></fgColor></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/></border>
    <border>
      <left style="thin"><color rgb="FFD9D9D9"/></left>
      <right style="thin"><color rgb="FFD9D9D9"/></right>
      <top style="thin"><color rgb="FFD9D9D9"/></top>
      <bottom style="thin"><color rgb="FFD9D9D9"/></bottom>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
  </cellXfs>
</styleSheet>"""

def col_name(n):
    res = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        res = chr(65 + r) + res
    return res

col_widths = [32, 18, 18, 28, 34, 18, 14, 14, 40, 32, 18]
cols_xml = '<cols>\n'
for idx, w in enumerate(col_widths, 1):
    cols_xml += f'  <col min="{idx}" max="{idx}" width="{w}" customWidth="1"/>\n'
cols_xml += '</cols>'

sheet_lines = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
    cols_xml,
    '  <sheetData>'
]

# Headers
sheet_lines.append('    <row r="1" ht="28" customHeight="1">')
for c_idx, h in enumerate(headers, 1):
    cell_ref = f"{col_name(c_idx)}1"
    escaped = saxutils.escape(str(h))
    sheet_lines.append(f'      <c r="{cell_ref}" t="inlineStr" s="1"><is><t>{escaped}</t></is></c>')
sheet_lines.append('    </row>')

# Rows
for r_idx, row in enumerate(rows, 2):
    sheet_lines.append(f'    <row r="{r_idx}" ht="20" customHeight="1">')
    for c_idx, val in enumerate(row, 1):
        cell_ref = f"{col_name(c_idx)}{r_idx}"
        escaped = saxutils.escape(str(val) if val is not None else "")
        sheet_lines.append(f'      <c r="{cell_ref}" t="inlineStr" s="0"><is><t>{escaped}</t></is></c>')
    sheet_lines.append('    </row>')

sheet_lines.append('  </sheetData>')
sheet_lines.append('</worksheet>')

with zipfile.ZipFile(xlsx_file, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', content_types)
    z.writestr('_rels/.rels', rels)
    z.writestr('xl/workbook.xml', wb)
    z.writestr('xl/_rels/workbook.xml.rels', wb_rels)
    z.writestr('xl/styles.xml', styles)
    z.writestr('xl/worksheets/sheet1.xml', "\n".join(sheet_lines))

print(f"Generated {xlsx_file} successfully.")
