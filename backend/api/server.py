from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import threading
from hub_model import segmentation
from utilities.utils import image_obj_to_base64
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import applications

def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.9.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.9.0/swagger-ui.min.css")

applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(
    title="AI Matting API",
    description="API for AI-based image matting without authentication.",
    version="1.0.0",
    docs_url="/api/docs",  # Custom URL for Swagger documentation
    redoc_url="/api/redoc", # Custom URL for ReDoc documentationI
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MattingRequest(BaseModel):
    """
    抠图请求
    """
    image_path: str = Field(..., description="本地路径、URL地址和图片Base64值")

    @field_validator('image_path')
    def validate_image_path(cls, image_path: str):
        if not Path(image_path).exists():
            raise ValueError("Image path does not exist")
        return image_path

class MattingResponse(BaseModel):
    status: str = Field(..., description="状态")
    no_bg_image: str = Field(..., description="抠图后的图片Base64值")


@app.post("/api/ai/matting", response_model=MattingResponse)
async def matting(request: MattingRequest ):
    no_bg_image = segmentation.segment_image(request.image_path)
    try:
        no_bg_image_base64 = image_obj_to_base64(no_bg_image)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    return {"status": "success", "no_bg_image": no_bg_image_base64}


class APIServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 11111):
        self.host = host
        self.port = port
        self.server_thread: Optional[threading.Thread] = None
        self.should_exit = threading.Event()

    def start(self):
        """在新线程中启动FastAPI服务器"""
        self.server_thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self.server_thread.start()

    def _run_server(self):
        """运行FastAPI服务器"""
        config = uvicorn.Config(
            app=app,
            host=self.host,
            port=self.port,
            limit_concurrency=1000,  # 限制并发连接数
            timeout_keep_alive=30,  # keepalive超时时间
            log_level="info"
        )
        server = uvicorn.Server(config)
        server.run()

    def stop(self):
        """停止FastAPI服务器"""
        self.should_exit.set()
        if self.server_thread:
            self.server_thread.join(timeout=1.0)

