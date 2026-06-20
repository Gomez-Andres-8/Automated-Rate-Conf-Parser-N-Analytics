from pathlib import Path
import pdfplumber


def extract_resume_text(pdf_path: Path) -> str:
    """
    Extract text from each page of a PDF resume and return one combined string.
    """
    text_parts = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()

            # Some pages may return None if no extractable text is found
            if page_text:
                text_parts.append(f"--- Page {i} ---\n{page_text}")

    return "\n\n".join(text_parts).strip()


def main():
    # Change this filename to match your actual resume PDF name
    pdf_path = Path("data/resume.pdf")
    output_path = Path("data/resume_text.txt")

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Could not find {pdf_path}. Put your resume PDF in the data folder."
        )

    resume_text = extract_resume_text(pdf_path)

    if not resume_text:
        raise ValueError(
            "No text was extracted from the PDF. Your resume may be image-based instead of text-based."
        )

    output_path.write_text(resume_text, encoding="utf-8")
    print(f"Saved extracted text to {output_path}")


if __name__ == "__main__":
    main()