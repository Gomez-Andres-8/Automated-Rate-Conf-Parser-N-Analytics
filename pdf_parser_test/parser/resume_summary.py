from pathlib import Path

def normalize_line(line: str) -> str:
    """
    Strip whitespace and collapse repeated spaces.
    """
    return " ".join(line.lower().strip().split())

def main():
    txt_path = Path("data/resume_text.txt")

    key_words = ["education", "summary", "coursework", "skills"]

    sections = {
        "header": [],
        "education": [],
        "summary": [],
        "coursework": [],
        "skills": [],
        "other": []
    }

    current_section = "header"

    with open(txt_path, "r") as txt:
        for line in txt:
            clean_line = normalize_line(line)

            # skip blank lines
            if not clean_line:
                continue

            # if the whole line is a section header, switch sections
            if clean_line in key_words:
                current_section = clean_line
                continue

            # otherwise store the line under the current section
            sections[current_section].append(line.strip())

    for section, lines in sections.items():
        print(f"\n--- {section.upper()} ---")
        for item in lines:
            print(item)



if __name__ == "__main__":
	main()