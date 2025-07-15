import time
from operator import truediv

from .base_page import BasePage


class MainPage(BasePage):
    def perform_startup_sequence(self):
        """执行启动序列"""
        print("启动OceanBase-Desktop")
        self.click_button("启 动", "Button",30)
        print("启动成功OceanBase-Desktop")
        return self.click_button("确 定", "Button",30)

    def perform_stop_sequence(self):
        """执行启动序列"""
        print("启动OceanBase-Desktop")
        self.click_button("停 止", "Button",30)
        print("启动成功OceanBase-Desktop")
        return self.click_button("确 定", "Button",30)

    def verify_running_status(self,):
        """验证运行状态"""
        expected_status = "状态： 运行中  版本号：4.3.5.1 架构：x86_64"
        return self.verify_text_contains(
            expected_status,
            r".*状态：.*",
            timeout=60
        )

    def verify_stopping_status(self):
        """验证运行状态"""
        expected_status = "状态： 已停止"
        return self.verify_text_contains(
            expected_status,
            r".*状态：.*",
            timeout=30
        )

    def verify_statement_txt(self,):
        """验证声明的文字"""
        expected_status = "产品概述 OceanBase 桌面版是由 OceanBase 团队开发的轻量级分布式数据库软件"
        return self.verify_text_contains(
            expected_status,
            r".*OceanBase .*",
            timeout=30
        )

    def connect_to_database(self):
        """连接数据库"""
        print("连接数据库操作...")
        return self.click_button(
            "连 接",
            "Button",
            30
        )

    def verify_ob_webView_status(self):
        """验证运行状态"""
        self.verify_ob_webView_contains(
            expected_url="https://www.oceanbase.com/",
            expected_title="OceanBase官网",
            timeout=30
        )
        return self.click_button("OceanBase官网", "Hyperlink", 300)

    def verify_help_installation_manual(self):
        """执行启动序列"""
        print("点击 帮助")
        self.click_button("bulb 帮助","Hyperlink", 300)
        #assert self.print_all_controls_info()
        self.verify_ob_webView_contains(
            expected_url="https://www.oceanbase.com/docs/common-oceanbase-database-cn-1000000002866370",
            expected_title="安装手册",
            timeout=30
        )
        print("点击 安装手册")
        return self.click_button("安装手册", "Hyperlink", 30)

    def verify_help_statement(self):
        """执行启动序列"""
        print("点击 帮助")
        self.click_button("bulb 帮助","Hyperlink", 30)
        print("点击 声明")
        self.click_button("声明", "Hyperlink", 30)
        return self.verify_statement_txt()
