import PyPDF2
import docx
import os
import asyncio
from urllib.parse import urlsplit
from io import BytesIO

def get_filename_from_url(url=None):
    if url is None:
        return None
    urlpath = urlsplit(url).path
    return os.path.basename(urlpath)

async def extract_text_from_pdf(uploaded_file):
    try:
        loop = asyncio.get_event_loop()
        if isinstance(uploaded_file, bytes):
            uploaded_file = BytesIO(uploaded_file)
        reader = await loop.run_in_executor(None, PyPDF2.PdfReader, uploaded_file)
        pdf_text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
        return pdf_text
    except Exception as e:
        return f"Error: {e}"

async def extract_text_from_docx_or_doc(uploaded_file, file_extension):
    try:
        loop = asyncio.get_event_loop()
        if isinstance(uploaded_file, bytes):
            uploaded_file = BytesIO(uploaded_file)
        if file_extension == 'docx':
            docx_text = await loop.run_in_executor(None, docx.Document, uploaded_file)
        else:
            docx_text = await loop.run_in_executor(None, docx.Document, uploaded_file)
        full_text = []
        for paragraph in docx_text.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"Error: {e}"