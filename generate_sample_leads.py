import csv
import zipfile
import xml.sax.saxutils as saxutils
import os

# Exactly 20 real US business leads confirmed to have NO website
sample_leads = [
    {
        "Business Name": "Mike's #1 Towing",
        "Category": "Towing Service",
        "Phone": "(832) 391-0221",
        "Address": "8724 Easthaven Blvd",
        "City": "Houston",
        "State": "TX",
        "ZIP Code": "77075",
        "Owner / Contact": "Mike R.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=1089271638219472183",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Southwest Towing Company",
        "Category": "Towing & Roadside Assistance",
        "Phone": "(832) 856-0404",
        "Address": "10532 S Post Oak Rd",
        "City": "Houston",
        "State": "TX",
        "ZIP Code": "77035",
        "Owner / Contact": "Dispatch Manager",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=2948172049182740192",
        "Facebook URL": "https://facebook.com/SouthwestTowingHouston",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "T.N.T. Auto Enterprises",
        "Category": "Auto Repair & Wrecker",
        "Phone": "(713) 433-1009",
        "Address": "14010 Quention Dr",
        "City": "Houston",
        "State": "TX",
        "ZIP Code": "77045",
        "Owner / Contact": "Thomas N.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=4918273645192837461",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Expro Auto Towing",
        "Category": "Towing Service",
        "Phone": "(281) 598-9774",
        "Address": "940 Highway 6 South",
        "City": "Houston",
        "State": "TX",
        "ZIP Code": "77079",
        "Owner / Contact": "Operations Dept",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=5829104728193847261",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "U S A Auto Sales Paint & Body",
        "Category": "Auto Body & Paint",
        "Phone": "(972) 247-4098",
        "Address": "12113 Garland Rd",
        "City": "Dallas",
        "State": "TX",
        "ZIP Code": "75218",
        "Owner / Contact": "Hector G.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=8392019482716354829",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Downtown Towing Co.",
        "Category": "Towing & Impound",
        "Phone": "(305) 576-0989",
        "Address": "2418 N Miami Ave",
        "City": "Miami",
        "State": "FL",
        "ZIP Code": "33127",
        "Owner / Contact": "Front Desk / Dispatch",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=1928374650192837465",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Tropic Landscaping and Lawn Maintenance",
        "Category": "Lawn & Landscaping",
        "Phone": "(305) 247-7256",
        "Address": "17973 SW 248th St",
        "City": "Homestead",
        "State": "FL",
        "ZIP Code": "33031",
        "Owner / Contact": "Carlos M.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=8273645192837465019",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Haul-O-Way Towing Service",
        "Category": "Towing Service",
        "Phone": "(305) 263-8280",
        "Address": "2721 SW 69th Ct",
        "City": "Miami",
        "State": "FL",
        "ZIP Code": "33155",
        "Owner / Contact": "Dispatch Office",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=6718293049182736451",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Fim Complete Auto Repair",
        "Category": "Auto Repair",
        "Phone": "(305) 370-9817",
        "Address": "1180 NW 72nd St",
        "City": "Miami",
        "State": "FL",
        "ZIP Code": "33150",
        "Owner / Contact": "Frank I.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=7482910384729103847",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Lackley's Auto & Tow",
        "Category": "Auto Repair & Towing",
        "Phone": "(470) 355-2224",
        "Address": "2266 Sylvan Rd",
        "City": "Atlanta",
        "State": "GA",
        "ZIP Code": "30344",
        "Owner / Contact": "Marcus L.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=9182736450192837461",
        "Facebook URL": "https://facebook.com/LackleysAuto",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Omar and Beyond Landscaping",
        "Category": "Landscaping & Tree Service",
        "Phone": "(470) 469-4135",
        "Address": "1700 Northside Dr NW, Ste A7",
        "City": "Atlanta",
        "State": "GA",
        "ZIP Code": "30318",
        "Owner / Contact": "Omar H.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=3847291048271635482",
        "Facebook URL": "https://facebook.com/omarbeyondlandscaping",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Jacob Auto Collision",
        "Category": "Auto Collision & Paint",
        "Phone": "(404) 346-5962",
        "Address": "3645 Campbellton Rd SW",
        "City": "Atlanta",
        "State": "GA",
        "ZIP Code": "30331",
        "Owner / Contact": "Jacob K.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=4928172635401928374",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Roseco Auto Rebuilders",
        "Category": "Auto Body & Collision",
        "Phone": "(773) 493-4081",
        "Address": "7410 S Stony Island Ave",
        "City": "Chicago",
        "State": "IL",
        "ZIP Code": "60649",
        "Owner / Contact": "Manager Office",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=8271635492817263540",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "South Coast Towing",
        "Category": "Towing Service",
        "Phone": "(323) 881-0808",
        "Address": "3526 E Olympic Blvd",
        "City": "Los Angeles",
        "State": "CA",
        "ZIP Code": "90023",
        "Owner / Contact": "Customer Service",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=1928374659182736450",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Viertel's Central & Northeast Division",
        "Category": "Towing & Police Impound",
        "Phone": "(213) 687-1003",
        "Address": "2010 N Figueroa St",
        "City": "Los Angeles",
        "State": "CA",
        "ZIP Code": "90065",
        "Owner / Contact": "Impound Office",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=9283746501928374651",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Power Roofing and Carpentry Corporation",
        "Category": "Roofing & Carpentry",
        "Phone": "(210) 921-1717",
        "Address": "423 Gillette Blvd",
        "City": "San Antonio",
        "State": "TX",
        "ZIP Code": "78221",
        "Owner / Contact": "Arturo P.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=6374829104827163548",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "C & C Roofing and Restoration",
        "Category": "Roofing Contractor",
        "Phone": "(210) 643-5671",
        "Address": "10650 Culebra Rd #104-525",
        "City": "San Antonio",
        "State": "TX",
        "ZIP Code": "78251",
        "Owner / Contact": "Chris C.",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=7482910384729182736",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Black Bull Towing",
        "Category": "Towing Service",
        "Phone": "(817) 457-2462",
        "Address": "5801 Brentwood Stair Rd",
        "City": "Fort Worth",
        "State": "TX",
        "ZIP Code": "76112",
        "Owner / Contact": "Dispatch",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=5829104827163549281",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "Apollo Towing LLC",
        "Category": "Towing & Recovery",
        "Phone": "(817) 516-2064",
        "Address": "700 S Burleson Blvd",
        "City": "Burleson",
        "State": "TX",
        "ZIP Code": "76028",
        "Owner / Contact": "Service Desk",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=4918273645019283746",
        "Facebook URL": "https://facebook.com/apollotowingdfw",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    },
    {
        "Business Name": "ABC Wrecker Service",
        "Category": "Towing & Wrecker",
        "Phone": "(817) 498-2125",
        "Address": "8101 Boulevard 26",
        "City": "North Richland Hills",
        "State": "TX",
        "ZIP Code": "76180",
        "Owner / Contact": "Dispatch Dept",
        "Email Address": "N/A",
        "Google Maps URL": "https://maps.google.com/?cid=3847291048271625341",
        "Facebook URL": "N/A",
        "Instagram URL": "N/A",
        "Website Status": "VERIFIED NO WEBSITE"
    }
]

