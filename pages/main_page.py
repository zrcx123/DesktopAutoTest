from .base_page import BasePage


class MainPage(BasePage):
    def perform_startup_sequence(self):
        """执行启动序列"""
        self.click_button("启 动", 300)
        print("启动OceanBase-Desktop")
        self.click_button("确 定", 300)
        print("启动成功OceanBase-Desktop")
        return True

    def perform_stop_sequence(self):
        """执行启动序列"""
        self.click_button("停 止", 300)
        print("启动OceanBase-Desktop")
        self.click_button("确 定", 300)
        print("启动成功OceanBase-Desktop")
        return True


    def verify_running_status(self):
        """验证运行状态"""
        expected_status = "状态： 运行中  版本号：4.3.5.1 架构：x86_64"
        return self.verify_text_contains(
            expected_status,
            r".*状态：.*",
            timeout=100
        )

    def verify_stopping_status(self):
        """验证运行状态"""
        expected_status = "状态： 已停止"
        return self.verify_text_contains(
            expected_status,
            r".*状态：.*",
            timeout=10
        )

    def connect_to_database(self):
        """连接数据库"""
        print("连接数据库操作...")
        return self.click_button("连 接", 300)

    def verify_webView_status(self):
        """验证运行状态"""
        expected_status = "https://www.oceanbase.com/"
        return self.verify_webView_contains(
            expected_status,
            timeout=10
        )
