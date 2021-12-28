#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import jinja2
from typing import Union, List
# Qt5 imports.
from PyQt5.QtGui import QPixmap, QIcon, QMovie, QColor
from PyQt5.QtCore import Qt, QEvent, QT_VERSION_STR, QSize, QObject, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QLabel, QWidget, QTabBar, QVBoxLayout, QHBoxLayout, QToolButton, QToolBar, QSizePolicy, QApplication, QGraphicsDropShadowEffect
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.api.widget.weather import WeatherEngine


countries = {
    "India": "ind.png"
}
# weather_emojis = {
#     "Mist": "", # 1
#     "Sunny": "", # 2
#     "Clear": "",  # 2
#     "Cloudy": "", # 3
#     "Overcast": "", # 3
#     "Partly cloudy": "", # 4
#     "Patchy rain pour": "", # 5 # doubt
#     "Light rain": "", # 6
#     "Light drizzle": "", # 6 
#     "Patchy light snow": "", # 7
#     "Blowing snow": "", # 8
#     "Patchy snow pour": "", # 9 
# }
def fetchIcon(desc):
    desc = desc.lower()
    if "haze" in desc:
        return "widget/weather/fog.gif"
    elif "mist" in desc:
        return "widget/weather/fog.gif"
    elif "fog" in desc:
        return "widget/weather/fog.gif"
    elif "sun" in desc:
        return "widget/weather/sun.gif"
    elif "clear" in desc:
        return "widget/weather/sun.gif"
    elif "cloud" in desc:
        return "widget/weather/cloudy.png"
    elif "overcast" in desc:
        return "widget/weather/cloudy.png"
    elif "snow" in desc:
        return "widget/weather/snow.gif"
    elif "rain" in desc:
        return "widget/weather/rain.gif"
    elif "drizzle" in desc:
        return "widget/weather/rain.gif"
    else:
        return desc


class WeatherAPIFetchWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str, str)
    def __init__(self):
        self.weather_engine = WeatherEngine()
        super(WeatherAPIFetchWorker, self).__init__()

    def run(self, **units):
        # fetch weather data.
        self.weather_engine()
        # get current weather condition.
        weather = self.weather_engine.get_current_condition()
        area = self.weather_engine.get_nearest_area()
        self.progress.emit(
            json.dumps(weather), 
            json.dumps(area)
        )
        self.finished.emit()
# worker.run(temp='C', precip='mm', pressure='inches', )

