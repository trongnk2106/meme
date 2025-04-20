from PIL import Image, ImageDraw, ImageFont
import os
import base64
import io
import json


import textwrap


def wrap_text_to_fit(draw, text, font_path, max_width, max_height, max_font_size=80):
    """
    Tìm font lớn nhất có thể, wrap theo TỪ, không cắt ngang từ.
    Trả về: font, wrapped_text (dùng '\n')
    """
    words = text.split()
    font_size = 5
    best_font = None
    best_wrapped = ""

    while font_size <= max_font_size:
        font = ImageFont.truetype(font_path, font_size)
        lines = []
        current_line = ""

        for word in words:
            test_line = word if not current_line else current_line + " " + word
            test_width = draw.textlength(test_line, font=font)
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        wrapped_text = "\n".join(lines)

        # Đo kích thước sau khi wrap
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, spacing=4)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if text_w <= max_width and text_h <= max_height:
            best_font = font
            best_wrapped = wrapped_text
            font_size += 1
        else:
            break

    return best_font or ImageFont.truetype(font_path, 10), best_wrapped or text


def hex_to_rgb(hex_color):
    """Chuyển mã hex thành RGB cho Pillow."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def draw_text_in_bbox_pillow(draw, text, bbox, color, font_path):
    """Vẽ text nằm gọn trong bbox, tự wrap + font."""
    x, y, w, h = bbox
    font, wrapped_text = wrap_text_to_fit(draw, text, font_path, w, h)

    bbox_text = draw.multiline_textbbox((0, 0), wrapped_text, font=font, spacing=4)
    text_w = bbox_text[2] - bbox_text[0]
    text_h = bbox_text[3] - bbox_text[1]

    # Căn giữa trong box
    text_x = x + (w - text_w) // 2
    text_y = y + (h - text_h) // 2

    draw.multiline_text(
        (text_x, text_y),
        wrapped_text,
        fill=color,
        font=font,
        align="center",
        spacing=4,
        stroke_width=2,
        stroke_fill=(0, 0, 0),  # viền đen
    )


def draw_bbox_pillow(
    image,
    box_infos,
    ImageWidh_infile,
    ImageHeight_infile,
    annot,
    font_path="arial.ttf",
):
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

    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    ratio_width = image_width / ImageWidh_infile
    ratio_height = image_height / ImageHeight_infile

    for idx, (box_info, ann) in enumerate(zip(box_infos, annot)):
        # Scale tọa độ
        x = int(box_info["x"] * ratio_width)
        y = int(box_info["y"] * ratio_height)
        w = int(box_info["width"] * ratio_width)
        h = int(box_info["height"] * ratio_height)
        angle = int(box_info["rotateAngle"])

        caption = ann["text"]
        color = hex_to_rgb(ann["color"])

        draw_text_in_bbox_pillow(draw, caption, (x, y, w, h), color, font_path)

    return image

