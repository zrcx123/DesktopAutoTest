from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
import time


def perform_ui_actions():
    print("执行UI操作...")
    try:
        app_path = r"C:\Program Files\OceanBase-Desktop\OceanBase-Desktop.exe"
        app = Application(backend="uia").start(app_path)  # 指定uia backend

        # 等待应用窗口出现
        main_window = app.window(title="OceanBase-Desktop")
        main_window.wait("visible", timeout=30)
        print("成功启动OceanBase-Desktop")

        # 打印窗口控件结构（调试用）
        main_window.print_control_identifiers()

        # 等待"启 动"按钮出现并点击
        print("等待'启 动'按钮出现...")
        start_button = wait_for_element(
            parent=main_window,
            title="启 动",
            control_type="Button",
            timeout=300
        )

        if start_button:
            print("'启 动'按钮已出现且可用，准备点击")
            start_button.click_input()
            print("已点击'启 动'按钮")

            # 等待确认对话框出现
            print("等待确 定对话框出现...")
            # 根据实际情况调整对话框标题和超时时间
            dialog = wait_for_element(
                parent=main_window,
                title="确 定",  # 请根据实际对话框标题修改
                control_type="Button",
                timeout=30
            )

            if dialog:
                print("确 定对话框已出现")
                # 打印对话框控件结构（调试用）
                dialog.print_control_identifiers()

                # 等待"确 认"按钮并点击
                confirm_button = wait_for_element(
                    parent=main_window,
                    title="确 定",
                    control_type="Button",
                    timeout=10
                )

                if confirm_button:
                    confirm_button.click_input()
                    print("已点击'确 定'按钮")
                    return True
                else:
                    print("未找到'确 定'按钮")
            else:
                print("未找到确 定对话框")
        else:
            print(f"等待超时，未找到'启 动'按钮")

        return False

    except Exception as e:
        print(f"执行UI操作时出错: {str(e)}")
        return False


def wait_for_element(parent, title, control_type, timeout=10):
    """等待指定元素出现并可用"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = parent.child_window(title=title, control_type=control_type)
            if element.exists() and element.is_enabled():
                return element
        except Exception as e:
            print(f"查找元素 {title} 时出错: {e}")

        time.sleep(0.5)

    return None


if __name__ == "__main__":
    launched_app = perform_ui_actions()
    if launched_app:
        print("应用程序已成功启动")
    else:
        print("应用程序启动失败")