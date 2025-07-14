运行所有测试：pytest 
只运行安装测试：pytest  -m installation
只运行UI操作测试：pytest -m operations
只运行数据库操作测试：pytest  -m database
只运行卸载测试：pytest  -m uninstallation
自定义路径运行：pytest  --setup-path=/custom/path/setup.exe --app-path=/custom/path/app.exe
传入自定义参数: pytest --html=report.html（通过pip install pytest-html安装插件）
生成测试报告: pytest --html=reports/report_$(Get-Date -Format "yyyy-MM-dd_HH-mm-ss").html
