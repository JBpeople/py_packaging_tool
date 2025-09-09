# Python项目打包工具

一个基于wxPython的图形化Python项目打包工具，使用PyInstaller将Python项目打包成可执行文件(.exe)。

## 功能特性

- 🖥️ **图形化界面**: 基于wxPython的直观易用的GUI界面
- 📦 **自动打包**: 使用PyInstaller自动将Python项目打包成可执行文件
- 🔧 **灵活配置**: 支持多种打包选项配置
- 📋 **依赖管理**: 自动处理项目依赖和环境隔离
- 📝 **实时日志**: 提供详细的打包过程日志输出
- 🎯 **多平台支持**: 支持Windows、macOS和Linux平台

## 主要功能

### 项目配置
- 选择项目根目录
- 指定入口文件（主程序文件）
- 配置requirements.txt依赖文件

### 打包选项
- **单文件模式**: 将所有文件打包成一个可执行文件
- **窗口模式**: 打包为GUI应用（无控制台窗口）
- **控制台模式**: 保留控制台输出
- **自定义图标**: 为可执行文件设置图标
- **自定义名称**: 设置输出文件名

### 环境管理
- 自动创建虚拟环境
- 安装项目依赖
- 隔离打包环境

## 安装要求

- Python 3.7+
- wxPython >= 4.2.1
- PyInstaller >= 5.13.0

## 安装方法

1. 克隆项目到本地：
```bash
git clone https://github.com/your-username/py_packaging_tool.git
cd py_packaging_tool
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行主程序：
```bash
python src/main.py
```

2. 在图形界面中配置项目：
   - 点击"选择目录"选择项目根目录
   - 点击"选择文件"选择入口文件（通常是main.py或app.py）
   - 选择requirements.txt文件（可选）

3. 配置打包选项：
   - 勾选需要的打包选项（单文件、窗口模式等）
   - 设置输出文件名和图标（可选）

4. 点击"开始打包"按钮开始打包过程

5. 等待打包完成，查看日志输出

6. 打包完成后，可执行文件将生成在项目的`dist`目录中

## 示例项目

项目中包含了一个示例项目`test_project`，展示了如何使用这个工具：

- `hello_world.py`: 一个简单的Tkinter GUI应用
- `requirements.txt`: 项目依赖文件
- `dist/`: 打包后的可执行文件输出目录

## 支持的打包选项

| 选项 | 说明 |
|------|------|
| `--onefile` | 打包成单个可执行文件 |
| `--windowed` | 无控制台窗口的GUI应用 |
| `--noconsole` | 不显示控制台窗口 |
| `--icon` | 设置可执行文件图标 |
| `--name` | 设置输出文件名 |

## 项目结构

```
py_packaging_tool/
├── src/
│   └── main.py              # 主程序文件
├── test_project/            # 示例项目
│   ├── hello_world.py       # 示例应用
│   ├── requirements.txt     # 依赖文件
│   └── dist/                # 打包输出目录
├── requirements.txt         # 工具依赖
└── README.md               # 说明文档
```

## 注意事项

1. **虚拟环境**: 工具会自动在项目目录下创建`venv_packaging`虚拟环境
2. **依赖安装**: 确保requirements.txt文件格式正确
3. **路径问题**: 避免项目路径中包含中文字符或特殊符号
4. **权限问题**: 在某些系统上可能需要管理员权限来创建虚拟环境

## 常见问题

### Q: 打包失败怎么办？
A: 检查日志输出中的错误信息，常见问题包括：
- 依赖文件路径错误
- 入口文件不存在
- 虚拟环境创建失败

### Q: 打包后的文件很大？
A: 这是正常现象，PyInstaller会包含Python解释器和所有依赖库。可以使用`--onefile`选项来减少文件数量。

### Q: 支持哪些Python版本？
A: 支持Python 3.7及以上版本。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的图形化打包功能
- 支持多种打包选项配置
- 提供示例项目