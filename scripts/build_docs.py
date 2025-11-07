#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文档站点构建和预览脚本

此脚本提供了以下功能：
1. 安装依赖
2. 构建静态文档站点
3. 启动本地预览服务器
4. 清理构建文件
"""

import os
import sys
import subprocess
import argparse
import time

def run_command(command, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        print(e.stderr)
        return False

def install_dependencies():
    """安装文档站点依赖"""
    print("正在安装依赖...")
    if not run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip']):
        return False
    
    requirements_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt')
    if os.path.exists(requirements_file):
        return run_command([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
    else:
        # 如果没有requirements.txt，直接安装必要的包
        packages = ['mkdocs>=1.5.0', 'mkdocs-material>=9.4.0', 'mkdocstrings>=0.24.0']
        return run_command([sys.executable, '-m', 'pip', 'install'] + packages)

def build_docs():
    """构建文档站点"""
    print("正在构建文档站点...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return run_command(['mkdocs', 'build'], cwd=project_root)

def serve_docs(port=8000):
    """启动本地预览服务器"""
    print(f"正在启动本地预览服务器，端口: {port}...")
    print(f"服务器启动后可以访问: http://localhost:{port}")
    print("按 Ctrl+C 停止服务器")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return run_command(['mkdocs', 'serve', '--dev-addr', f'localhost:{port}'], cwd=project_root)

def clean_docs():
    """清理构建文件"""
    print("正在清理构建文件...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_dir = os.path.join(project_root, 'site')
    
    if os.path.exists(site_dir):
        import shutil
        try:
            shutil.rmtree(site_dir)
            print(f"已删除构建目录: {site_dir}")
            return True
        except Exception as e:
            print(f"清理构建目录失败: {e}")
            return False
    else:
        print("构建目录不存在，无需清理")
        return True

def main():
    parser = argparse.ArgumentParser(description='文档站点构建和预览工具')
    
    parser.add_argument('--install', action='store_true', help='安装依赖')
    parser.add_argument('--build', action='store_true', help='构建文档站点')
    parser.add_argument('--serve', action='store_true', help='启动本地预览服务器')
    parser.add_argument('--clean', action='store_true', help='清理构建文件')
    parser.add_argument('--port', type=int, default=8000, help='预览服务器端口，默认8000')
    parser.add_argument('--all', action='store_true', help='执行安装、构建和预览完整流程')
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，显示帮助信息
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # 执行指定的操作
    success = True
    
    if args.all or args.install:
        success = install_dependencies() and success
    
    if args.all or args.clean:
        success = clean_docs() and success
    
    if args.all or args.build:
        success = build_docs() and success
    
    if args.all or args.serve:
        # 服务是阻塞的，所以放在最后
        success = serve_docs(args.port) and success
    
    if success:
        print("\n操作完成！")
    else:
        print("\n操作失败，请查看错误信息。")
        sys.exit(1)

if __name__ == '__main__':
    main()