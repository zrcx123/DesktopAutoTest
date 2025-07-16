import pytest

@pytest.mark.uninstallation
class TestUnInstallation:
    @pytest.mark.run(order=101)
    def test_uninstall_application(self, uninstallation_page):
        """测试应用安装"""
        assert uninstallation_page.uninstall_application(), "应用卸载失败"

