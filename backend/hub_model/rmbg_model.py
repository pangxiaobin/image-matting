from transformers import AutoModelForImageSegmentation
from torchvision.transforms.functional import normalize
from torch import (
    device,
    tensor,
    cuda,
    Tensor,
    float32,
    unsqueeze,
    divide,
    squeeze,
    max,
    min,
)
import torch.nn.functional as F
import numpy as np
from skimage import io
from PIL import Image
from io import BytesIO
from pathlib import Path
import sys
import time
import requests
import base64

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from utilities.log import logger
    from utilities.utils import img_to_base64
except ImportError:
    sys.path.append(str(BASE_DIR))
    from utilities.log import logger
    from utilities.utils import img_to_base64


# 下载模型
# AutoModelForImageSegmentation.from_pretrained("briaai/RMBG-1.4", trust_remote_code=True).save_pretrained("RMBG-1_4")


class ImageSegmentation:
    def __init__(self, model_name=str(BASE_DIR / "hub_model" / "briaai" / "RMBG-1.4")):
        logger.info("Loading model...")
        star_time = time.time()
        self.model = AutoModelForImageSegmentation.from_pretrained(
            model_name, trust_remote_code=True, local_files_only=True
        )
        logger.info(f"Model loaded, time cost: {time.time() - star_time:.2f}s")
        self.device = device("cuda:0" if cuda.is_available() else "cpu")
        self.model.to(self.device)

    def preprocess_image(self, im: np.ndarray, model_input_size: list) -> Tensor:
        if len(im.shape) < 3:
            im = im[:, :, np.newaxis]
        im_tensor = tensor(im, dtype=float32).permute(2, 0, 1)
        im_tensor = F.interpolate(
            unsqueeze(im_tensor, 0), size=model_input_size, mode="bilinear"
        )
        image = divide(im_tensor, 255.0)
        image = normalize(image, [0.5, 0.5, 0.5], [1.0, 1.0, 1.0])
        return image

    def postprocess_image(self, result: Tensor, im_size: list) -> np.ndarray:
        # 使用双线性插值法调整结果张量的尺寸到目标图像尺寸
        result = squeeze(F.interpolate(result, size=im_size, mode="bilinear"), 0)
        ma = max(result)
        mi = min(result)
        result = (result - mi) / (ma - mi)
        im_array = (result * 255).permute(1, 2, 0).cpu().data.numpy().astype(np.uint8)
        im_array = np.squeeze(im_array)
        return im_array

    def read_image(self, img: str) -> Image.Image:
        if img.startswith("http"):
            response = requests.get(img)
            return Image.open(BytesIO(response.content))
        elif ";base64," in img:
            base64_string = img.split(";base64,")[-1]
            image_data = base64.b64decode(base64_string)
            return Image.open(BytesIO(image_data))
        elif Path(img).exists():
            return Image.open(fp=img, mode="r")
        else:
            raise FileNotFoundError(f"File {img} not found.")

    def segment_image(self, img_obj: str) -> Image.Image:
        # 读取图像
        orig_image = self.read_image(img_obj)
        # 去除alpha通道
        input_image = orig_image.convert("RGB")
        image_array = np.array(input_image)
        image_size = (input_image.size[1], input_image.size[0])
        model_input_size = [1024, 1024]

        image = self.preprocess_image(image_array, model_input_size).to(self.device)

        # 推理
        result = self.model(image)

        # 后处理
        result_image = self.postprocess_image(result[0][0], image_size)

        # 保存结果
        pil_im = Image.fromarray(result_image)
        no_bg_image = Image.new("RGBA", pil_im.size, (0, 0, 0, 0))
        no_bg_image.paste(orig_image, mask=pil_im)

        return no_bg_image


if __name__ == "__main__":
    # 示例使用：
    segmentation = ImageSegmentation()
    base_path = BASE_DIR / "hub_model" / "test_images"
    test_imgs = [
        # "test.jpg",
        # "car.jpg",
        "input.jpg",
    ]
    for img_name in test_imgs:
        print(img_to_base64(str(base_path / img_name)))
        with open("demo.txt", "w+") as f:
            f.write(img_to_base64(str(base_path / img_name)))
            break

        # img_path = str(base_path / img_name)
        # file_name = img_name.split(".")[0]
        # no_bg_image = segmentation.segment_image(img_path)
        # no_bg_image.save(str(base_path / f"no_bg_{file_name}.png"))
        # logger.info(f"Image {img_name} has been processed successfully.")
