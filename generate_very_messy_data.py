"""
Enterprise Raw Data Synthesizer: Very Messy Telecommunications & Fintech Dataset
================================================================================
Generates intentionally chaotic, real-world raw datasets to demonstrate advanced
data cleaning, normalization, regex parsing, and multi-format conversions.

Issues Injected:
1. Inconsistent Phone Numbers (E.164, local, hyphens, brackets, alphabetic noise, missing prefixes).
2. Multi-Format Timestamps (ISO, US mm/dd/yyyy, UK dd/mm/yyyy, Unix epoch, named months, 'yesterday').
3. Dirty Currencies & Numbers (commas, currency symbols, trailing signs, negative spaces, 'FREE', nulls).
4. Corrupted Text & Encodings (BOM, zero-width spaces, mixed casing, typos, escaped quotes).
5. Duplicate Records (exact duplicates, near-duplicates with conflicting timestamps).
6. Nested Irregular JSON (mixed types, missing fields, stringified numbers, unescaped payloads).
"""

import csv
import json
import random
import time
import os

SEED = 42
random.seed(SEED)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MESSY_CSV_PATH = os.path.join(OUTPUT_DIR, "raw_messy_telecom_data.csv")
MESSY_JSON_PATH = os.path.join(OUTPUT_DIR, "raw_messy_customer_events.json")

def generate_messy_phone(base_num):
    """Injects 10+ real-world phone number corruptions."""
    choice = random.random()
    s = str(base_num)  # e.g., 714011243
    if choice < 0.15:
        return f"+255 {s[:3]} {s[3:6]} {s[6:]}"  # +255 714 011 243
    elif choice < 0.30:
        return f"0{s[:3]}-{s[3:6]}-{s[6:]}"     # 0714-011-243
    elif choice < 0.42:
        return f"255{s}"                         # 255714011243
    elif choice < 0.52:
        return f"0{s}"                           # 0714011243
    elif choice < 0.62:
        return f"+255(0){s}"                     # +255(0)714011243
    elif choice < 0.72:
        return f"tel:+255-{s[:3]}-{s[3:]}"       # tel:+255-714-011243
    elif choice < 0.82:
        return f"  {s}  "                         # leading/trailing spaces
    elif choice < 0.90:
        return f"+255/{s[:3]}/{s[3:]}"           # slashes
    elif choice < 0.96:
        return "N/A"                             # missing string
    else:
        return "0000000000"                      # invalid dummy zero

def generate_messy_timestamp():
    """Injects chaotic timestamp formats and corrupted strings."""
    choice = random.random()
    # Base timestamp: Oct-Nov 2023
    base_epoch = 1699100000 + random.randint(0, 86400 * 30)
    struct_t = time.gmtime(base_epoch)

    if choice < 0.25:
        # Standard ISO-like with space
        return time.strftime("%Y-%m-%d %H:%M:%S", struct_t)
    elif choice < 0.45:
        # US format with AM/PM
        return time.strftime("%m/%d/%Y %I:%M %p", struct_t)
    elif choice < 0.60:
        # UK/European day first
        return time.strftime("%d-%m-%Y %H:%M:%S", struct_t)
    elif choice < 0.72:
        # Textual month
        return time.strftime("%b %d, %Y %H:%M", struct_t)
    elif choice < 0.85:
        # Raw Unix epoch integer as string
        return str(base_epoch)
    elif choice < 0.92:
        # ISO with erratic timezone
        return time.strftime("%Y-%m-%dT%H:%M:%S+03:00", struct_t)
    elif choice < 0.97:
        return "2023/11/04"  # Date only without time
    else:
        return "UNKNOWN_TIME"

def generate_messy_amount():
    """Injects dirty currency strings, commas, erratic decimals, and non-numeric labels."""
    val = round(random.uniform(500, 150000), 2)
    choice = random.random()
    if choice < 0.25:
        return f"TZS {val:,.2f}/="
    elif choice < 0.45:
        return f"{val:,.2f}"
    elif choice < 0.60:
        usd = round(val / 2500.0, 2)
        return f"$ {usd:,.2f} USD"
    elif choice < 0.72:
        return f"  {val:.0f}  "
    elif choice < 0.82:
        return f"-{val:,.2f}" if random.random() < 0.3 else f"{val:,.4f}"
    elif choice < 0.90:
        return "FREE"
    elif choice < 0.96:
        return "NaN"
    else:
        return ""

def generate_messy_status():
    """Injects inconsistent casing, typos, whitespace, and invisible characters."""
    statuses = [
        "ACTIVE", "Active", "  active  ", "actve", "ACTV",
        "SUSPENDED", "Suspended", "suspnded",
        "TERMINATED", "Terminated", "Term",
        "CHURNED", "churn",
        "PENDING_KYC", "pending", "Pending_Kyc\u200b", # zero-width space
        "UNKNOWN", "null", ""
    ]
    return random.choice(statuses)

def generate_messy_location():
    """Injects messy city/region names with dirty characters."""
    locations = [
        "Dar es Salaam", "DAR ES SALAAM", "dar-es-salaam", "  Dar es Salaam  ",
        "Arusha", "ARUSHA", "Arusha (CBD)", "Arusha\ufeff", # UTF-8 BOM
        "Mwanza", "mwanza", "Mwanza Rock City",
        "Dodoma", "DODOMA (Capital)", "Dodoma ",
        "Zanzibar", "Stone Town, Zanzibar", "ZNZ",
        "Mbeya", "Morogoro", "Tanga", "N/A", ""
    ]
    return random.choice(locations)

