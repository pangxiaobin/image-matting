import webview
from utilities.log import logger, init_logging
from utilities.response import res200, res500
from utilities.utils import base64_to_png, save_bs64_image_add_bg
from conf.setting import settings
from conf.config import config
import os
from api import API
import mimetypes
import time
from api.user_api import SettingAPI
from api.ai_matting import AIMattingAPI
from api.convert_image_api import ConvertImageAPI
import platform
import subprocess
import os
import traceback


def main():
    mimetypes.add_type("application/javascript", ".js")

    # 初始化日志
    init_logging(log_name="image-matting")

    if settings.DEBUG:
        url = os.getenv("DEV_URL", "http://localhost:4000")
    else:
        url = "web/index.html"
    VERSION = settings.VERSION

    def open_file_dialog(self, multiple=False):
        # jpg/png/gif/webp/bmp
        file_types = ("Image Files (*.bmp;*.jpg;*.gif;*.png;*.webp;*.jpeg)",)
        result = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=bool(multiple), file_types=file_types
        )
        print(result)
        return res200({"file_path": result[0] if result else ""})

    def open_folder_dialog(self, initial_directory=""):
        result = window.create_file_dialog(
            webview.FOLDER_DIALOG, directory=initial_directory
        )
        print(result)
        return res200({"folder_path": result[0] if result else ""})

    def save_png_dialog(
        self,
        png_data,
        initial_directory="",
    ):
        filename = f"[{settings.TOOL_NAME}]-{int(time.time()*1000)}.png"
        result = window.create_file_dialog(
            webview.SAVE_DIALOG, directory=initial_directory, save_filename=filename
        )
        if not result:
            return
        try:
            base64_to_png(png_data, result)
        except Exception as e:
            logger.error(f"save_png_dialog error: {e}")
            return res500(f"save_png_dialog error: {e}")
        return res200({"file_path": result})

    def open_save_dialog(self, save_filename):
        result = window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename=save_filename,
        )
        return result

    def save_png_add_bg_dialog(
        self,
        playload,
        initial_directory="",
    ):

        base64_data = playload.get("base64_data")
        hex_color = playload.get("hex_color")

        filename = f"[{settings.TOOL_NAME}]-{int(time.time()*1000)}.png"
        result = window.create_file_dialog(
            webview.SAVE_DIALOG, directory=initial_directory, save_filename=filename
        )
        if not result:
            return
        try:
            save_bs64_image_add_bg(base64_data, hex_color, result)
        except Exception as e:
            logger.error(f"save_png_add_bg_dialog error: {e}")
            return res500(f"save_png_add_bg_dialog error: {e}")
        return res200({"file_path": result})

    def open_and_select_file(self, file_path):
        system = platform.system()

        if system == "Windows":
            # 在Windows系统上打开文件夹并选中文件
            subprocess.call(["explorer", "/select,", os.path.normpath(file_path)])
        elif system == "Darwin":  # macOS
            # 在macOS系统上打开Finder并选中文件
            subprocess.call(["open", "-R", file_path])
        elif system == "Linux":
            # 在Linux系统上打开文件管理器并选中文件
            # 使用xdg-open无法直接选中文件，因此这里只是打开文件夹
            subprocess.call(["xdg-open", os.path.dirname(file_path)])
        else:
            raise OSError("Unsupported operating system")

    # 绑定API
    API.open_file_dialog = open_file_dialog
    API.open_folder_dialog = open_folder_dialog
    API.save_png_dialog = save_png_dialog
    API.open_and_select_file = open_and_select_file
    API.save_png_add_bg_dialog = save_png_add_bg_dialog
    API.open_save_dialog = open_save_dialog

    api = API()

    api_class_list = [SettingAPI, AIMattingAPI, ConvertImageAPI]
    for api_class in api_class_list:
        api.add_apis(api_class)
    try:
        window = webview.create_window(
            f"{settings.TOOL_NAME} - {VERSION}",
            url=url,
            js_api=api,
            width=config.get("window.width", 1000),
            height=config.get("window.height", 800),
            x=config.get("window.x", 0),
            y=config.get("window.y", 0),
            on_top=config.get("window.on_top", False),
            confirm_close=True,
        )
    except Exception as e:
        traceback.print_exc()

    logger.info(f"Debug: {settings.DEBUG}")
    logger.info(f"Version: {VERSION}")
    logger.info(f"load url: {url}")

    def on_close():
        logger.info("process closed")
        config.close()
        window.destroy()

    def on_moved(x, y):
        config.save("window.x", int(x))
        config.save("window.y", int(y))

    def on_resized(width, height):
        config.save("window.width", int(width))
        config.save("window.height", int(height))

    def bind(window):
        window.events.closed += on_close
        window.events.resized += on_resized
        window.events.moved += on_moved

    try:
        webview.start(bind, window, debug=settings.DEBUG, http_server=True)
    except:
        traceback.print_exc()
        logger.error("Error: webview.start() failed")


if __name__ == "__main__":
    main()
