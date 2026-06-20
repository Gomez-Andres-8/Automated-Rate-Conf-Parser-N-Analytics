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

    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_image = page.to_image(resolution=dpi).original
            page_text = pytesseract.image_to_string(page_image, lang="eng", config="--psm 3")
            if page_text and page_text.strip():
                text_parts.append(f"--- Page {i} ---\n{page_text.strip()}")

    return "\n\n".join(text_parts).strip()

def parse_fields(raw_text: str) -> dict:
    """
    Parse the raw text and extract relevant fields.
    """
    # Placeholder for actual parsing logic
    return {}

def extract_and_parse_pdf(pdf_path: str) -> dict:
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Could not find {pdf_path}. Please upload rate confirmation PDF."
        )

    print(f"Extracting text from {str(pdf_path).split('/')[-1]}...")

    raw_text = extract_pdf_text(pdf_path)
    extraction_method = "pdfplumber"

    if not raw_text:
        print("No selectable text found. Falling back to OCR...")
        raw_text = ocr_from_pdf(pdf_path)
        extraction_method = "OCR"
        
        if not raw_text:
            raise ValueError(
                "OCR did not return any text. Check that the PDF contains legible scanned images or try a different OCR configuration."
            )

    # fields = some function(raw_text)
    fields = {}

    return {
        "raw_text" : raw_text,
        "extraction_method" : extraction_method,
        "fields" : fields
    }


if __name__ == "__main__":
    extract_and_parse_pdf()