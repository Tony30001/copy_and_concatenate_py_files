# copy_and_concatenate_py_files

# 🚀 PyCodeGather: 高级Python代码聚合与整理工具

## 🌟 项目简介

`PyCodeGather` 是一个实用的 Python 脚本，旨在自动化收集、整理和合并 Python 项目中的所有 `.py` 文件。它的主要目标是将一个复杂项目的所有 Python 代码精炼到一个中心文件夹，并将其内容整合进一个易于分析的文本文件。这对于以下场景尤其有用：

- **AI/LLM 代码学习与分析**：将整个项目的代码作为输入，喂给大型语言模型进行代码理解、重构建议、Bug 查找或功能扩展。
- **项目概览与审计**：快速获取项目所有 Python 文件的视图，便于代码审计、风格检查或高层级理解。
- **知识共享与文档准备**：方便地分享项目的全部核心代码，或作为项目技术文档的一部分。
- **备份与归档**：将项目的所有 Python 源文件集中归档，便于管理。

## ✨ 主要功能

- **深度目录搜索**：从脚本所在目录的父目录开始，递归搜索所有子目录中的 `.py` 文件。
- **智能文件复制**：将找到的 `.py` 文件复制到脚本所在的目录，同时：
    - 智能跳过已存在且内容相同（通过大小初步判断）的文件，避免重复。
    - 提示并覆盖目标目录中同名但内容不同的文件。
    - 自动跳过脚本自身，避免循环复制。
- **代码内容合并**：将所有被检测到的 `.py` 文件的代码内容，按照清晰的标记（包含文件路径）顺序合并到一个独立的 `TXT` 文件中。
- **鲁棒的错误处理**：处理文件读写、复制过程中可能出现的权限、编码或未知错误，并提供详细的日志输出。
- **清晰的执行报告**：在脚本执行完毕后，提供复制、跳过、合并和错误的文件统计，让您对操作结果一目了然。

## 🛠️ 如何使用

### 前提条件

- 安装了 Python 3.x 环境。

### 1. 文件放置

将 `copy_and_concatenate_py_files.py` 脚本放置于您 **希望收集代码的父目录** 中的 **任何子目录** 下。

例如，如果您的项目结构如下：

```
MyProject/
├── src/
│   ├── module_a.py
│   └── sub_src/
│       └── module_b.py
├── tests/
│   └── test_c.py
└── scripts/
    └── copy_and_concatenate_py_files.py  <-- 脚本放在这里
```

当 `copy_and_concatenate_py_files.py` 运行时，它会识别 `MyProject` 为其父目录，然后从 `MyProject` 开始搜索所有 `.py` 文件。

最终，`src/module_a.py`, `src/sub_src/module_b.py`, `tests/test_c.py` 以及脚本自身 `scripts/copy_and_concatenate_py_files.py` 的副本和合并内容都将生成或存储在 `scripts/` 目录下。

### 2. 运行脚本

打开命令行或终端，导航到脚本 `copy_and_concatenate_py_files.py` 所在的目录，然后运行：

```bash
python copy_and_concatenate_py_files.py
```

### 3. 查看结果

脚本执行完成后，在 `copy_and_concatenate_py_files.py` 所在的目录下，您会找到：

- **复制的 `.py` 文件**：所有在父目录及其子目录中找到的 `.py` 文件副本。
- **`concatenated_python_code.txt`**：一个文本文件，包含了所有 `.py` 文件的代码内容，每个文件之间有清晰的分隔符和路径标记。

## 📜 输出示例

当脚本运行时，您会在控制台看到类似以下的输出：

```
脚本所在目录 (目标目录): $ /path/to/MyProject/scripts $
将从以下目录及其所有子目录搜索 .py 文件: $ /path/to/MyProject $
所有 .py 文件的代码将合并到: $ /path/to/MyProject/scripts/concatenated_python_code.txt $
------------------------------------------------------------
已复制: $ /path/to/MyProject/src/module_a.py $ -> $ /path/to/MyProject/scripts $
已合并代码: $ /path/to/MyProject/src/module_a.py $
已复制: $ /path/to/MyProject/src/sub_src/module_b.py $ -> $ /path/to/MyProject/scripts $
已合并代码: $ /path/to/MyProject/src/sub_src/module_b.py $
跳过文件 (文件已在目标目录或为脚本自身): $ /path/to/MyProject/scripts/copy_and_concatenate_py_files.py $
已合并代码: $ /path/to/MyProject/scripts/copy_and_concatenate_py_files.py $
------------------------------------------------------------
搜索完成。
成功复制 2 个 .py 文件。
跳过 1 个文件 (已存在或为脚本自身)。
成功合并 3 个 .py 文件的代码到 concatenated_python_code.txt。
发生 0 个错误。
脚本执行完毕。
```

`concatenated_python_code.txt` 文件的内容会是这样：

```
========== Start of file: /path/to/MyProject/src/module_a.py ==========

# module_a.py
def greet(name):
    return f"Hello, {name}!"

========== End of file: /path/to/MyProject/src/module_a.py ==========
--------------------------------------------------------------------------------

========== Start of file: /path/to/MyProject/src/sub_src/module_b.py ==========

# module_b.py
class MyClass:
    def __init__(self, value):
        self.value = value

========== End of file: /path/to/MyProject/src/sub_src/module_b.py ==========
--------------------------------------------------------------------------------

========== Start of file: /path/to/MyProject/scripts/copy_and_concatenate_py_files.py ==========

# (这里是脚本自身的代码内容)
import os
import shutil
# ... 等等

========== End of file: /path/to/MyProject/scripts/copy_and_concatenate_py_files.py ==========
--------------------------------------------------------------------------------
```

## ⚠️ 注意事项

- **目标目录清理**：每次运行脚本时，`concatenated_python_code.txt` 文件都会被清空并重新写入。如果您不希望覆盖目标目录中的 `.py` 文件，请在运行前备份。
- **编码问题**：脚本默认使用 `utf-8` 编码读取和写入文件。如果您的 Python 文件使用其他编码，可能会导致 $UnicodeDecodeError$。脚本会捕获此错误并跳过合并，但您可能需要手动调整文件编码或修改脚本。
- **大文件/大量文件**：对于包含数千个文件或非常大的文件，脚本执行时间可能会较长，且合并的 `TXT` 文件会非常大。
- **非代码文件**：脚本仅处理 `.py` 后缀的文件。其他类型的文件（如 `.txt`, `.md`, `.json` 等）不会被复制或合并。如果您需要处理其他类型的文件，需要修改脚本。

## 🤝 贡献

欢迎任何形式的贡献！如果您有改进建议、Bug 报告或新功能请求，请随时提交 Issue 或 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
```
