import time
from utilities.utils import is_image, image_obj_to_base64, image_to_psd, read_image
from hub_model import segmentation
from utilities.log import logger
from utilities.response import res200, res400, res500
import os
from conf.setting import settings
from conf.config import config


class AIMattingAPI:
    name = "ai_matting"

    def __init__(self):
        pass

    def predict(self, image_path: str) -> dict:
        """
        Predict the no-background image of the input image.

        :param image_path: The path of the input image.
        :return: The response object with the no-background image in base64 format.
        """
        sart_time = time.time()
        try:
            no_bg_image = segmentation.segment_image(image_path)
            no_bg_image_base64 = image_obj_to_base64(no_bg_image)
            logger.info(f"Predicted image time: {time.time() - sart_time}")
        except Exception as e:
            logger.error(f"Error in predict: {e} {image_path}")
            return res500("Error in predict")

        return res200(
            data={
                "no_bg_image": no_bg_image_base64,
            }
        )

    def get_folder_images(self, folder_path: str) -> dict:
        """
        Get the list of images in the input folder.


        :param folder_path: The path of the input folder.

        :return: The response object with the list of images in the folder.

        """
        try:
            image_list = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if is_image(file):
                        image_path = os.path.join(root, file)
                        tem = {
                            "image_name": os.path.basename(image_path),
                            "image_path": image_path,
                            "base64_image": "",
                            "status": "waiting",
                            "no_bg_image": "",
                        }
                        image_list.append(tem)
            return res200(data={"image_list": image_list, "folder_path": folder_path})
        except Exception as e:
            logger.error(f"Error in get_folder_images: {e} {folder_path}")
            return res500("Error in get_folder_images")

    def predict_from_folder_img(self, playload: dict) -> dict:
        """
        Predict the no-background image of the input image.

        :param image_path: The path of the input image.
        :return: The response object with the no-background image in base64 format.
        """
        try:
            image_path = playload.get("image_path")
            folder_path = playload.get("folder_path")
            no_bg_image = segmentation.segment_image(image_path)
            filename, _ = os.path.splitext(image_path)
            save_folder = os.path.join(folder_path, f"[{settings.TOOL_NAME}]抠图结果")
            if not os.path.exists(save_folder):
                os.makedirs(save_folder, exist_ok=True)
            export_format = config.get("export_format", "png")
            new_image_name = f"[{settings.TOOL_NAME}]-{filename}_{int(time.time() * 1000)}.{export_format}"
            save_path = os.path.join(save_folder, new_image_name)

            if export_format == "psd":
                origin_image = read_image(image_path)
                image_to_psd(no_bg_image, save_path, origin_image=origin_image)
            elif export_format == "jpg":
                no_bg_image.convert("RGB").save(save_path, "JPEG")
            else:
                no_bg_image.save(save_path)
            return res200(data={"no_bg_image": save_path})
        except Exception as e:
            logger.error(f"Error in predict_from_folder_img: {e} {image_path}")
            return res500("Error in predict_from_folder_img")
