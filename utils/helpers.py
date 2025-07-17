def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption("--setup-path", action="store", default=r"C:\lvwei\OceanBase-Desktop-Setup-1.0.0.exe")
    parser.addoption("--app-path", action="store", default=r"C:\Program Files\OceanBase-Desktop\OceanBase-Desktop.exe")
    parser.addoption("--window-title", action="store", default="OceanBase-Desktop")
    parser.addoption("--uninstall-path", action="store", default=r"C:\Program Files\OceanBase-Desktop\Uninstall OceanBase-Desktop.exe")
    parser.addoption("--OceanBase-hyperlink", action="store", default="https://www.oceanbase.com/")

def setup_logging():
    """设置日志配置"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('test.log'),
            logging.StreamHandler()
        ]
    )