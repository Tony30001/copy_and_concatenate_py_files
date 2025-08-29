import os
import shutil
import sys


def copy_and_concatenate_py_files():
    """
    搜索脚本所在文件夹的父文件夹下的所有子目录中的 .py 文件，
    将其复制到脚本所在的文件夹，并将其代码内容合并到一个 TXT 文件中。
    """
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)

    # 获取脚本所在的目录 (目标目录)
    destination_folder = os.path.dirname(script_path)

    # 获取脚本所在目录的父目录 (搜索的根目录)
    search_root = os.path.dirname(destination_folder)

    # 定义合并代码的 TXT 文件名和路径
    output_txt_filename = "concatenated_python_code.txt"
    output_txt_path = os.path.join(destination_folder, output_txt_filename)

    print(f"脚本所在目录 (目标目录): $ {destination_folder} $")
    print(f"将从以下目录及其所有子目录搜索 .py 文件: $ {search_root} $")
    print(f"所有 .py 文件的代码将合并到: $ {output_txt_path} $")
    print("-" * 60)

    copied_count = 0
    skipped_count = 0
    concatenated_count = 0
    error_count = 0

    # 使用 'w' 模式打开 TXT 文件，如果文件存在则清空，确保每次运行都是全新的合并
    # 使用 'utf-8' 编码以支持大多数 Python 文件
    try:
        with open(output_txt_path, 'w', encoding='utf-8') as outfile:
            # 遍历搜索根目录及其所有子目录
            for dirpath, dirnames, filenames in os.walk(search_root):
                for filename in filenames:
                    # 检查文件是否以 .py 结尾
                    if filename.lower().endswith('.py'):
                        source_file_path = os.path.join(dirpath, filename)
                        destination_file_path = os.path.join(destination_folder, filename)

                        # --- 文件复制逻辑 ---
                        # 避免将文件复制到它自己 (如果脚本本身是 .py 文件且在搜索路径中)
                        # 或者避免将文件复制到目标目录中已存在的同名文件（如果它们是同一个文件）
                        try:
                            if os.path.samefile(source_file_path, destination_file_path):
                                print(f"跳过文件 (文件已在目标目录或为脚本自身): $ {source_file_path} $")
                                skipped_count += 1
                                # 即使跳过复制，我们仍然可以合并其代码
                                pass
                        except FileNotFoundError:
                            # 如果目标文件不存在，os.path.samefile 会抛出 FileNotFoundError
                            # 这表示源文件和目标文件不可能是同一个文件，可以继续处理
                            pass
                        except Exception as e:
                            print(
                                f"检查文件 $ {source_file_path} $ 与 $ {destination_file_path} $ 是否相同时发生错误: $ {e} $")
                            error_count += 1
                            continue  # 跳过当前文件，避免后续操作出错

                        try:
                            # 检查目标目录是否已存在同名文件
                            if os.path.exists(destination_file_path):
                                # 进一步检查文件内容是否相同，避免不必要的复制和覆盖
                                # 简单比较文件大小，更严格的可以比较哈希值
                                if os.path.getsize(source_file_path) == os.path.getsize(destination_file_path):
                                    print(f"跳过文件 (目标目录已存在同名且同大小文件): $ {filename} $")
                                    skipped_count += 1
                                else:
                                    print(f"目标目录已存在同名文件 $ {filename} $，但大小不同，将覆盖。")
                                    shutil.copy2(source_file_path, destination_folder)
                                    print(f"已覆盖并复制: $ {source_file_path} $ -> $ {destination_folder} $")
                                    copied_count += 1
                            else:
                                # 复制文件，shutil.copy2 会保留文件的元数据 (如修改时间)
                                shutil.copy2(source_file_path, destination_folder)
                                print(f"已复制: $ {source_file_path} $ -> $ {destination_folder} $")
                                copied_count += 1
                        except shutil.Error as e:
                            print(f"复制文件 $ {source_file_path} $ 时发生 shutil 错误: $ {e} $")
                            error_count += 1
                        except OSError as e:
                            print(f"复制文件 $ {source_file_path} $ 时发生操作系统错误 (权限/路径问题): $ {e} $")
                            error_count += 1
                        except Exception as e:
                            print(f"处理文件 $ {source_file_path} $ 时发生未知错误: $ {e} $")
                            error_count += 1

                        # --- 代码合并逻辑 ---
                        try:
                            # 读取 .py 文件的内容
                            with open(source_file_path, 'r', encoding='utf-8') as infile:
                                content = infile.read()

                            # 写入标题和文件内容到合并的 TXT 文件
                            outfile.write(f"\n\n{'=' * 10} Start of file: $ {source_file_path} $ {'=' * 10}\n\n")
                            outfile.write(content)
                            outfile.write(f"\n\n{'=' * 10} End of file: $ {source_file_path} $ {'=' * 10}\n")
                            outfile.write("-" * 80 + "\n\n")  # 添加一个分隔符
                            concatenated_count += 1
                            print(f"已合并代码: $ {source_file_path} $")

                        except UnicodeDecodeError:
                            print(f"警告: 无法以 UTF-8 编码读取文件 $ {source_file_path} $，跳过代码合并。")
                            error_count += 1
                        except IOError as e:
                            print(f"错误: 无法读取文件 $ {source_file_path} $ 进行代码合并: $ {e} $")
                            error_count += 1
                        except Exception as e:
                            print(f"合并文件 $ {source_file_path} $ 代码时发生未知错误: $ {e} $")
                            error_count += 1

        print("-" * 60)
        print(f"搜索完成。")
        print(f"成功复制 $ {copied_count} $ 个 .py 文件。")
        print(f"跳过 $ {skipped_count} $ 个文件 (已存在或为脚本自身)。")
        print(f"成功合并 $ {concatenated_count} $ 个 .py 文件的代码到 $ {output_txt_filename} $。")
        print(f"发生 $ {error_count} $ 个错误。")
        print("脚本执行完毕。")

    except IOError as e:
        print(f"致命错误: 无法创建或写入合并文件 $ {output_txt_path} $: $ {e} $")
    except Exception as e:
        print(f"创建或写入合并文件时发生未知错误: $ {e} $")


if __name__ == "__main__":
    copy_and_concatenate_py_files()
