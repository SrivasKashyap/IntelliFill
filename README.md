# IntelliFill

**AI-Powered Template Detection & Auto-Filling Engine**

IntelliFill is an intelligent document automation system that analyzes any template—PDFs, images, or scanned forms—detects input fields, and automatically fills them with user-provided data. It removes repetitive manual work and enables fast, accurate, and scalable document generation for tickets, forms, receipts, certificates, and more.

---

## Features

* **Automatic Field Detection**
  Uses AI to analyze template layout and identify text boxes, labels, and input fields.

* **Multi-Format Support**
  Works with PDFs, PNG/JPG images, scanned documents, and custom templates.

* **Smart Auto-Filling**
  Takes structured input (JSON, form data, API) and fills all fields while preserving original formatting.

* **Template-Agnostic**
  No predefined structure required—just drop a template and IntelliFill maps everything automatically.

* **Image & PDF Rendering**
  Converts PDFs into images for processing and reconstructs the final filled output with high accuracy.

* **Extensible Pipeline**
  Easily integrate into backend systems, automation scripts, or workflow tools.

---

## Project Structure

```
/templates          # Input templates (PDF or images)
/data               # Intermediate files, converted images, etc.
/field_detection    # AI-based field extraction logic
/output             # Final auto-filled documents
/main.py            # Entry point for running IntelliFill
```

---

## Installation

```bash
git clone https://github.com/your-username/intellifill.git
cd intellifill
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

(Windows PowerShell)

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

---

## Usage

### **1. Add templates**

Place your templates (PDF or images) inside:

```
/templates
```

### **2. Run field detection**

```bash
python field_detection/detect_fields.py
```

This extracts all input fields from the template.

### **3. Auto-fill with your data**

Pass your data to the filler script:

```bash
python autofill.py --input data.json
```

### **4. Output**

All completed documents will appear in:

```
/output
```

---

## Example Workflow

1. Upload a blank ticket template.
2. IntelliFill detects fields like: *Name, Event, Seat, Date, QR zone, Signature box*.
3. Provide JSON with values.
4. The system outputs a fully filled ticket identical to the original layout.

---

## Why IntelliFill?

* Saves hours of manual data entry
* Reduces errors and inconsistencies
* Scales effortlessly for bulk generation
* Works with **any document**, not just predefined forms

---

## Contributing

PRs and feature ideas are welcome! Feel free to open issues for suggestions or bug reports.

---

## License

MIT License

---

