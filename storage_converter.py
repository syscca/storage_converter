import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QComboBox,
                             QPushButton, QMenu, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard

class StorageConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("存储单位换算工具")
        # 移除固定窗口大小，设置最小尺寸
        self.setMinimumSize(400, 300)

        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 添加边距

        # 添加使用提示标签
        tip_label = QLabel("提示：可以使用鼠标滚轮、键盘上下键或右侧按钮来调整数值")
        tip_label.setStyleSheet("color: #666666; font-size: 10pt;")
        main_layout.addWidget(tip_label)

        # 单位列表
        self.units = ["B", "KB", "MB", "GB", "TB"]

        # 创建输入框和标签
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)  # 增加组件间距

        value_label = QLabel("输入数值：")
        self.value_entry = QLineEdit()
        self.value_entry.setText("1")  # 设置默认值为1
        self.value_entry.wheelEvent = self.handle_wheel_event
        self.value_entry.keyPressEvent = self.handle_key_press
        self.value_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 允许水平扩展

        # 移除鼠标点击事件处理器，恢复手动输入功能

        # 创建上下调节按钮
        adjust_buttons_widget = QWidget()
        adjust_buttons_layout = QVBoxLayout(adjust_buttons_widget)
        adjust_buttons_layout.setContentsMargins(0, 0, 0, 0)
        adjust_buttons_layout.setSpacing(2)

        self.up_button = QPushButton("▲")
        self.up_button.setFixedSize(20, 20)
        self.up_button.clicked.connect(self.increase_value)

        self.down_button = QPushButton("▼")
        self.down_button.setFixedSize(20, 20)
        self.down_button.clicked.connect(self.decrease_value)

        adjust_buttons_layout.addWidget(self.up_button)
        adjust_buttons_layout.addWidget(self.down_button)

        input_layout.addWidget(value_label)
        input_layout.addWidget(self.value_entry)
        input_layout.addWidget(adjust_buttons_widget)

        # 创建单位选择部件
        unit_widget = QWidget()
        unit_layout = QHBoxLayout(unit_widget)
        unit_layout.setContentsMargins(0, 0, 0, 0)
        unit_layout.setSpacing(5)  # 设置组件之间的间距

        from_label = QLabel("从：")
        from_label.setFixedWidth(30)  # 设置标签固定宽度
        self.from_unit = QComboBox()
        self.from_unit.addItems(self.units)
        self.from_unit.setCurrentText("GB")  # 设置默认源单位为GB

        to_label = QLabel("转换到：")
        to_label.setFixedWidth(50)  # 设置标签固定宽度
        self.to_unit = QComboBox()
        self.to_unit.addItems(self.units)
        self.to_unit.setCurrentText("MB")  # 设置默认目标单位为MB

        unit_layout.addWidget(from_label)
        unit_layout.addWidget(self.from_unit)
        unit_layout.addSpacing(10)  # 添加固定间距
        unit_layout.addWidget(to_label)
        unit_layout.addWidget(self.to_unit)
        unit_layout.addStretch()  # 添加弹性空间

        # 创建转换按钮
        self.convert_button = QPushButton("转换")
        self.convert_button.clicked.connect(self.convert)

        # 创建结果显示框
        self.result_entry = QLineEdit()
        self.result_entry.setReadOnly(True)
        self.result_entry.setText("结果将在这里显示")
        self.result_entry.setContextMenuPolicy(Qt.CustomContextMenu)
        self.result_entry.customContextMenuRequested.connect(self.show_context_menu)

        # 创建复制按钮
        self.copy_button = QPushButton("复制结果")
        self.copy_button.clicked.connect(self.copy_result)
        self.copy_button.setEnabled(False)

        # 创建结果区域布局
        result_widget = QWidget()
        result_layout = QHBoxLayout(result_widget)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.addWidget(self.result_entry)
        result_layout.addWidget(self.copy_button)

        # 添加所有部件到主布局
        main_layout.addWidget(input_widget)
        main_layout.addWidget(unit_widget)
        main_layout.addWidget(self.convert_button)
        main_layout.addWidget(result_widget)
        main_layout.addStretch()

        # 用于存储当前结果
        self.current_result = ""

    def convert(self):
        try:
            value = float(self.value_entry.text())
            from_unit = self.from_unit.currentText()
            to_unit = self.to_unit.currentText()

            bytes_value = self.to_bytes(value, from_unit)
            result = self.from_bytes(bytes_value, to_unit)

            self.current_result = f"{value} {from_unit} = {result:,.0f} {to_unit}"
            self.result_entry.setText(self.current_result)
            self.copy_button.setEnabled(True)
        except ValueError:
            self.result_entry.setText("请输入有效的数字")
            self.copy_button.setEnabled(False)
            self.current_result = ""

    def copy_result(self):
        if self.current_result:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_result)

    def show_context_menu(self, pos):
        if self.current_result:
            context_menu = QMenu(self)
            copy_selected_action = context_menu.addAction("复制选中内容")
            copy_all_action = context_menu.addAction("复制全部")

            action = context_menu.exec_(self.result_entry.mapToGlobal(pos))

            if action == copy_selected_action:
                self.copy_selected()
            elif action == copy_all_action:
                self.copy_result()

    def copy_selected(self):
        if self.result_entry.hasSelectedText():
            clipboard = QApplication.clipboard()
            clipboard.setText(self.result_entry.selectedText())

    def to_bytes(self, value, unit):
        multipliers = {
            "B": 1,
            "KB": 1024,
            "MB": 1024 ** 2,
            "GB": 1024 ** 3,
            "TB": 1024 ** 4
        }
        return value * multipliers[unit]

    def from_bytes(self, bytes_value, unit):
        divisors = {
            "B": 1,
            "KB": 1024,
            "MB": 1024 ** 2,
            "GB": 1024 ** 3,
            "TB": 1024 ** 4
        }
        return bytes_value / divisors[unit]

    def increase_value(self):
        text = self.value_entry.text()
        try:
            current_value = float(text) if text else 0
            new_value = current_value + 1
            self.value_entry.setText(f"{int(new_value)}")
            self.convert()
        except ValueError:
            pass

    def decrease_value(self):
        text = self.value_entry.text()
        try:
            current_value = float(text) if text else 0
            new_value = max(0, current_value - 1)  # 减少1GB，但不小于0
            self.value_entry.setText(f"{int(new_value)}")
            self.convert()
        except ValueError:
            pass

    def handle_wheel_event(self, event):
        text = self.value_entry.text()
        try:
            current_value = float(text) if text else 0
            delta = event.angleDelta().y()
            
            # 使用统一的1GB步长
            if delta > 0:
                new_value = current_value + 1
            else:
                new_value = max(0, current_value - 1)  # 确保不会小于0
            
            self.value_entry.setText(f"{int(new_value)}")
            self.convert()
        except ValueError:
            pass

    def handle_key_press(self, event):
        if event.key() in [Qt.Key_Up, Qt.Key_Down]:
            text = self.value_entry.text()
            try:
                current_value = float(text) if text else 0
                
                if event.key() == Qt.Key_Up:
                    new_value = current_value + 1
                else:
                    new_value = max(0, current_value - 1)  # 确保不会小于0
                
                self.value_entry.setText(f"{int(new_value)}")
                self.convert()
            except ValueError:
                pass
        else:
            QLineEdit.keyPressEvent(self.value_entry, event)  # 使用原始的QLineEdit键盘事件处理

    def handle_mouse_press(self, event):
        try:
            current_value = float(self.value_entry.text())
            height = self.value_entry.height()
            y = event.pos().y()
            
            # 使用统一的1GB步长
            if y < height / 2:
                new_value = current_value + 1
            else:
                new_value = max(0, current_value - 1)  # 确保不会小于0
            
            self.value_entry.setText(f"{new_value:.1f}")
            self.convert()
        except ValueError:
            pass  # 如果当前输入不是有效数字，忽略鼠标点击事件

def main():
    app = QApplication(sys.argv)
    window = StorageConverter()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
