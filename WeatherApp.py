import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("Data/")

    return os.path.join(base_path, relative_path)


import requests
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(470, 770)
        self.output_button = QPushButton("Get the weather", self)
        self.input_stroke = QLineEdit(self)
        self.temperature_label = QLabel("-°C",self)
        self.emoji_label = QLabel(self)
        pixmap = QPixmap(resource_path("leaves.png"))
        self.emoji_label.setPixmap(pixmap)
        self.description_label = QLabel("undefined",self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon(resource_path("weather.png")))
        self.input_stroke.setPlaceholderText("Enter city title:")

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_stroke)
        vbox.addWidget(self.output_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.input_stroke.setAlignment(Qt.AlignHCenter)
        self.temperature_label.setAlignment(Qt.AlignHCenter)
        self.emoji_label.setAlignment(Qt.AlignHCenter)
        self.description_label.setAlignment(Qt.AlignHCenter)

        self.input_stroke.setObjectName("input_stroke")
        self.output_button.setObjectName("output_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
        QWidget {background-color: hsl(229, 65%, 5%);}
        QPushButton, QLabel, QLineEdit {font-size: 40px;
                                        padding: 5px;
                                        font-family: calibri;
                                        font-style: italic;}
        QLineEdit#input_stroke {color: white;
                                border: 3px solid;
                                border-color: hsl(270, 56%, 59%);
                                border-radius: 5px;}
        QPushButton#output_button {font-size: 20px;
                                   color: white;
                                   background-color: hsl(256, 91%, 58%);
                                   border: 3px solid hsl(256, 91%, 18%);
                                   border-radius: 10px;}
        QLabel#temperature_label {font-size: 70px;
                                  font-weight: bold;
                                  color: white;
                                  background-color: hsl(301, 48%, 5%);
                                  border-width: thick;
                                  border: 3px solid;
                                  border-color: hsl(301, 48%, 54%);
                                  padding: 45px;
                                  border-radius: 10px;
                                  margin: 50px;}
        QLabel#emoji_label {font-size: 80px;
                            font-style: normal;
                            margin: 20px;
                            font-family: Segoe UI Emoji;}
        QLabel#description_label {color: white;
                                  margin: 0px 0px 30px;
                                  color: white;}
        QPushButton#output_button:hover {background-color: hsl(256, 91%, 28%);
                                         color: hsl(256, 100%, 88%);}
        """)

        self.output_button.clicked.connect(self.get_weather)
        self.input_stroke.returnPressed.connect(self.get_weather)

    def get_weather(self):
        key = "10cf9c1d3ba97e25ab5c51a5e94210fb"
        city = self.input_stroke.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"

        try:
            response = requests.get(url)
            response_json = response.json()

            response.raise_for_status()

            weather_description = response_json["weather"][0]["description"]
            weather_id = response_json["weather"][0]["id"]

            if response_json["cod"] == 200:
                self.display_temperature(response_json)
                self.description_label.setText(weather_description)
                self.emoji_label.setText(self.display_emoji(weather_id))

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_errors("Bad Request:\nCheck your input")
                case 401:
                    self.display_errors("Unauthorized:\nChek your API key")
                case 403:
                    self.display_errors("Forbidden:\nYou have not access")
                case 404:
                    self.display_errors("Not Found:\nPlace is not found")
                case 500:
                    self.display_errors("Internal Server: \nError\nWait some time")
                case 502:
                    self.display_errors("Bad Gateway:\nServer is temporarily\n unresponsive")
                case 503:
                    self.display_errors("Service Unavailable:\nTry again later")
                case 504:
                    self.display_errors("Gateway Timeout:\nNo response from server")
                case _:
                    self.display_errors(f"Error: \n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_errors("Connection Error\nCheck your\n internet connection")
        except requests.exceptions.Timeout:
            self.display_errors("TimeoutError\nThe response\n timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_errors("Too many redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_errors(f"Request Error\n{req_error}")


    def display_errors(self, message):
        self.emoji_label.clear()
        self.description_label.clear()
        self.temperature_label.setStyleSheet("font-size: 30px;"
                                             "padding: 15px;"
                                             "font-style: normal;"
                                             "font-family: Comic Sans MS;"
                                             "color: hsl(299, 100%, 80%);")
        self.temperature_label.setText(message)


    def display_temperature(self, temperature):
        self.temperature_label.setStyleSheet("font-size: 70px;")
        weather_C = (temperature["main"]["temp"] - 272.594)
        self.temperature_label.setText(f"{int(weather_C)}°C")


    def display_emoji(self, weather_id):
        if 200 <= weather_id <= 232:
            self.emoji_label.setPixmap(QPixmap(resource_path("thunder_cloud_and_rain.png")))
        elif  300 <= weather_id <= 321:
            self.emoji_label.setPixmap(QPixmap(resource_path("partly_sunny_rain.png")))
        elif 500 <= weather_id <= 531:
            self.emoji_label.setPixmap(QPixmap(resource_path("rain_cloud.png")))
        elif 600 <= weather_id <= 622:
            self.emoji_label.setPixmap(QPixmap(resource_path("snow_cloud.png")))
        elif 701 <= weather_id <= 781:
            self.emoji_label.setPixmap(QPixmap(resource_path("tornado.png")))
        elif 800 == weather_id:
            self.emoji_label.setPixmap(QPixmap(resource_path("sunny.png")))
        elif 801 <= weather_id <= 804:
            self.emoji_label.setPixmap(QPixmap(resource_path("cloud.png")))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec_())









