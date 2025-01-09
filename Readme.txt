QWidget
    QWidget là lớp cơ bản của mọi widget trong PyQt5. Mỗi thành phần giao diện người dùng (như nút bấm, hộp văn bản, v.v.) đều kế thừa từ QWidget.

    Các thuộc tính và phương thức cơ bản:
    setWindowTitle("Title"): Đặt tiêu đề cho cửa sổ.
    resize(width, height): Thay đổi kích thước của widget.
    show(): Hiển thị widget.

QTabWidget
    QTabWidget cho phép bạn tạo một giao diện với các tab, rất hữu ích khi bạn muốn tổ chức nội dung trong một ứng dụng.

    Các thuộc tính và phương thức cơ bản:
    addTab(widget, "Tab Name"): Thêm một tab mới với một widget con.
    removeTab(index): Xóa tab tại vị trí chỉ định.
    setTabText(index, "New Name"): Đổi tên tab.
    currentIndex(): Lấy chỉ số của tab hiện tại.

QPushButton: Nút bấm.
QLabel: Hiển thị văn bản hoặc hình ảnh.
QLineEdit: Hộp nhập liệu đơn dòng.
QTextEdit: Hộp nhập liệu đa dòng.
QComboBox: Hộp thả xuống.
QCheckBox: Hộp kiểm.
QRadioButton: Nút radio.

QVBoxLayout: Sắp xếp các widget theo chiều dọc.
QHBoxLayout: Sắp xếp các widget theo chiều ngang.
QGridLayout: Sắp xếp các widget theo dạng lưới.

CSS cơ bản cho PyQt5:
    background-color: Chỉ định màu nền của widget.
    color: Thay đổi màu chữ (ví dụ: "color: red;").
    border: Thiết lập viền cho widget (ví dụ: "border: 1px solid black;").