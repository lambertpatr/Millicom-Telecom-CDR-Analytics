"""
Millicom (Tigo Tanzania) Telecommunications CDR & Mediation Ingestion Engine
=============================================================================
Project: Millicom Enterprise Telecom CDR Analytics & Network Intelligence Platform
Operator: MIC Tanzania PLC (Tigo Tanzania / Millicom Group) - MCC: 640, MNC: 02
Author: Principal Telecommunications Data Scientist & Network Architect

Extracts and models multi-domain telecommunications datasets:
1. millicom_cell_towers_infrastructure.csv: BTS / NodeB / eNodeB / gNodeB infrastructure across Tanzania.
2. millicom_subscribers_master.csv: Subscriber profiles, SIM IMSI/IMEI pairs, ARPU segments, tenancy.
3. millicom_cdr_voice.csv: Voice Call Detail Records (VoLTE, 3G, 2G, CSFB, on-net, off-net, roaming, dropped).
4. millicom_cdr_data_sessions.csv: Packet Data Protocol (PDP) data sessions (4G/LTE, 5G, 3G, APNs, QCI).
5. millicom_cdr_tigo_pesa_momo.csv: Mobile Money (Tigo Pesa) USSD & App transactions.
6. millicom_interconnect_operator_rates.csv: National & International Interconnect MTR settlements.
"""

import os
import csv
import random
import math
from datetime import datetime, timedelta

