from PIL import Image, ImageDraw, ImageFont
import os
import json


TEMPLATE_PATH = "template.jpg"  
FONT_BOLD_PATH = "fonts/Roboto-Bold.ttf"
FONT_REGULAR_PATH = "fonts/Roboto-Regular.ttf"
OUTPUT_DIR = "output_slides"
CONFIG_PATH = "slides_config.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def wrap_text(text, font, max_width, draw):
    """Wrap text based on width"""
    lines = []
    words = text.split()
    line = ''
    for word in words:
        test_line = line + word + " "
        # Get bounding box instead of textsize
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())
    return "\n".join(lines)

def create_slide(index, title, desc):
    image = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_title = ImageFont.truetype(FONT_BOLD_PATH, slide.get("font_title_size", 60))
    font_desc = ImageFont.truetype(FONT_REGULAR_PATH, slide.get("font_desc_size", 32))
    font_number = ImageFont.truetype(FONT_BOLD_PATH, 100)

    # Positioning Config 
    title_x, title_y = slide.get("title_pos", [100, 200])
    desc_x, desc_y = slide.get("desc_pos", [100, 400])
    max_text_width = image.width - 2 * 100 

    # Slide Number (e.g. 01, 02...)
    slide_number = f"{index+1:02}"
    draw.text((image.width - 180, 30), slide_number, font=font_number, fill=(30, 30, 30))

    # Wrapped Text
    wrapped_title = wrap_text(slide["title"], font_title, max_text_width, draw)
    wrapped_desc = wrap_text(slide["desc"], font_desc, max_text_width, draw)

    # Draw
    draw.text((title_x, title_y), wrapped_title, font=font_title, fill=(255, 199, 44))
    draw.text((desc_x, desc_y), wrapped_desc, font=font_desc, fill="white")


    # Save
    output_path = os.path.join(OUTPUT_DIR, f"slide_{index+1}.jpg")
    image.save(output_path)
    print(f"✅ Saved: {output_path}")

# Generate All Slides
with open(CONFIG_PATH, "r") as f:
    slides = json.load(f)
for i, slide in enumerate(slides):
    create_slide(i, slide["title"], slide["desc"])
