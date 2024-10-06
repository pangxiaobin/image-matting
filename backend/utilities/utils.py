import base64
from PIL import Image
from io import BytesIO
import os
import traceback
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer

import numpy as np


def is_image(filename):
    return any(
        filename.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif"]
    )


def can_convert_file(filename):
    """
    ["PNG", "JPEG", "GIF", "BMP", "WEBP", "ICO", "ICNS", "TIFF"]
    """
    return any(
        filename.lower().endswith(ext)
        for ext in [
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".webp",
            ".ico",
            ".icns",
            ".tiff",
        ]
    )


# Image 转base64
def image_obj_to_base64(image_obj: Image):
    buffered = BytesIO()
    image_obj.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return "data:image/png;base64," + img_str


# # img to base64
# def img_to_base64(img_path: str):
#     with open(img_path, "rb") as f:
#         data = f.read()
#         base64_img = base64.b64encode(data).decode("utf-8")
#         return f"data:image/{img_path.split('.')[-1]};base64,{base64_img}"


def img_to_base64(image_path: str):
    with Image.open(image_path) as img:
        # Check if the image is in WebP format
        if img.format == "WEBP":
            # Convert the image to a format supported by pywebview (e.g., PNG or JPEG)
            img = img.convert("RGBA")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_format = "image/png"
        else:
            buffer = BytesIO()
            img.save(buffer, format=img.format)
            img_format = f"image/{img.format.lower()}"

        # Encode the image to base64
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Create the data URL
        data_url = f"data:{img_format};base64,{img_str}"

    return data_url


# base64 转 png
def base64_to_image(base64_data, save_path: str):
    image_data = base64.b64decode(base64_data.split(",")[1])
    image_obj = Image.open(BytesIO(image_data))
    _, extension = os.path.splitext(save_path)
    if extension.lower() == ".jpg" or extension.lower() == ".jpeg":
        image_obj = image_obj.convert("RGB")
        image_obj.save(save_path, "JPEG")
    else:
        image_obj.save(save_path, extension[1:].upper())
    return save_path


def hex_to_rgb(hex_color):
    # 移除前缀 '#'
    hex_color = hex_color.lstrip("#")
    # 将十六进制颜色转换为 RGB 元组，确保每个值是整数
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def save_bs64_image_add_bg(base64_data, hex_color, save_path):
    if hex_color == "transparent":
        base64_to_image(base64_data, save_path)
        return save_path
    # 读取图片
    image_data = base64.b64decode(base64_data.split(",")[1])
    image = Image.open(BytesIO(image_data)).convert("RGBA")
    # 将十六进制颜色转换为 RGB
    background_color = hex_to_rgb(hex_color)

    # 创建带有背景颜色的新图像
    background_image = Image.new("RGBA", image.size, background_color + (255,))

    # 粘贴解码后的图像到背景图像上
    background_image.paste(image, (0, 0), image)

    # 保存合成后的图像
    background_image.save(save_path, "PNG")

    return save_path


def convert_image_format(input_path, output_format, output_path=None):
    try:
        # 打开原始图片
        image = Image.open(input_path)

        # 确保输出格式合法并转换格式
        if output_format.lower() == "jpg" or output_format.lower() == "jpeg":
            image = image.convert("RGB")  # 转换为RGB格式
            image.save(output_path, "JPEG")
        elif output_format.lower() == "png":
            image.save(output_path, "PNG")
        elif output_format.lower() == "gif":
            image.save(output_path, "GIF")
        elif output_format.lower() == "bmp":
            image.save(output_path, "BMP")
        elif output_format.lower() == "ico":
            image.save(output_path, "ICO")
        elif output_format.lower() == "icns":
            image.save(output_path, "ICNS")
        elif output_format.lower() == "webp":
            image.save(output_path, "WEBP")
        elif output_format.lower() == "pdf":
            image.save(output_path, "PDF")
        elif output_format.lower() == "tiff":
            image.save(output_path, "TIFF")
        else:
            return False
        return True
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        return False


def get_img_info(img_path):
    # 获取图片信息，包括尺寸、格式 、 色彩空间、文件大小
    try:
        with Image.open(img_path) as img:
            width, height = img.size
            format = img.format
            mode = img.mode
            file_size = os.path.getsize(img_path)
            return {
                "size": f"{width}x{height}",
                "format": format,
                "colorMode": mode,
                "fileSize": file_size,
                "formatSize": format_size(file_size),
                "path": img_path,
            }
    except Exception as e:
        return None


def get_base64_img_info(base64_data):
    # 获取 base64 图片信息，包括尺寸、格式、色彩模式、分辨率、色彩空间、文件大小
    img_data = base64.b64decode(base64_data.split(",")[1])
    with Image.open(BytesIO(img_data)) as img:
        width, height = img.size
        format = img.format
        mode = img.mode
        file_size = len(img_data)
        return {
            "size": f"{width}x{height}",
            "format": format,
            "colorMode": mode,
            "fileSize": file_size,
            "formatSize": format_size(file_size),
        }


def format_size(size):
    # 格式化文件大小
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f}KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / 1024 / 1024:.2f}MB"
    else:
        return f"{size / 1024 / 1024 / 1024:.2f}GB"


def get_file_size_info(file_path):
    # 获取文件大小信息
    file_size = os.path.getsize(file_path)
    return {"fileSize": file_size, "formatSize": format_size(file_size)}


def can_compress_image(file_name):
    if not file_name:
        return False
    if any(
        file_name.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]
    ):
        return True
    return False


def base64_to_psd(base64_data, save_path):
    image_data = base64.b64decode(base64_data.split(",")[1])
    image_obj = Image.open(BytesIO(image_data)).convert("RGBA")
    image_to_psd(image_obj, save_path)


def image_to_psd(image_obj: Image, save_path):
    if image_obj.mode != "RGBA":
        image_obj = image_obj.convert("RGBA")
    psd = PSDImage.frompil(image_obj)
    # Create a new layer for the image
    pixel_layer = PixelLayer.frompil(image_obj, psd)
    # Set the pixel layer to be visible
    pixel_layer.visible = True

    psd.append(pixel_layer)

    psd.save(save_path)
