from typing import Callable, Optional

class CallbackClass:
    def __init__(self):
        self._callback: Optional[Callable[[str], None]] = None

    def register_callback(self, callback: Callable[[str], None]):
        """
        注册回调函数。
        :param callback: 回调函数，接受一个字符串参数。
        """
        self._callback = callback

    def some_method(self):
        """
        触发回调的某个方法。
        """
        print("some_method 被调用了！")
        # 触发回调函数
        if self._callback:
            self._callback("some_method 执行完成！")

    def another_method(self):
        """
        不触发回调的另一个方法。
        """
        print("another_method 被调用了！")


# 使用示例
def my_callback(message: str):
    print(f"回调函数被触发，消息：{message}")

# 创建类的实例
obj = CallbackClass()

# 注册回调函数
obj.register_callback(my_callback)

# 调用触发回调的方法
obj.some_method()

# 调用不触发回调的方法
obj.another_method()