# Deterministic seed for reproducible analytics
random.seed(42)

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------------------------------------------------------
# 1. TANZANIA TELECOMMUNICATIONS TOPOLOGY & CELL TOWERS
# -----------------------------------------------------------------------------
# Real geographic coordinates, CGI configurations (MCC 640, MNC 02), and sector layouts
TOWERS_SPEC = [
    # Dar es Salaam - Eastern Zone (Commercial Mega-Hub)
    {"id": "TZ-DAR-001", "name": "Posta CBD Prime eNodeB", "region": "Dar es Salaam", "district": "Ilala", "lat": -6.8163, "lon": 39.2889, "tech": "5G", "capacity": 96, "azimuth": 45, "height_m": 42},
    {"id": "TZ-DAR-002", "name": "Kariakoo Market Commercial Sector", "region": "Dar es Salaam", "district": "Ilala", "lat": -6.8228, "lon": 39.2745, "tech": "4G", "capacity": 120, "azimuth": 120, "height_m": 38},
    {"id": "TZ-DAR-003", "name": "Oysterbay Diplomatic Hub", "region": "Dar es Salaam", "district": "Kinondoni", "lat": -6.7750, "lon": 39.2700, "tech": "5G", "capacity": 80, "azimuth": 0, "height_m": 35},
    {"id": "TZ-DAR-004", "name": "Masaki Peninsula Marina Site", "region": "Dar es Salaam", "district": "Kinondoni", "lat": -6.7482, "lon": 39.2785, "tech": "5G", "capacity": 64, "azimuth": 90, "height_m": 32},
    {"id": "TZ-DAR-005", "name": "Mwenge IT & University Corridor", "region": "Dar es Salaam", "district": "Kinondoni", "lat": -6.7725, "lon": 39.2223, "tech": "4G", "capacity": 96, "azimuth": 180, "height_m": 40},
    {"id": "TZ-DAR-006", "name": "Sinza Commercial Hub", "region": "Dar es Salaam", "district": "Ubungo", "lat": -6.7865, "lon": 39.2230, "tech": "4G", "capacity": 88, "azimuth": 270, "height_m": 36},
    {"id": "TZ-DAR-007", "name": "Ubungo Magufuli Terminal Junction", "region": "Dar es Salaam", "district": "Ubungo", "lat": -6.7885, "lon": 39.1982, "tech": "4G", "capacity": 112, "azimuth": 60, "height_m": 45},
    {"id": "TZ-DAR-008", "name": "Mbezi Beach Residential eNodeB", "region": "Dar es Salaam", "district": "Kinondoni", "lat": -6.7025, "lon": 39.2081, "tech": "4G", "capacity": 72, "azimuth": 135, "height_m": 35},
    {"id": "TZ-DAR-009", "name": "Tegeta Commercial Center", "region": "Dar es Salaam", "district": "Kinondoni", "lat": -6.6712, "lon": 39.1678, "tech": "4G", "capacity": 64, "azimuth": 210, "height_m": 38},
    {"id": "TZ-DAR-010", "name": "Temeke Industrial Port Gate", "region": "Dar es Salaam", "district": "Temeke", "lat": -6.8520, "lon": 39.2740, "tech": "4G", "capacity": 96, "azimuth": 300, "height_m": 45},
    {"id": "TZ-DAR-011", "name": "Kigamboni Ferry & Deepwater Pier", "region": "Dar es Salaam", "district": "Kigamboni", "lat": -6.8285, "lon": 39.3082, "tech": "4G", "capacity": 64, "azimuth": 45, "height_m": 36},
    {"id": "TZ-DAR-012", "name": "JNIA Airport Terminal 3 International", "region": "Dar es Salaam", "district": "Ilala", "lat": -6.8781, "lon": 39.2026, "tech": "5G", "capacity": 112, "azimuth": 180, "height_m": 40},
    {"id": "TZ-DAR-013", "name": "Gerezani SGR Central Station", "region": "Dar es Salaam", "district": "Ilala", "lat": -6.8241, "lon": 39.2840, "tech": "5G", "capacity": 96, "azimuth": 90, "height_m": 35},
    {"id": "TZ-DAR-014", "name": "Kurasini TIPER Depot Industrial", "region": "Dar es Salaam", "district": "Temeke", "lat": -6.8610, "lon": 39.2885, "tech": "3G", "capacity": 48, "azimuth": 150, "height_m": 42},
    {"id": "TZ-DAR-015", "name": "Gongolamboto Transit Corridor", "region": "Dar es Salaam", "district": "Ilala", "lat": -6.8970, "lon": 39.1550, "tech": "3G", "capacity": 56, "azimuth": 240, "height_m": 38},

    # Coastal Zone (Pwani & Tanga)
    {"id": "TZ-PWA-001", "name": "Kibaha Maili Moja Industrial", "region": "Pwani", "district": "Kibaha", "lat": -6.7712, "lon": 38.9880, "tech": "4G", "capacity": 64, "azimuth": 60, "height_m": 45},
    {"id": "TZ-PWA-002", "name": "Bagamoyo Special Economic Zone", "region": "Pwani", "district": "Bagamoyo", "lat": -6.4420, "lon": 38.9050, "tech": "4G", "capacity": 56, "azimuth": 90, "height_m": 40},
    {"id": "TZ-TAN-001", "name": "Tanga Port Marine Gantry", "region": "Tanga", "district": "Tanga City", "lat": -5.0680, "lon": 39.1020, "tech": "4G", "capacity": 64, "azimuth": 45, "height_m": 42},
    {"id": "TZ-TAN-002", "name": "Chumbageni Tanga CBD", "region": "Tanga", "district": "Tanga City", "lat": -5.0745, "lon": 39.0910, "tech": "3G", "capacity": 48, "azimuth": 180, "height_m": 36},
    {"id": "TZ-TAN-003", "name": "Korogwe Junction Transit Hub", "region": "Tanga", "district": "Korogwe", "lat": -5.1580, "lon": 38.4820, "tech": "3G", "capacity": 40, "azimuth": 270, "height_m": 45},

    # Northern Zone (Arusha, Kilimanjaro, Manyara)
    {"id": "TZ-ARU-001", "name": "Arusha Clocktower Central CBD", "region": "Arusha", "district": "Arusha City", "lat": -3.3725, "lon": 36.6944, "tech": "5G", "capacity": 88, "azimuth": 0, "height_m": 40},
    {"id": "TZ-ARU-002", "name": "Njiro Diplomatic Complex", "region": "Arusha", "district": "Arusha City", "lat": -3.4020, "lon": 36.7110, "tech": "4G", "capacity": 64, "azimuth": 120, "height_m": 35},
    {"id": "TZ-ARU-003", "name": "Kisongo EAC Industrial Corridor", "region": "Arusha", "district": "Arumeru", "lat": -3.4110, "lon": 36.6180, "tech": "4G", "capacity": 56, "azimuth": 210, "height_m": 42},
    {"id": "TZ-KIL-001", "name": "Moshi Town KNCU Central Site", "region": "Kilimanjaro", "district": "Moshi Urban", "lat": -3.3349, "lon": 37.3404, "tech": "4G", "capacity": 72, "azimuth": 60, "height_m": 38},
    {"id": "TZ-KIL-002", "name": "Machame Kilimanjaro Foothills", "region": "Kilimanjaro", "district": "Hai", "lat": -3.2250, "lon": 37.2400, "tech": "3G", "capacity": 40, "azimuth": 30, "height_m": 32},
    {"id": "TZ-KIL-003", "name": "Himo Kenya-Tanzania Border Hub", "region": "Kilimanjaro", "district": "Moshi Rural", "lat": -3.3850, "lon": 37.5480, "tech": "3G", "capacity": 48, "azimuth": 90, "height_m": 45},

    # Lake Zone (Mwanza, Mara, Kagera, Geita, Shinyanga)
    {"id": "TZ-MWA-001", "name": "Mwanza Capri Point Lake Tower", "region": "Mwanza", "district": "Ilemela", "lat": -2.5180, "lon": 32.8980, "tech": "5G", "capacity": 88, "azimuth": 315, "height_m": 42},
    {"id": "TZ-MWA-002", "name": "Nyegezi Bus & Lake Ferry Hub", "region": "Mwanza", "district": "Nyamagana", "lat": -2.5710, "lon": 32.9150, "tech": "4G", "capacity": 80, "azimuth": 180, "height_m": 38},
    {"id": "TZ-MWA-003", "name": "Kirumba CCM Stadium Sector", "region": "Mwanza", "district": "Ilemela", "lat": -2.5020, "lon": 32.9050, "tech": "4G", "capacity": 72, "azimuth": 45, "height_m": 36},
    {"id": "TZ-GEI-001", "name": "Geita Gold Mine Industrial Gateway", "region": "Geita", "district": "Geita Urban", "lat": -2.8710, "lon": 32.2280, "tech": "4G", "capacity": 64, "azimuth": 90, "height_m": 45},
    {"id": "TZ-SHI-001", "name": "Shinyanga Diamond Trade Hub", "region": "Shinyanga", "district": "Shinyanga Urban", "lat": -3.6639, "lon": 33.4211, "tech": "3G", "capacity": 48, "azimuth": 270, "height_m": 40},
    {"id": "TZ-BUK-001", "name": "Bukoba Lake Port Commercial", "region": "Kagera", "district": "Bukoba Urban", "lat": -1.3317, "lon": 31.8122, "tech": "3G", "capacity": 48, "azimuth": 60, "height_m": 38},
    {"id": "TZ-MAR-001", "name": "Musoma Lake Victoria Pier", "region": "Mara", "district": "Musoma Urban", "lat": -1.5030, "lon": 33.8050, "tech": "3G", "capacity": 40, "azimuth": 120, "height_m": 35},
    {"id": "TZ-TAR-001", "name": "Tarime Sirari Border Post", "region": "Mara", "district": "Tarime", "lat": -1.3490, "lon": 34.3680, "tech": "3G", "capacity": 48, "azimuth": 45, "height_m": 42},

    # Central Zone (Dodoma - National Capital, Singida, Tabora)
    {"id": "TZ-DOM-001", "name": "Dodoma National Parliament (Bunge)", "region": "Dodoma", "district": "Dodoma Urban", "lat": -6.1730, "lon": 35.7480, "tech": "5G", "capacity": 96, "azimuth": 0, "height_m": 40},
    {"id": "TZ-DOM-002", "name": "Mtumba Government City Sector A", "region": "Dodoma", "district": "Dodoma Urban", "lat": -6.1150, "lon": 35.9120, "tech": "5G", "capacity": 88, "azimuth": 90, "height_m": 45},
    {"id": "TZ-DOM-003", "name": "Jamatini Dodoma CBD Central", "region": "Dodoma", "district": "Dodoma Urban", "lat": -6.1820, "lon": 35.7420, "tech": "4G", "capacity": 80, "azimuth": 180, "height_m": 38},
    {"id": "TZ-SNG-001", "name": "Singida Crossroads Logistics Center", "region": "Singida", "district": "Singida Urban", "lat": -4.8160, "lon": 34.7430, "tech": "3G", "capacity": 48, "azimuth": 270, "height_m": 40},
    {"id": "TZ-TAB-001", "name": "Tabora Railway Junction Hub", "region": "Tabora", "district": "Tabora Urban", "lat": -5.0160, "lon": 32.8000, "tech": "3G", "capacity": 48, "azimuth": 135, "height_m": 42},

    # Southern Highlands Zone (Mbeya, Iringa, Songwe, Njombe, Ruvuma)
    {"id": "TZ-MBY-001", "name": "Mwanjelwa Market Mbeya Central", "region": "Mbeya", "district": "Mbeya City", "lat": -8.9094, "lon": 33.4608, "tech": "4G", "capacity": 80, "azimuth": 45, "height_m": 40},
    {"id": "TZ-MBY-002", "name": "Uyole TAZARA & TANZAM Junction", "region": "Mbeya", "district": "Mbeya Rural", "lat": -8.9320, "lon": 33.5350, "tech": "4G", "capacity": 72, "azimuth": 120, "height_m": 45},
    {"id": "TZ-IRI-001", "name": "Iringa Kihesa Highland Ridge", "region": "Iringa", "district": "Iringa Urban", "lat": -7.7710, "lon": 35.6980, "tech": "4G", "capacity": 64, "azimuth": 0, "height_m": 38},
    {"id": "TZ-TND-001", "name": "Tunduma Zambia Border Clearance", "region": "Songwe", "district": "Momba", "lat": -9.3020, "lon": 32.7680, "tech": "3G", "capacity": 64, "azimuth": 220, "height_m": 42},
    {"id": "TZ-NJO-001", "name": "Makambako Agro-Railway Interchange", "region": "Njombe", "district": "Makambako", "lat": -8.8480, "lon": 34.8320, "tech": "3G", "capacity": 48, "azimuth": 180, "height_m": 38},
    {"id": "TZ-SON-001", "name": "Songea Commercial Gateway", "region": "Ruvuma", "district": "Songea Urban", "lat": -10.6830, "lon": 35.6500, "tech": "3G", "capacity": 40, "azimuth": 90, "height_m": 35},

    # Zanzibar Archipelago (Unguja & Pemba - Zantel / Tigo Integration)
    {"id": "TZ-ZNZ-001", "name": "Stone Town Old Fort & Seafront", "region": "Zanzibar", "district": "Mjini", "lat": -6.1620, "lon": 39.1880, "tech": "5G", "capacity": 88, "azimuth": 270, "height_m": 30},
    {"id": "TZ-ZNZ-002", "name": "Mwanakwerekwe Trade Corridor", "region": "Zanzibar", "district": "Magharibi", "lat": -6.1750, "lon": 39.2280, "tech": "4G", "capacity": 72, "azimuth": 90, "height_m": 36},
    {"id": "TZ-ZNZ-003", "name": "Nungwi Tourism & Beach Resort Hub", "region": "Zanzibar", "district": "Kaskazini A", "lat": -5.7250, "lon": 39.2980, "tech": "4G", "capacity": 64, "azimuth": 0, "height_m": 32},
    {"id": "TZ-ZNZ-004", "name": "Paje Kite Beach Resort Hub", "region": "Zanzibar", "district": "Kusini", "lat": -6.2650, "lon": 39.5350, "tech": "4G", "capacity": 56, "azimuth": 60, "height_m": 28},
    {"id": "TZ-PEM-001", "name": "Chake Chake Clove Capital", "region": "Pemba", "district": "Kusini Pemba", "lat": -5.2450, "lon": 39.7680, "tech": "3G", "capacity": 40, "azimuth": 180, "height_m": 35},

    # Western & Southern Coastal (Morogoro, Mtwara, Kigoma)
    {"id": "TZ-MOR-001", "name": "Morogoro Msamvu Transit Hub", "region": "Morogoro", "district": "Morogoro Urban", "lat": -6.8120, "lon": 37.6620, "tech": "4G", "capacity": 72, "azimuth": 45, "height_m": 42},
    {"id": "TZ-MTW-001", "name": "Mtwara Deepwater Energy & Port Hub", "region": "Mtwara", "district": "Mtwara Urban", "lat": -10.2740, "lon": 40.1820, "tech": "4G", "capacity": 64, "azimuth": 90, "height_m": 45},
    {"id": "TZ-KIG-001", "name": "Kigoma Port Lake Tanganyika Pier", "region": "Kigoma", "district": "Kigoma Urban", "lat": -4.8760, "lon": 29.6260, "tech": "3G", "capacity": 48, "azimuth": 270, "height_m": 40},
    {"id": "TZ-KAH-001", "name": "Kahama Gold Corridor Commercial", "region": "Shinyanga", "district": "Kahama", "lat": -3.8370, "lon": 32.6000, "tech": "4G", "capacity": 64, "azimuth": 0, "height_m": 38}
]

