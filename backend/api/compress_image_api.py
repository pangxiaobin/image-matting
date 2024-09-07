from utilities.utils import get_img_info, img_to_base64
from utilities.response import res200, res400, res500
from utilities.tinify_client import tinify_client
from pathlib import Path


class CompressImageAPI:

    name = "compress_image"

    def get_image_info(self, image_path):
        try:
            img_info = get_img_info(image_path)
            img_info["img"] = img_to_base64(image_path)
            return res200(data=img_info)
        except Exception as e:
            return res500(str(e))

    def single_compress_image(self, img_path):
        if not img_path:
            return res400("Image path is required.")

        if not any(
            img_path.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]
        ):
            return res400(
                "Only support jpg, jpeg, png and webp format. please use convert function"
            )
        img_dir_path = Path(img_path)
        if not img_dir_path.exists():
            return res400("Image path does not exist.")

        save_folder = img_dir_path.parent
        save_filename = f"compressed_{img_dir_path.name}"
        save_path = save_folder / save_filename

        flag, message = tinify_client.compress_image(img_path, save_path)
        if flag:
            return res200(data={"save_path": str(save_path)})
        else:
            return res500(message)
