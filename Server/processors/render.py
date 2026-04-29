from PIL import Image, ImageDraw, ImageFont
import textwrap

# Clears the text in the textbox in the image
def clear_text_box(draw: ImageDraw.ImageDraw, region: dict, padding: int = 10, fill_color: str = "white") -> None:
    # Calculates the coordinates of the textbox
    x = max(0, region["x"] - padding)
    y = max(0, region["y"] - padding)
    w = region["width"] + (padding * 2)
    h = region["height"] + (padding * 2)
    
    # Draws the rectangle
    draw.rectangle([x, y, x + w, y + h], fill=fill_color)


# Writes the translated text in the image
def write_translated_text(draw: ImageDraw.ImageDraw, region: dict, text: str, font_path: str = "arial.ttf", font_size: int = 16) -> None:
    # Loads the font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Calculates the coordinates of the textbox
    x, y = region["x"], region["y"]
    w, h = region["width"], region["height"]
    
    # Calculates the average character width
    avg_char_width = font_size * 0.6
    max_chars_per_line = max(1, int(w / avg_char_width))
    wrapped_text = textwrap.fill(text, width=max_chars_per_line)
    
    # Writes the text in the image
    draw.multiline_text((x + 2, y + 2), wrapped_text, fill="black", font=font, align="center")


# Renders the translated image
def render_translated_image(image_path: str, output_path: str, translations: list[dict]) -> str:
    # Opens the image
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Iterates through the translations
    for item in translations:
        region = item.get("region")
        text = item.get("text")
        # Clears the text in the textbox and writes the translated text
        if region and text:
            clear_text_box(draw, region, padding=12)
            write_translated_text(draw, region, text)
            
    # Saves the image
    img.save(output_path, format="PNG")
    return output_path