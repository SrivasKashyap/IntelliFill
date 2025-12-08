import json
from pathlib import Path
from openpyxl import Workbook

FIELDS_JSON = Path("data/mappings/fields_list.json")
OUTPUT_XLSX = Path("data/excel/template.xlsx")

def create_excel():
    print("[📄] Reading detected fields...")

    if not FIELDS_JSON.exists():
        raise FileNotFoundError("❌ fields_list.json not found. Run detect_fields.py first.")

    # Read JSON safely (handles BOM, whitespace, etc)
    with open(FIELDS_JSON, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            raise ValueError("❌ fields_list.json is empty.")
        fields = json.loads(content)

    # Extract only the suggested_field values → unique
    unique_fields = []
    for item in fields:
        field_name = item.get("suggested_field")
        if field_name and field_name not in unique_fields:
            unique_fields.append(field_name)

    if not unique_fields:
        raise ValueError("❌ No field names found in fields_list.json.")

    print(f"[✔] Found {len(unique_fields)} fields.")

    # Create Excel
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Ticket Data"

    # Write headings
    for i, col in enumerate(unique_fields, start=1):
        sheet.cell(row=1, column=i, value=col)

    OUTPUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT_XLSX)

    print(f"[✔] Excel template created: {OUTPUT_XLSX}")
    print("[→] Columns:")
    for col in unique_fields:
        print("   -", col)

if __name__ == "__main__":
    create_excel()
