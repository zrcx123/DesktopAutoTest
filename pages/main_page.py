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
        """执行停止序列"""
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
        """验证停止状态"""
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

    def verify_EN_txt(self,):
        """验证切换为英文状态"""
        expected_status = "Home OB Dashboard OB Website Help English    Status: "
        return self.verify_text_contains(
            expected_status,
            r".*Status .*",
            timeout=30
        )

    def verify_ZH_txt(self,):
        """验证切换为中文状态"""
        expected_status = "回到首页 进入管控页面 OceanBase官网 帮助 中文    状态： 已停止"
        return self.verify_text_contains(
            expected_status,
            r".*状态：.*",
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
        """验证ob webView状态"""
        self.verify_ob_webView_contains(
            expected_url="https://www.oceanbase.com/",
            expected_title="OceanBase官网",
            timeout=30
        )
        return self.click_button("OceanBase官网", "Hyperlink", 300)

    def verify_help_installation_manual(self):
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
        print("点击 帮助")
        self.click_button("bulb 帮助","Hyperlink", 30)
        print("点击 声明")
        self.click_button("声明", "Hyperlink", 30)
        return self.verify_statement_txt()

    def verify_switch_language(self, language):
        """执行语言切换并验证结果
        参数:
            language: 要切换的语言 ("中文" 或 "English")
        """
        # 第一步：点击全局语言切换
        global_buttons = ["global 中文", "global English"]
        clicked = False

        for btn in global_buttons:
            try:
                self.main_window.child_window(
                    title=btn,
                    control_type="Hyperlink"
                ).wait('ready', timeout=3)
                print(f"点击 {btn}")
                self.click_button(btn, "Hyperlink", 30)
                clicked = True
                break
            except:
                continue

        if not clicked:
            raise Exception("未找到全局语言切换按钮")

        # 第二步：点击目标语言按钮
        print(f"切换至 {language} 语言")
        self.click_button(language, "Hyperlink", 30)

        time.sleep(3)  # 等待语言切换完成

        # 根据目标语言返回对应的验证结果
        if language == "中文":
            return self.verify_ZH_txt()
        elif language == "English":
            return self.verify_EN_txt()
        else:
            raise ValueError(f"不支持的语言选项: {language}")
