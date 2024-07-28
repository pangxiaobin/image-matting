# backend

## 运行

- 开发环境
  - python 3.12.4
  - node v20.11.0

- 安装依赖
  - pdm 安装 参考 <https://pdm-project.org/zh-cn/latest/>
  - pnpm 安装 参考 <https://pnpm.io/zh/installation>

- 开发模式下运行

- 下载模型

```shell
HF_ENDPOINT=https://hf-mirror.com python hub_model/download.py
```

- 启动服务

```shell
# 运行前端
cd frontend && npm run dev
# 运行后端
cd backend && pmd dev
```

### 打包

- 构建前端

```shell
# 打包前端
pdm build-front
```

- 构建后端

```shell
# 打包后端,可执行文件
pdm build-release

# 构建mac 应用
build-mac-release
```
