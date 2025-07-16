import os
import time
from pywinauto import Desktop, Application
from pywinauto.findwindows import ElementNotFoundError


class UnInstallationPage:
    def __init__(self, uninstall_path):
        self.uninstall_path = uninstall_path

    def uninstall_application(self):
        """卸载应用程序"""
        if not os.path.exists(self.uninstall_path):
            raise FileNotFoundError(f"卸载程序未找到：{self.uninstall_path}")

        try:
            # 启动卸载程序
            Application(backend="uia").start(self.uninstall_path)
            time.sleep(3)

            # 使用Desktop查找窗口
            desktop = Desktop(backend="uia")
            install_dlg = None

            # 查找窗口并重新连接
            start_time = time.time()
            while time.time() - start_time < 30:
                for window in desktop.windows():
                    print(f"- 标题: {window.window_text()}")
                    if "OceanBase-Desktop" in window.window_text() and "解除安装" in window.window_text():
                        # 关键修改：使用窗口句柄重新连接
                        install_dlg = Application(backend="uia").connect(handle=window.handle).window()
                        print("找到并连接卸载窗口:", install_dlg.window_text())
                        break
                if install_dlg:
                    break
                time.sleep(1)

            if not install_dlg:
                raise ElementNotFoundError("未找到卸载窗口")

            # 自定义等待窗口就绪
            start_time = time.time()
            while time.time() - start_time < 30:
                if install_dlg.exists() and install_dlg.is_enabled():
                    break
                time.sleep(1)
            else:
                raise Exception("窗口未在30秒内准备就绪")

            print("解除安装OceanBase-Desktop 应用程序")

            # 查找并点击按钮
            install_button = install_dlg.child_window(
                title="解除安装(U)",
                control_type="Button"
            )
            install_button.wait('enabled', timeout=10)
            install_button.click_input()
            time.sleep(1)
            # 尝试查找"确定"按钮，如果存在则点击
            try:
                ok_button = install_dlg.child_window(
                    title="确定",
                    control_type="Button"
                )
                ok_button.wait('enabled', timeout=10)  # Shorter timeout for this optional button
                if ok_button.exists() and ok_button.is_enabled():
                    print("找到确定按钮，正在点击...")
                    ok_button.click_input()
                else:
                    print("确定按钮不存在或不可点击")
            except Exception as e:
                print(f"未找到确定按钮或出现错误: {str(e)}")
                # 继续执行而不中断流程

            # 等待卸载完成
            start_time = time.time()
            while time.time() - start_time < 300:
                try:
                    finish_button = install_dlg.child_window(
                        title_re="完成\\(F\\)|完成|Finish",
                        control_type="Button"
                    )
                    if finish_button.exists() and finish_button.is_enabled():
                        print("卸载成功完成！")
                        finish_button.click_input()
                        return True
                except ElementNotFoundError:
                    if not install_dlg.exists():
                        print("卸载窗口已关闭，可能已完成")
                        return True
                time.sleep(2)

            print("卸载超时")
            return False

        except Exception as e:
            raise Exception(f"自动化卸载失败: {str(e)}")