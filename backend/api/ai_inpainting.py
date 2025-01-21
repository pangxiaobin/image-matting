from utilities.utils import base64_to_image_obj, image_obj_to_base64
from hub_model import migan
from utilities.response import res200, res500
import time
from utilities.log import logger


class AIInpaintingAPI:
    name = "ai_inpainting"

    def __init__(self):
        pass

    def inpainting(self, payload: dict) -> dict:
        origin_base64 = payload.get("origin_base64")
        mask_base64 = payload.get("mask_base64")
        start_time = time.time()
        try:
            origin_image = base64_to_image_obj(origin_base64)
            mask_image = base64_to_image_obj(mask_base64)
            result = migan.process_image(origin_image, mask_image, 512)
            result_base64 = image_obj_to_base64(result)
            logger.info(f"Inpainting image time: {time.time() - start_time}")
            return res200(data={"result_base64": result_base64})
        except Exception as e:
            logger.error(f"Error in inpainting: {e}")
            return res500("Error in inpainting")
