from pywinauto.application import Application


def verify_status_text(expected_status, timeout=10):
    """
    验证状态文本是否符合预期
    :param expected_status: 预期的状态值(如"运行中")
    :param timeout: 查找超时时间(秒)
    :return: True/False
    """
    print(f"验证状态是否为: '{expected_status}'...")
    app_path = r"C:\Program Files\OceanBase-Desktop\OceanBase-Desktop.exe"
    expected_window_title = "OceanBase-Desktop"

    try:
        # 启动应用
        app = Application(backend="uia").start(app_path)
        main_window = app.window(title=expected_window_title)

        # 先找到包含"状态"的父容器
        status_container = main_window.child_window(
            title_re=".*状态.*",  # 匹配包含"状态"的容器
            control_type="Group"  # 或 "Pane"、"Panel"等，根据实际UI调整
        ).wait('visible', timeout=timeout)

        print("找到状态容器，内容如下:")
        status_container.print_control_identifiers(depth=1)  # 打印容器内元素结构

        # 在容器内查找状态值
        status_value = status_container.child_window(
            title=expected_status,
            control_type="Text"
        ).wait('visible', timeout=5)

        print(f"状态验证成功: 找到 '{expected_status}'")
        return True

    except Exception as e:
        print(f"验证状态文本时出错: {type(e).__name__}: {str(e)}")

        # 调试：打印整个窗口结构
        try:
            main_window.print_control_identifiers()
        except:
            pass

        return False


if __name__ == "__main__":
    is_running = verify_status_text("运行中")
    if is_running:
        print("验证通过: OceanBase集群正在运行")
    else:
        print("验证失败: 集群未运行或状态异常")