
from PIL import Image, ImageDraw, ImageFont
import json
import requests
from io import BytesIO

def generate_collage(json_data):
    data = json.loads(json_data)
    font = ImageFont.load_default()
    item_width, item_height = 200, 250
    margin = 20
    max_columns = 4

    sections = []
    for section in data:
        section_title = section['category']
        items = section['items']
        section_images = []
        for item in items:
            img = Image.new("RGBA", (item_width, item_height), (30, 30, 30))
            try:
                response = requests.get(item["image"])
                item_img = Image.open(BytesIO(response.content)).resize((item_width, 180))
                img.paste(item_img, (0, 0))
            except:
                pass
            draw = ImageDraw.Draw(img)
            draw.text((10, 185), item["title"][:20], font=font, fill=(255, 255, 255))
            draw.text((10, 205), f'Цена: {item["price"]}', font=font, fill=(255, 255, 0))
            section_images.append(img)
        sections.append((section_title, section_images))

    section_heights = [((len(items) + max_columns - 1) // max_columns) * (item_height + margin) + 50 for _, items in sections]
    total_height = sum(section_heights) + margin * (len(section_heights) + 1)
    collage_width = max_columns * (item_width + margin) + margin
    collage = Image.new("RGB", (collage_width, total_height), (20, 20, 20))

    y_offset = margin
    for section_title, items in sections:
        draw = ImageDraw.Draw(collage)
        draw.text((margin, y_offset), section_title, font=font, fill=(255, 255, 255))
        y_offset += 30
        for i, item_img in enumerate(items):
            x = margin + (i % max_columns) * (item_width + margin)
            y = y_offset + (i // max_columns) * (item_height + margin)
            collage.paste(item_img, (x, y))
        y_offset += ((len(items) + max_columns - 1) // max_columns) * (item_height + margin) + margin

    out_path = "shop_collage.jpg"
    collage.save(out_path)
    return out_path
