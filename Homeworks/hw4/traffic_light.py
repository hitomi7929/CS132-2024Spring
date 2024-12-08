import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow
from PyQt5.QtCore import Qt, QTimer


def TrafficLight():
    app = QApplication(sys.argv)

    traffic_light_display = TrafficLightDisplay()
    control_panel = ControlPanel(traffic_light_display)

    control_panel.move(100, 100)
    traffic_light_display.move(400, 300)

    control_panel.show()
    traffic_light_display.show()

    sys.exit(app.exec_())


class ControlPanel(QMainWindow):
    def __init__(self, traffic_light_display):
        super().__init__()
        self.traffic_light_display = traffic_light_display
        
        self.setWindowTitle('Control Panel')
        widget = QWidget()
        self.setCentralWidget(widget)

        
        self.red = QLineEdit()
        self.red.setPlaceholderText("Red Duration (s)")
        self.yellow = QLineEdit()
        self.yellow.setPlaceholderText("Yellow Duration (s)")
        self.green = QLineEdit()
        self.green.setPlaceholderText("Green Duration (s)")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        input_layout.addWidget(self.red)
        input_layout.addWidget(self.yellow)
        input_layout.addWidget(self.green)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        widget.setLayout(main_layout)

        self.set_enabled(True)
    
    def set_enabled(self, enabled):
        self.red.setEnabled(enabled)
        self.yellow.setEnabled(enabled)
        self.green.setEnabled(enabled)

    def start(self):
        try:
            red_duration = int(self.red.text())
            yellow_duration = int(self.yellow.text())
            green_duration = int(self.green.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", 
                    "Durations should be positive integers, please reset.")
            return

        if yellow_duration <= 0 or red_duration <= 0 or green_duration <= 0:
            QMessageBox.warning(self, "Time Error", 
                    "Durations should be positive integers, please reset.")
            return

        if yellow_duration > red_duration or yellow_duration > green_duration:
            QMessageBox.warning(self, "Time Error", 
                    "Yellow duration should not exceed red or green duration, please reset.")
            return

        self.set_enabled(False)
        self.traffic_light_display.set_durations(red_duration, yellow_duration, green_duration)
        self.traffic_light_display.start()

    def stop(self):
        self.traffic_light_display.stop()
        self.set_enabled(True)
    
    def closeEvent(self, event):
        self.traffic_light_display.close()
        event.accept()


class TrafficLightDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.red_duration = 0
        self.yellow_duration = 0
        self.green_duration = 0
        self.current_light = 'red'

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_lights)
        self.time_left = 0

        self.flashing_timer = QTimer(self)
        self.flashing_timer.timeout.connect(self.flash_yellow)
        self.yellow_visible = True

        self.setWindowTitle('Traffic Light Display')

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        self.red_light = QLabel("Red Light")
        self.yellow_light = QLabel("Yellow Light")
        self.green_light = QLabel("Green Light")
        self.timer_display = QLabel("Timer: 0s")
        self.red_light.setAlignment(Qt.AlignCenter)
        self.yellow_light.setAlignment(Qt.AlignCenter)
        self.green_light.setAlignment(Qt.AlignCenter)
        self.timer_display.setAlignment(Qt.AlignCenter)

        self.red_light.setStyleSheet("background-color: grey; color: white;")
        self.yellow_light.setStyleSheet("background-color: grey; color: white;")
        self.green_light.setStyleSheet("background-color: grey; color: white;")

        layout.addWidget(self.red_light)
        layout.addWidget(self.yellow_light)
        layout.addWidget(self.green_light)
        layout.addWidget(self.timer_display)

        widget.setLayout(layout)

    def set_durations(self, red_duration, yellow_duration, green_duration):
        self.red_duration = red_duration
        self.yellow_duration = yellow_duration
        self.green_duration = green_duration

    def start(self):
        self.current_light = 'red'
        self.time_left = self.red_duration
        self.update_light_display()
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()
        self.current_light = 'flashing_yellow'
        self.update_light_display()
    
    def flash_yellow(self):
        self.yellow_visible = not self.yellow_visible
        if self.yellow_visible:
            self.yellow_light.setStyleSheet("background-color: yellow; color: grey;")
        else:
            self.yellow_light.setStyleSheet("background-color: grey; color: white;")

    def update_lights(self):
        self.time_left -= 1
        if self.time_left <= 0:
            if self.current_light == 'red':
                self.current_light = 'green'
                self.time_left = self.green_duration
            elif self.current_light == 'green':
                self.current_light = 'yellow'
                self.time_left = self.yellow_duration
            elif self.current_light == 'yellow':
                self.current_light = 'red'
                self.time_left = self.red_duration
        self.update_light_display()

    def update_light_display(self):
        if self.current_light == 'red':
            self.flashing_timer.stop()
            self.red_light.setStyleSheet("background-color: red; color: white;")
            self.yellow_light.setStyleSheet("background-color: grey; color: white;")
            self.green_light.setStyleSheet("background-color: grey; color: white;")
        elif self.current_light == 'yellow':
            self.flashing_timer.stop()
            self.red_light.setStyleSheet("background-color: grey; color: white;")
            self.yellow_light.setStyleSheet("background-color: yellow; color: grey;")
            self.green_light.setStyleSheet("background-color: grey; color: white;")
        elif self.current_light == 'green':
            self.flashing_timer.stop()
            self.red_light.setStyleSheet("background-color: grey; color: white;")
            self.yellow_light.setStyleSheet("background-color: grey; color: white;")
            self.green_light.setStyleSheet("background-color: green; color: white;")
        elif self.current_light == 'flashing_yellow':
            self.flashing_timer.start(500)
            self.red_light.setStyleSheet("background-color: grey; color: white;")
            self.green_light.setStyleSheet("background-color: grey; color: white;")

        self.timer_display.setText(f"Timer: {self.time_left}s")
    
    def closeEvent(self, event):
        QApplication.instance().quit()
