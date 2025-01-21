# -*- coding: utf-8 -*-
import os
import shlex
import shutil
import argparse
import platform
import subprocess
from pathlib import Path


def run_cmd(cmd: str, split=False):
    """
    Run command in shell
    """
    if split:
        cmd = shlex.split(cmd)
    return subprocess.run(cmd, shell=True)


def build_zip(version):
    system_name = platform.system().lower()
    if system_name == "darwin":
        platform_name = "mac"
        root_dir = Path("./dist/mac-release")
        base_dir = "小宾AI抠图.app"
    elif system_name == "windows":
        platform_name = "windows"
        root_dir = Path("./dist/release")
        base_dir = "小宾AI抠图"
    else:
        raise ValueError("Unsupported platform")

    zip_filename = f"小宾AI抠图-{platform_name}-v{version}.zip"
    zip_filepath = Path(f"./dist/{zip_filename}")

    # 删除已存在的 zip 文件
    if zip_filepath.exists():
        os.remove(zip_filepath)
    if platform_name == 'mac':
        # 使用命令行 zip 进行压缩，-r 表示递归，-9 表示最高压缩级别
        current_dir = os.getcwd()
        print(f"current_dir: {current_dir}")
        os.chdir(root_dir)  # 切换到源目录
        try:
            print(os.getcwd())
            run_cmd(f"zip -ry -9 {zip_filename} {base_dir}")
            print(f"Created {zip_filename} at {zip_filepath}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            os.chdir(current_dir)  # 切换回原目录
    else:
        shutil.make_archive(
        base_name=zip_filepath.with_suffix(""),
        format="zip",
        root_dir=root_dir,
        base_dir=base_dir,
    )
    


def build_production(version):
    system_name = platform.system().lower()
    if system_name == "darwin":
        platform_name = "mac"
    elif system_name == "windows":
        platform_name = "windows"
    else:
        platform_name = "linux"
    if platform_name == "mac":
        run_cmd("pyinstaller --noconfirm --clean mac_main.spec --distpath dist/mac-release", split=False)
    else:
        run_cmd("pyinstaller --noconfirm --clean main.spec --distpath dist/release", split=False)
    # Create the ZIP file
    build_zip(version)
    

def build_development(version):
    run_cmd("pyinstaller debug.spec --noconfirm", split=False)
    # Create a version file in ./dist/img-matting/
    version_txt_path = Path("./dist/img-matting/version.txt")
    if not version_txt_path.parent.exists():
        version_txt_path.parent.mkdir(parents=True, exist_ok=True)
    with open("./dist/img-matting/version.txt", "w") as f:
        f.write(version)
    with open("./dist/img-matting/DEBUG", "w") as f:
        f.write("1")


def build_frontend():
    if os.name == "nt":
        split = True
    else:
        split = False
    run_cmd("cd '../frontend' && pnpm run build", split=split)
    web_path = Path("./web")
    if web_path.exists():
        shutil.rmtree(web_path)
    web_path.mkdir()
    # 遍历../frontend/dist并将所有文件按路径复制到./web
    for file_path in Path("../frontend/dist").rglob("*"):
        if file_path.is_file():
            target_file_path = Path("./web") / file_path.relative_to("../frontend/dist")
            if not target_file_path.parent.exists():
                target_file_path.parent.mkdir(parents=True)
            shutil.copy(file_path, target_file_path)
    # 遍历../frontend/src/assets/并将所有文件按路径复制到./web/assets/
    for file_path in Path("../frontend/src/assets/").rglob("*"):
        if file_path.is_file():
            target_file_path = Path("./web/assets/") / file_path.relative_to(
                "../frontend/src/assets/"
            )
            if not target_file_path.parent.exists():
                target_file_path.parent.mkdir(parents=True)
            shutil.copy(file_path, target_file_path)


parser = argparse.ArgumentParser(description="Build software.")
parser.add_argument(
    "-v", "--version", default="0.1.0", help="version number, default: 0.1.0"
)
parser.add_argument(
    "-t",
    "--type",
    default="production",
    help="build type: development(d) or production(p) or frontend(f)",
)
args = parser.parse_args()
if args.type == "p" or args.type == "production":
    build_production(args.version)
elif args.type == "d" or args.type == "development":
    build_development(args.version)
elif args.type == "f" or args.type == "frontend":
    build_frontend()
elif args.type == "z" or args.type == "zip":
    build_zip(args.version)
