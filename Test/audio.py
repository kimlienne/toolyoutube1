import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,
                             QPushButton, QTextEdit, QComboBox, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import từ PySide6
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QUrl


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Tool")
        self.resize(800, 600)
        default_font = QFont('Times New Roman', 16)
        self.setFont(default_font)

        self.notebook = QTabWidget(self)
        self.setCentralWidget(self.notebook)

        # Tab Task
        self.task_frame = QWidget()
        self.notebook.addTab(self.task_frame, "Task")

        main_task_layout = QVBoxLayout()
        main_task_layout.setAlignment(Qt.AlignTop)
        self.task_frame.setLayout(main_task_layout)

        # Section: STT
        stt_frame = QWidget()
        stt_layout = QHBoxLayout()
        stt_frame.setLayout(stt_layout)
        main_task_layout.addWidget(stt_frame)

        stt_label = QLabel("STT:")
        stt_label.setFixedWidth(100)
        stt_layout.addWidget(stt_label)

        self.stt_entry = QLineEdit()
        self.stt_entry.setFixedWidth(200)
        stt_layout.addWidget(self.stt_entry)

        # Section: Audio Player (dùng PySide6)
        audio_frame = QWidget()
        audio_layout = QHBoxLayout()
        audio_frame.setLayout(audio_layout)
        main_task_layout.addWidget(audio_frame)

        audio_label = QLabel("Audio:")
        audio_label.setFixedWidth(100)
        audio_layout.addWidget(audio_label)

        self.audio_button = QPushButton("Select Audio")
        audio_layout.addWidget(self.audio_button)

        self.play_button = QPushButton("Play")
        self.play_button.setEnabled(False)
        audio_layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        audio_layout.addWidget(self.stop_button)

        # Set up PySide6 audio player
        self.audio_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_player.setAudioOutput(self.audio_output)

        # Connect buttons
        self.audio_button.clicked.connect(self.select_audio)
        self.play_button.clicked.connect(self.play_audio)
        self.stop_button.clicked.connect(self.stop_audio)

    def select_audio(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_name:
            self.audio_player.setSource(QUrl.fromLocalFile(file_name))
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)

    def play_audio(self):
        if self.audio_player.playbackState() == QMediaPlayer.PlayingState:
            self.audio_player.pause()
            self.play_button.setText("Play")
        else:
            self.audio_player.play()
            self.play_button.setText("Pause")

    def stop_audio(self):
        self.audio_player.stop()
        self.play_button.setText("Play")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())