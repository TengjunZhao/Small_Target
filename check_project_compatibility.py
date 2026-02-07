#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3.9.7 兼容性检查脚本（仅检查项目源码）
专门检查我们自己编写的Python文件的3.9兼容性
"""

import ast
import sys
import os
from pathlib import Path

def check_python_39_compatibility(file_path):
    """检查单个Python文件的3.9兼容性"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
        # 检查match-case语句（Python 3.10+特性）
        if 'match ' in content and ' case ' in content:
            # 找到具体的行号
            for i, line in enumerate(lines, 1):
                if 'match ' in line and ' case ' in content:
                    issues.append(f"第{i}行: 使用了match-case语句（Python 3.10+特性）")
                    break
        
        # 检查海象运算符 := （Python 3.8+支持，3.9完全兼容）
        # 这个是兼容的，不需要报告
        
        # 检查f-string（Python 3.6+支持，3.9完全兼容）
        # 这些都是兼容的
        
        # 检查typing模块的现代用法
        if 'from typing import Literal' in content:
            issues.append("使用了Literal类型注解（建议使用typing-extensions或传统方式）")
            
        if 'from typing import TypedDict' in content:
            issues.append("使用了TypedDict（建议使用typing-extensions或传统方式）")
            
        # 检查__future__导入（通常是安全的）
        if 'from __future__ import annotations' in content:
            issues.append("使用了__future__.annotations（在Python 3.9中可用但需要注意）")
            
        # 检查union类型语法 | （Python 3.10+特性）
        for i, line in enumerate(lines, 1):
            # 排除注释和字符串中的情况
            if '|' in line and not line.strip().startswith('#'):
                # 检查是否是类型注解中的union语法
                if 'int | str' in line or 'str | None' in line or 'x | y' in line:
                    issues.append(f"第{i}行: 可能使用了Python 3.10+的union类型语法 '|' ")
                    break
                    
    except Exception as e:
        issues.append(f"文件读取错误: {str(e)}")
    
    return issues

def scan_project_source_code(project_root):
    """扫描项目源码检查兼容性"""
    print(f"🔍 正在检查项目源码的Python 3.9.7兼容性...")
    print("=" * 60)
    
    # 定义项目源码目录
    source_dirs = [
        "BackEnd",
        "Utils"
    ]
    
    incompatible_files = []
    compatible_files = []
    
    # 检查每个源码目录
    for src_dir in source_dirs:
        dir_path = Path(project_root) / src_dir
        if not dir_path.exists():
            continue
            
        print(f"\n📁 检查目录: {src_dir}")
        print("-" * 40)
        
        # 收集该目录下的Python文件
        py_files = list(dir_path.rglob("*.py"))
        
        # 排除虚拟环境和第三方包
        project_py_files = [
            f for f in py_files 
            if '.venv' not in str(f) and 'site-packages' not in str(f)
        ]
        
        for py_file in project_py_files:
            relative_path = py_file.relative_to(project_root)
            issues = check_python_39_compatibility(py_file)
            
            if issues:
                incompatible_files.append((relative_path, issues))
                print(f"❌ {relative_path}:")
                for issue in issues:
                    print(f"   • {issue}")
            else:
                compatible_files.append(relative_path)
                print(f"✅ {relative_path}")
    
    print("\n" + "=" * 60)
    print("📊 检查结果汇总:")
    print(f"总文件数: {len(compatible_files) + len(incompatible_files)}")
    print(f"兼容的文件: {len(compatible_files)}")
    print(f"有问题的文件: {len(incompatible_files)}")
    
    if incompatible_files:
        print("\n⚠️  发现兼容性问题:")
        for file_path, issues in incompatible_files:
            print(f"\n📁 {file_path}:")
            for issue in issues:
                print(f"   • {issue}")
        
        print("\n💡 解决方案建议:")
        print("1. 将match-case语句替换为传统的if-elif结构")
        print("2. 使用typing.Union代替 | 语法")
        print("3. 对于Literal和TypedDict，考虑使用typing-extensions包")
        print("4. __future__.annotations通常是安全的，但要注意类型检查工具的兼容性")
        
        return False
    else:
        print("\n🎉 恭喜！项目源码完全兼容Python 3.9.7！")
        return True

if __name__ == "__main__":
    # 获取项目根目录
    project_root = Path(__file__).parent.absolute()
    is_compatible = scan_project_source_code(project_root)
    
    # 返回适当的退出码
    sys.exit(0 if is_compatible else 1)