def create_messy_csv(num_rows=2500):
    """Generates the messy CSV with unescaped commas, messy types, and injected duplicates."""
    headers = [
        "record_id", "subscriber_msisdn", "recipient_number", "event_timestamp",
        "transaction_type", "amount_paid", "service_status", "location_cell",
        "session_duration_sec", "network_layer", "user_agent_device", "notes_field"
    ]

    devices = [
        'Samsung Galaxy A14; Android 13', 'iPhone 13,2 (iOS 16.5)', 'Tecno Spark 10 Pro',
        'Transsion Infinix Hot 30', 'Huawei P40 Lite', 'Nokia 105 (Feature Phone)', 'Unknown'
    ]

    tx_types = ['VOICE_CALL', 'DATA_RECHARGE', 'TIGO_PESA_CASH_IN', 'TIGO_PESA_CASH_OUT', 'BUNDLE_PURCHASE', 'SMS_PACK']
    networks = ['4G LTE', '4G', '5G NR', '3G WCDMA', '2G GSM', 'LTE-A', 'unknown']

    records = []
    base_subscribers = [714000000 + i * 137 for i in range(250)]

    for i in range(1, num_rows + 1):
        sub_base = random.choice(base_subscribers)
        recip_base = random.choice(base_subscribers)

        rec = {
            "record_id": f"REC-{100000 + i}",
            "subscriber_msisdn": generate_messy_phone(sub_base),
            "recipient_number": generate_messy_phone(recip_base),
            "event_timestamp": generate_messy_timestamp(),
            "transaction_type": random.choice(tx_types),
            "amount_paid": generate_messy_amount(),
            "service_status": generate_messy_status(),
            "location_cell": generate_messy_location(),
            "session_duration_sec": str(random.choice([-15, 0, 45, 120, 360, "30s", "02:15", "N/A", 1800])),
            "network_layer": random.choice(networks),
            "user_agent_device": random.choice(devices),
            "notes_field": random.choice([
                "VIP Subscriber, priority routing",
                "Flagged for KYC update; verified by agent",
                "USSD session timeout, retry OK",
                'Customer stated: "Cannot connect to 4G in Posta area, please help"',
                "Standard call; cell handover success",
                "",
                "None"
            ])
        }
        records.append(rec)

    # Inject 8% exact and near-duplicates
    num_dupes = int(num_rows * 0.08)
    for _ in range(num_dupes):
        source_rec = random.choice(records)
        dupe_rec = dict(source_rec)
        if random.random() < 0.5:
            # Exact duplicate
            records.append(dupe_rec)
        else:
            # Near duplicate with slightly corrupted timestamp or status
            dupe_rec["event_timestamp"] = generate_messy_timestamp()
            records.append(dupe_rec)

    # Shuffle to scatter duplicates
    random.shuffle(records)

    with open(MESSY_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    print(f"[OK] Generated {len(records):,} very messy CSV rows at: {MESSY_CSV_PATH}")
    return len(records)

def create_messy_json(num_events=1000):
    """Generates deeply nested, irregular JSON with schema drifts."""
    events = []
    base_subscribers = [714000000 + i * 211 for i in range(150)]

    for i in range(1, num_events + 1):
        sub = random.choice(base_subscribers)
        is_deeply_nested = random.random() < 0.65

        event = {
            "event_id": f"EVT_{200000 + i}",
            "msisdn_raw": generate_messy_phone(sub),
            "created_at_raw": generate_messy_timestamp(),
            "status_code": generate_messy_status()
        }

        if is_deeply_nested:
            event["payload"] = {
                "financials": {
                    "raw_fee": generate_messy_amount(),
                    "currency_guess": random.choice(["TZS", "USD", None]),
                    "tax_bracket": random.choice(["18%", 0.18, "none", None])
                },
                "telemetry": {
                    "cell_id": random.choice(["DAR_POSTA_01", "ARU_CBD_04", "DO_CAP_02", None]),
                    "signal_dbm": random.choice([-85, "-92 dBm", -110, "poor", None]),
                    "packet_loss_pct": random.choice(["0.5%", 0.005, "0", None])
                },
                "device_info": {
                    "brand": random.choice(["Samsung", "Apple", "Transsion", "UNKNOWN"]),
                    "imei": random.choice([f"35{random.randint(1000000000000, 9999999999999)}", "INVALID", None])
                }
            }
        else:
            # Flattened / schema drift variant
            event["flat_fee"] = generate_messy_amount()
            event["signal"] = random.choice([-88, -105, "N/A"])
            event["device"] = random.choice(["Samsung A14", "iPhone", None])

        events.append(event)

    with open(MESSY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    print(f"[OK] Generated {len(events):,} messy nested JSON records at: {MESSY_JSON_PATH}")
    return len(events)

def generate_all_messy_data():
    t0 = time.time()
    csv_count = create_messy_csv(2500)
    json_count = create_messy_json(1000)
    print(f"[COMPLETE] Messy Data Synthesis took {time.time() - t0:.2f}s | {csv_count} CSV records + {json_count} JSON records")

if __name__ == "__main__":
    generate_all_messy_data()