# Interconnect Operators in Tanzania (TCRA Regulated)
OPERATORS = {
    "TIGO_ON_NET": {"name": "Tigo Tanzania (On-Net)", "prefixes": ["25571", "25565", "25567", "25577"], "in_mtr": 0.0, "out_mtr": 0.0, "retail_rate_tzs_min": 30.0},
    "VODACOM": {"name": "Vodacom Tanzania", "prefixes": ["25574", "25575", "25576"], "in_mtr": 15.6, "out_mtr": 15.6, "retail_rate_tzs_min": 45.0},
    "AIRTEL": {"name": "Airtel Tanzania", "prefixes": ["25568", "25569", "25578"], "in_mtr": 15.6, "out_mtr": 15.6, "retail_rate_tzs_min": 45.0},
    "HALOTEL": {"name": "Halotel (Viettel)", "prefixes": ["25562", "25561"], "in_mtr": 15.6, "out_mtr": 15.6, "retail_rate_tzs_min": 45.0},
    "TTCL": {"name": "TTCL Corporation", "prefixes": ["25573"], "in_mtr": 15.6, "out_mtr": 15.6, "retail_rate_tzs_min": 45.0},
    "INTL_KENYA": {"name": "Safaricom Kenya", "prefixes": ["2547"], "in_mtr": 45.0, "out_mtr": 120.0, "retail_rate_tzs_min": 250.0},
    "INTL_UGANDA": {"name": "MTN Uganda", "prefixes": ["2567"], "in_mtr": 45.0, "out_mtr": 120.0, "retail_rate_tzs_min": 250.0},
    "INTL_UK": {"name": "Vodafone UK", "prefixes": ["447"], "in_mtr": 65.0, "out_mtr": 350.0, "retail_rate_tzs_min": 600.0},
    "INTL_USA": {"name": "AT&T USA", "prefixes": ["1"], "in_mtr": 30.0, "out_mtr": 200.0, "retail_rate_tzs_min": 450.0},
    "FRAUD_PREMIUM": {"name": "Global Satellite Gateway", "prefixes": ["882", "881"], "in_mtr": 15.0, "out_mtr": 1200.0, "retail_rate_tzs_min": 2500.0}
}