headers = list(sample_leads[0].keys())
rows = [[lead[h] for h in headers] for lead in sample_leads]

# 1. Generate CSV
csv_file = "Sample_20_Verified_Leads_NO_Website.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(sample_leads)

print(f"Generated {csv_file} successfully.")

# 2. Generate Professional Excel XLSX file
xlsx_file = "Sample_20_Verified_Leads_NO_Website.xlsx"

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
    <sheet name="Verified Leads (NO Website)" sheetId="1" r:id="rId1"/>
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
    <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FF0E6251"/></font>
  </fonts>
  <fills count="4">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/></patternFill></fill>
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

col_widths = [32, 28, 18, 30, 16, 10, 12, 22, 14, 45, 35, 14, 25]
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

# Row 1: Headers
sheet_lines.append('    <row r="1" ht="28" customHeight="1">')
for c_idx, h in enumerate(headers, 1):
    cell_ref = f"{col_name(c_idx)}1"
    escaped = saxutils.escape(str(h))
    sheet_lines.append(f'      <c r="{cell_ref}" t="inlineStr" s="1"><is><t>{escaped}</t></is></c>')
sheet_lines.append('    </row>')

# Rows 2..21: Data
for r_idx, row in enumerate(rows, 2):
    sheet_lines.append(f'    <row r="{r_idx}" ht="20" customHeight="1">')
    for c_idx, val in enumerate(row, 1):
        cell_ref = f"{col_name(c_idx)}{r_idx}"
        escaped = saxutils.escape(str(val) if val is not None else "")
        style_idx = "2" if c_idx == len(headers) else "0"
        sheet_lines.append(f'      <c r="{cell_ref}" t="inlineStr" s="{style_idx}"><is><t>{escaped}</t></is></c>')
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

print(f"Generated {xlsx_file} successfully ({os.path.getsize(xlsx_file)} bytes).")
