from PIL import Image, ImageDraw, ImageFont
import os
import base64
import io
import json

def hex_to_rgb(hex_color):
    """Chuyển mã hex thành RGB cho Pillow."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
def get_fit_font(draw, text, font_path, max_width, max_height, start_size=40):
    """Tìm font size sao cho text fit trong box (Pillow >=10)."""
    font_size = start_size
    while font_size > 5:
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=4)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= max_width and h <= max_height:
            return font
        font_size -= 1
    return ImageFont.truetype(font_path, 10)  # fallback

def draw_text_in_bbox_pillow(draw, text, bbox, color, font_path):
    """Vẽ text nằm gọn trong bbox, tự co dãn font."""
    x, y, w, h = bbox
    font = get_fit_font(draw, text, font_path, w, h)

    bbox_text = draw.multiline_textbbox((0, 0), text, font=font, spacing=4)
    text_w = bbox_text[2] - bbox_text[0]
    text_h = bbox_text[3] - bbox_text[1]

    # Căn giữa trong box
    text_x = x + (w - text_w) // 2
    text_y = y + (h - text_h) // 2

    draw.multiline_text(
        (text_x, text_y),
        text,
        fill=color,
        font=font,
        align="center",
        spacing=4
    )

def draw_bbox_pillow(image_path, box_infos, ImageWidh_infile, ImageHeight_infile, annot, font_path="arial.ttf"):
    """
    Vẽ bbox và caption bằng Pillow (đẹp hơn OpenCV).

    Args:
        image_path (str): Tên file ảnh.
        box_infos (list): Danh sách bbox.
        ImageWidh_infile (int): Chiều rộng gốc.
        ImageHeight_infile (int): Chiều cao gốc.
        annot (list): Annotation gồm text, fontSize, color.
        font_path (str): Đường dẫn đến font .ttf
    """
    from PIL import ImageOps, ImageDraw, ImageFont
    image = Image.open(os.path.join("images", image_path)).convert("RGB")
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    ratio_width = image_width / ImageWidh_infile
    ratio_height = image_height / ImageHeight_infile

    for idx, (box_info, ann) in enumerate(zip(box_infos, annot)):
        # Scale tọa độ
        x = int(box_info['x'] * ratio_width)
        y = int(box_info['y'] * ratio_height)
        w = int(box_info['width'] * ratio_width)
        h = int(box_info['height'] * ratio_height)
        angle = int(box_info['rotateAngle'])

        # Vẽ bbox viền xanh lá
        # draw.rectangle([(x, y), (x + w, y + h)], outline=(3, 252, 61), width=2)

        # Vẽ ID
        # draw.text((x + 5, y + 5), f"ID: {idx + 1}", fill=(255, 0, 0), font=ImageFont.truetype(font_path, 14))

        # Vẽ caption nằm trong bbox
        caption = ann['text']
        color = hex_to_rgb(ann['color'])

        draw_text_in_bbox_pillow(draw, caption, (x, y, w, h), color, font_path)

    image.show()
    
    
annot = [{'id': 1, 'text': 'Bad idea:\nTexting ex at 3am', 'fontSize': 22, 'color': '#000000', 'lineBreaks': True}, {'id': 2, 'text': 'Good vibes:\nWatching cat videos\nat 3am', 'fontSize': 22, 'color': '#000000', 'lineBreaks': True}]

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
data = load_json_data('filterJson.json')

for item in data:
    if item["imageName"] == "Drake-Hotline-Bling.png":
        draw_bbox_pillow(item["imageName"], item["initialCaptions"], item["imageWidth"], item['imageHeight'], annot)
