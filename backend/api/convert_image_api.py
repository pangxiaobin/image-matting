from utilities.response import res500, res200, res400
from utilities.utils import convert_image_format
from conf.setting import settings
from webview import SAVE_DIALOG, OPEN_DIALOG
import webview
import time


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