HANDSET_MODELS = [
    ("Samsung Galaxy S24 Ultra (5G)", "Smartphone 5G", 0.08),
    ("Apple iPhone 15 Pro Max (5G)", "Smartphone 5G", 0.07),
    ("Samsung Galaxy A54 (5G)", "Smartphone 5G", 0.15),
    ("Tecno Camon 20 Pro (4G)", "Smartphone 4G", 0.22),
    ("Infinix Hot 30 (4G)", "Smartphone 4G", 0.20),
    ("Xiaomi Redmi Note 12 (4G)", "Smartphone 4G", 0.12),
    ("Nokia 105 Dual SIM (2G Feature)", "Feature Phone 2G", 0.10),
    ("Itel Magic 2 (3G Feature)", "Feature Phone 3G", 0.06)
]

CUSTOMER_SEGMENTS = [
    ("Corporate VIP", 0.05, (120000, 450000)),
    ("High-Value Data Pro", 0.15, (60000, 180000)),
    ("SME Trader & Merchant", 0.25, (30000, 95000)),
    ("Youth & Campus Streamer", 0.30, (12000, 45000)),
    ("Mass Market Voice/SMS", 0.20, (3000, 18000)),
    ("Dormant / At-Risk", 0.05, (0, 3000))
]

def generate_msisdn(operator_key="TIGO_ON_NET"):
    prefixes = OPERATORS[operator_key]["prefixes"]
    prefix = random.choice(prefixes)
    if len(prefix) == 5: # e.g. 25571
        suffix = f"{random.randint(100000, 999999)}"
        return f"+{prefix}{suffix}"
    elif len(prefix) == 4: # e.g. 2547
        suffix = f"{random.randint(1000000, 9999999)}"
        return f"+{prefix}{suffix}"
    elif prefix == "1":
        suffix = f"{random.randint(2000000000, 9999999999)}"
        return f"+{prefix}{suffix}"
    else:
        suffix = f"{random.randint(100000, 999999)}"
        return f"+{prefix}{suffix}"

