from PIL import Image, ImageDraw, ImageFont
import os

# Define your data: title + description per slide
slides = [
    {
        "title": "UNDERSTAND WHO YOUR TARGET MARKET IS",
        "desc": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin eu odio in leo posuere ultrices."
    },
    {
        "title": "CREATE A PROMOTION FUND BUDGET",
        "desc": "Pellentesque pulvinar tristique elit. Pellentesque tincidunt suscipit nulla."
    },
    {
        "title": "OPTIMIZING SOCIAL MEDIA AS MARKETING",
        "desc": "Maecenas congue pellentesque arcu et laoreet. In ut libero at augue congue."
    },
    {
        "title": "RUNNING A DROPSHIP OR RESELLER",
        "desc": "Ut at enim ut augue varius sodales in non neque. Mauris fermentum."
    },
    {
        "title": "UTILIZING DIGITAL MARKETING STRATEGIES",
        "desc": "Vestibulum eget lacus eget enim convallis feugiat. Suspendisse eu neque."
    }
]


TEMPLATE_PATH = "template.jpg"  
FONT_BOLD_PATH = "fonts/Roboto-Bold.ttf"
FONT_REGULAR_PATH = "fonts/Roboto-Regular.ttf"
OUTPUT_DIR = "output_slides"

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
    font_title = ImageFont.truetype(FONT_BOLD_PATH, 60)
    font_desc = ImageFont.truetype(FONT_REGULAR_PATH, 32)
    font_number = ImageFont.truetype(FONT_BOLD_PATH, 100)

    # === Positioning Config ===
    margin_x = 100
    title_y = 200
    desc_y = 400
    max_text_width = image.width - 2 * margin_x

    # === Slide Number (e.g. 01, 02...) ===
    slide_number = f"{index+1:02}"
    draw.text((image.width - 180, 30), slide_number, font=font_number, fill=(30, 30, 30))

    # === Title Text ===
    wrapped_title = wrap_text(title, font_title, max_text_width, draw)
    draw.text((margin_x, title_y), wrapped_title, font=font_title, fill=(255, 199, 44))  # Yellow-ish

    # === Description Text ===
    wrapped_desc = wrap_text(desc, font_desc, max_text_width, draw)
    draw.text((margin_x, desc_y), wrapped_desc, font=font_desc, fill="white")

    # Save
    output_path = os.path.join(OUTPUT_DIR, f"slide_{index+1}.jpg")
    image.save(output_path)
    print(f"✅ Saved: {output_path}")

# === Generate All Slides ===
for i, slide in enumerate(slides):
    create_slide(i, slide["title"], slide["desc"])
