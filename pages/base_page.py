import time
from datetime import datetime, timedelta
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import findwindows
from pywinauto.controls.uia_controls import ButtonWrapper, EditWrapper


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
            try:
                # 将窗口提到前台
                self.main_window.set_focus()
                # 确保窗口处于可点击状态
                self.main_window.wait('ready', timeout=10)
                return True
            except Exception as e:
                raise Exception(f"窗口前置操作失败: {e}")

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

    def click_button(self, button_title, button_type="Button",timeout=10):
        """点击按钮"""
        print(f"等待'{button_title}'按钮出现...")
        button = self.wait_for_element(
            title=button_title,
            control_type=button_type,
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

    def verify_ob_webView_contains(self, expected_url, expected_title,timeout=10):
        """验证超链接包含预期内容"""
        print(f"验证超链接是否为: '{expected_url}'...")

        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)

        while datetime.now() < end_time:
            try:
                remaining_seconds = max(0.0, float((end_time - datetime.now()).total_seconds()))
                wait_timeout = min(2.0, remaining_seconds)

                button = self.main_window.child_window(
                    title=expected_title,
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
                    if link_target == expected_url:
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

    def print_all_controls_info(self, indent=0, max_depth=3,
                                show_only_types=None,
                                show_properties=['control_type', 'name', 'automation_id', 'is_enabled']):
        """
        递归打印窗口下所有组件的结构化信息
        参数:
            indent: 缩进级别
            max_depth: 最大递归深度
            show_only_types: 只显示指定类型的控件
            show_properties: 需要显示的属性列表
        """
        if max_depth < 0 or not hasattr(self, 'main_window') or not self.main_window:
            return

        prefix = "  " * indent
        element = getattr(self.main_window, 'element_info', self.main_window)

        try:
            # 基础信息检查
            control_type = getattr(element, 'control_type', None)
            if not control_type or (show_only_types and control_type not in show_only_types):
                return

            # 收集和打印属性信息
            info = {
                'control_type': f"类型: {control_type}",
                'name': f"名称: {getattr(element, 'name', '')}",
                'automation_id': f"ID: {getattr(element, 'automation_id', '')}",
                'is_enabled': f"启用: {'是' if self.main_window.is_enabled() else '否'}",
                'is_visible': f"可见: {'是' if self.main_window.is_visible() else '否'}"
            }
            print(prefix + "└── " + " | ".join(info[prop] for prop in show_properties if prop in info))

            # 特殊控件处理
            if hasattr(self.main_window, 'window_text'):
                text = self.main_window.window_text()
                if isinstance(self.main_window, ButtonWrapper):
                    print(prefix + f"    文本: {text}")
                elif isinstance(self.main_window, EditWrapper):
                    print(prefix + f"    内容: {text}")

            # 递归处理子控件
            if indent < max_depth and hasattr(self.main_window, 'children'):
                for child in self.main_window.children():
                    if child:
                        temp_obj = self.__class__()
                        temp_obj.main_window = child
                        temp_obj.print_all_controls_info(indent + 1, max_depth, show_only_types, show_properties)

        except Exception as e:
            print(prefix + f" 发生错误: {str(e)}")