weather_widget_style = '''
QWidget#WeatherWidget {
    color: #fff;
    padding: 10px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
}
QLabel#Weather {
    color: #fff;
    padding: 5px;
    background: transparent;
}
QToolButton#AreaButton {
    border: 0px;
    color: #6e6e6e;
    background: transparent;
}'''
# also add moon phase widgets.
class WeatherWidget(QWidget):
    '''weather info, moon phase info and weekly forecast.'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(WeatherWidget, self).__init__(parent)
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(3,3)
        glow_effect.setColor(QColor(235, 95, 52))
        self.setGraphicsEffect(glow_effect)

        self.apiData = None
        currentWeather = QWidget()
        cwLayout = QVBoxLayout()
        cwLayout.setContentsMargins(0, 0, 0, 0)
        cwLayout.setSpacing(0)
        currentWeather.setLayout(cwLayout)
        # widget to display area.
        self.area = self.initArea()
        self.current_weather = self.initWeather()
        # add widgets to layout.
        cwLayout.addWidget(self.current_weather)
        cwLayout.addWidget(self.area)
        self.setObjectName("WeatherWidget")
        # self.setLayout(self.layout)
        self.setStyleSheet(weather_widget_style)
        # add current weather.
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        forecast = QWidget()
        foreLayout = QVBoxLayout()
        foreLayout.setContentsMargins(0, 0, 0, 0)
        foreLayout.setSpacing(0)
        forecast.setLayout(foreLayout)
        # add sub widgets to weather widget.
        self.layout.addWidget(currentWeather)
        self.layout.addWidget(forecast)

        wrapperWidget = QWidget()
        wrapperWidget.setObjectName("WeatherWidget")
        wrapperWidget.setLayout(self.layout)
        wrapperLayout = QVBoxLayout()
        wrapperLayout.setContentsMargins(0, 0, 0, 0)
        wrapperLayout.addWidget(wrapperWidget)
        self.setLayout(wrapperLayout)

    def update(self):
        import time
        s = time.time()
        # create updating thread.
        self.update_thread = QThread()
        # create weather API fetching worker.
        self.fetch_worker = WeatherAPIFetchWorker()
        self.fetch_worker.moveToThread(self.update_thread)
        # connect to slots
        self.update_thread.started.connect(self.fetch_worker.run)
        self.update_thread.finished.connect(self.update_thread.deleteLater)

        self.fetch_worker.finished.connect(self.update_thread.quit)
        self.fetch_worker.finished.connect(self.fetch_worker.deleteLater)
        self.fetch_worker.progress.connect(self.reportProgress)
        # start updation thread.
        self.update_thread.start()
        print(f"update request launched in {time.time()-s}s")

    def initWeather(self):
        weather = QWidget()
        weather.setObjectName("Weather")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        weather.setLayout(layout)
        # weather icon
        tempIcon = QLabel()
        desc = "Loading"
        descLabel = QLabel(f"<span style='font-size: 20px; font-weight: bold; color: #eb5f34;'>{desc}</span>")
        descLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(descLabel)
        path = FigD.icon(fetchIcon(""))
        print(path)
        self.weatherGif = QMovie(path)
        tempIcon.setMovie(self.weatherGif)
        tempIcon.setAlignment(Qt.AlignCenter)
        layout.addWidget(tempIcon)
        self.weatherGif.start()
        # temperature
        tempLabel = QLabel("<span style='font-size: 40px; font-weight: bold;'>0°C</span> <span style='font-size: 16px; color: #eb5f34;'> <br> <span style='font-size: 20px; font-weight: bold; color: gray;'>feels like 0°C</span> <br> observed at 12:00AM</span>") 
        tempLabel.setObjectName("Weather")
        tempLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(tempLabel)
        # humidity and precipitation
        rainGroup = QWidget()
        rainLayout = QHBoxLayout()
        rainLayout.setContentsMargins(0, 0, 0, 0)
        rainGroup.setLayout(rainLayout)
        humidity = self.initAreaBtn(
            text=" 0%",
            icon="widget/weather/humidity.png",
            tip="Humidity percentage"
        )
        cloudCover = self.initAreaBtn(
            text=" 0%",
            icon="widget/weather/cloud.svg",
            tip="Cloud cover"
        )
        precipitation = self.initAreaBtn(
            text=" 0 mm",
            icon="widget/weather/rain.png",
            tip="Precipitation amount mm/inches"
        )
        rainLayout.addWidget(humidity)
        rainLayout.addWidget(cloudCover)
        rainLayout.addWidget(precipitation)
        layout.addWidget(rainGroup)
        # wind speed and direction.
        windGroup = QWidget()
        windLayout = QHBoxLayout()
        windLayout.setContentsMargins(0, 0, 0, 0)
        windGroup.setLayout(windLayout)
        windDir = self.initAreaBtn(
            text=" 0°, N",
            icon="widget/weather/direction.svg",
            tip="Wind direction"
        )
        windSpeed = self.initAreaBtn(
            text=" 0 kmph",
            icon="widget/weather/wind_speed.svg",
            tip="Wind speed"
        )
        windLayout.addWidget(windSpeed)
        windLayout.addWidget(windDir)
        layout.addWidget(windGroup)
        # pressure, uv
        miscGroup = QWidget()
        miscLayout = QHBoxLayout()
        miscLayout.setContentsMargins(0, 0, 0, 0)
        miscGroup.setLayout(miscLayout)
        pressure = self.initAreaBtn(
            text=" 0 inches",
            icon="widget/weather/pressure.png",
            tip="Pressure in inches"
        )
        uvIndex = self.initAreaBtn(
            text="index 1",
            icon="widget/weather/uv.png",
            tip="UV index"
        )
        miscLayout.addWidget(pressure)
        miscLayout.addWidget(uvIndex)
        layout.addWidget(miscGroup)
        # create referencs for relevant widgets.
        self.tempIcon = tempIcon
        self.tempLabel = tempLabel
        self.descLabel = descLabel
        self.humidity = humidity
        self.windDir = windDir
        self.windSpeed = windSpeed
        self.cloudCover = cloudCover
        self.precipitation = precipitation
        self.pressure = pressure
        self.uvIndex = uvIndex

        return weather

    def initArea(self):
        '''widget to display information about nearest area whose weather is reported.'''
        area = QWidget()
        area.setObjectName("WeatherArea")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # region and additional info about country and location
        region = QWidget()
        regionLayout = QHBoxLayout()
        regionLayout.setContentsMargins(0, 0, 0, 0)
        region.setLayout(regionLayout)
        
        additionalInfo = QWidget()
        additionalInfoLayout = QHBoxLayout()
        additionalInfoLayout.setContentsMargins(0, 0, 0, 0)
        additionalInfo.setLayout(additionalInfoLayout)
        # city and region.
        cityAndRegion = self.initAreaBtn(
            text=" City, Area",
            icon="widget/weather/location.svg",
            tip="City and region info for the nearest area"
        )
        regionLayout.addWidget(cityAndRegion)
        # country.
        country = self.initAreaBtn(
            text=" Country",
            icon="flags/ind.svg",
            tip="Country of nearest area"
        )
        country.setIconSize(QSize(30,30))
        regionLayout.addWidget(country)
        # coordinates.
        coords = self.initAreaBtn(
            text=" (0, 0)",
            icon="widget/weather/coordinates.svg",
            tip="Latitude and Longitude information about nearest region"
        )
        additionalInfoLayout.addWidget(coords)
        # population.
        population = self.initAreaBtn(
            text=" 0",
            icon="widget/weather/population.svg",
            tip="Population count of nearest region"
        )
        additionalInfoLayout.addWidget(population)
        # add widgets to layout.
        layout.addWidget(region)
        layout.addWidget(additionalInfo)
        area.setLayout(layout)
        self.cityAndRegion = cityAndRegion
        self.coords = coords
        self.country = country
        self.population = population

        return area

    def reportProgress(self, weather: str, area: str):
        area = json.loads(area)
        weather = json.loads(weather)
        self.apiData = {"area": area, "weather": weather}
        # update area related fields.
        self.cityAndRegion.setText(f"{area['area']}, {area['region']}")
        x, y = area["coords"]
        self.coords.setText(f" {x}, {y}")
        self.country.setText(" "+area["country"])
        self.population.setText(" "+area["population"])
        # update weather related fields.
        self.humidity.setText(" "+weather["humidity"]+"%")
        wind = weather["wind"]
        self.windSpeed.setText(f" {wind['speed']} kmph")
        self.windDir.setText(f" {wind['deg']}°, {wind['dir']}")
        self.cloudCover.setText(f" {weather['cloud_cover']}%")
        self.precipitation.setText(f" {weather['precipitation']['mm']} mm")
        self.pressure.setText(f" {weather['pressure']['inches']} inches")
        self.uvIndex.setText(f" uv index: {weather['uv']}")
        self.tempLabel.setText(f"<span style='font-size: 40px; font-weight: bold;'>{weather['temp']['C']}°C</span> <span style='font-size: 16px; color: #eb5f34;'> <br> <span style='font-size: 20px; font-weight: bold; color: gray;'>feels like {weather['feels_like']['C']}°C</span> <br> observed at {weather['observed_at']}</span>")
        self.descLabel.setText(f"<span style='font-size: 20px; font-weight: bold; color: #eb5f34;'>{weather['desc']}</span>")
        # path = fetchIcon(weather['desc'])
        path = FigD.icon(fetchIcon('mist'))
        self.weatherGif = QMovie(path)
        self.weatherGif.setScaledSize(QSize(150,150))
        self.tempIcon.setMovie(self.weatherGif)
        self.weatherGif.start()
        # resize widget.
        w = self.width()
        h = self.height()
        self.resize(w+80, h)

    def toggle(self):
        if self.apiData is None:
            self.update()
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def initAreaBtn(self, text: str, icon: str, tip: str):
        btn = QToolButton(self)
        btn.setText(text)
        btn.setToolTip(tip)
        btn.setIcon(FigD.Icon(icon))
        btn.setIconSize(QSize(20,20))
        btn.setObjectName("AreaButton")
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        return btn


def test_weather_widget():
    import sys, time
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    s = time.time()
    weather = WeatherWidget()
    weather.show()
    weather.update()
    print(time.time()-s)
    app.exec()


if __name__ == '__main__':
    test_weather_widget()