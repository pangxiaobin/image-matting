import hashlib
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent


def calculate_sha256(file_path):
    """计算文件的 SHA256 哈希值"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        # 逐块读取文件并更新哈希值
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def download_rmgb_onnx_model(expected_sha256):
    BASE_DIR = Path(".")
    mistral_models_path = BASE_DIR.joinpath("hub_model", "briaai", "RMBG-1.4")
    mistral_models_path.mkdir(parents=True, exist_ok=True)

    model_path = mistral_models_path.joinpath("model.onnx")
    if model_path.exists():
        print("RMBG-1.4 ONNX model already exists.")
        # 校验文件完整性
        calculated_sha256 = calculate_sha256(model_path)
        if calculated_sha256 == expected_sha256:
            print("File integrity check passed.")
        else:
            print(
                "File integrity check failed. Expected SHA256:",
                expected_sha256,
                "Calculated SHA256:",
                calculated_sha256,
            )
            # sha256 校验失败，删除文件
            print("Please delete the file and try again.")
        return

    print("Downloading RMBG-1.4 ONNX model...")
    url = "https://hf-mirror.com/briaai/RMBG-1.4/resolve/main/onnx/model.onnx?download=true"

    response = requests.get(url, stream=True)

    # 获取文件总大小
    total_size = int(response.headers.get("content-length", 0))
    downloaded_size = 0

    with open(model_path, "wb") as f:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)  # 写入文件
            downloaded_size += len(data)  # 更新已下载的字节数

            # 计算下载进度
            progress = (downloaded_size / total_size) * 100
            print(f"\rDownloading: {progress:.2f}%", end="")  # 打印进度，不换行

    print("\nRMBG-1.4 ONNX model downloaded.")

    # 校验文件完整性
    calculated_sha256 = calculate_sha256(model_path)
    if calculated_sha256 == expected_sha256:
        print("File integrity check passed.")
    else:
        print(
            "File integrity check failed. Expected SHA256:",
            expected_sha256,
            "Calculated SHA256:",
            calculated_sha256,
        )


if __name__ == "__main__":
    download_rmgb_onnx_model(
        "8cafcf770b06757c4eaced21b1a88e57fd2b66de01b8045f35f01535ba742e0f"
    )
