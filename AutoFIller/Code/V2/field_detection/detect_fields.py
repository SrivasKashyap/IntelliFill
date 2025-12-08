import json
import os
from openai import OpenAI
from pdf2image import convert_from_path
from openpyxl import Workbook
import base64

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# -------------------------
# OpenAI CLIENT
# -------------------------
client = OpenAI(api_key="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")
MODEL = "gpt-4.1"

# -------------------------
# PATHS
# -------------------------
IMG_BLANK = "data/images/ticket_blank.png"
IMG_FILLED = "data/images/ticket_filled.png"

TEMPLATE_BLANK = "data/templates/ticket_blank.pdf"
TEMPLATE_FILLED = "data/templates/ticket_filled.pdf"

OUTPUT_JSON = "data/fields/fields.json"
OUTPUT_EXCEL = "data/excel/fields.xlsx"


# -------------------------
# Ensure folders exist
# -------------------------
os.makedirs("data/images", exist_ok=True)
os.makedirs("data/excel", exist_ok=True)
os.makedirs("data/fields", exist_ok=True)
os.makedirs("data/templates", exist_ok=True)


# -------------------------
# Convert PDF → PNG
# -------------------------
def convert_pdfs():
    print("[🖼️] Converting PDFs...")

    blank_imgs = convert_from_path(TEMPLATE_BLANK)
    filled_imgs = convert_from_path(TEMPLATE_FILLED)

    blank_imgs[0].save(IMG_BLANK)
    filled_imgs[0].save(IMG_FILLED)

    print("[✔] Images saved.")


# -------------------------
# Ask OpenAI to detect fields
# -------------------------
def ask_model_for_fields():
    print("[🧠] Detecting fields...")

    blank_b64 = encode_image(IMG_BLANK)
    filled_b64 = encode_image(IMG_FILLED)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Compare the blank and filled ticket. Extract only the differences. "
                    "Return strict JSON array of objects: {text, suggested_field, x, y}."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{blank_b64}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{filled_b64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content



# -------------------------
# JSON Repair Helper
# -------------------------
def repair_json(bad_json):
    print("[🔧] Attempting JSON repair...")

    try:
        fixed = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system",
                 "content": "Fix the broken JSON and return ONLY valid JSON."},
                {"role": "user", "content": bad_json}
            ]
        )
        return fixed.choices[0].message.content
    except:
        return None


# -------------------------
# Save Excel
# -------------------------
def save_excel(fields):
    print("[📘] Creating Excel sheet...")

    wb = Workbook()
    ws = wb.active
    ws.title = "Fields"

    ws.append(["Field Name", "Extracted Text", "X", "Y"])

    for f in fields:
        ws.append([
            f.get("suggested_field", ""),
            f.get("text", ""),
            f.get("x", ""),
            f.get("y", "")
        ])

    wb.save(OUTPUT_EXCEL)
    print("[✔] Excel saved:", OUTPUT_EXCEL)


# -------------------------
# Save JSON
# -------------------------
def save_json(fields):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(fields, f, indent=4)
    print("[✔] JSON saved:", OUTPUT_JSON)


# -------------------------
# Main Detection Flow
# -------------------------
def detect_fields():
    convert_pdfs()
    raw = ask_model_for_fields()

    try:
        data = json.loads(raw)
    except:
        print("❌ Invalid JSON from model:")
        print(raw)

        repaired = repair_json(raw)
        if repaired:
            try:
                data = json.loads(repaired)
                print("[✔] JSON repair successful.")
            except:
                print("❌ JSON repair failed.")
                return
        else:
            print("❌ No repair possible.")
            return

    save_json(data)
    save_excel(data)
    print("[🎉] Field detection complete!")


if __name__ == "__main__":
    detect_fields()
