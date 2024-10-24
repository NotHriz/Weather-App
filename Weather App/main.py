import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

# Weather App Class
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # initialize label
        self.city_label = QLabel('Enter City Name', self)
        self.city_input = QLineEdit(self)        
        self.get_weather_button = QPushButton('Get Weather', self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        
        self.initUI()
        
    def initUI(self):
        # Set Title
        self.setWindowTitle('Weather App')
            
        # Set Layout
        vbox = QVBoxLayout()
         
        # Add Widgets   
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        # Set Alignment
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # Set object name
        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temp_label.setObjectName('temp_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')
        
        # Set Styles
        self.setStyleSheet("""
                            QLabel, QPushButton{
                                font-family: Calibri;
                            }
                            QLabel#city_label{
                               font-size: 40px;
                               font-style: italic;
                            }
                            QLineEdit{
                                font-size: 40px;
                            }
                            QPushButton#get_weather_button{
                                font-size: 30px;
                                font-weight: bold;
                            }
                            QLabel#temp_label{
                                font-size: 75px;
                            }
                            QLabel#emoji_label{
                                font-size: 100px;
                                font-family: Segoe UI Emoji;
                            }
                            QLabel#description_label{
                                font-size: 50px;
                            }                          
                            """)
        
        # Connect Button
        self.get_weather_button.clicked.connect(self.get_weather)
            
    def get_weather(self):
        api_key = 'e0691531f32dd4904025b48915e34793'
        
        # Get City Name
        city = self.city_input.text()
        
        # Get Weather Data
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        
        # Get Response
        try:    
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data['cod'] == 200: # Check if city is found
                self.display_weather(data)
        
        # Handle Errors     
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error('Bad Request\nPlease Check Your Input')
                case 401:
                    self.display_error('Unauthorized\nInvalid API Key')
                case 403:
                    self.display_error('Forbidden\nAccess Denied')
                case 404:
                    self.display_error('City Not Found')
                case 429:
                    self.display_error('Too Many Requests\n Please Try Again Later')
                case 500:
                    self.display_error('Internal Server Error\nPlease Try Again Later')
                case 502:
                    self.display_error('Bad Gateway\nPlease Try Again Later')
                case 503:
                    self.display_error('Service Unavailable\nPlease Try Again Later')
                case 504:
                    self.display_error('Gateway Timeout\nPlease Try Again Later')
                case _:
                    self.display_error(f"HTTP Error Occurred: {response.status_code}") 
        
        except requests.exceptions.ConnectionError:
            self.display_error('Connection Error\nPlease Check Your Internet Connection')        
        
        except requests.exceptions.Timeout:
            self.display_error('Timeout Error\nRequest Timed Out')
        
        except requests.exceptions.TooManyRedirects:
            self.display_error('Too Many Redirects\nCheck Your URL')
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f'Request Error Occurred: {req_error}')
              
    
    def display_error(self, message):
        # Change font size and color then display error message
        self.temp_label.setStyleSheet("font-size: 30px; color: red;")
        self.temp_label.setText(message)
        
        # Clear Other Labels
        self.emoji_label.clear()
        self.description_label.clear()
    
    
    def display_weather(self, data):
        # Reset Styles
        self.temp_label.setStyleSheet("font-size: 75px; color: black;")
        
        # Get Weather Description
        temp = data['main']['temp'] - 273.15
        description = data['weather'][0]['description']

        
        # Display Data To User
        self.temp_label.setText(f'{temp:.2f}°C')
        self.description_label.setText(description)
        self.emoji_label.setText(self.get_weather_emoji(data['weather'][0]['id']))
    
    @staticmethod    
    def get_weather_emoji(weather_id):
        # Turn Weather ID to Emoji
        match weather_id:
            case 200 | 201 | 202 | 210 | 211 | 212 | 221 | 230 | 231 | 232:
                return '⛈️'
            case 300 | 301 | 302 | 310 | 311 | 312 | 313 | 314 | 321:
                return '🌧️'
            case 500 | 501 | 502 | 503 | 504 | 511 | 520 | 521 | 522 | 531:
                return '🌧️'
            case 600 | 601 | 602 | 611 | 612 | 613 | 615 | 616 | 620 | 621 | 622:
                return '❄️'
            case 701 | 711 | 721 | 731 | 741 | 751 | 761 | 762 | 771 | 781:
                return '🌫️'
            case 800:
                return '☀️'
            case 801 | 802:
                return '🌤️'
            case 803 | 804:
                return '☁️'
            case _:
                return '❓'
    

# Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    