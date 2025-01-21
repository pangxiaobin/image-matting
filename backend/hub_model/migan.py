import numpy as np
import onnxruntime
from PIL import Image
from pathlib import Path
import time
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from utilities.log import logger
except ImportError:
    sys.path.append(str(BASE_DIR))
    from utilities.log import logger


def resize(image, max_size, interpolation=Image.BICUBIC):
    w, h = image.size
    if w > max_size or h > max_size:
        resize_ratio = max_size / w if w > h else max_size / h
        image = image.resize(
            (int(w * resize_ratio), int(h * resize_ratio)), interpolation
        )
    return image


def read_mask(mask_image: Image, invert=False):
    mask = resize(mask_image, max_size=512, interpolation=Image.NEAREST)
    mask = np.array(mask)
    print(mask.shape)
    if len(mask.shape) == 3:
        if mask.shape[2] == 4:
            _r, _g, _b, _a = np.rollaxis(mask, axis=-1)
            mask = np.dstack([_a, _a, _a])
        elif mask.shape[2] == 2:
            _l, _a = np.rollaxis(mask, axis=-1)
            mask = np.dstack([_a, _a, _a])
        elif mask.shape[2] == 3:
            _r, _g, _b = np.rollaxis(mask, axis=-1)
            mask = np.dstack([_r, _r, _r])
    else:
        mask = np.dstack([mask, mask, mask])  # 将mask扩展为三通道
    if invert:
        mask = 255 - mask
    mask[mask < 255] = 0
    return Image.fromarray(mask).convert("L")


def preprocess(img: Image, mask: Image, resolution: int) -> np.ndarray:
    """
    Preprocesses the image and mask, resizing them and normalizing pixel values.
    """
    # Resize images and masks to the required resolution
    img = img.resize((resolution, resolution), Image.BICUBIC)
    mask = mask.resize((resolution, resolution), Image.NEAREST)

    # Convert to numpy arrays (uint8) as required by ONNX model
    img = np.array(img).astype(np.uint8)  # Image should be uint8
    mask = np.array(mask).astype(np.uint8)  # Mask should be uint8

    # Ensure mask has shape [batch_size, 1, height, width]
    mask = np.expand_dims(mask, axis=0)  # Add batch dimension
    mask = np.expand_dims(mask, axis=0)  # Add channel dimension for mask

    # Ensure image has shape [batch_size, 3, height, width]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = np.transpose(img, (0, 3, 1, 2))  # HWC to NCHW format

    # Return a dictionary with both image and mask for model input
    return img, mask


class MiganInpainting:
    """
    黑色mask是要处理的数据
    """

    def __init__(
        self, model_path: str = str(BASE_DIR / "hub_model" / "rmodel" / "model.onnx")
    ):
        self.model_path = model_path
        self.providers = onnxruntime.get_available_providers()
        try:
            logger.info("Loading model...")
            start_time = time.time()
            self.ort_session = onnxruntime.InferenceSession(
                self.model_path, providers=self.providers
            )
            for i in self.ort_session.get_inputs():
                logger.info(f"Input: {i.name}, shape: {i.shape}, type: {i.type}")
            logger.info(
                f"{self.model_path} Model loaded in {time.time() - start_time:.2f} seconds"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load ONNX model: {e}")

    def process_image(self, img: Image, mask: Image, resolution: int) -> Image:
        """
        Process the image with the provided mask using the ONNX model.
        """
        img = img.convert("RGB")
        mask = read_mask(mask, invert=True)
        # Preprocess the input image and mask
        img_input, mask_input = preprocess(img, mask, resolution=512)

        # Run inference with ONNX
        result_image = self.ort_session.run(
            None,
            {
                self.ort_session.get_inputs()[0].name: img_input.astype(
                    np.uint8
                ),  # Image input
                self.ort_session.get_inputs()[1].name: mask_input.astype(
                    np.uint8
                ),  # Mask input
            },
        )[0]

        # Post-process the result image (convert to [0, 255] range and back to HWC format)
        result_image = np.clip(result_image, 0, 255).astype(np.uint8)
        result_image = np.transpose(result_image, (0, 2, 3, 1))  # NCHW to NHWC
        result_image = result_image[0]  # Remove batch dimension
        result_image = Image.fromarray(result_image)
        result_image = result_image.resize(img.size, Image.BICUBIC)
        return result_image


if __name__ == "__main__":
    model = MiganInpainting()
    image = Image.open("luck.png").convert("RGB")
    mask = read_mask(Image.open("luck-apha.png").convert("L"), invert=True)
    result = model.process_image(image, mask, 512)
    result.save("output3.png")
