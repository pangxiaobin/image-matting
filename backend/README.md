# backend

## 运行

- 开发环境
  - python 3.12.4
  - node v20.11.0

- 安装依赖
  - pdm 安装 参考 <https://pdm-project.org/zh-cn/latest/>
  - pnpm 安装 参考 <https://pnpm.io/zh/installation>

- 开发模式下运行
  - 安装后端依赖

    ```shell
    cd backend
    pdm install
    ```

  - 安装前端依赖

    ```shell
    cd frontend
    pnpm install
    ```

  - 下载模型
  
    - mac

      ```shell
      # 激活虚拟环境
      cd backend
      source .venv/bin/activate
      HF_ENDPOINT=https://hf-mirror.com python hub_model/download.py
      ```

    - windows

      ```shell
      # windows
      # 激活虚拟环境
      cd backend
      .venv\Scripts\activate
      # 下载模型
      $env:HF_ENDPOINT = "https://hf-mirror.com"
      python .\hub_model\download.py
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
# 如果你构建pdm环境时，没有选择python版本，需要修改main.spec中的内容，根据自己情况找到虚拟环境中的tinify路径
('./.venv/lib/python3.12/site-packages/tinify', 'tinify')  --》 ('./.venv/lib/site-packages/tinify', 'tinify')

# 打包后端,可执行文件
pdm build-release

# 构建mac 应用
pdm build-mac-release
```
