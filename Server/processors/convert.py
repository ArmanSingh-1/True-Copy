import base64
import io
from PIL import Image

# Convert an image file to PNG format
def convert_image_to_png(input_image_path: str, output_image_path: str) -> str:
    image = Image.open(input_image_path)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.save(output_image_path, format="PNG")
    return output_image_path

# Encode an image file as a Base64 string
def encode_image_to_base64(input_image_path: str) -> str:
    with open(input_image_path, "rb") as image_file:
        image_bytes = image_file.read()
    
    base64_string = base64.b64encode(image_bytes).decode("utf-8")
    return base64_string

# Decode a Base64 string and save it as a PNG image
def decode_base64_to_image(base64_string: str, output_image_path: str) -> str:
    image_bytes = base64.b64decode(base64_string)
    image_stream = io.BytesIO(image_bytes)

    image = Image.open(image_stream)
    
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    image.save(output_image_path, format="PNG")
    return output_image_path