from pdfrw import PdfReader

TEMPLATE_PDF = "Sample-Fillable-PDF.pdf"
pdf = PdfReader(TEMPLATE_PDF)

print("PDF form fields:")
for page in pdf.pages:
    if "/Annots" in page:
        for annot in page["/Annots"]:
            if annot.get("/T"):
                field_name = annot["/T"][1:-1]  # remove parentheses
                print(field_name)
