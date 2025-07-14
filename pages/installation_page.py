import os
import time
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError


class InstallationPage:
    def __init__(self, setup_path):
        self.setup_path = setup_path

    def install_application(self):
        """安装应用程序"""

        if not os.path.exists(self.setup_path):
            raise FileNotFoundError(f"安装程序未找到：{self.setup_path}")

        try:
            install_app = Application(backend="uia").start(self.setup_path)
            print("所有顶层窗口:", install_app.windows())
            install_dlg = install_app.window(title_re="OceanBase-Desktop 安装 ")
            install_dlg.wait('ready', timeout=30)
            print("启动OceanBase-Desktop 安装应用程序")

            install_button = install_dlg.child_window(
                title="安装(I)",
                control_type="Button"
            )
            install_button.click_input()

            start_time = time.time()
            while time.time() - start_time < 300:
                try:
                    finish_button = install_dlg.child_window(
                        title_re="完成\\(F\\)|完成|Finish",
                        control_type="Button"
                    )
                    if finish_button.exists() and finish_button.is_enabled():
                        #install_dlg["完成(F)"].click()
                        print("安装成功完成！")
                        return True
                except ElementNotFoundError:
                    if not install_dlg.exists():
                        return False
                time.sleep(2)
            return False
        except Exception as e:
            raise Exception(f"自动化安装失败: {str(e)}")