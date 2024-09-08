from utilities.utils import (
    get_img_info,
    img_to_base64,
    get_file_size_info,
    can_compress_image,
)
from utilities.response import res200, res400, res500
from utilities.tinify_client import tinify_client
from pathlib import Path
import os
from utilities.log import logger
from conf.setting import settings
import time


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

        if not can_compress_image(img_path):
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

    def get_folder_compress_images(self, folder_path: str) -> dict:
        """
        Get the list of images in the input folder.


        :param folder_path: The path of the input folder.

        :return: The response object with the list of images in the folder.

        """
        try:
            compress_images = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if can_compress_image(file):
                        image_path = os.path.join(root, file)
                        img_info = get_file_size_info(image_path)
                        img_info["image_name"] = os.path.basename(image_path)
                        img_info["image_path"] = image_path
                        img_info["img"] = img_to_base64(image_path)
                        img_info["status"] = ""
                        img_info["compress_result"] = ""
                        compress_images.append(img_info)
            return res200(
                data={"compress_images": compress_images, "folder_path": folder_path}
            )
        except Exception as e:
            logger.error(f"Error in get_folder_compress_images: {e} {folder_path}")
            return res500("Error in get_folder_compress_images")

    def compress_image_from_folder(self, playload):
        try:
            image_path = playload.get("image_path")
            folder_path = playload.get("folder_path")
            img_name = os.path.basename(image_path)
            save_folder = os.path.join(
                folder_path, f"[{settings.TOOL_NAME}]-compress-output"
            )
            if not os.path.exists(save_folder):
                os.makedirs(save_folder, exist_ok=True)
            filename = f"compressed-{int(time.time()*1000)}-{img_name}"
            save_path = os.path.join(save_folder, filename)
            flag, message = tinify_client.compress_image(image_path, save_path)
            logger.info(f"compress image {image_path} to {save_path} success")
            if flag:
                compress_info = get_file_size_info(save_path)
                compress_info["save_path"] = save_path
                return res200(data={"compress_result": compress_info})
            else:
                return res500(message)

        except Exception as e:
            logger.error(f"Error in compress image: {e} {image_path}")
            return res500("Error in compress image")
