from utilities.utils import base64_to_image
from pathlib import Path
from utilities.log import logger
from utilities.response import res200, res400, res500
from conf.setting import settings
from utilities.utils import img_to_base64
import webbrowser


class API:
    def __init__(self):
        pass

    def add_apis(self, APIClass):
        for method_name in dir(APIClass):
            method = getattr(APIClass, method_name)
            if callable(method) and not method_name.startswith("_"):
                setattr(API, f"{APIClass.name}__{method_name}", method)

    def save_image(self, base64_image: str, save_folder: str, image_name: str) -> dict:
        """
        Save the input image to the save_folder.

        :param base64_image: The base64 format of the input image.
        :param save_folder: The path of the input image.
        :param image_name: The name of the input image.
        :return: The response object with the path of the saved image.
        """
        try:
            save_path = Path(save_folder) / f"{image_name}.png"
            base64_to_image(base64_image, str(save_path.absolute))
            return res200(data={"image_path": str(save_path.absolute)})
        except Exception as e:
            logger.error(f"Error in save_image: {e} {image_name}")
            return res500("Error in save_image")

    def get_system_info(self, playload) -> dict:
        """
        Get the version of the backend.
        :return: The response object with the version of the backend.
        """

        return res200(
            data={
                "version": settings.VERSION,
                "author": settings.AUTHOR,
                "email": settings.EMAIL,
                "github": settings.GITHUB,
                "website": settings.WEBSITE,
            }
        )

    def get_local_file_base64(self, file):
        try:
            img = img_to_base64(file)
            return res200(data={"base64_image": img})
        except Exception as e:
            return res500(f"Error in get_local_file_base64: {e}")

    def open_link(self, link):
        webbrowser.open(link)
