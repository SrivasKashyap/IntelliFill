import os
import pandas as pd
from pdfrw import PdfReader, PdfWriter, PdfName, PdfString

TEMPLATE_PDF = "Sample-Fillable-PDF.pdf"
EXCEL_FILE = "form_data.xlsx"
OUTPUT_FOLDER = "output_pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df = pd.read_excel(EXCEL_FILE)

# Map PDF field names to Excel columns
pdf_field_map = {
    "Name": "Name",
    "Dropdown2": "Dropdown",
    "Option 1": "Option1",
    "Option 2": "Option2",
    "Option 3": "Option3"
}

for idx, row in df.iterrows():
    pdf = PdfReader(TEMPLATE_PDF)
    pdf.Root.AcroForm.update({PdfName('NeedAppearances'): True})

    for page in pdf.pages:
        if "/Annots" in page:
            for annot in page["/Annots"]:
                if annot.get("/T"):
                    field_name = annot["/T"][1:-1]  # remove parentheses
                    if field_name in pdf_field_map:
                        excel_column = pdf_field_map[field_name]
                        value = str(row[excel_column])
                        annot.update({
                            PdfName("/V"): PdfString.encode(value),
                            PdfName("/AP"): None
                        })

    output_file = os.path.join(OUTPUT_FOLDER, f"{row['Name'].replace(' ','_')}_form.pdf")
    PdfWriter(output_file, trailer=pdf).write()
    print(f"Generated: {output_file}")

print("🎉 Done! Check the output_pdfs folder.")
