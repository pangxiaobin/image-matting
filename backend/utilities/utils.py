import base64
from PIL import Image
from io import BytesIO


def is_image(filename):
    return any(
        filename.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif"]
    )


# Image 转base64
def image_obj_to_base64(image_obj: Image):
    buffered = BytesIO()
    image_obj.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return "data:image/png;base64," + img_str


# img to base64
def img_to_base64(img_path: str):
    with open(img_path, "rb") as f:
        data = f.read()
        base64_img = base64.b64encode(data).decode("utf-8")
        return f"data:image/{img_path.split('.')[-1]};base64,{base64_img}"


# base64 转 png
def base64_to_png(base64_data, save_path: str):
    base64_data = base64_data.split(",")[1]
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(base64_data))
    return save_path
