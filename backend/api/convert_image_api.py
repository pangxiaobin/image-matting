from utilities.response import res500, res200, res400
from utilities.utils import convert_image_format, can_convert_file, img_to_base64
from utilities.log import logger
from conf.setting import settings
from webview import SAVE_DIALOG, OPEN_DIALOG
import webview
import time
import os


class ConvertImageAPI:
    name = "convert_image"

    def get_convert_image(self, playload):
        try:
            input_path = playload["input_path"]
            output_format = playload["output_format"]
        except KeyError:
            return res500("Invalid input")
        filename = f"[{settings.TOOL_NAME}]-{int(time.time()*1000)}-output.{output_format.lower()}"
        result = self.open_save_dialog(
            filename,
        )
        if not result:
            return res200(msg="Cancel")
        flag = convert_image_format(input_path, output_format, result)
        if flag:
            return res200(msg="Success")
        else:
            return res400(msg="Cancel")

    def get_folder_convert_images(self, folder_path: str) -> dict:
        """
        Get the list of images in the input folder.


        :param folder_path: The path of the input folder.

        :return: The response object with the list of images in the folder.

        """
        try:
            convert_images = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if can_convert_file(file):
                        image_path = os.path.join(root, file)
                        tem = {
                            "image_name": os.path.basename(image_path),
                            "image_path": image_path,
                            "status": "",
                            "convert_result": "",
                        }
                        convert_images.append(tem)
            return res200(
                data={"convert_images": convert_images, "folder_path": folder_path}
            )
        except Exception as e:
            logger.error(f"Error in get_folder_convert_images: {e} {folder_path}")
            return res500("Error in get_folder_convert_images")

    def convert_image_from_folder(self, playload):
        try:
            image_path = playload.get("image_path")
            folder_path = playload.get("folder_path")
            output_format = playload["output_format"]
            img_name = os.path.basename(image_path).split(".")[0]
            save_folder = os.path.join(folder_path, f"[{settings.TOOL_NAME}]-output")
            if not os.path.exists(save_folder):
                os.makedirs(save_folder, exist_ok=True)
            filename = f"[{settings.TOOL_NAME}]-{img_name}-{int(time.time()*1000)}.{output_format.lower()}"
            save_path = os.path.join(save_folder, filename)
            flag = convert_image_format(image_path, output_format, save_path)
            logger.info(f"convert image {image_path} to {save_path} success")
            if flag:
                return res200(data={"convert_result": save_path})
            else:
                return res500(msg="convert image failed")

        except Exception as e:
            logger.error(f"Error in convert image: {e} {image_path}")
            return res500("Error in convert image")
