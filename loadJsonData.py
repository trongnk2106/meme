import json 
from PIL import Image, ImageDraw
import cv2
import numpy as np
import os 

# def draw_bbox(image_path, box_infos, ImageWidh_infile, ImageHeight_infile, annot):
#     """
#     Draw a bounding box on an image.

#     Args:
#         image_path (str): Path to the image file.
#         bbox (list): List of bounding box coordinates [x1, y1, x2, y2].
#         label (str, optional): Label for the bounding box. Defaults to None.
#     """
#     image = cv2.imread(os.path.join("images",image_path))
#     image_width = image.shape[1]
#     image_height = image.shape[0]
    
#     ratio_width = image_width / ImageWidh_infile
#     ratio_height = image_height / ImageHeight_infile
    
#     for idx, (box_info, ann) in enumerate(zip(box_infos, annot)):
#         # Convert the box coordinates to integers
#         box_info['x'] = int(box_info['x'] * ratio_width)
#         box_info['y'] = int(box_info['y'] * ratio_height)
        
        
#         box_info['width'] = int(box_info['width'] * ratio_width)
#         box_info['height'] = int(box_info['height']     * ratio_height)
        
#         box_info['rotateAngle'] = int(box_info['rotateAngle'])
#         box_center = (box_info['x'] + box_info['width'] // 2,
#                 box_info['y'] + box_info['height'] // 2)
#         box_size = (box_info['width'], box_info['height'])
#         angle = box_info['rotateAngle']

    
#     # image = Image.open(image_path)
#     # draw = ImageDraw.Draw(image)

#         rotated_rect = ((box_center[0], box_center[1]), box_size, angle)
#         box_points = cv2.boxPoints(rotated_rect).astype(np.int32)

#         cv2.polylines(image, [box_points], isClosed=True, color=(3, 252, 61), thickness=2)
#         # Show the image with the bounding box
        
#         # add id to the box inside the bounding box

#         # cv2.putText(image, str(f"ID: {idx + 1}"), (box_info['x'] + 10, box_info['y'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (3, 252, 94), 2)
#         cv2.putText(image, str(f"ID: {idx + 1}"), (box_info['x'] + 10, box_center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
#         caption = ann['text']
#         font_size = ann['fontSize']
#         hex_color = ann['color']
#         # Convert hex color to RGB tuple
#         color = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
#         # Draw the text on the image
#         text_position = (box_info['x'], box_info['y'] - 10)
#         cv2.putText(image, caption, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
#     cv2.imshow("Image with Bounding Box", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

       

    # save the image
    # cv2.imwrite(os.path.join("images_full", image_path), image)
       
def hex_to_bgr(hex_color):
    """Chuyển mã hex thành màu BGR cho OpenCV."""
    return tuple(int(hex_color[i:i + 2], 16) for i in (5, 3, 1))  # BGR thứ tự ngược

def draw_text_in_bbox(image, text, bbox, color, max_font_scale=2.0, font=cv2.FONT_HERSHEY_SIMPLEX):
    """Vẽ text nằm gọn trong bbox, tự co dãn font."""
    x, y, w, h = bbox
    font_scale = max_font_scale
    thickness = 1

    while font_scale > 0.1:
        (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        if text_w <= w and text_h + baseline <= h:
            break
        font_scale -= 0.1

    # Tính vị trí để căn giữa text trong bbox
    text_x = x + (w - text_w) // 2
    text_y = y + (h + text_h) // 2

    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)

