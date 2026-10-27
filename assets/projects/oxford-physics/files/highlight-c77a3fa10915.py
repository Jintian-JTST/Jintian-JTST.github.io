import fitz
import pandas as pd
from pathlib import Path
from reportlab.platypus import (
SimpleDocTemplate,
Image,
PageBreak
)
from reportlab.lib.pagesizes import A4

ROOT = Path(r"./data/resource")

OUT_DIR = ROOT / "SelectedProblems"
IMG_DIR = OUT_DIR / "pages"

OUT_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)

records = []
saved_pages = set()

for pdf_file in ROOT.rglob("*.pdf"):


    print("Processing:", pdf_file.name)

    try:

        doc = fitz.open(pdf_file)

        for page_num in range(len(doc)):

            page = doc[page_num]

            annot = page.first_annot

            has_highlight = False

            while annot:

                if annot.type[0] == 8:
                    has_highlight = True
                    break

                annot = annot.next

            if not has_highlight:
                continue

            key = (
                pdf_file.stem,
                page_num
            )

            if key in saved_pages:
                continue

            saved_pages.add(key)

            image_name = (
                f"{pdf_file.stem}_page{page_num+1}.png"
            )

            image_path = IMG_DIR / image_name

            pix = page.get_pixmap(
                matrix=fitz.Matrix(4,4),
                alpha=False
            )

            pix.save(str(image_path))

            records.append({
                "file": pdf_file.stem,
                "page": page_num + 1,
                "image": image_name
            })

        doc.close()

    except Exception as e:
        print(pdf_file.name, e)


df = pd.DataFrame(records)

csv_path = OUT_DIR / "selected_pages.csv"

df.to_csv(
csv_path,
index=False,
encoding="utf-8-sig"
)

print()
print("Pages saved:", len(df))

pdf_path = OUT_DIR / "SelectedProblems.pdf"

doc = SimpleDocTemplate(
str(pdf_path),
pagesize=A4
)

import img2pdf
from pathlib import Path

pdf_path = OUT_DIR / "SelectedProblems.pdf"

image_files = [
    str(IMG_DIR / row["image"])
    for row in records
]

with open(pdf_path, "wb") as f:
    f.write(img2pdf.convert(image_files))

print()
print("Created:")
print(pdf_path)
