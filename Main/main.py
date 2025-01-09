import os
import sys
from functools import partial

from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QMainWindow, QFrame, QPushButton, \
    QHBoxLayout, QLineEdit, QTextEdit, QSizePolicy, QSpacerItem, QGridLayout, QComboBox, QSlider, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from Main import dictionary
from utilizes.txt_handler import read_json
from utilizes.var_manager import variable_manager as vm
from Main.back_end import eu

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        eu.main_ui = self

        self.load_setting = read_json('language.json')
        self.language = self.load_setting.get('language', 'VietNam')
        vm.set_svm('language', self.language)
        self.get_language()

        self.setWindowTitle("Youtube Tool")
        default_font = QFont('Times New Roman', 16)
        self.setFont(default_font)

        self.notebook = QTabWidget(self)
        self.setCentralWidget(self.notebook)

        self.task_frame = QWidget()
        self.notebook.addTab(self.task_frame, "Task")

        main_task_layout = QVBoxLayout()
        main_task_layout.setAlignment(Qt.AlignTop)
        self.task_frame.setLayout(main_task_layout)

        task_info_frame = QWidget()
        task_info_layout = QGridLayout()
        task_info_layout.setContentsMargins(0, 0, 0, 0)
        task_info_frame.setLayout(task_info_layout)
        task_info_layout.setAlignment(Qt.AlignLeft)
        main_task_layout.addWidget(task_info_frame)

        task_info_layout.setColumnStretch(0, 1)
        task_info_layout.setColumnStretch(1, 3)
        task_info_layout.setColumnStretch(2, 1)


        info_frame = QWidget()
        info_layout = QGridLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_frame.setLayout(info_layout)
        task_info_layout.addWidget(info_frame, 0, 0)

        info_layout.addWidget(QLabel("Thông tin"), 0, 0)

        info_main = QWidget()
        info_main_layout = QGridLayout()
        info_main.setStyleSheet("background-color: #F0F0F0; border: 2px solid #F0F0F0; border-radius: 10px; font: 16pt 'Times New Roman';")
        info_main.setLayout(info_main_layout)
        info_layout.addWidget(info_main, 1, 0)

        info_main_layout.addWidget(QLabel("Tổng: "), 0, 0)
        sum_index = QLabel(str(vm.set_ivm("sum_index", 0)))
        info_main_layout.addWidget(sum_index, 0, 1)
        vm.int_var_changed.connect(sum_index.setText(int(vm.get_ivm_value("sum_index"))))
        info_main_layout.addWidget(QLabel("Đã làm: "), 1, 0)
        info_main_layout.addWidget(QLabel("1"), 1, 1)

        guide_frame = QWidget()
        guide_layout = QGridLayout()
        guide_layout.setContentsMargins(0, 0, 0, 0)
        guide_frame.setLayout(guide_layout)
        task_info_layout.addWidget(guide_frame, 0, 1)

        guide_layout.addWidget(QLabel("Hướng dẫn"), 0, 0)

        guide_main = QWidget()
        guide_main_layout = QGridLayout()
        guide_main.setStyleSheet("background-color: #F0F0F0; border: 2px solid #F0F0F0; border-radius: 10px; font: 16pt 'Times New Roman';")
        guide_main.setLayout(guide_main_layout)
        guide_layout.addWidget(guide_main, 1, 0)

        guide_main_layout.addWidget(QLabel("Tổng: "), 0, 0)
        guide_main_layout.addWidget(QLabel(vm.get_svm_value("notice")), 0, 1)
        guide_main_layout.addWidget(QLabel("Đã làm: "), 1, 0)
        guide_main_layout.addWidget(QLabel("1"), 1, 1)

        version_frame = QWidget()
        version_layout = QGridLayout()
        version_layout.setContentsMargins(0, 0, 0, 0)
        version_frame.setLayout(version_layout)
        task_info_layout.addWidget(version_frame, 0, 2)

        version_layout.addWidget(QLabel("Phiên bản"), 0, 0)

        version_main = QWidget()
        version_main_layout = QGridLayout()
        version_main.setStyleSheet("background-color: #F0F0F0; border: 2px solid #F0F0F0; border-radius: 10px; font: 16pt 'Times New Roman';")
        version_main.setLayout(version_main_layout)
        version_layout.addWidget(version_main, 1, 0)

        version_main_layout.addWidget(QLabel("Version: "), 0, 0)
        version_main_layout.addWidget(QLabel("1.0"), 0, 1)
        version_main_layout.addWidget(QLabel("Language: "), 1, 0)
        language = QComboBox()
        language.addItem("VietNam")
        language.addItem("ThaiLan")
        language.setCurrentIndex(0 if self.language == "VietNam" else 1)
        language.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 0px;")
        version_main_layout.addWidget(language, 1, 1)

        main_task_layout.addWidget(QLabel("Thông tin câu"))

        sentence_frame = QWidget()
        sentence_frame.setObjectName("sentence_frame")
        sentence_frame.setStyleSheet("QWidget#sentence_frame {background-color: #F0F0F0; border: 2px solid #F0F0F0; border-radius: 10px; } QWidget {font: 16pt 'Times New Roman';}")
        main_task_layout.addWidget(sentence_frame)

        sentence_layout = QVBoxLayout()
        sentence_layout.setAlignment(Qt.AlignTop)
        sentence_frame.setLayout(sentence_layout)

        stt_frame = QWidget()
        stt_layout = QHBoxLayout()
        stt_layout.setAlignment(Qt.AlignLeft)
        stt_frame.setLayout(stt_layout)
        sentence_layout.addWidget(stt_frame)

        stt_label = QLabel("STT")
        stt_label.setFixedWidth(200)
        stt_layout.addWidget(stt_label)

        stt_entry = QLineEdit()
        stt_entry.setFixedWidth(100)
        stt_layout.addWidget(stt_entry)

        slider_playback = QSlider(Qt.Horizontal)
        label_timer = QLabel("00:00:00")
        stt_layout.addWidget(slider_playback)
        stt_layout.addWidget(label_timer)

        filename_frame = QWidget()
        filename_layout = QHBoxLayout()
        filename_layout.setAlignment(Qt.AlignLeft)
        filename_frame.setLayout(filename_layout)
        sentence_layout.addWidget(filename_frame)

        filename_label = QLabel("Tên file")
        filename_label.setFixedWidth(200)
        filename_layout.addWidget(filename_label)

        filename_entry = QLineEdit()
        filename_layout.addWidget(filename_entry)
        # filename_layout.setStretch(1, 1)

        button_delete = QPushButton("Đánh dấu xóa")
        button_cut = QPushButton("Đánh dấu cắt")
        button_raw = QPushButton("Về câu gốc")

        button_style = """
                QPushButton {
                    background-color: white;
                    border: 1px solid #D0D0D0;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: deepskyblue;  /* Màu khi di chuột qua */
                }
                QPushButton:pressed {
                    background-color: dodgerblue;  /* Màu khi nhấn */
                }
                """

        button_delete.setStyleSheet(button_style)
        button_cut.setStyleSheet(button_style)
        button_raw.setStyleSheet(button_style)

        filename_layout.addWidget(button_delete)
        filename_layout.addWidget(button_cut)
        filename_layout.addWidget(button_raw)

        normalize_frame = QWidget()
        normalize_layout = QHBoxLayout()
        normalize_layout.setAlignment(Qt.AlignLeft)
        normalize_frame.setLayout(normalize_layout)
        sentence_layout.addWidget(normalize_frame)

        normalize_label = QLabel("Chuẩn hóa")
        normalize_label.setFixedWidth(200)
        normalize_layout.addWidget(normalize_label)

        normalize_entry = QTextEdit()
        normalize_entry.setMinimumHeight(200)
        normalize_entry.setMinimumWidth(1000)
        normalize_entry.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        normalize_layout.addWidget(normalize_entry)

        itn_frame = QWidget()
        itn_layout = QHBoxLayout()
        itn_layout.setAlignment(Qt.AlignLeft)
        itn_frame.setLayout(itn_layout)
        sentence_layout.addWidget(itn_frame)

        itn_label = QLabel("Chuẩn hóa ITN")
        itn_label.setFixedWidth(200)
        itn_layout.addWidget(itn_label)

        itn_entry = QTextEdit()
        itn_entry.setMinimumHeight(200)
        itn_entry.setMinimumWidth(1000)
        itn_entry.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        itn_layout.addWidget(itn_entry)


        self.login_frame = QWidget()
        self.notebook.addTab(self.login_frame, "Login")

        main_login_layout = QGridLayout()
        main_login_layout.setAlignment(Qt.AlignTop)
        self.login_frame.setLayout(main_login_layout)

        main_login_layout.addWidget(QLabel("Login Local"), 0, 0)

        login_local = QWidget()
        login_local_layout = QGridLayout()
        login_local.setStyleSheet("background-color: #F0F0F0; border: 2px solid #F0F0F0; border-radius: 10px; font: 16pt 'Times New Roman';")
        login_local.setLayout(login_local_layout)
        main_login_layout.addWidget(login_local, 1, 0)

        login_local_layout.addWidget(QLabel("File ans:"), 0, 0)
        self.file_ans = QLineEdit(vm.set_svm("file_ans", ""))
        self.file_ans.setAcceptDrops(True)
        self.file_ans.setStyleSheet("background-color: white; border: 1px solid #D0D0D0; border-radius: 0px; font: 16pt 'Times New Roman';")
        login_local_layout.addWidget(self.file_ans, 0, 1, 1, 3)

        login_local_layout.addWidget(QLabel("File scp:"), 1, 0)
        self.file_scp = QLineEdit(vm.set_svm("file_scp", ""))
        self.file_scp.setAcceptDrops(True)
        self.file_scp.setStyleSheet("background-color: white; border: 1px solid #D0D0D0; border-radius: 0px; font: 16pt 'Times New Roman';")
        login_local_layout.addWidget(self.file_scp, 1, 1, 1, 3)

        login_local_layout.addWidget(QLabel("Folder audio:"), 2, 0)
        self.file_audio = QLineEdit(vm.set_svm("file_audio", ""))
        self.file_audio.setAcceptDrops(True)
        self.file_audio.setStyleSheet("background-color: white; border: 1px solid #D0D0D0; border-radius: 0px; font: 16pt 'Times New Roman';")
        login_local_layout.addWidget(self.file_audio, 2, 1, 1, 3)

        login_local_layout.addWidget(QLabel("Start index:"), 3, 0)
        self.start_index = QLineEdit(str(vm.set_ivm("start_index", 0)))
        self.start_index.setStyleSheet("background-color: white; border: 1px solid #D0D0D0; border-radius: 0px; font: 16pt 'Times New Roman';")
        login_local_layout.addWidget(self.start_index, 3, 1)

        login_local_layout.addWidget(QLabel("End index:"), 3, 2)
        self.end_index = QLineEdit(str(vm.set_ivm("end_index", 0)))
        self.end_index.setStyleSheet("background-color: white; border: 1px solid #D0D0D0; border-radius: 0px; font: 16pt 'Times New Roman';")
        login_local_layout.addWidget(self.end_index, 3, 3)

        local_button = QPushButton("Login")
        local_button.setStyleSheet(button_style)
        local_button.setMaximumWidth(100)
        login_local_layout.addWidget(local_button, 4, 1)

        self.file_ans.dragEnterEvent = self.drag_enter_event
        self.file_ans.dragMoveEvent = self.drag_move_event
        self.file_ans.dropEvent = partial(self.drop_event, file = self.file_ans)

        self.file_scp.dragEnterEvent = self.drag_enter_event
        self.file_scp.dragMoveEvent = self.drag_move_event
        self.file_scp.dropEvent = partial(self.drop_event, file=self.file_scp)

        self.file_audio.dragEnterEvent = self.drag_enter_event
        self.file_audio.dragMoveEvent = self.drag_move_event
        self.file_audio.dropEvent = partial(self.drop_event, file=self.file_audio)

        local_button.clicked.connect(self.get_data_local)

        main_login_layout.addWidget(QLabel("Login Server"), 2, 0)

        self.notebook.setCurrentIndex(1)

        self.resize(400, 300)

    def get_language(self):
        for text_id in dictionary.keys():
            langs = dictionary.get(text_id)
            lang = self.language
            vm.set_svm(text_id, langs.get(lang))

    def drag_enter_event(self, event):
        # Kiểm tra xem nội dung kéo vào có phải là file không
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drag_move_event(self, event):
        event.accept()

    def drop_event(self, event, file):
        # Lấy đường dẫn file khi thả vào ô
        if event.mimeData().hasUrls():
            file_urls = event.mimeData().urls()
            if file_urls:
                # Hiển thị đường dẫn file đầu tiên trong QLineEdit
                file_path = file_urls[0].toLocalFile()
                file.setText(file_path)
        else:
            event.ignore()

    def get_data_local(self):
        vm.set_svm_value("file_ans", self.file_ans.text())
        vm.set_svm_value("file_scp", self.file_scp.text())
        vm.set_svm_value("file_audio", self.file_audio.text())
        if vm.get_svm_value("file_ans") == "" or ".ans" != os.path.splitext(vm.get_svm_value("file_ans"))[1]:
            if self.messagebox("File ans không đúng!"):
                return
        elif vm.get_svm_value("file_scp") == "" or ".scp" != os.path.splitext(vm.get_svm_value("file_scp"))[1]:
            if self.messagebox("File scp không đúng!"):
                return
        elif vm.get_svm_value("file_audio") == "":
            if self.messagebox("Hãy điền link folder audio!"):
                return
        else:
            vm.set_ivm_value("start_index", int(self.start_index.text()))
            vm.set_ivm_value("end_index", int(self.end_index.text()))
            if (vm.get_ivm_value("start_index") == 0 and vm.get_ivm_value("end_index") == 0) or vm.get_ivm_value("start_index") > vm.get_ivm_value("end_index"):
                if self.messagebox("Vui lòng nhập đúng index!"):
                    return
            if eu.get_data_local():
                self.notebook.setCurrentIndex(0)

    def messagebox(self, value):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Cảnh báo")
        msg.setText(value)
        msg.setStandardButtons(QMessageBox.Ok)

        msg.setStyleSheet("QLabel { font-size: 18px; font-family: Times New Roman; }")

        window_rect = self.geometry()
        popup_rect = msg.rect()
        popup_position = window_rect.center() - popup_rect.center()
        msg.move(popup_position)

        response = msg.exec()

        if response:
            return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_ui = MainUI()
    main_ui.show()
    sys.exit(app.exec())