import fitz
import re


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract and clean text from a PDF file uploaded via Streamlit."""
    try:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        pages_text = []
        for page in doc:
            pages_text.append(page.get_text())

        doc.close()

        raw_text = "\n".join(pages_text)

        if not raw_text.strip():
            raise ValueError("no_text")

        return _clean_text(raw_text)

    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {e}") from e


def _clean_text(text: str) -> str:
    """Remove excessive whitespace while preserving meaningful structure."""
    # Collapse 3+ blank lines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing spaces on each line
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()
