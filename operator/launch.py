from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
import time


def launch_oceanbase_desktop():
    """启动OceanBase-Desktop 1.0.0应用程序"""

    try:
        # 方法1：直接通过已知的exe路径启动（最可靠）
        app_path = r"C:\Program Files\OceanBase-Desktop\OceanBase-Desktop.exe"
        app = Application().start(app_path)

        # 等待应用窗口出现
        main_window = app.window(title="OceanBase-Desktop")
        main_window.wait("visible", timeout=30)
        print("成功启动OceanBase-Desktop")
        return app

    except Exception as e:
        print(f"通过exe路径启动失败: {e}")
        print("尝试通过开始菜单启动...")



if __name__ == "__main__":
    launched_app = launch_oceanbase_desktop()
    if launched_app:
        print("应用程序已成功启动")
    else:
        print("应用程序启动失败")