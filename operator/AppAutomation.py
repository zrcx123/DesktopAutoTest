import os
import time
from datetime import datetime, timedelta
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError

class AppAutomation:
    def __init__(self, setup_path, app_path, expected_window_title):
        """
        初始化自动化测试类
        :param setup_path: 安装程序路径
        :param app_path: 应用程序路径
        :param expected_window_title: 应用主窗口标题
        """
        self.setup_path = setup_path
        self.app_path = app_path
        self.expected_window_title = expected_window_title
        self.app = None
        self.main_window = None
        self._is_app_running = False

    def install_application(self):
        if not os.path.exists(self.setup_path):
            raise FileNotFoundError(f"安装程序未找到：{self.setup_path}")

        try:
            # 启动安装程序（独立实例）
            install_app = Application(backend="uia").start(self.setup_path)
            install_dlg = install_app.window(title_re="OceanBase-Desktop 安装 ")
            install_dlg.wait('ready', timeout=30)

            install_button = install_dlg.child_window(
                title="安装(I)",
                control_type="Button"
            )
            install_button.click_input()

            # 等待安装完成
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
                        print("安装窗口意外关闭")
                        return False
                time.sleep(2)

        except Exception as e:
            print(f"自动化安装失败: {str(e)}")
            return False

    def launch_application(self):
        """启动应用（如果未启动）"""
        return self._start_app()

    def perform_ui_actions(self):
        print("执行UI操作...")
        if not self._start_app():
            return False

        try:
            if not self._click_button("启 动", 300):
                return False

            if not self._click_button("确 定", 300):
                return False

            return True

        except Exception as e:
            print(f"执行UI操作时出错: {str(e)}")
            return False

    def verify_results(self):
        """验证操作结果是否符合预期"""
        return self.verify_status_text(
        "状态： 运行中  版本号：4.3.5.1 架构：x86_64",
        r".*状态：.*",
        timeout=100)

    def connect_database_actions(self):
        print("连接数据库操作...")
        if not self._start_app():
            return False

        try:
            if not self._click_button("连 接", 300):
                return False

            return True

        except Exception as e:
            print(f"连接数据库操作时出错: {str(e)}")
            return False

    def close_application(self):
        """关闭应用程序"""
        print("关闭应用程序...")
        try:
            if self._is_app_running and self.app:
                self.app.kill()
                self._is_app_running = False
                self.app = None
                self.main_window = None
            return True
        except Exception as e:
            print(f"关闭应用程序时出错: {str(e)}")
            return False

    def _start_app(self):
        """启动应用（私有方法，确保只被调用一次）"""
        if self._is_app_running:
            return True

        try:
            self.app = Application(backend="uia").start(self.app_path)
            print("启动OceanBase-Desktop")
            self.main_window = self.app.window(title=self.expected_window_title)
            self.main_window.wait("visible", timeout=10)
            self._is_app_running = True
            print("成功启动OceanBase-Desktop")
            return True
        except Exception as e:
            print(f"启动应用失败: {e}")
            return False

    def _click_button(self, button_title, timeout=30):
        """封装按钮点击操作"""
        print(f"等待'{button_title}'按钮出现...")
        button = wait_for_element(
            parent=self.main_window,
            title=button_title,
            control_type="Button",
            timeout=timeout
        )

        if not button:
            print(f"未找到'{button_title}'按钮")
            return False

        print(f"'{button_title}'按钮已出现且可用，准备点击")
        button.click_input()
        print(f"已点击'{button_title}'按钮")
        return True

    def verify_status_text(self, expected_status, title_pattern, timeout=30):
        """
        验证状态文本是否符合预期
        :param expected_status: 预期的状态值(如"运行中")
        :param title_pattern: 用于匹配Document控件的正则表达式模式
        :param timeout: 查找超时时间(秒)
        :return: True/False
        """
        print(f"验证状态是否为: '{expected_status}'...")

        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)

        try:
            # # 启动应用
            # self.app = Application(backend="uia").start(self.app_path)
            # self.main_window = self.app.window(title=self.expected_window_title)

            while datetime.now() < end_time:
                try:
                    # 获取包含状态信息的Document控件
                    remaining_seconds = max(0.0, float((end_time - datetime.now()).total_seconds()))
                    wait_timeout = min(2.0, remaining_seconds)  # 明确使用浮点数
                    doc = self.main_window.child_window(
                        control_type="Document",
                        title_re=title_pattern
                    ).wait('visible', timeout=wait_timeout)

                    # 获取完整文本内容
                    full_text = doc.window_text()
                    print(f"获取到的完整文本:\n{full_text}")

                    if expected_status in full_text:
                        print("验证通过: OceanBase集群正在运行")
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


def run_test_case():
    """执行完整的测试用例"""
    # 配置参数
    installer_path = r"C:\111\OceanBase-Desktop-Setup-1.0.0.exe"
    app_path = r"C:\Program Files\OceanBase-Desktop\OceanBase-Desktop.exe"
    app_window_title = "OceanBase-Desktop"

    # 初始化自动化工具
    automator = AppAutomation(installer_path, app_path, app_window_title)

    # 执行测试步骤
    steps = [
        ("安装应用", automator.install_application),
        ("启动应用", automator.launch_application),
        ("执行操作", automator.perform_ui_actions),
        ("验证结果", automator.verify_results),
        ("连接数据库", automator.connect_database_actions),
        ("关闭应用", automator.close_application)
    ]

    # 运行测试
    case_passed = True
    for step_name, step_func in steps:
        print(f"\n=== 正在执行步骤: {step_name} ===")
        if not step_func():
            print(f"!!! 步骤失败: {step_name}")
            case_passed = False
            break

    # 输出测试结果
    print("\n=== 测试结果 ===")
    if case_passed:
        print("✅ 测试用例通过")
    else:
        print("❌ 测试用例失败")
    return case_passed

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
    run_test_case()