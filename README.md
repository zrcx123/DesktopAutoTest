```bash
安装依赖
 pip install pytest-ordering
 pip install pytest-html

# 运行所有测试
pytest

# 只运行安装测试
pytest -m installation

# 只运行UI操作测试
pytest -m operations

# 只运行数据库操作测试
pytest -m database

# 只运行卸载测试
pytest -m uninstallation

# 自定义路径运行
pytest --setup-path=/custom/path/setup.exe --app-path=/custom/path/app.exe	

# 传入自定义参数（生成HTML报告）
pytest --html=report.html  # 需先安装 pytest-html

# 生成带时间戳的测试报告
pytest --html=reports/report_$(Get-Date -Format "yyyy-MM-dd_HH-mm-ss").html

框架目录结构
oceanbase_test/
├── conftest.py                 # pytest全局配置和fixture定义
├── pages/                      # 页面对象类
│   ├── __init__.py
│   ├── base_page.py            # 基础页面类
│   ├── installation_page.py    # 安装页面类
│   └── main_page.py            # 主应用页面类
├── test_cases/                 # 测试用例
│   ├── __init__.py
│   ├── test_installation.py    # 安装测试用例
│   ├── test_operations.py      # 操作测试用例
│   ├── test_database.py        # 连接数据库用例
│   └── test_uninstallation.py  # 卸载测试用例
└── utils/                      # 工具函数
    ├── __init__.py
    └── helpers.py              # 辅助函数
└── reports/                    # 工具函数
    ├── assets                  # css函数目录
    └── report_2025-07-08_11-13-52.html

```


