# Pipenv

**Pipenv** 是 Python 的依赖管理和虚拟环境工具，它将 `pip` 和 `virtualenv` 的功能整合在一起，并引入了类似 npm 的依赖锁机制（`Pipfile.lock`）。以下是详细说明和 FastAPI 的安装示例：

------

## 一、**Pipenv 的核心功能**

1. **自动创建虚拟环境**：无需手动激活 `venv`，自动隔离项目依赖。
2. 依赖管理：
   - 用 `Pipfile` 记录依赖（替代 `requirements.txt`）。
   - 用 `Pipfile.lock` 锁定依赖版本（确保环境一致性）。
3. **开发依赖分离**：区分生产依赖（`[packages]`）和开发依赖（`[dev-packages]`）。

------

## 二、**安装 Pipenv**

```bash
# 全局安装（确保 Python 已安装）
pip install pipenv
```

------

## 三、**使用 Pipenv 创建 FastAPI 项目**

### 1. 创建项目目录并初始化环境

```bash
mkdir fastapi-demo && cd fastapi-demo

# 初始化虚拟环境（自动生成 Pipfile）
pipenv install --python 3.9  # 指定 Python 版本（可选）
```

### 2. 安装 FastAPI 和 Uvicorn

```bash
# 安装生产依赖
pipenv install fastapi

# 安装开发依赖（如测试工具，可选）
pipenv install uvicorn --dev  # Uvicorn 是 ASGI 服务器，用于运行 FastAPI
```

### 3. 编写示例代码

创建文件 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### 4. 运行 FastAPI 服务

```bash
# 在 Pipenv 环境中启动服务（自动激活虚拟环境）
pipenv run uvicorn main:app --reload
```

- 访问 `http://localhost:8000` 查看接口。
- 访问 `http://localhost:8000/docs` 查看自动生成的 Swagger 文档。

------

## 四、**Pipenv 常用命令**

|            命令             |               作用               |
| :-------------------------: | :------------------------------: |
|      `pipenv install`       |   安装所有依赖（根据 Pipfile）   |
|    `pipenv install <包>`    |    安装生产依赖并更新 Pipfile    |
| `pipenv install <包> --dev` |           安装开发依赖           |
|   `pipenv uninstall <包>`   |             卸载依赖             |
|       `pipenv shell`        |    激活虚拟环境的交互式 Shell    |
|     `pipenv run <命令>`     | 直接运行命令（无需手动激活环境） |
|        `pipenv lock`        |      生成/更新 Pipfile.lock      |
|       `pipenv graph`        |            查看依赖树            |

------

## 五、**目录结构及文件说明**

```bash
fastapi-demo/
├── Pipfile       # 记录依赖配置（类似 package.json）
├── Pipfile.lock  # 锁定精确依赖版本（类似 package-lock.json）
└── main.py       # FastAPI 代码
```

------

## 六、**Pipenv vs 传统工具**

|     操作     |      传统方式（pip + venv）       |                Pipenv                |
| :----------: | :-------------------------------: | :----------------------------------: |
| **创建环境** |      `python -m venv myenv`       |       自动创建（无需手动操作）       |
| **安装依赖** | `pip install -r requirements.txt` |           `pipenv install`           |
| **记录依赖** |    手动维护 `requirements.txt`    | 自动更新 `Pipfile` 和 `Pipfile.lock` |
| **依赖锁定** |  `pip freeze > requirements.txt`  |       自动生成 `Pipfile.lock`        |

------

## 七、**注意事项**

1. 跨平台兼容性：
   - Windows 系统可能需要启用脚本执行权限（若遇到权限错误，尝试以管理员身份运行终端）。
2. 依赖冲突：
   - 若安装失败，检查 `Pipfile` 中的版本约束，或手动指定版本（如 `pipenv install fastapi==0.68.0`）。
3. 环境位置：
   - Pipenv 默认将虚拟环境存储在用户目录下（可通过 `pipenv --venv` 查看路径）。