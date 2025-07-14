import pytest

@pytest.mark.installation
class TestInstallation:
    @pytest.mark.run(order=1)
    def test_install_application(self, installation_page):
        """测试应用安装"""
        assert installation_page.install_application(), "应用安装失败"

