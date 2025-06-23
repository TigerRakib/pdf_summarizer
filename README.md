
# 🧾 ADT-1 PDF Parser & Summarizer using Python + LLM

This python script extracts structured data and embedded attachments from a PDF which is ADT-1 (filed under the Companies Act) form, summarizes it using a local LLM (via Ollama), and saves both Json_Data and human-friendly text summaries.

---

## 🚀 Features

- ✅ Extracts form fields (CIN, company name, auditor details, etc.) from the ADT-1_type.pdf using AcroForm widgets.
- 📁 Extracts embedded PDF attachments (e.g., consent letter, board resolution) into a local `attachments/` folder.
- Generates:
  - A structured JSON file (`output.json`)
  - A readable summary.txt file (`summary.txt`)
- 🤖 Uses **Ollama** to generate natural language summaries (e.g., with Mistral or TinyLLaMA).

---

## 📂 Project Structure

```
├── extractor.py               # Main script
├── Form ADT-1-29092023_signed.pdf  # Input form
├── output.json                # Extracted structured data
├── summary.txt                # Final generated summary
├── attachments/               # Extracted embedded PDFs
```

---

## How It Works

1. Reads and extracts fields from the PDF's AcroForm.
2. Maps the raw form data into a dictionary and converts it into a Json file.
3. Summarizes it using `ollama run mistral`.
4. Extracts and summarizes the embedded PDFs (attachments).
5. Combines both the structured json data and embedded pdfs summary and returns a human-friedly AI generated summary.

---

## ⚙️ Requirements

Install Python libraries:

```bash
pip install pymupdf
```

Install and configure [Ollama](https://ollama.com):

```bash
ollama pull mistral
# or
ollama pull tinyllama
```

Ensure Ollama is running in the background.
```bash
ollama --version

```
---

## ▶️ How to Run

Place your ADT-1 PDF in the project folder and replace the file_path variable in extractor.py then hit RUN:

```bash
python extractor.py
```

This will:
- Create `output.json`
- Create `attachments/` with extracted PDFs
- Create `summary.txt` containing:
  - AI summary of the structured json data
  - AI summary of the attachments

---

## 📝 Output Example

**summary.txt:**
```
ALUPA FOODS PRIVATE LIMITED has reappointed M/s XYZ & Co. as its statutory auditor, effective from 29 September 2023. The appointment was disclosed via Form ADT-1, with supporting documents including a signed consent letter, board resolution, and intimation letter confirming compliance with Companies Act regulations.
```

---

## 💡 Customization

- Change the Ollama model: `"mistral"` → `"tinyllama"` or any other supported model.
- Extend the `extract_adt1_from_dict()` function to include more fields if needed.

---

## 🛠️ Troubleshooting

- If no form fields are extracted, ensure the PDF is not scanned/image-based.
- If attachments don’t extract, they might have corrupt metadata — the script skips such cases gracefully.
- If you see `UnicodeEncodeError`, it's usually due to malformed embedded file names — these are now safely skipped.

---

## 📜 License

This project is open-source and free to use for educational or internal use cases.

---

## 👤 Author

Made by Nazrul Islam Rakib — Problem solving and challenges handling enthusiast.
