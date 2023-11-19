import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QTextEdit, \
    QMessageBox, QDialog
from PyQt5.QtGui import QPalette, QColor, QLinearGradient, QBrush
import os
from Backend.onos_configuration import configure_network

CONF_FILE = 'conf.json'
global root_dir
global network_file_path
global json_folder_path
global streams_file_path
network_file_path = ""
json_folder_path = ""
streams_file_path = ""
root_dir = ""

class ViewConfigDialog(QDialog):
    def __init__(self, json_data):
        super().__init__()
        self.setWindowTitle('View Configuration File')

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setPlainText(json_data)
        text_edit.setReadOnly(True)

        layout.addWidget(text_edit)

        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)

        layout.addWidget(close_button)

        self.setLayout(layout)

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

        self.select_network_button = QPushButton("Select Network File", self)
        self.select_network_button.setStyleSheet("QPushButton { height: 100px; font-size: 16px; }")
        self.select_network_button.clicked.connect(self.select_network_file)
        layout.addWidget(self.select_network_button)

        self.select_config_button = QPushButton("Select Configuration File Location", self)
        self.select_config_button.setStyleSheet("QPushButton { height: 100px; font-size: 16px; }")
        self.select_config_button.clicked.connect(self.select_config_location)
        layout.addWidget(self.select_config_button)

        self.ip_input = QLineEdit(self)  # QLineEdit for IP input
        self.ip_input.setPlaceholderText("Enter IP Address")
        layout.addWidget(self.ip_input)

        self.save_ip_button = QPushButton("Save IP Address", self)
        self.save_ip_button.setStyleSheet("QPushButton { height: 100px; font-size: 16px; }")
        self.save_ip_button.clicked.connect(self.save_ip_address)
        layout.addWidget(self.save_ip_button)

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


    def save_ip_address(self):
        global ip
        ip = str(self.ip_input.text())
        if ip:
            self.ip = ip
            self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
            self.status_label.setText(f"Saved IP Address: {self.ip}")
        else:
            self.status_label.setStyleSheet("QLabel { font-size: 20px; color: red; }")
            self.status_label.setText("Please enter an IP address")

    def select_streams_file(self):
        global streams_file_path
        file_dialog = QFileDialog()
        streams_file_path, _ = file_dialog.getOpenFileName(self, "Select iPerf Streams File", "","Text files (*.txt)")
        self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
        self.status_label.setText(f"Selected iPerf Streams File: {streams_file_path}")

    def select_network_file(self):
        global network_file_path
        file_dialog = QFileDialog()
        network_file_path, _ = file_dialog.getOpenFileName(self, "Select iPerf Streams File", "","CSV files (*.csv)")
        self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
        self.status_label.setText(f"Selected iPerf Streams File: {network_file_path}")

    def select_config_location(self):
        global root_dir
        folder_dialog = QFileDialog()
        root_dir = folder_dialog.getExistingDirectory(self, "Select Configuration File Location")
        self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
        self.status_label.setText(f"Selected Configuration File Location: {root_dir}")

    def configure_network(self):
        self.status_label.setStyleSheet("QLabel { font-size: 20px; }")
        self.status_label.setText("Configuring Optimal Network")
        print(configure_network(network_file_path, streams_file_path, ip, root_dir).edges)

    def view_config_file(self):
        global json_file_path
        json_file_path = f"{root_dir}\\{CONF_FILE}"  # Ustawienie ścieżki pliku JSON

        if json_file_path:
            try:
                with open(json_file_path, 'r') as file:
                    data = json.load(file)
                    pretty_json = json.dumps(data, indent=4)

                    dialog = ViewConfigDialog(pretty_json)
                    dialog.exec_()

            except FileNotFoundError:
                print(f'File "{json_file_path}" not found.')
            except json.JSONDecodeError:
                print(f'File "{json_file_path}" is not a valid JSON file.')
        else:
            print('No JSON file selected.')



def run_application():
    app = QApplication(sys.argv)
    window = NetworkConfigurator()
    window.show()
    sys.exit(app.exec_())