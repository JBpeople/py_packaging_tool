#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import json
import datetime

class HelloWorldApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hello World Test App")
        self.root.geometry("300x200")
        
        # 创建界面
        label = tk.Label(self.root, text="这是一个测试应用", font=("Arial", 12))
        label.pack(pady=20)
        
        button = tk.Button(self.root, text="点击我", command=self.on_click)
        button.pack(pady=10)
        
        info_button = tk.Button(self.root, text="显示信息", command=self.show_info)
        info_button.pack(pady=10)
        
        quit_button = tk.Button(self.root, text="退出", command=self.root.quit)
        quit_button.pack(pady=10)
        
    def on_click(self):
        messagebox.showinfo("消息", "Hello World! 打包工具测试成功!")
        
    def show_info(self):
        info = {
            "应用名称": "Hello World Test App",
            "当前时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Python版本": "3.x",
            "状态": "运行正常"
        }
        info_str = json.dumps(info, ensure_ascii=False, indent=2)
        messagebox.showinfo("应用信息", info_str)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HelloWorldApp()
    app.run()