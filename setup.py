# -*- coding:utf-8 -*-
import sys
from cx_Freeze import setup, Executable

# 自动检测依赖项，但有时需要手动添加
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI 程序需要不同的base，默认是控制台程序
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("dealWaterData.py", base=base)])