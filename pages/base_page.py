import time
from datetime import datetime, timedelta
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError


class BasePage:
    def __init__(self, app_path=None, window_title=None):
        self.app_path = app_path
        self.window_title = window_title
        self.app = None
        self.main_window = None
        self._is_app_running = False

    def start_application(self):
        """启动应用程序"""
        if self._is_app_running:
            return True

        try:
            self.app = Application(backend="uia").start(self.app_path)
            self.main_window = self.app.window(title=self.window_title)
            self.main_window.wait("visible", timeout=10)
            self._is_app_running = True
            return True
        except Exception as e:
            raise Exception(f"启动应用失败: {e}")

    def close_application(self):
        """关闭应用程序"""
        print("关闭应用程序")
        try:
            if self._is_app_running and self.app:
                self.app.kill()
                self._is_app_running = False
                self.app = None
                self.main_window = None
            return True
        except Exception as e:
            print(f"关闭应用程序时出错: {str(e)}")
            raise Exception(f"关闭应用程序时出错: {str(e)}")

    def click_button(self, button_title, timeout=30):
        """点击按钮"""
        print(f"等待'{button_title}'按钮出现...")
        button = self.wait_for_element(
            title=button_title,
            control_type="Button",
            timeout=timeout
        )
        if not button:
            print(f"未找到'{button_title}'按钮")
            raise ElementNotFoundError(f"未找到'{button_title}'按钮")
        print(f"'{button_title}'按钮已出现且可用，准备点击")
        button.click_input()
        print(f"已点击'{button_title}'按钮")
        return True

    def wait_for_element(self, title, control_type, timeout=10):
        """等待指定元素出现并可用"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                element = self.main_window.child_window(
                    title=title,
                    control_type=control_type
                )
                if element.exists() and element.is_enabled():
                    return element
            except Exception as e:
                print(f"查找元素 {title} 时出错: {e}")
            time.sleep(0.5)
        return None

    def verify_text_contains(self, expected_text, title_pattern, timeout=30):
        """验证文本包含预期内容"""
        print(f"验证状态是否为: '{expected_text}'...")

        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)

        while datetime.now() < end_time:
            try:
                remaining_seconds = max(0.0, float((end_time - datetime.now()).total_seconds()))
                wait_timeout = min(2.0, remaining_seconds)

                doc = self.main_window.child_window(
                    control_type="Document",
                    title_re=title_pattern
                ).wait('visible', timeout=wait_timeout)

                full_text = doc.window_text()
                print(f"获取到的完整文本:\n{full_text}")

                if expected_text in full_text:
                    print("验证通过: OceanBase集群正在运行")
                    return True
                time.sleep(2)
            except Exception:
                print("文本不匹配，等待2秒后重试...")
                time.sleep(2)
                continue
        print(f"操作超时，总耗时: {timeout}秒")
        return False

    def verify_webView_contains(self, expected_text, timeout=10):
        """验证超链接包含预期内容"""
        print(f"验证超链接是否为: '{expected_text}'...")

        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)

        while datetime.now() < end_time:
            try:
                remaining_seconds = max(0.0, float((end_time - datetime.now()).total_seconds()))
                wait_timeout = min(2.0, remaining_seconds)

                button = self.main_window.child_window(
                    title="OceanBase官网",
                    control_type="Hyperlink"  # 或 "Button"（取决于UI框架）
                ).wait('visible', timeout=wait_timeout)

                if button.is_active():
                    # 获取超链接地址（如果有）
                    link_target=''
                    # 方法1：尝试获取 ValuePattern 的值（适用于超链接）
                    try:
                        if hasattr(button, 'iface_value'):
                            link_target = button.iface_value.CurrentValue
                            print("超链接地址 (ValuePattern):", link_target)
                    except Exception as e:
                        print("无法通过 ValuePattern 获取:", str(e))

                    # 检查是否正确
                    if link_target == expected_text:
                        print("超链接正确",link_target)
                        return True
                else:
                    print("按钮不存在")
            except Exception as e:
                print("获取超链接失败:等待2秒后重试...", e)
                time.sleep(2)
                continue
        print(f"操作超时，总耗时: {timeout}秒")
        return False