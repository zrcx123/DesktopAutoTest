import time

import pytest

@pytest.mark.operations
class TestOperations:
    @pytest.mark.run(order=2)
    def test_startup_sequence(self, main_page):
        """测试启动"""
        assert main_page.start_application(), "应用启动失败"
        assert main_page.perform_startup_sequence(), "集群启动执行失败"
        assert main_page.verify_running_status(), "状态验证失败"

    @pytest.mark.run(order=3)
    def test_stop_sequence(self, main_page):
        """测试停止"""
        assert main_page.start_application(), "应用启动失败"
        assert main_page.perform_stop_sequence(), "集群停止执行失败"
        assert main_page.verify_stopping_status(), "状态验证失败"

    @pytest.mark.run(order=4)
    def test_check_ob_webView(self, main_page):
        """测试ob官网超链接"""
        assert main_page.start_application(), "应用启动失败"
        assert main_page.verify_ob_webView_status(), "ob官网 超链接验证失败"

    @pytest.mark.run(order=5)
    def test_application_close(self, main_page):
        """测试应用关闭"""
        assert main_page.close_application(), "应用关闭失败"

    @pytest.mark.run(order=6)
    def test_check_help_installation_Manual(self, main_page):
        """测试 帮助-安装手册 超链接"""
        time.sleep(1)
        assert main_page.start_application(), "应用启动失败"
        time.sleep(1)
        assert main_page.verify_help_installation_manual(), "帮助-安装手册 超链接验证失败"

    @pytest.mark.run(order=7)
    def test_application_close(self, main_page):
        """测试应用关闭"""
        assert main_page.close_application(), "应用关闭失败"

    @pytest.mark.run(order=8)
    def test_check_help_statement(self, main_page):
        """测试 帮助-声明 """
        assert main_page.start_application(), "应用启动失败"
        assert main_page.verify_help_statement(), "帮助-声明  验证失败"

