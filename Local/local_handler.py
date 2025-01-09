def drag_enter_event(event):
    if event.mimeData().hasUrls():
        event.accept()
    else:
        event.ignore()

def drag_move_event(self, event):
    event.accept()

def drop_event(self, event):
    # Lấy đường dẫn file khi thả vào ô
    if event.mimeData().hasUrls():
        file_urls = event.mimeData().urls()
        if file_urls:
            # Hiển thị đường dẫn file đầu tiên trong QLineEdit
            file_path = file_urls[0].toLocalFile()
            self.file_input.setText(file_path)
    else:
        event.ignore()