def generate_imsi(msisdn):
    # Tanzania MCC 640, Tigo MNC 02
    return f"64002{random.randint(1000000000, 9999999999)}"

def generate_imei():
    tac = random.choice(["35689111", "86420504", "35204410", "35872109"])
    sn = f"{random.randint(100000, 999999)}"
    cd = f"{random.randint(0, 9)}"
    return f"{tac}{sn}{cd}"

def generate_data():
    print("[1/5] Generating Telecom Infrastructure & Cell Towers...")
    towers_file = os.path.join(WORKSPACE_DIR, 'millicom_cell_towers_infrastructure.csv')
    with open(towers_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'tower_id', 'tower_name', 'region', 'district', 'latitude', 'longitude',
            'technology', 'voice_capacity_erlangs', 'data_backhaul_capacity_gbps',
            'antenna_azimuth_deg', 'tower_height_m', 'operational_status'
        ])
        for t in TOWERS_SPEC:
            backhaul = 10.0 if t['tech'] == '5G' else (2.5 if t['tech'] == '4G' else 0.5)
            status = "Operational" if random.random() > 0.03 else "Maintenance Degradation"
            writer.writerow([
                t['id'], t['name'], t['region'], t['district'], t['lat'], t['lon'],
                t['tech'], t['capacity'], backhaul, t['azimuth'], t['height_m'], status
            ])
    print(f" -> Created {len(TOWERS_SPEC)} cell towers across 14 Tanzanian regions.")

    # -------------------------------------------------------------------------
    # 2. SUBSCRIBERS MASTER REGISTER (Including SIM-box fraud rings & churners)
    # -------------------------------------------------------------------------
    print("[2/5] Ingesting Subscriber Master Profiles (1,500 subscribers)...")
    subscribers = []
    subscribers_file = os.path.join(WORKSPACE_DIR, 'millicom_subscribers_master.csv')

    # Assign fraud groups: 8 SIM-box accounts, 5 Wangiri fraud accounts
    simbox_indices = set(range(10, 18))
    wangiri_indices = set(range(25, 30))

    with open(subscribers_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'subscriber_id', 'msisdn', 'imsi', 'imei', 'plan_type', 'customer_segment',
            'handset_model', 'handset_category', 'tenancy_months', 'arpu_monthly_tzs',
            'home_region', 'primary_cell_id', 'is_simbox_suspect', 'is_wangiri_suspect',
            'predicted_churn_tier'
        ])

        for i in range(1500):
            sub_id = f"TGO-SUB-{100000 + i}"
            msisdn = generate_msisdn("TIGO_ON_NET")
            imsi = generate_imsi(msisdn)
            imei = generate_imei()

            # Handset choice
            h_choice = random.choices(HANDSET_MODELS, weights=[h[2] for h in HANDSET_MODELS])[0]

            # Segment
            seg_choice = random.choices(CUSTOMER_SEGMENTS, weights=[s[1] for s in CUSTOMER_SEGMENTS])[0]
            arpu = random.uniform(seg_choice[2][0], seg_choice[2][1])
            plan = "Postpaid" if seg_choice[0] == "Corporate VIP" else ("Hybrid" if "SME" in seg_choice[0] else "Prepaid")

            tower = random.choice(TOWERS_SPEC)
            is_simbox = 1 if i in simbox_indices else 0
            is_wangiri = 1 if i in wangiri_indices else 0

            # Churn propensity
            if is_simbox or is_wangiri:
                churn_tier = "Fraud Blacklist"
            elif seg_choice[0] == "Dormant / At-Risk":
                churn_tier = "High Churn Risk (85%+)"
            elif random.random() < 0.12:
                churn_tier = "Medium Churn Risk (40-60%)"
            else:
                churn_tier = "Low Churn Risk (<15%)"

            # Ingest SIM box characteristics (fixed tower, same cheap feature phone IMEI tac)
            if is_simbox:
                h_choice = ("SIM-Box 32-Port Gateway", "SIM-Box Bypass", 0.0)
                imei = f"864205040000{i:02d}"
                tower = TOWERS_SPEC[0] # All stuck on Posta CBD / Kariakoo
                plan = "Prepaid (Unlimited Flat Rate)"
                arpu = 85000.0

            tenancy = random.randint(1, 120) if not is_simbox else random.randint(1, 3)

            sub_record = {
                'id': sub_id, 'msisdn': msisdn, 'imsi': imsi, 'imei': imei,
                'plan': plan, 'segment': seg_choice[0], 'handset': h_choice[0],
                'handset_cat': h_choice[1], 'tenancy': tenancy, 'arpu': round(arpu, 2),
                'region': tower['region'], 'tower_id': tower['id'],
                'is_simbox': is_simbox, 'is_wangiri': is_wangiri, 'churn_tier': churn_tier
            }
            subscribers.append(sub_record)

            writer.writerow([
                sub_id, msisdn, imsi, imei, plan, seg_choice[0], h_choice[0],
                h_choice[1], tenancy, round(arpu, 2), tower['region'], tower['id'],
                is_simbox, is_wangiri, churn_tier
            ])

    print(f" -> Created {len(subscribers)} subscribers (including 8 SIM-box and 5 Wangiri fraud profiles).")

    # -------------------------------------------------------------------------
    # 3. VOICE CALL DETAIL RECORDS (CDRs) - 10,000 Call Events
    # -------------------------------------------------------------------------
    print("[3/5] Ingesting Voice CDRs (10,000 records) with TCRA QoS and Fraud Scenarios...")
    voice_file = os.path.join(WORKSPACE_DIR, 'millicom_cdr_voice.csv')

    base_time = datetime(2026, 9, 1, 0, 0, 0)
    op_keys = list(OPERATORS.keys())
    op_weights = [0.55, 0.20, 0.12, 0.07, 0.02, 0.015, 0.01, 0.008, 0.005, 0.002]

    # Pre-select SIM-box and Wangiri subscribers for injection
    simbox_subs = [s for s in subscribers if s['is_simbox']]
    wangiri_subs = [s for s in subscribers if s['is_wangiri']]
    normal_subs = [s for s in subscribers if not s['is_simbox'] and not s['is_wangiri']]

    voice_records = []
    with open(voice_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'cdr_id', 'timestamp', 'calling_msisdn', 'called_msisdn', 'call_direction',
            'call_type', 'duration_sec', 'termination_cause', 'call_status',
            'cell_id', 'interconnect_operator', 'retail_revenue_tzs', 'settlement_mtr_tzs',
            'erlang_fraction', 'is_dropped', 'is_simbox_flag', 'is_wangiri_flag'
        ])

        cdr_idx = 1000000
        for day in range(7): # 7-day telecommunications sample
            for h in range(24):
                # Diurnal traffic curve: peak in morning 9-11 and evening 19-21
                if 9 <= h <= 11 or 19 <= h <= 21:
                    calls_in_hour = random.randint(75, 110)
                elif 0 <= h <= 5:
                    calls_in_hour = random.randint(10, 25)
                else:
                    calls_in_hour = random.randint(40, 70)

                for _ in range(calls_in_hour):
                    cdr_idx += 1
                    call_dt = base_time + timedelta(days=day, hours=h, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                    call_ts_str = call_dt.strftime("%Y-%m-%d %H:%M:%S")

                    # Fraud injection probability
                    is_simbox_call = False
                    is_wangiri_call = False

                    dice = random.random()
                    if dice < 0.035 and simbox_subs:
                        # SIM-box call: massive outgoing call burst, strictly terminating locally from international bypass
                        caller = random.choice(simbox_subs)
                        called_op = random.choice(["TIGO_ON_NET", "VODACOM", "AIRTEL"])
                        callee_msisdn = generate_msisdn(called_op)
                        direction = "MO (Mobile Originated)"
                        call_type = "VoLTE"
                        duration = random.randint(180, 420) # Prolonged bypass conversation
                        status = "ANSWERED"
                        cause = "NORMAL_CLEARING"
                        is_dropped = 0
                        is_simbox_call = True
                        interconnect_op = called_op
                        retail_rev = 0.0 # Unlimited plan or zero retail tariff
                        settlement_mtr = OPERATORS[called_op]['out_mtr'] * (duration / 60.0)
                        tower = TOWERS_SPEC[0] # Stationary

                    elif dice < 0.045 and wangiri_subs:
                        # Wangiri call: 1 ring (1-3 seconds), dropped immediately to entice call-back
                        caller = random.choice(wangiri_subs)
                        direction = "MO (Mobile Originated)"
                        call_type = "CS_VOICE"
                        duration = random.randint(1, 3) # Flash call
                        status = "NO_ANSWER_FLASH"
                        cause = "CALLER_ABANDON"
                        is_dropped = 0
                        is_wangiri_call = True
                        interconnect_op = "FRAUD_PREMIUM"
                        callee_msisdn = generate_msisdn("TIGO_ON_NET")
                        retail_rev = 0.0
                        settlement_mtr = 0.0
                        tower = random.choice(TOWERS_SPEC)

                    else:
                        # Regular subscriber
                        caller = random.choice(normal_subs)
                        direction = "MO (Mobile Originated)" if random.random() > 0.45 else "MT (Mobile Terminated)"
                        called_op = random.choices(op_keys, weights=op_weights)[0]
                        callee_msisdn = generate_msisdn(called_op)
                        interconnect_op = called_op
                        tower = next((t for t in TOWERS_SPEC if t['id'] == caller['tower_id']), random.choice(TOWERS_SPEC))

                        # Call setup success and completion modeling
                        # TCRA Target: CCR >= 98%, Dropped < 0.8%
                        call_type = random.choice(["VoLTE", "VoLTE", "3G_CS", "2G_CS"])
                        r_outcome = random.random()

                        if r_outcome < 0.68:
                            # Successful Answered Call
                            status = "ANSWERED"
                            duration = random.randint(15, 360)
                            cause = "NORMAL_CLEARING"
                            is_dropped = 0
                        elif r_outcome < 0.80:
                            # User Busy
                            status = "BUSY"
                            duration = 0
                            cause = "USER_BUSY"
                            is_dropped = 0
                        elif r_outcome < 0.94:
                            # No Answer / Ring timeout
                            status = "NO_ANSWER"
                            duration = 0
                            cause = "NO_ANSWER_TIMEOUT"
                            is_dropped = 0
                        elif r_outcome < 0.985:
                            # Network Dropped Call (TCRA SLA metric)
                            status = "DROPPED"
                            duration = random.randint(10, 120)
                            cause = random.choice(["RADIO_LINK_FAILURE", "HANDOVER_FAILURE", "UPLINK_INTERFERENCE"])
                            is_dropped = 1
                        else:
                            # Network Congestion Block (Erlang B blockage)
                            status = "CONGESTION_BLOCKED"
                            duration = 0
                            cause = "TRUNK_CIRCUIT_CONGESTION"
                            is_dropped = 0

                        # Tariffs & Revenues
                        if status in ["ANSWERED", "DROPPED"]:
                            mins = math.ceil(duration / 60.0)
                            rate = OPERATORS[interconnect_op]['retail_rate_tzs_min']
                            retail_rev = mins * rate
                            settlement_mtr = mins * OPERATORS[interconnect_op]['out_mtr'] if interconnect_op != "TIGO_ON_NET" else 0.0
                        else:
                            retail_rev = 0.0
                            settlement_mtr = 0.0

                    erlang_fraction = round(duration / 3600.0, 6)

                    writer.writerow([
                        f"CDR-V-{cdr_idx}", call_ts_str, caller['msisdn'], callee_msisdn,
                        direction, call_type, duration, cause, status, tower['id'],
                        interconnect_op, round(retail_rev, 2), round(settlement_mtr, 2),
                        erlang_fraction, is_dropped, 1 if is_simbox_call else 0, 1 if is_wangiri_call else 0
                    ])
                    voice_records.append(cdr_idx)

    print(f" -> Created {len(voice_records)} Voice CDRs.")

    # -------------------------------------------------------------------------
    # 4. MOBILE DATA SESSION CDRs (4G/5G/3G PDP Contexts) - 5,000 Records
    # -------------------------------------------------------------------------
    print("[4/5] Ingesting Mobile Data Sessions (5,000 records)...")
    data_file = os.path.join(WORKSPACE_DIR, 'millicom_cdr_data_sessions.csv')
    apns = [
        ("tigo.internet", 0.70, "General Mobile Web / Social / Video"),
        ("tigo.corporate", 0.12, "Enterprise Dedicated APN"),
        ("tigo.pesa.app", 0.15, "Zero-Rated Financial Services APN"),
        ("tigo.mms", 0.03, "Multimedia Messaging Service")
    ]

    with open(data_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'session_id', 'timestamp', 'msisdn', 'imsi', 'cell_id', 'technology',
            'apn_name', 'uplink_mb', 'downlink_mb', 'total_traffic_mb', 'duration_min',
            'avg_throughput_mbps', 'rtt_latency_ms', 'packet_loss_pct', 'billable_amount_tzs'
        ])

        for i in range(5000):
            sess_id = f"CDR-D-{2000000 + i}"
            day = random.randint(0, 6)
            h = random.randint(0, 23)
            sess_dt = base_time + timedelta(days=day, hours=h, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
            sub = random.choice(normal_subs)
            tower = next((t for t in TOWERS_SPEC if t['id'] == sub['tower_id']), random.choice(TOWERS_SPEC))
            tech = tower['tech']

            apn_item = random.choices(apns, weights=[a[1] for a in apns])[0]
            apn = apn_item[0]

            duration_min = random.randint(2, 90)

            # Throughput & traffic by technology
            if tech == "5G":
                dl_mb = random.uniform(150.0, 3200.0)
                ul_mb = dl_mb * random.uniform(0.12, 0.25)
                throughput = random.uniform(45.0, 280.0)
                rtt = random.uniform(12.0, 28.0)
                loss = random.uniform(0.01, 0.15)
            elif tech == "4G":
                dl_mb = random.uniform(25.0, 950.0)
                ul_mb = dl_mb * random.uniform(0.15, 0.30)
                throughput = random.uniform(12.0, 65.0)
                rtt = random.uniform(25.0, 55.0)
                loss = random.uniform(0.05, 0.45)
            else: # 3G
                dl_mb = random.uniform(5.0, 85.0)
                ul_mb = dl_mb * random.uniform(0.20, 0.40)
                throughput = random.uniform(1.2, 7.5)
                rtt = random.uniform(65.0, 140.0)
                loss = random.uniform(0.5, 2.8)

            total_mb = dl_mb + ul_mb

            # Tariff: ~TZS 2.5 per MB or zero-rated
            if apn == "tigo.pesa.app":
                billable = 0.0 # Zero-rated
            else:
                billable = round(total_mb * 2.2, 2)

            writer.writerow([
                sess_id, sess_dt.strftime("%Y-%m-%d %H:%M:%S"), sub['msisdn'], sub['imsi'],
                tower['id'], tech, apn, round(ul_mb, 2), round(dl_mb, 2), round(total_mb, 2),
                duration_min, round(throughput, 2), round(rtt, 1), round(loss, 2), billable
            ])

    print(" -> Created 5,000 Data PDP Context CDRs.")

    # -------------------------------------------------------------------------
    # 5. TIGO PESA MOBILE MONEY TRANSACTIONS (3,500 Records)
    # -------------------------------------------------------------------------
    print("[5/5] Processing Tigo Pesa Mobile Money CDRs (3,500 records)...")
    momo_file = os.path.join(WORKSPACE_DIR, 'millicom_cdr_tigo_pesa_momo.csv')

    momo_types = [
        ("P2P_TRANSFER", 0.35, (5000, 250000)),
        ("CASH_OUT_WAKALA", 0.22, (10000, 500000)),
        ("LIPA_KWA_SIMU_MERCHANT", 0.20, (2000, 150000)),
        ("AIRTIME_TOP_UP", 0.15, (500, 20000)),
        ("BANK_TO_WALLET_DEPOSIT", 0.08, (50000, 1000000))
    ]

    with open(momo_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'transaction_id', 'timestamp', 'sender_msisdn', 'recipient_identifier',
            'channel', 'transaction_type', 'amount_tzs', 'fee_revenue_tzs',
            'cell_id', 'status', 'failure_reason'
        ])

        for i in range(3500):
            tx_id = f"TPESA-{3000000 + i}"
            day = random.randint(0, 6)
            h = random.randint(6, 23)
            tx_dt = base_time + timedelta(days=day, hours=h, minutes=random.randint(0, 59), seconds=random.randint(0, 59))

            sender = random.choice(normal_subs)
            tx_type = random.choices(momo_types, weights=[m[1] for m in momo_types])[0]
            amount = round(random.uniform(tx_type[2][0], tx_type[2][1]), -2)

            channel = "TIGO_PESA_APP" if "Smartphone" in sender['handset_cat'] and random.random() > 0.4 else "USSD_*150*01#"
            tower = next((t for t in TOWERS_SPEC if t['id'] == sender['tower_id']), random.choice(TOWERS_SPEC))

            if tx_type[0] == "AIRTIME_TOP_UP":
                recipient = sender['msisdn']
                fee = 0.0 # Free to user, retail voice airtime credited
            elif tx_type[0] == "LIPA_KWA_SIMU_MERCHANT":
                recipient = f"TILL-{random.randint(500000, 999999)}"
                fee = round(amount * 0.008, 2)
            else:
                recipient = generate_msisdn("TIGO_ON_NET") if random.random() > 0.25 else generate_msisdn("VODACOM")
                fee = round(max(350.0, amount * 0.015), 2)

            is_success = random.random() > 0.018
            status = "SUCCESS" if is_success else "FAILED"
            fail_reason = "NONE" if is_success else random.choice(["INSUFFICIENT_FUNDS", "USSD_TIMEOUT", "PIN_MAX_ATTEMPTS_EXCEEDED", "SYSTEM_BUSY"])

            writer.writerow([
                tx_id, tx_dt.strftime("%Y-%m-%d %H:%M:%S"), sender['msisdn'], recipient,
                channel, tx_type[0], amount, fee if is_success else 0.0, tower['id'],
                status, fail_reason
            ])

    print(" -> Created 3,500 Tigo Pesa mobile money records.")

    # -------------------------------------------------------------------------
    # 6. OPERATOR INTERCONNECT SETTLEMENT RATES TABLE
    # -------------------------------------------------------------------------
    interconnect_file = os.path.join(WORKSPACE_DIR, 'millicom_interconnect_operator_rates.csv')
    with open(interconnect_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'operator_key', 'operator_name', 'voice_inbound_mtr_tzs',
            'voice_outbound_mtr_tzs', 'sms_mtr_tzs', 'standard_retail_rate_tzs'
        ])
        for op_k, op_v in OPERATORS.items():
            writer.writerow([
                op_k, op_v['name'], op_v['in_mtr'], op_v['out_mtr'],
                5.0 if "INTL" not in op_k else 25.0, op_v['retail_rate_tzs_min']
            ])

    print("\n[SUCCESS] Enterprise Telecom CDR Data Ingestion & Extraction completed successfully!")
    print(f"Output files stored in: {WORKSPACE_DIR}")

if __name__ == '__main__':
    generate_data()