def draw_bbox(image_path, box_infos, ImageWidh_infile, ImageHeight_infile, annot):
    """
    Vẽ bbox có ID và caption nằm gọn trong box.

    Args:
        image_path (str): Tên file ảnh.
        box_infos (list): Danh sách bbox (dict gồm x, y, width, height, rotateAngle).
        ImageWidh_infile (int): Chiều rộng gốc.
        ImageHeight_infile (int): Chiều cao gốc.
        annot (list): Danh sách annotation tương ứng với từng bbox (gồm text, fontSize, color).
    """
    image = cv2.imread(os.path.join("images", image_path))
    image_width = image.shape[1]
    image_height = image.shape[0]
    
    ratio_width = image_width / ImageWidh_infile
    ratio_height = image_height / ImageHeight_infile

    for idx, (box_info, ann) in enumerate(zip(box_infos, annot)):
        # Scale tọa độ
        x = int(box_info['x'] * ratio_width)
        y = int(box_info['y'] * ratio_height)
        w = int(box_info['width'] * ratio_width)
        h = int(box_info['height'] * ratio_height)
        angle = int(box_info['rotateAngle'])

        box_center = (x + w // 2, y + h // 2)
        box_size = (w, h)

        # Vẽ bbox xoay
        rotated_rect = (box_center, box_size, angle)
        box_points = cv2.boxPoints(rotated_rect).astype(np.int32)
        cv2.polylines(image, [box_points], isClosed=True, color=(3, 252, 61), thickness=2)

        # Vẽ ID
        cv2.putText(image, f"ID: {idx + 1}", (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Vẽ caption nằm trong bbox
        caption = ann['text']
        hex_color = ann['color']
        color_bgr = hex_to_bgr(hex_color)

        draw_text_in_bbox(image, caption, (x, y, w, h), (0, 0, 0))

    cv2.imshow("Meme Result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


from PIL import Image, ImageDraw, ImageFont
import io
import base64

def draw_meme_text(base64_img, captions, font_path="arial.ttf"):
    # Decode base64 image
    img_data = base64.b64decode(base64_img)
    image = Image.open(io.BytesIO(img_data)).convert("RGBA")

    draw = ImageDraw.Draw(image)

    for cap in captions:
        box_id = cap["id"]
        text = cap["text"]
        font_size = cap["fontSize"]
        color = cap["color"]
        
        # Bạn cần mapping từ ID → bbox (left, top, width, height)
        # Ở đây demo giả định bạn đã có bbox_dict
        bbox = bbox_dict[box_id]  # e.g. (x, y, w, h)

        font = ImageFont.truetype(font_path, font_size)

        # Tính vị trí để text nằm giữa box
        text_size = draw.multiline_textsize(text, font=font)
        x = bbox[0] + (bbox[2] - text_size[0]) / 2
        y = bbox[1] + (bbox[3] - text_size[1]) / 2

        draw.multiline_text(
            (x, y),
            text,
            fill=color,
            font=font,
            align="center",
            spacing=4
        )

    # Convert lại thành base64 nếu muốn trả về
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# annot = [{'id': 1, 'text': 'Step 1: Make a plan', 'fontSize': 22, 'color': '#FFFFFF', 'lineBreaks': True}, 
#          {'id': 2, 'text': 'Step 2: Execute\nthe plan', 'fontSize': 22, 'color': '#FFFFFF', 'lineBreaks': True}, 
#          {'id': 3, 'text': 'Step 3: Wait\nfor glory', 'fontSize': 22, 'color': '#FFFFFF', 'lineBreaks': True}, 
#          {'id': 4, 'text': "Step 4: Realize\nit's Monday", 'fontSize': 22, 'color': '#FFFFFF', 'lineBreaks': True}, 
#          {'id': 5, 'text': 'The end:\nStay in bed', 'fontSize': 22, 'color': '#FFFFFF', 'lineBreaks': True}]


annot = [{'id': 1, 'text': 'Bad idea:\nTexting ex at 3am', 'fontSize': 22, 'color': '#000000', 'lineBreaks': True}, {'id': 2, 'text': 'Good vibes:\nWatching cat videos\nat 3am', 'fontSize': 22, 'color': '#000000', 'lineBreaks': True}]

data = load_json_data('filterJson.json')
# print(len(data))
# with open('view.json', 'w') as file:

#     json.dump(data[0], file, indent=4)
# breakpoint()
for item in data:
    if item["imageName"] == "Drake-Hotline-Bling.png":
        draw_bbox(item["imageName"], item["initialCaptions"], item["imageWidth"], item['imageHeight'], annot)

# result_list = []
# for item in data:
#     pagePros = item['pageProps']
#     imageName = pagePros['imageName']
#     imageDescription = pagePros['imageDescription']
#     imageWidth = pagePros['imageWidth']
#     imageHeight = pagePros['imageHeight']
#     initialCaptions = pagePros['initialCaptions']
#     memeOrigin = pagePros['memeOrigin']
#     memeExamples = pagePros['memeExamples']
#     res = {
#         'imageName': imageName,
#         'imageDescription': imageDescription,
#         'imageWidth': imageWidth,
#         'imageHeight': imageHeight,
#         'initialCaptions': initialCaptions,
#         'memeOrigin': memeOrigin,
#         'memeExamples': memeExamples
#     }
#     result_list.append(res)

# with open('filterJson.json', 'w') as file:
#     json.dump(result_list, file, indent=4)

# pageProps    
#     imageName
#     imageDescription
#     imageWidth
#     imageHeight
#     initialCaptions --> tọa độ 
#     memeOrigin
#     memeExamples