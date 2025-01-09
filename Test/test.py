import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QSlider, QToolButton, QMenuBar, QMenu, QStatusBar)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QTime, Qt, QSize
from PySide6.QtGui import QIcon, QFont, QAction


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ứng dụng phát nhạc với giao diện chính")
        self.resize(600, 300)

        # Cờ kiểm tra trạng thái âm lượng (tắt hoặc bật)
        self.muted = True

        # Khởi tạo giao diện chính
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # Thanh trượt phát nhạc và hiển thị thời gian
        self.playback_layout = QHBoxLayout()
        self.slider_playback = QSlider(Qt.Horizontal)
        self.label_timer = QLabel("00:00:00")
        self.label_timer.setFont(QFont("Arial", 14))
        self.playback_layout.addWidget(self.slider_playback)
        self.playback_layout.addWidget(self.label_timer)
        self.main_layout.addLayout(self.playback_layout)

        # Các nút điều khiển phát nhạc
        self.controls_layout = QHBoxLayout()
        self.btn_play = QToolButton()
        self.btn_play.setIcon(QIcon(":/icons/play.png"))
        self.btn_play.setIconSize(QSize(32, 32))
        self.controls_layout.addWidget(self.btn_play)

        self.btn_pause = QToolButton()
        self.btn_pause.setIcon(QIcon(":/icons/pause.png"))
        self.btn_pause.setIconSize(QSize(32, 32))
        self.controls_layout.addWidget(self.btn_pause)

        self.btn_stop = QToolButton()
        self.btn_stop.setIcon(QIcon(":/icons/stop.png"))
        self.btn_stop.setIconSize(QSize(32, 32))
        self.controls_layout.addWidget(self.btn_stop)

        self.btn_volume = QToolButton()
        self.btn_volume.setIcon(QIcon(":/icons/volume.png"))
        self.btn_volume.setIconSize(QSize(32, 32))
        self.controls_layout.addWidget(self.btn_volume)

        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setValue(70)
        self.controls_layout.addWidget(self.slider_volume)

        self.main_layout.addLayout(self.controls_layout)

        # Khởi tạo thanh menu
        self.menu_bar = QMenuBar()
        self.menu_file = QMenu("Tệp")
        self.action_open = QAction("Mở nhạc")
        self.menu_file.addAction(self.action_open)
        self.menu_bar.addMenu(self.menu_file)
        self.setMenuBar(self.menu_bar)

        # Khởi tạo thanh trạng thái
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Khởi tạo trình phát nhạc
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.audio.setVolume(0.7)
        self.player.setAudioOutput(self.audio)

        # Kết nối các tín hiệu và sự kiện
        self.action_open.triggered.connect(self.open_music)
        self.btn_play.clicked.connect(self.play_music)
        self.btn_pause.clicked.connect(self.pause_music)
        self.btn_stop.clicked.connect(self.stop_music)
        self.slider_volume.valueChanged.connect(self.change_volume)
        self.slider_playback.sliderMoved.connect(self.change_position)
        self.btn_volume.clicked.connect(self.toggle_mute)

        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

    def open_music(self):
        """Mở tệp nhạc."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Mở nhạc", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_name:
            self.player.setSource(QUrl.fromLocalFile(file_name))
            self.status_bar.showMessage(f"Đã tải: {file_name}")

    def play_music(self):
        """Phát nhạc."""
        self.player.play()

    def pause_music(self):
        """Tạm dừng nhạc."""
        self.player.pause()

    def stop_music(self):
        """Dừng phát nhạc."""
        self.player.stop()

    def change_volume(self, value):
        """Thay đổi âm lượng."""
        self.audio.setVolume(value / 100)

    def change_position(self, position):
        """Thay đổi vị trí phát nhạc."""
        self.player.setPosition(position)

    def toggle_mute(self):
        """Bật/tắt tiếng."""
        if self.muted:
            self.audio.setMuted(False)
            self.muted = False
            self.btn_volume.setIcon(QIcon(":/icons/volume.png"))
        else:
            self.audio.setMuted(True)
            self.muted = True
            self.btn_volume.setIcon(QIcon(":/icons/mute.png"))

    def update_position(self, position):
        """Cập nhật thanh trượt và thời gian khi vị trí phát thay đổi."""
        self.slider_playback.setValue(position)
        time = QTime(0, 0, 0).addMSecs(position)
        self.label_timer.setText(time.toString())

    def update_duration(self, duration):
        """Cập nhật phạm vi thanh trượt khi thời lượng thay đổi."""
        self.slider_playback.setRange(0, duration)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())