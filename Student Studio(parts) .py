
import csv
import ctypes
import os
import sys
import math
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, font as tkfont, messagebox, simpledialog, ttk

from score_manager import stu_score_lis



# ===================== 视觉主题 =====================
BG = "#0A1020"
SIDEBAR = "#0E192B"
PANEL = "#121F34"
CARD = "#172740"
CARD_HOVER = "#203653"
BORDER = "#263B59"
BLUE = "#398BFF"
CYAN = "#25C6D7"
PURPLE = "#A58BFF"
ORANGE = "#F2AE55"
GREEN = "#28C797"
RED = "#E66A79"
WHITE = "#EDF4FF"
MUTED = "#8EA3C0"
DARK_TEXT = "#071321"
FONT = "Microsoft YaHei UI" if sys.platform == "win32" else "Noto Sans CJK SC"

def enable_windows_dpi_awareness():
    """让 Tk 窗口按真实显示器 DPI 绘制，避免 Windows 位图缩放造成文字发虚。"""
    if sys.platform != "win32":
        return
    try:
        # Windows 10+：优先使用 Per-Monitor V2。
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
        return
    except Exception:
        pass
    try:
        # Windows 8.1 兼容方案。
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except Exception:
        pass
    try:
        # 更旧 Windows 的回退方案。
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


enable_windows_dpi_awareness()

manager = stu_score_lis()
root = tk.Tk()
root.title("STUDENT STUDIO  |  学生成绩管理系统")
root.geometry("1700x1060")
root.configure(bg=BG)

# 选择本机真实存在的无衬线界面字体，避免缺字时回退到衬线字体。
try:
    available_fonts = {name.casefold(): name for name in tkfont.families(root)}
    preferred_fonts = (
        ("Microsoft YaHei UI", "Microsoft YaHei", "微软雅黑", "Segoe UI")
        if sys.platform == "win32"
        else ("Noto Sans CJK SC", "Noto Sans CJK JP", "DejaVu Sans")
    )
    FONT = next((available_fonts[name.casefold()] for name in preferred_fonts
                 if name.casefold() in available_fonts), FONT)
except Exception:
    pass

try:
    manager.load_scores()
except Exception as error:
    messagebox.showerror("数据读取失败", f"无法读取成绩文件：\n{error}\n\n原文件不会被自动覆盖。")
    root.destroy()
    raise SystemExit

current_page = "控制面板"
active_save_handler = None
page_body = None
page_title = None
page_subtitle = None
nav_buttons = {}


# ===================== 主窗口骨架 =====================
shell = tk.Frame(root, bg=BG)
shell.pack(fill="both", expand=True)
sidebar = tk.Frame(shell, bg=SIDEBAR, width=380)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

brand = tk.Frame(sidebar, bg=SIDEBAR)
brand.pack(fill="x", padx=23, pady=(28, 29))
brand_mark = tk.Frame(brand, bg=SIDEBAR)
brand_mark.pack(anchor="w")
label(brand_mark, "◈", 22, CYAN, True, bg=SIDEBAR).pack(side="left")
label(brand_mark, "STUDENT", 17, CYAN, True, bg=SIDEBAR).pack(side="left", padx=(8, 0))
label(brand, "STUDIO", 14, WHITE, True).pack(anchor="w", padx=(34, 0), pady=(0, 1))
label(brand, "ACADEMIC DATA WORKSPACE", 7, MUTED, True).pack(anchor="w", padx=(3, 0), pady=(7, 0))

nav_label = tk.Frame(sidebar, bg=SIDEBAR)
nav_label.pack(fill="x", padx=22, pady=(0, 10))
label(nav_label, "WORKSPACE", 8, "#7189A8", True).pack(side="left")
label(nav_label, "工作空间", 8, MUTED).pack(side="left", padx=(8, 0))

nav_specs = [
    ("⌂", "控制面板", "总览、设置与快捷操作"),
    ("▦", "成绩列表", "所有考试成绩表"),
    ("＋", "成绩录入", "创建或继续编辑"),
    ("◉", "成绩分析", "图表与数据洞察"),
]
for icon, name, hint in nav_specs:
    nav = tk.Frame(sidebar, bg=SIDEBAR, padx=11, pady=10,
                   highlightthickness=1, highlightbackground=SIDEBAR)
    nav.pack(fill="x", padx=12, pady=4)
    icon_box = tk.Frame(nav, bg="#172A43", width=38, height=38)
    icon_box.pack(side="left")
    icon_box.pack_propagate(False)
    icon_label = label(icon_box, icon, 17, "#A9BED8", True, bg="#172A43")
    icon_label.place(relx=.5, rely=.5, anchor="center")
    text_area = tk.Frame(nav, bg=SIDEBAR)
    text_area.pack(side="left", fill="x", expand=True, padx=(11, 4))
    title_label = label(text_area, name, 10, WHITE, True, bg=SIDEBAR)
    title_label.pack(anchor="w")
    hint_label = label(text_area, hint, 8, MUTED, bg=SIDEBAR)
    hint_label.pack(anchor="w", pady=(3, 0))
    arrow_label = label(nav, "›", 18, "#6F86A4", True, bg=SIDEBAR)
    arrow_label.pack(side="right", padx=(2, 3))
    parts = {"frame": nav, "icon_box": icon_box, "icon": icon_label,
             "text_area": text_area, "title": title_label,
             "hint": hint_label, "arrow": arrow_label}
    nav_buttons[name] = parts