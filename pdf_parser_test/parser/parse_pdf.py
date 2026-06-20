from pathlib import Path
import pdfplumber


def extract_pdf_text(pdf_path: Path) -> str:
    """
    Extract text from each page of a PDF and return one combined string.
    """
    text_parts = []

    with pdfplumber.open(pdf_path) as pdf:
        
        # Go through each page and extract text
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()

            # Some pages may return None if no extractable text is found
            if page_text:

                # Format:
                # --- Page 1 ---
                # Text in page 1
                text_parts.append(f"--- Page {i} ---\n{page_text}")

    # Double indentation as visual aid for next page
    return "\n\n".join(text_parts).strip()



def main():
    # This path will eventually become uploaded file
    pdf_path = Path("data/TQL_RateConf - 36965517.pdf")
    output_path = Path("data/TQL_RateConf - 36965517_extracted.txt")

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Could not find {pdf_path}. Put your resume PDF in the data folder."
        )

    print(f"Extracting text from {str(pdf_path).split("/")[-1]}...")

    pdf_text = extract_pdf_text(pdf_path)

    if not pdf_text:
        raise ValueError(
            "No selectable text found. This rate confirmation may be scanned or image-based and may require OCR."
        )

    output_path.write_text(pdf_text, encoding="utf-8")
    print(f"Saved extracted text to {output_path}")


if __name__ == "__main__":
    main()