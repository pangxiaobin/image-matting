# -*- coding: utf-8 -*-
# 应用名称
app_name = "小宾AI抠图"

version = "V0.2.5"
# DMG 输出文件名
filename = f"[mac]-{app_name}-{version}.dmg"

# 设置卷名
volume_name = f"{app_name} {version} installer"

# 目标应用路径
app_path = "./dist/mac-release/小宾AI抠图.app"


# 应用程序图标
icon = "./assets/icon.icns"

# DMG 的体积大小，根据实际应用大小调整
# 放入 .app 文件和 Applications 链接
files = [
    (app_path, "小宾AI抠图.app"),
    "./assets/小宾AI抠图.webloc",
]

symlinks = {"Applications": "/Applications"}

# DMG 详细配置
window_rect = ((200, 200), (590, 416))  # 使窗口大小与背景图匹配

icon_locations = {
    "小宾AI抠图.app": (160, 120),
    "Applications": (430, 120),
    "小宾AI抠图.webloc": (450, 243),
}

icon_size = 60
text_size = 12
format = "UDBZ"
