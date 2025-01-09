from PySide6.QtCore import QObject, Signal


# class VariableManager:
#     string_var_manager = {}
#     int_var_manager = {}
#
#     def __init__(self):
#         pass
#
#     def reset_variables(self):
#         for key in self.string_var_manager.keys():
#             self.string_var_manager[key] = ""  # Đặt giá trị chuỗi về rỗng
#         for key in self.int_var_manager.keys():
#             self.int_var_manager[key] = 0  # Đặt giá trị số nguyên về 0
#
#     def set_svm(self, key, value) -> str:
#         if key in self.string_var_manager:
#             raise ValueError(f'Key {key} already exists')
#         if not isinstance(value, str):
#             raise TypeError(f'Value for {key} must be a string')
#         else:
#             self.string_var_manager[key] = value
#             return self.string_var_manager[key]
#
#     def get_svm(self, key) -> str:
#         if key not in self.string_var_manager:
#             raise ValueError(f'Key {key} does not exist')
#         else:
#             return self.string_var_manager[key]
#
#     def get_svm_value(self, key) -> str:
#         return self.get_svm(key)
#
#     def set_svm_value(self, key, value) -> None:
#         if key not in self.string_var_manager:
#             raise ValueError(f'Key {key} does not exist')
#         if not isinstance(value, str):
#             raise TypeError(f'Value for {key} must be a string')
#         else:
#             self.string_var_manager[key] = value
#
#     def set_ivm(self, key, value=0) -> int:
#         if key in self.int_var_manager:
#             raise ValueError(f'Key {key} already exists')
#         if not isinstance(value, int):
#             raise TypeError(f'Value for {key} must be an integer')
#         else:
#             self.int_var_manager[key] = value
#             return self.int_var_manager[key]
#
#     def get_ivm(self, key) -> int:
#         if key not in self.int_var_manager:
#             raise ValueError(f'Key {key} does not exist')
#         else:
#             return self.int_var_manager[key]
#
#     def set_ivm_value(self, key, value) -> None:
#         if key not in self.int_var_manager:
#             raise ValueError(f'Key {key} does not exist')
#         if not isinstance(value, int):
#             raise TypeError(f'Value for {key} must be an integer')
#         else:
#             self.int_var_manager[key] = value
#
#     def get_ivm_value(self, key) -> int:
#         return self.int_var_manager.get(key, 0)
#
#     def __str__(self) -> str:
#         return f"String Variables: {self.string_var_manager}\nInteger Variables: {self.int_var_manager}"

class VariableManager(QObject):
    # Tạo tín hiệu để thông báo khi giá trị thay đổi
    string_var_changed = Signal(str, str)
    int_var_changed = Signal(str, int)

    def __init__(self):
        super().__init__()
        self.string_var_manager = {}
        self.int_var_manager = {}

    def reset_variables(self):
        for key in self.string_var_manager.keys():
            self.string_var_manager[key] = ""  # Đặt giá trị chuỗi về rỗng
            self.string_var_changed.emit(key, "")  # Phát tín hiệu khi giá trị thay đổi
        for key in self.int_var_manager.keys():
            self.int_var_manager[key] = 0  # Đặt giá trị số nguyên về 0
            self.int_var_changed.emit(key, 0)  # Phát tín hiệu khi giá trị thay đổi

    def set_svm(self, key, value) -> str:
        if key in self.string_var_manager:
            raise ValueError(f'Key {key} already exists')
        if not isinstance(value, str):
            raise TypeError(f'Value for {key} must be a string')
        else:
            self.string_var_manager[key] = value
            self.string_var_changed.emit(key, value)  # Phát tín hiệu khi giá trị thay đổi
            return self.string_var_manager[key]

    def get_svm(self, key) -> str:
        if key not in self.string_var_manager:
            raise ValueError(f'Key {key} does not exist')
        else:
            return self.string_var_manager[key]

    def get_svm_value(self, key) -> str:
        """ Lấy giá trị của key trong string_var_manager """
        if key not in self.string_var_manager:
            raise ValueError(f'Key {key} does not exist')
        else:
            return self.string_var_manager[key]  # Trả về giá trị của key

    def set_svm_value(self, key, value) -> None:
        if key not in self.string_var_manager:
            raise ValueError(f'Key {key} does not exist')
        if not isinstance(value, str):
            raise TypeError(f'Value for {key} must be a string')
        else:
            self.string_var_manager[key] = value
            self.string_var_changed.emit(key, value)  # Phát tín hiệu khi giá trị thay đổi

    def set_ivm(self, key, value=0) -> int:
        if key in self.int_var_manager:
            raise ValueError(f'Key {key} already exists')
        if not isinstance(value, int):
            raise TypeError(f'Value for {key} must be an integer')
        else:
            self.int_var_manager[key] = value
            self.int_var_changed.emit(key, value)  # Phát tín hiệu khi giá trị thay đổi
            return self.int_var_manager[key]

    def get_ivm(self, key) -> int:
        if key not in self.int_var_manager:
            raise ValueError(f'Key {key} does not exist')
        else:
            return self.int_var_manager[key]

    def set_ivm_value(self, key, value) -> None:
        if key not in self.int_var_manager:
            raise ValueError(f'Key {key} does not exist')
        if not isinstance(value, int):
            raise TypeError(f'Value for {key} must be an integer')
        else:
            self.int_var_manager[key] = value
            self.int_var_changed.emit(key, value)  # Phát tín hiệu khi giá trị thay đổi

    def get_ivm_value(self, key) -> int:
        return self.int_var_manager.get(key, 0)

    def __str__(self) -> str:
        return f"String Variables: {self.string_var_manager}\nInteger Variables: {self.int_var_manager}"

variable_manager = VariableManager()
