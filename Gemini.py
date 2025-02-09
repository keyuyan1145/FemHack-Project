import google.generativeai as genai
import os
import fitz  # PyMuPDF for PDF handling

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def ask_gemini_about_pdf(pdf_path, question):
    """Asks Gemini a question about the content of a PDF."""

    pdf_text = extract_text_from_pdf(pdf_path)

    if pdf_text is None:
        return "Could not extract text from the PDF."

    prompt = f"Here is the content of a PDF:\n\n{pdf_text}\n\nQuestion:\n{question}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error asking Gemini: {e}"

def main():
    pdf_file_path = "Manual.pdf"

    questions = [
        "I just shared a manufacturing installation manual for a product with you. If you understand the following information from the manual, answer yes. Here is the product to be installed (with exact product name and model number if provided, required tools with details, cautious items during installation, and step by step process."
    ]

    for question in questions:
        answer = ask_gemini_about_pdf(pdf_file_path, question)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()