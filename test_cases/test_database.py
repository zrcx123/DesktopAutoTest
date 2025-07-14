import time
import pytest

@pytest.mark.database
class TestDatabase:
    @pytest.mark.run(order=6)
    def test_database_connection(self, main_page):
        """测试数据库连接"""
        assert main_page.start_application(), "应用启动失败"
        #assert main_page.perform_stop_sequence(), "集群停止执行失败"
        assert main_page.perform_startup_sequence(), "集群启动执行失败"
        assert main_page.verify_running_status(), "状态验证失败"
        assert main_page.connect_to_database(), "数据库连接失败"
        time.sleep(3)

