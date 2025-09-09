#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import threading
from pathlib import Path

import wx


class PackagingTool(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Python项目打包工具", size=(800, 600))

        self.project_path = ""
        self.entry_file = ""
        self.requirements_file = ""

        self.init_ui()
        self.Center()

    def init_ui(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 标题
        title = wx.StaticText(panel, label="Python项目打包工具")
        title_font = title.GetFont()
        title_font.PointSize += 4
        title_font = title_font.Bold()
        title.SetFont(title_font)
        main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)

        # 文件选择区域
        file_box = wx.StaticBox(panel, label="项目文件配置")
        file_sizer = wx.StaticBoxSizer(file_box, wx.VERTICAL)

        # 项目路径选择
        project_sizer = wx.BoxSizer(wx.HORIZONTAL)
        project_sizer.Add(wx.StaticText(panel, label="项目路径:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.project_path_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        project_sizer.Add(self.project_path_text, 1, wx.EXPAND | wx.ALL, 5)
        self.project_path_btn = wx.Button(panel, label="选择目录")
        project_sizer.Add(self.project_path_btn, 0, wx.ALL, 5)
        file_sizer.Add(project_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 入口文件选择
        entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        entry_sizer.Add(wx.StaticText(panel, label="入口文件:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.entry_file_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        entry_sizer.Add(self.entry_file_text, 1, wx.EXPAND | wx.ALL, 5)
        self.entry_file_btn = wx.Button(panel, label="选择文件")
        entry_sizer.Add(self.entry_file_btn, 0, wx.ALL, 5)
        file_sizer.Add(entry_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # requirements.txt文件选择
        req_sizer = wx.BoxSizer(wx.HORIZONTAL)
        req_sizer.Add(wx.StaticText(panel, label="Requirements:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.requirements_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        req_sizer.Add(self.requirements_text, 1, wx.EXPAND | wx.ALL, 5)
        self.requirements_btn = wx.Button(panel, label="选择文件")
        req_sizer.Add(self.requirements_btn, 0, wx.ALL, 5)
        file_sizer.Add(req_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # PyInstaller配置区域
        config_box = wx.StaticBox(panel, label="PyInstaller配置")
        config_sizer = wx.StaticBoxSizer(config_box, wx.VERTICAL)

        # 打包名称
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(wx.StaticText(panel, label="打包名称:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.name_text = wx.TextCtrl(panel)
        name_sizer.Add(self.name_text, 1, wx.EXPAND | wx.ALL, 5)
        config_sizer.Add(name_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 选项配置
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧选项
        left_options = wx.BoxSizer(wx.VERTICAL)
        self.console_cb = wx.CheckBox(panel, label="显示控制台")
        self.onefile_cb = wx.CheckBox(panel, label="单文件打包")
        self.windowed_cb = wx.CheckBox(panel, label="窗口模式")
        left_options.Add(self.console_cb, 0, wx.ALL, 5)
        left_options.Add(self.onefile_cb, 0, wx.ALL, 5)
        left_options.Add(self.windowed_cb, 0, wx.ALL, 5)
        options_sizer.Add(left_options, 1, wx.EXPAND)

        # 右侧图标选择
        right_options = wx.BoxSizer(wx.VERTICAL)
        icon_sizer = wx.BoxSizer(wx.HORIZONTAL)
        icon_sizer.Add(wx.StaticText(panel, label="图标文件:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.icon_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        icon_sizer.Add(self.icon_text, 1, wx.EXPAND | wx.ALL, 5)
        self.icon_btn = wx.Button(panel, label="选择图标")
        icon_sizer.Add(self.icon_btn, 0, wx.ALL, 5)
        right_options.Add(icon_sizer, 0, wx.EXPAND)
        options_sizer.Add(right_options, 1, wx.EXPAND)

        config_sizer.Add(options_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(config_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # 操作按钮区域
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.package_btn = wx.Button(panel, label="开始打包")
        self.package_btn.SetBackgroundColour(wx.Colour(0, 128, 0))
        self.package_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        button_sizer.Add(self.package_btn, 0, wx.ALL, 5)

        self.clear_btn = wx.Button(panel, label="清空配置")
        button_sizer.Add(self.clear_btn, 0, wx.ALL, 5)

        main_sizer.Add(button_sizer, 0, wx.CENTER | wx.ALL, 10)

        # 日志输出区域
        log_box = wx.StaticBox(panel, label="日志输出")
        log_sizer = wx.StaticBoxSizer(log_box, wx.VERTICAL)
        self.log_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        log_sizer.Add(self.log_text, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(log_sizer, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(main_sizer)

        # 绑定事件
        self.bind_events()

    def bind_events(self):
        self.project_path_btn.Bind(wx.EVT_BUTTON, self.on_select_project_path)
        self.entry_file_btn.Bind(wx.EVT_BUTTON, self.on_select_entry_file)
        self.requirements_btn.Bind(wx.EVT_BUTTON, self.on_select_requirements)
        self.icon_btn.Bind(wx.EVT_BUTTON, self.on_select_icon)
        self.package_btn.Bind(wx.EVT_BUTTON, self.on_package)
        self.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)

    def on_select_project_path(self, event):
        """选择项目路径"""
        dlg = wx.DirDialog(self, "选择Python项目目录")
        if dlg.ShowModal() == wx.ID_OK:
            self.project_path = dlg.GetPath()
            self.project_path_text.SetValue(self.project_path)
            self.log(f"已选择项目路径: {self.project_path}")
        dlg.Destroy()

    def on_select_entry_file(self, event):
        """选择入口文件"""
        wildcard = "Python文件 (*.py)|*.py|所有文件 (*.*)|*.*"
        dlg = wx.FileDialog(self, "选择入口文件", wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.entry_file = dlg.GetPath()
            self.entry_file_text.SetValue(self.entry_file)
            self.log(f"已选择入口文件: {self.entry_file}")
            # 自动设置打包名称
            if not self.name_text.GetValue():
                name = Path(self.entry_file).stem
                self.name_text.SetValue(name)
        dlg.Destroy()

    def on_select_requirements(self, event):
        """选择requirements.txt文件"""
        wildcard = "Requirements文件 (*.txt)|*.txt|所有文件 (*.*)|*.*"
        dlg = wx.FileDialog(self, "选择requirements.txt文件", wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.requirements_file = dlg.GetPath()
            self.requirements_text.SetValue(self.requirements_file)
            self.log(f"已选择requirements文件: {self.requirements_file}")
        dlg.Destroy()

    def on_select_icon(self, event):
        """选择图标文件"""
        wildcard = "图标文件 (*.ico;*.png)|*.ico;*.png|所有文件 (*.*)|*.*"
        dlg = wx.FileDialog(self, "选择图标文件", wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            icon_file = dlg.GetPath()
            self.icon_text.SetValue(icon_file)
            self.log(f"已选择图标文件: {icon_file}")
        dlg.Destroy()

    def on_package(self, event):
        """开始打包"""
        if not self.validate_inputs():
            return

        # 禁用打包按钮防止重复点击
        self.package_btn.Enable(False)
        self.log("开始打包流程...")

        # 在新线程中执行打包
        thread = threading.Thread(target=self.do_packaging)
        thread.daemon = True
        thread.start()

    def on_clear(self, event):
        """清空配置"""
        self.project_path = ""
        self.entry_file = ""
        self.requirements_file = ""

        self.project_path_text.SetValue("")
        self.entry_file_text.SetValue("")
        self.requirements_text.SetValue("")
        self.icon_text.SetValue("")
        self.name_text.SetValue("")

        self.console_cb.SetValue(False)
        self.onefile_cb.SetValue(False)
        self.windowed_cb.SetValue(False)

        self.log_text.Clear()
        self.log("配置已清空")

    def validate_inputs(self):
        """验证输入参数"""
        if not self.project_path:
            wx.MessageBox("请选择项目路径", "错误", wx.OK | wx.ICON_ERROR)
            return False

        if not self.entry_file:
            wx.MessageBox("请选择入口文件", "错误", wx.OK | wx.ICON_ERROR)
            return False

        if not self.requirements_file:
            wx.MessageBox("请选择requirements.txt文件", "错误", wx.OK | wx.ICON_ERROR)
            return False

        if not os.path.exists(self.entry_file):
            wx.MessageBox("入口文件不存在", "错误", wx.OK | wx.ICON_ERROR)
            return False

        if not os.path.exists(self.requirements_file):
            wx.MessageBox("Requirements文件不存在", "错误", wx.OK | wx.ICON_ERROR)
            return False

        return True

    def do_packaging(self):
        """执行打包流程"""
        try:
            # 创建虚拟环境
            if not self.create_virtual_env():
                return

            # 安装依赖
            if not self.install_dependencies():
                return

            # 执行PyInstaller打包
            if not self.run_pyinstaller():
                return

            self.log("打包完成!")
            wx.CallAfter(self.package_btn.Enable, True)

        except Exception as e:
            self.log(f"打包失败: {str(e)}")
            wx.CallAfter(self.package_btn.Enable, True)

    def create_virtual_env(self):
        """创建虚拟环境"""
        venv_path = os.path.join(self.project_path, "venv_packaging")

        if os.path.exists(venv_path):
            self.log("检测到已存在的虚拟环境，正在删除...")
            import shutil

            shutil.rmtree(venv_path)

        self.log("正在创建虚拟环境...")
        cmd = [sys.executable, "-m", "venv", venv_path]

        try:
            subprocess.run(cmd, check=True, cwd=self.project_path)
            self.log("虚拟环境创建成功")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"创建虚拟环境失败: {e}")
            return False

    def install_dependencies(self):
        """安装依赖"""
        venv_path = os.path.join(self.project_path, "venv_packaging")

        # Windows下的pip路径
        if sys.platform == "win32":
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
        else:
            pip_path = os.path.join(venv_path, "bin", "pip")

        self.log("正在安装依赖...")
        cmd = [pip_path, "install", "-r", self.requirements_file]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.log("依赖安装成功")
            self.log("正在安装PyInstaller...")

            # 安装PyInstaller
            cmd_pyinstaller = [pip_path, "install", "pyinstaller"]
            subprocess.run(cmd_pyinstaller, check=True)
            self.log("PyInstaller安装成功")
            return True

        except subprocess.CalledProcessError as e:
            self.log(f"安装依赖失败: {e}")
            return False

    def run_pyinstaller(self):
        """运行PyInstaller"""
        venv_path = os.path.join(self.project_path, "venv_packaging")

        # Windows下的pyinstaller路径
        if sys.platform == "win32":
            pyinstaller_path = os.path.join(venv_path, "Scripts", "pyinstaller.exe")
        else:
            pyinstaller_path = os.path.join(venv_path, "bin", "pyinstaller")

        # 构建PyInstaller命令
        cmd = [pyinstaller_path]

        # 添加选项
        if self.onefile_cb.GetValue():
            cmd.append("--onefile")

        if self.windowed_cb.GetValue():
            cmd.append("--windowed")

        if not self.console_cb.GetValue():
            cmd.append("--noconsole")

        # 添加图标
        icon_file = self.icon_text.GetValue()
        if icon_file and os.path.exists(icon_file):
            cmd.extend(["--icon", icon_file])

        # 添加名称
        name = self.name_text.GetValue()
        if name:
            cmd.extend(["--name", name])

        # 添加入口文件
        cmd.append(self.entry_file)

        self.log("正在执行PyInstaller打包...")
        self.log(f"命令: {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=self.project_path)
            self.log("PyInstaller打包成功")

            # 显示输出路径
            dist_path = os.path.join(self.project_path, "dist")
            if os.path.exists(dist_path):
                self.log(f"打包文件位置: {dist_path}")

            return True

        except subprocess.CalledProcessError as e:
            self.log(f"PyInstaller打包失败: {e}")
            if e.stdout:
                self.log(f"标准输出: {e.stdout}")
            if e.stderr:
                self.log(f"错误输出: {e.stderr}")
            return False

    def log(self, message):
        """输出日志信息"""
        wx.CallAfter(self._append_log, message)

    def _append_log(self, message):
        """在主线程中添加日志"""
        self.log_text.AppendText(f"{message}\n")


class PackagingApp(wx.App):
    def OnInit(self):
        frame = PackagingTool()
        frame.Show()
        return True


if __name__ == "__main__":
    app = PackagingApp()
    app.MainLoop()
