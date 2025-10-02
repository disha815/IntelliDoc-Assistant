from docling.document_converter import DocumentConverter

def extract_text_with_docling(pdf_path):
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    text = result.document.export_to_markdown() if result.document else ""
    return text
