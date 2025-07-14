运行所有测试：
1. pytest 
只运行安装测试：
2. pytest  -m installation
只运行UI操作测试：
3. pytest -m operations
只运行数据库操作测试：
4. pytest  -m database
只运行卸载测试：
5. pytest  -m uninstallation
自定义路径运行：
6. pytest  --setup-path=/custom/path/setup.exe --app-path=/custom/path/app.exe
传入自定义参数
7. pytest --html=report.html（通过pip install pytest-html安装插件）
生成测试报告
8.  pytest --html=reports/report_$(Get-Date -Format "yyyy-MM-dd_HH-mm-ss").html
