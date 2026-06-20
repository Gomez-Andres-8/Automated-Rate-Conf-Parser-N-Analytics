from pathlib import Path
import pdfplumber
import pytesseract


def extract_pdf_text(pdf_path: Path) -> str:
    """
    Extract text from each page of a PDF and return one combined string.
    """
    text_parts = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(f"--- Page {i} ---\n{page_text.strip()}")

    return "\n\n".join(text_parts).strip()


def ocr_from_pdf(pdf_path: Path, dpi: int = 300) -> str:
    """
    Perform OCR on each page of a PDF and return a combined string.
    """
    if pytesseract is None:
        raise ImportError(
            "pytesseract is required for OCR. Install it with `pip install pytesseract` "
            "and ensure Tesseract OCR is installed on your system. `brew install tesseract` on macOS."
        )

    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_image = page.to_image(resolution=dpi).original
            page_text = pytesseract.image_to_string(page_image, lang="eng", config="--psm 3")
            if page_text and page_text.strip():
                text_parts.append(f"--- Page {i} ---\n{page_text.strip()}")

    return "\n\n".join(text_parts).strip()

def main():
    # This path will eventually become an uploaded file
    pdf_path = Path("data/TA_RateConf.pdf")
    output_path = Path("data/TA_RateConf_extracted.txt")

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Could not find {pdf_path}. Put rate confirmation PDF in the data folder."
        )

    print(f"Extracting text from {str(pdf_path).split('/')[-1]}...")

    pdf_text = extract_pdf_text(pdf_path)

    if not pdf_text:
        print("No selectable text found. Falling back to OCR...")
        pdf_text = ocr_from_pdf(pdf_path)

        if not pdf_text:
            raise ValueError(
                "OCR did not return any text. Check that the PDF contains legible scanned images or try a different OCR configuration."
            )

    output_path.write_text(pdf_text, encoding="utf-8")
    print(f"Saved extracted text to {output_path}")


if __name__ == "__main__":
    main()