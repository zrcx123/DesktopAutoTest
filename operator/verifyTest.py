from pywinauto.application import Application
import re
import time
from datetime import datetime, timedelta


def verify_status_text(expected_status, title_pattern, timeout=30):
    """
    验证状态文本是否符合预期
    :param expected_status: 预期的状态值(如"运行中")
    :param title_pattern: 用于匹配Document控件的正则表达式模式
    :param timeout: 查找超时时间(秒)
    :return: True/False
    """
    print(f"验证状态是否为: '{expected_status}'...")
    app_path = r"C:\Program Files\OceanBase-Desktop\OceanBase-Desktop.exe"
    expected_window_title = "OceanBase-Desktop"

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=timeout)

    try:
        # 启动应用
        app = Application(backend="uia").start(app_path)
        main_window = app.window(title=expected_window_title)

        while datetime.now() < end_time:
            try:
                # 获取包含状态信息的Document控件
                remaining_time = (end_time - datetime.now()).total_seconds()
                doc = main_window.child_window(
                    control_type="Document",
                    title_re=title_pattern
                ).wait('visible', timeout=min(2, remaining_time))  # 每次最多等待2秒

                # 获取完整文本内容
                full_text = doc.window_text()
                print(f"获取到的完整文本:\n{full_text}")

                if expected_status in full_text:
                    return True
                else:
                    print("文本不匹配，等待2秒后重试...")
                    time.sleep(2)  # 等待2秒后重试
                    continue

            except Exception as e:
                print(f"查找控件失败，等待2秒后重试... ({type(e).__name__}: {str(e)})")
                time.sleep(2)  # 等待2秒后重试
                continue

        # 如果超时仍未找到
        print(f"操作超时，总耗时: {timeout}秒")
        return False

    except Exception as e:
        print(f"验证状态文本时出错: {type(e).__name__}: {str(e)}")
        return False


if __name__ == "__main__":
    is_running = verify_status_text(
        "状态： 运行中  版本号：4.3.5.1 架构：x86_64",
        r".*状态：.*",
        timeout=30)
    if is_running:
        print("验证通过: OceanBase集群正在运行")
    else:
        print("验证失败: 集群未运行或状态异常")