import time
from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
import keyboard


def handle_uac():
    """尝试处理UAC弹窗"""
    try:
        # 等待UAC窗口出现
        uac_window = Desktop(backend="uia").window(title_re=".*用户账户控制.*")
        uac_window.wait("exists visible", timeout=10)
        uac_window.set_focus()

        # 发送Alt+Y快捷键点击"是"
        send_keys("%Y")
        keyboard.press_and_release('alt+y')
        send_keys("{TAB}{ENTER}")
        print("已处理UAC弹窗")
        return True
    except Exception as e:
        print(f"处理UAC弹窗失败: {e}")
        return False


def uninstall_oceanbase():
    """卸载OceanBase-Desktop 1.0.0"""
    try:
        # 打开控制面板的程序和功能
        Application(backend="uia").start("control.exe appwiz.cpl")
        app = Application(backend="uia").connect(title="程序和功能")
        window = app.window(title="程序和功能")
        window.wait("ready", timeout=10)

        # 获取程序列表视图
        list_view = window.child_window(class_name="SysListView32")

        # 查找OceanBase程序条目 - 改进的查找逻辑
        print("正在查找OceanBase-Desktop 1.0.0...")
        found = False

        # 尝试获取列表项的更健壮方法
        try:
            # 方法1: 尝试直接获取项
            items = list_view.items()
            for item in items:
                # 使用更安全的方式获取文本
                item_text = item.texts()[0] if item.texts() else ""
                if "OceanBase-Desktop 1.0.0" in item_text:
                    item.select()
                    found = True
                    break
        except Exception as e:
            print(f"方法1查找失败: {e}")
            # 方法2: 尝试通过点击坐标选择
            print("尝试备用方法查找程序...")
            list_view.click_input()  # 激活列表
            list_view.type_keys("^f")  # Ctrl+F打开查找

            # 在搜索框中输入程序名称
            search_box = window.child_window(title="搜索程序和功能", control_type="Edit")
            search_box.set_text("OceanBase")
            time.sleep(1)  # 等待搜索

            # 尝试选择第一个结果
            try:
                first_item = list_view.items()[0]
                first_item.select()
                found = True
                print("通过搜索找到了OceanBase程序")
            except:
                pass

        if not found:
            # 最后的手段: 尝试模糊匹配
            print("尝试模糊匹配程序名称...")
            items = list_view.items()
            for item in items:
                item_text = item.texts()[0] if item.texts() else ""
                if "OceanBase" in item_text:
                    item.select()
                    found = True
                    print(f"找到匹配程序: {item_text}")
                    break

        if not found:
            raise RuntimeError("未找到OceanBase-Desktop 1.0.0程序")

        # 点击卸载按钮
        print("找到程序，正在启动卸载...")
        window.child_window(title="卸载", control_type="Button").click_input()

        # 等待并处理UAC弹窗
        time.sleep(2)  # 给UAC弹窗出现的时间

        if not handle_uac():
            print("请手动确认UAC弹窗")
            time.sleep(10)  # 给用户时间手动处理

        # 等待卸载完成
        print("正在卸载，请稍候...")
        time.sleep(30)  # 根据实际卸载时间调整

        # 检查是否存在卸载完成窗口并关闭
        finish_window = Desktop(backend="uia").window(title_re=".*完成.*")
        if finish_window.exists(timeout=5):
            finish_window.child_window(title="确定", control_type="Button").click_input()
            print("已关闭卸载完成窗口")

        print("OceanBase-Desktop 1.0.0卸载成功！")
        return True

    except Exception as e:
        print(f"卸载过程发生错误: {e}")
        return False


if __name__ == "__main__":
    uninstall_oceanbase()