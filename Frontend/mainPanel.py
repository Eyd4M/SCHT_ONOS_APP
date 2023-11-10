import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPalette, QColor, QLinearGradient, QBrush


class NetworkConfigurator(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        #buttons
        self.select_streams_button = QPushButton("Select iPerf Streams File", self)
        self.select_streams_button.setStyleSheet("QPushButton { height: 100px; font-size: 16px; }")
        self.select_streams_button.clicked.connect(self.select_streams_file)
        layout.addWidget(self.select_streams_button)

        self.select_config_button = QPushButton("Select Configuration File Location", self)
        self.select_config_button.setStyleSheet("QPushButton { height: 100px; font-size: 16px; }")
        self.select_config_button.clicked.connect(self.select_config_location)
        layout.addWidget(self.select_config_button)

        self.configure_button = QPushButton("Configure Optimal Network", self)
        self.configure_button.setStyleSheet("QPushButton { height: 100px; font-size: 16px; }")
        self.configure_button.clicked.connect(self.configure_network)
        layout.addWidget(self.configure_button)

        self.view_config_button = QPushButton("View Configuration File", self)
        self.view_config_button.setStyleSheet("QPushButton { height: 100px; font-size: 16px; }")
        self.view_config_button.clicked.connect(self.view_config_file)
        layout.addWidget(self.view_config_button)

        self.status_label = QLabel(self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        #Backgroung color gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(180, 180, 180))
        brush = QBrush(gradient)

        palette = self.palette()
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('Network Configurator')


    def select_streams_file(self):
        global file_path
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select iPerf Streams File", "")
        self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
        self.status_label.setText(f"Selected iPerf Streams File: {file_path}")

    def select_config_location(self):
        global folder_path
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, "Select Configuration File Location")
        self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
        self.status_label.setText(f"Selected Configuration File Location: {folder_path}")

    def configure_network(self):
        # this method will call function from backend
        self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
        self.status_label.setText("Configuring Optimal Network")

    def view_config_file(self):
        if hasattr(self, config_file_path) and self.config_file_path:
            subprocess.Popen(['notepad.exe', self.config_file_path])
            self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
            self.status_label.setText("Viewing Configuration File")
        else:
            self.status_label.setStyleSheet("QLabel { font-size: 20px; color: red; }")
            self.status_label.setText("No configuration file")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NetworkConfigurator()
    window.show()
    sys.exit(app.exec_())