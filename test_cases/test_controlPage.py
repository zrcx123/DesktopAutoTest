import time

import pytest

@pytest.mark.controlPage
class TestControlPage:
    @pytest.mark.run(order=21)
    def test_go_control_page(self, main_page, app_path):
        """测试进入管控页面"""
        assert main_page.start_application(True), "应用启动失败"
        assert main_page.perform_startup_cluster(), "集群启动执行失败"
        assert main_page.verify_running_status(), "状态验证失败"
        assert main_page.perform_go_control_page()

