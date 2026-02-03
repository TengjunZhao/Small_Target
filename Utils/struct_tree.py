import os
import pathspec
from argparse import ArgumentParser
from typing import Set


def load_gitignore(gitignore_path: str = ".gitignore") -> pathspec.PathSpec:
    """
    加载并解析.gitignore文件，返回路径匹配器
    :param gitignore_path: .gitignore文件路径，默认当前目录
    :return: 路径匹配器对象
    """
    # 如果没有.gitignore文件，返回空规则（不过滤任何内容）
    if not os.path.exists(gitignore_path):
        print(f"提示：未找到{gitignore_path}，将生成完整树形结构")
        return pathspec.PathSpec.from_lines("gitwildmatch", [])

    # 读取.gitignore并解析规则
    with open(gitignore_path, "r", encoding="utf-8") as f:
        gitignore_lines = f.readlines()

    # 构建匹配器（适配gitignore语法）
    spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_lines)
    return spec


# 定义需要忽略具体内容的大型目录集合
IGNORE_CONTENT_DIRS: Set[str] = {
    "venv",
    "env", 
    "node_modules",
    "__pycache__",
    ".idea",
    ".vscode"
}

def should_ignore_content(dir_name: str) -> bool:
    """
    判断是否应该忽略目录的具体内容
    :param dir_name: 目录名称
    :return: 是否忽略内容
    """
    return dir_name in IGNORE_CONTENT_DIRS

def generate_tree(
        root_dir: str = ".",
        spec: pathspec.PathSpec = None,
        prefix: str = "",
        is_last: bool = True,
        output_lines: list = None,
        ignore_content_dirs: Set[str] = None
) -> None:
    """
    递归生成文件树形结构（过滤.gitignore规则）
    :param root_dir: 根目录，默认当前目录
    :param spec: .gitignore规则匹配器
    :param prefix: 缩进前缀（内部递归使用）
    :param is_last: 是否是最后一个节点（内部递归使用）
    :param output_lines: 存储输出行的列表（内部递归使用）
    """
    if output_lines is None:
        output_lines = []
    if ignore_content_dirs is None:
        ignore_content_dirs = IGNORE_CONTENT_DIRS

    # 处理根目录路径（规范化）
    root_dir = os.path.abspath(root_dir)
    # 获取当前目录下的所有文件/目录，按名称排序
    entries = sorted(os.listdir(root_dir), key=lambda x: (not os.path.isdir(os.path.join(root_dir, x)), x))

    # 过滤.gitignore匹配的路径
    filtered_entries = []
    for entry in entries:
        # 拼接完整路径，转换为相对路径（匹配.gitignore规则）
        entry_path = os.path.join(root_dir, entry)
        rel_path = os.path.relpath(entry_path, start=os.path.dirname(root_dir))
        # 跳过.git目录（默认过滤）
        if entry == ".git":
            continue
        # 如果匹配.gitignore规则，跳过
        if spec and spec.match_file(rel_path):
            continue
        filtered_entries.append(entry)

    # 遍历过滤后的条目，生成树形
    for idx, entry in enumerate(filtered_entries):
        entry_path = os.path.join(root_dir, entry)
        is_entry_last = idx == len(filtered_entries) - 1

        # 构建树形符号
        if is_last:
            current_prefix = prefix + "    "
        else:
            current_prefix = prefix + "│   "

        # 节点符号：├── 或 └──
        node_symbol = "└── " if is_entry_last else "├── "
        line = prefix + node_symbol + entry

        # 如果是目录，添加/标识
        if os.path.isdir(entry_path):
            line += "/"

        output_lines.append(line)
        print(line)  # 实时打印到控制台

        # 递归处理子目录
        if os.path.isdir(entry_path):
            # 如果是需要忽略内容的目录，只显示目录名，不展开内容
            if should_ignore_content(entry):
                # 添加省略号表示内容被忽略
                ellipsis_line = current_prefix + "└── [...]"
                output_lines.append(ellipsis_line)
                print(ellipsis_line)
            else:
                generate_tree(
                    root_dir=entry_path,
                    spec=spec,
                    prefix=current_prefix,
                    is_last=is_entry_last,
                    output_lines=output_lines,
                    ignore_content_dirs=ignore_content_dirs
                )

    return output_lines


def main():
    """主函数：解析参数，执行生成逻辑"""
    # 解析命令行参数
    parser = ArgumentParser(description="生成过滤.gitignore规则的文件树形结构")
    parser.add_argument("--dir", default="..", help="目标目录（默认当前目录）")
    parser.add_argument("--gitignore", default=".gitignore", help=".gitignore文件路径（默认当前目录）")
    parser.add_argument("--output", help="导出文件路径（如tree.md，可选）")
    parser.add_argument("--ignore-dirs", nargs='*', default=[], 
                       help="额外要忽略内容的目录名称（如 '.git' 'build'），默认忽略 venv node_modules 等")
    args = parser.parse_args()

    # 加载.gitignore规则
    spec = load_gitignore(args.gitignore)
    
    # 合并默认忽略目录和用户指定的忽略目录
    ignore_dirs_set = IGNORE_CONTENT_DIRS.copy()
    ignore_dirs_set.update(set(args.ignore_dirs))
    
    # 生成树形结构
    print(f"\n📁 生成 {args.dir} 的文件树形结构（已过滤.gitignore规则）：\n")
    output_lines = generate_tree(root_dir=args.dir, spec=spec, ignore_content_dirs=ignore_dirs_set)

    # 导出到文件（如果指定）
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            # 包裹成Markdown代码块，方便直接复制到MarkText
            f.write("```\n")
            f.write("\n".join(output_lines))
            f.write("\n```")
        print(f"\n✅ 树形结构已导出到：{os.path.abspath(args.output)}")
    
    # 显示忽略的目录信息
    if args.ignore_dirs or IGNORE_CONTENT_DIRS:
        print(f"\n📋 已忽略内容的目录: {', '.join(sorted(ignore_dirs_set))}")


if __name__ == "__main__":
    main()