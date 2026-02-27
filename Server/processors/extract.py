import torch
from PIL import Image
from manga_ocr import MangaOcr

# Initializes the Manga-OCR Engine
def initialize_ocr() -> MangaOcr:
    return MangaOcr()

# Extracts text from the merged dialogue regions
def extract_text(input_image_path: str, ocr_engine: MangaOcr) -> str:
    image = Image.open(input_image_path).convert("RGB")

    # Extracts text from the image
    extracted_text = ocr_engine(image)
    return extracted_text.strip()