from pywinauto import ElementNotFoundError
from pywinauto.application import Application
import time
import os

def auto_install_oceanbase():
    installer_path = r"C:\111\OceanBase-Desktop-Setup-1.0.0.exe"
    if not os.path.exists(installer_path):
        raise FileNotFoundError(f"安装程序未找到：{installer_path}")

    try:
        # 启动安装程序
        app = Application(backend="uia").start(installer_path)
        # 等待并连接到安装窗口
        install_dlg = app.window(title_re="OceanBase-Desktop 安装 ")
        install_dlg.wait('ready', timeout=30)
        # 点击安装按钮
        install_button = install_dlg.child_window(
            title="安装(I)",
            control_type="Button"
        )
        install_button.click_input()
        # 等待安装完成
        # 等待安装完成
        start_time = time.time()
        while time.time() - start_time < 300:
            try:
                finish_button = install_dlg.child_window(
                    title_re="完成\\(F\\)|完成|Finish",
                    control_type="Button"
                )
                if finish_button.exists() and finish_button.is_enabled():
                    # install_dlg["完成(F)"].click()
                    print("安装成功完成！")
                    return True

            except ElementNotFoundError:
                if not install_dlg.exists():
                    print("安装窗口意外关闭")
                    return False
            time.sleep(2)
    except Exception as e:
        print(f"自动化安装失败: {str(e)}")
        raise

if __name__ == "__main__":
    auto_install_oceanbase()
