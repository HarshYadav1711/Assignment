"""
PDF extraction utility.
Handles downloading and extracting text from PDF files.
"""
import requests
import io
import logging
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def download_pdf_from_gdrive(url):
    """
    Download PDF from Google Drive.
    Converts Google Drive share URL to direct download URL.
    """
    try:
        # Extract file ID from Google Drive URL
        file_id = url.split('/d/')[1].split('/')[0]
        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        response = requests.get(direct_url, allow_redirects=True)
        response.raise_for_status()
        
        return io.BytesIO(response.content)
    except Exception as e:
        logger.error(f"Failed to download PDF: {e}")
        raise

def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF file.
    Returns: list of page texts
    """
    try:
        reader = PdfReader(pdf_file)
        pages = []
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                pages.append({
                    'page': page_num + 1,
                    'text': text
                })
        
        logger.info(f"Extracted {len(pages)} pages from PDF")
        return pages
    except Exception as e:
        logger.error(f"Failed to extract PDF text: {e}")
        raise

def extract_pdf_from_url(url):
    """
    Download and extract text from PDF URL.
    Returns: list of page texts
    """
    pdf_file = download_pdf_from_gdrive(url)
    return extract_text_from_pdf(pdf_file)

