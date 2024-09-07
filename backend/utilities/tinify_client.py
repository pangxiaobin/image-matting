import tinify
from conf.config import config
import base64
import requests


class TinifyClient:

    def __init__(self, tinigy_key):
        tinify.key = tinigy_key
        self.tinigy_key = tinigy_key

    def update_key(self, key):
        tinify.key = key

    def compress_image(self, input_image_path, output_image_path):
        """
        Compress the input image to the output image with the same size and format.
        """
        try:
            tinify.validate()
            source = tinify.from_file(input_image_path)
            preserve = config.get("tinify.preserve")
            if preserve:
                copyrighted = source.preserve(*preserve)
                copyrighted.to_file(output_image_path)
            else:
                source.to_file(output_image_path)
            compression_count = tinify.compression_count
            config.save("tinify.compression_count", compression_count)
            return True, output_image_path
        except tinify.Error as e:
            #  Validation of API key failed.
            return False, e.message

    def compress_image_from_base64(self, input_image_base64, output_image_path):
        """
        Compress the input image from base64 to the output image with the same size and format.
        """
        try:
            tinify.validate()
            image_data = base64.b64decode(input_image_base64)

            # 使用 tinify 进行压缩
            compressed_image = tinify.from_buffer(image_data).to_buffer()

            # 将压缩后的图片保存到指定路径
            with open(output_image_path, "wb") as f:
                f.write(compressed_image)
                return True, output_image_path
        except tinify.Error as e:
            #  Validation of API key failed.
            return False, e.message


tinify_client = TinifyClient(config.get("tinify.tinify_key", ""))
