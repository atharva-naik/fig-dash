#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::widget::weather")
import os
import sys
import json
import time
import jinja2
import datetime
from functools import partial
from typing import Union, List
import matplotlib.pyplot as plt
# Qt5 imports.
from PyQt5.QtGui import QPixmap, QImage, QIcon, QMovie, QColor
from PyQt5.QtCore import Qt, QEvent, QT_VERSION_STR, QSize, QObject, pyqtSlot, pyqtSignal, QThread, QPoint
from PyQt5.QtWidgets import QLabel, QMenu, QWidget, QMainWindow, QScrollArea, QSplitter, QTabBar, QVBoxLayout, QHBoxLayout, QToolButton, QToolBar, QSizePolicy, QApplication, QGraphicsDropShadowEffect
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.api.widget.weather import WeatherEngine
from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
from fig_dash.ui import FigDAppContainer, styleWindowStatusBar, wrapFigDWindow, DashWidgetGroup, DashRibbonMenu, styleContextMenu, DASH_WIDGET_SCROLL_AREA

# icon and flag mappings.
WEATHER_WIDGET_FLAG_MAP = {
    "India": "ind.svg",
    "United States of America": "usa.svg",
}
WEATHER_WIDGET_ICON_MAP = {
    "fog": ("gifs/fog.gif", "gifs/fog.gif"),
    "haze": ("sun/6.png", "moon/2.2.png"),
    "smoke": ("cloud/35.png", "cloud/35.png"),
    "partly cloudy": ("sun/27.png", "moon/15.png"),
}
WEATHER_WIDGET_ICON_MAP = {
    key: (
        FigD.icon(os.path.join(
            "widget/weather", p1
        )),
        FigD.icon(os.path.join(
            "widget/weather", p2
        )),
    ) for key, (p1, p2) in WEATHER_WIDGET_ICON_MAP.items()
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
# def fetchIcon(desc):
#     desc = desc.lower()
#     if "haze" in desc:
#         return "widget/weather/fog.gif"
#     elif "mist" in desc:
#         return "widget/weather/fog.gif"
#     elif "fog" in desc:
#         return "widget/weather/fog.gif"
#     elif "sun" in desc:
#         return "widget/weather/sun.gif"
#     elif "clear" in desc:
#         return "widget/weather/sun.gif"
#     elif "cloud" in desc:
#         return "widget/weather/cloudy.png"
#     elif "overcast" in desc:
#         return "widget/weather/cloudy.png"
#     elif "snow" in desc:
#         return "widget/weather/snow.gif"
#     elif "rain" in desc:
#         return "widget/weather/rain.gif"
#     elif "drizzle" in desc:
#         return "widget/weather/rain.gif"
#     else:
#         return desc
class WeatherAPIFetchWorker(QObject):
    finished = pyqtSignal()
    urlBuilt = pyqtSignal(str)
    progress = pyqtSignal(str, str, str)
    def __init__(self):
        self.weather_engine = WeatherEngine()
        super(WeatherAPIFetchWorker, self).__init__()

    def run(self, **args):
        # fetch weather data.
        print(args)
        # get the wttr.in url.
        url = self.weather_engine.build_query(**args)
        self.urlBuilt.emit(url)
        # launch the query.
        self.weather_engine(**args)
        # get current weather condition.
        weather_forecast = self.weather_engine.get_weather_forecast() 
        current_weather = self.weather_engine.get_current_condition()
        area = self.weather_engine.get_nearest_area()
        # print the weather info.
        self.progress.emit(
            json.dumps(current_weather), 
            json.dumps(area),
            json.dumps(weather_forecast),
        )
        self.finished.emit()
# worker.run(temp='C', precip='mm', pressure='inches', )

weather_widget_style = '''
QWidget#CurrentWeatherWidget {
    color: #fff;
    padding: 10px;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 0.8), stop : 0.6 rgba(29, 29, 29, 0.6));
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
}
QLabel#Weather {
    color: #fff;
    padding: 5px;
    background: transparent;
}
QToolButton#AreaButton {
    color: #fff;
    border: 0px;
    background: transparent;
}'''
# weather widget menu
class WeatherWidgetMenu(DashRibbonMenu):
    def __init__(self, accent_color: str="orange", 
                 parent: Union[None, QWidget]=None):
        super(WeatherWidgetMenu, self).__init__(
            parent=parent, group_names=[
                "File", "View", "Convert", "Search", "Filters"
            ]
        )
        self.addWidgetGroup("File", [
            ({
                "text": "Export As", 
                "tip": "Export all data as a given format",
                "icon": "widget/weather/save.svg", 
                "size": (30,30),
                "style": Qt.ToolButtonTextUnderIcon,
                "background": accent_color,
            }, {}),
            ([
                {
                    "icon": "widget/weather/export_json.svg",
                    "text": "Export JSON",
                    "tip": "Export current weather as JSON",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (20,20),
                },
                {
                    "icon": "widget/weather/export_csv.svg",
                    "text": "Export\nForecast CSV",
                    "tip": "Export forecast data as CSV.",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (20,20),
                }
            ], {
               "alignment_flag": Qt.AlignLeft, 
               "orient": "vertical",
            }),
        ])
        self.addWidgetGroup("View", [
            ([
                {
                    "text": "Wind",
                    "icon": "widget/weather/wind_speed.svg",
                    "tip": "Toggle wind group visibility",
                    "size": (25,25),
                    "style": Qt.ToolButtonTextUnderIcon,
                    "background": accent_color,
                },
                {
                    # "icon": "widget/weather/pressure.png",
                    "text": "Misc",
                    "tip": "Toggle visibility of misc group",
                    "background": accent_color,
                    # "style": Qt.ToolButtonTextBesideIcon,
                    # "size": (20,20),
                },
            ], {
               "alignment_flag": Qt.AlignCenter, 
               "orient": "vertical",
            }),
            ([
                {
                    "icon": "widget/weather/rain.png",
                    "text": "Rain",
                    "tip": "Toggle visibility of rain group",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (20,20),
                },
                {
                    "icon": "widget/weather/location.svg",
                    "text": "Area",
                    "tip": "Toggle visibility of additional info (in area)",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (20,20),
                },
            ], {
               "alignment_flag": Qt.AlignRight, 
               "orient": "vertical",
            }),
            ({
                "icon": "widget/floatmenu/weather.png",
                "text": "Forecast",
                "tip": "Toggle visibility of weekly forecast",
                "background": accent_color,
                "style": Qt.ToolButtonTextUnderIcon,
                "size": (40,40),
            }, {})
        ])
        self.windBtn = self.widgetGroupAt("View").memberAt(0).btns[0]
        self.miscBtn = self.widgetGroupAt("View").memberAt(0).btns[1]
        self.rainBtn = self.widgetGroupAt("View").memberAt(1).btns[0]
        self.additionalBtn = self.widgetGroupAt("View").memberAt(1).btns[1]

    def connectCurrentWeather(self, widget: QWidget):
        self.current_weather = widget
        for type_, suffix in [
            ("rain","Group"), ("wind","Group"), 
            ("misc","Group"), ("additional","Info")
        ]:
            btn = getattr(self, type_+"Btn")
            btn.clicked.connect(partial(
                self.current_weather.toggleGroup,
                type_+suffix,
            ))
# # simplified weather widget.
# class WeatherWidgetSimpleMenu(DashWidgetGroup):
#     pass

# also add moon phase widgets.
class CurrentWeatherWidget(QWidget):
    dataReceived = pyqtSignal(str)
    '''weather info, moon phase info and weekly forecast.'''
    def __init__(self, accent_color: str="yellow", 
                 parent: Union[None, QWidget]=None):
        super(CurrentWeatherWidget, self).__init__(parent)
        self.accent_color = accent_color
        # glow_effect = QGraphicsDropShadowEffect()
        # glow_effect.setBlurRadius(30)
        # glow_effect.setOffset(0,0)
        # glow_effect.setColor(QColor(235, 95, 52, 150))
        # self.setGraphicsEffect(glow_effect)
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
        cwLayout.addStretch(1)
        self.setObjectName("CurrentWeatherWidget")
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
        wrapperWidget.setObjectName("CurrentWeatherWidget")
        wrapperWidget.setLayout(self.layout)
        wrapperLayout = QVBoxLayout()
        wrapperLayout.setContentsMargins(0, 0, 0, 0)
        wrapperLayout.addWidget(wrapperWidget)
        self.setLayout(wrapperLayout)

    def update(self, **args):
        import time
        s = time.time()
        # create updating thread.
        self.update_thread = QThread()
        # create weather API fetching worker.
        self.fetch_worker = WeatherAPIFetchWorker()
        self.fetch_worker.urlBuilt.connect(self.showUrl)
        self.fetch_worker.moveToThread(self.update_thread)
        # connect to slots
        self.update_thread.started.connect(partial(self.fetch_worker.run, **args))
        self.update_thread.finished.connect(self.update_thread.deleteLater)

        self.fetch_worker.finished.connect(self.update_thread.quit)
        self.fetch_worker.finished.connect(self.fetch_worker.deleteLater)
        self.fetch_worker.progress.connect(self.reportProgress)
        # start updation thread.
        self.update_thread.start()
        print(f"update request launched in {time.time()-s}s")
        self.showMessage("    querying wttr.in")

    def showMessage(self, *args, **kwargs) -> None:
        error_string = "ui::widget::weather.CurrentWeatherWidget.update: weather_widget not connected"
        try:
            statusbar = self.weather_widget.statusbar
            statusbar.showMessage(*args, **kwargs)
        except AttributeError as e:
            print(error_string, e)

    def showUrl(self, url: str):
        self.showMessage("    "+url)

    def connectWeatherWidget(self, weather_widget: QWidget):
        self.weather_widget = weather_widget

    def toggleGroup(self, group_name: str=""):
        gagAssertErorr = "DumbProgrammerException:P this group doesn't exist :/"
        assert group_name in ["rainGroup", "miscGroup", "windGroup", "additionalInfo"], gagAssertErorr
        group = getattr(self, group_name)
        if group.isVisible():
            group.hide()
        else: group.show()

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
        path = FigD.icon("")
        # self.weatherGif = QMovie(path)
        # tempIcon.setMovie(self.weatherGif)
        self.weatherPixmap = QPixmap(path)
        tempIcon.setPixmap(self.weatherPixmap)
        tempIcon.setAlignment(Qt.AlignCenter)
        tempIcon.setMinimumHeight(150)
        layout.addWidget(tempIcon)
        # self.weatherGif.start()

        # temperature
        tempLabel = QLabel("<span style='font-size: 40px; font-weight: bold;'>0°C</span> <span style='font-size: 16px; color: #eb5f34;'> <br> <span style='font-size: 20px; font-weight: bold; color: #eb5f34;'>feels like 0°C</span> <br> observed at 12:00AM</span>") 
        tempLabel.setObjectName("Weather")
        tempLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(tempLabel)
        # humidity and precipitation
        rainGroup = QWidget()
        rainLayout = QHBoxLayout()
        rainLayout.setContentsMargins(0, 0, 0, 0)
        rainLayout.addStretch(1)
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
        rainLayout.addStretch(1)
        self.rainGroup = rainGroup
        self.rainGroup.hide()
        layout.addWidget(rainGroup)
        # wind speed and direction.
        windGroup = QWidget()
        windLayout = QHBoxLayout()
        windLayout.setContentsMargins(0, 0, 0, 0)
        windLayout.addStretch(1)
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
        windLayout.addStretch(1)
        layout.addWidget(windGroup)
        self.windGroup = windGroup
        self.windGroup.hide()
        # pressure, uv
        miscGroup = QWidget()
        miscLayout = QHBoxLayout()
        miscLayout.setContentsMargins(0, 0, 0, 0)
        miscLayout.addStretch(1)
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
        miscLayout.addStretch(1)
        self.miscGroup = miscGroup
        self.miscGroup.hide()
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
        regionLayout.addStretch(1)
        regionLayout.setContentsMargins(0, 0, 0, 0)
        region.setLayout(regionLayout)
        
        additionalInfo = QWidget()
        additionalInfoLayout = QHBoxLayout()
        additionalInfoLayout.setContentsMargins(0, 0, 0, 0)
        additionalInfoLayout.addStretch(1)
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
            tip="Country of nearest area",
            icon="",
        )
        country.setIconSize(QSize(30,30))
        regionLayout.addWidget(country)
        regionLayout.addStretch(1)
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
        additionalInfoLayout.addStretch(1)
        self.additionalInfo = additionalInfo
        self.additionalInfo.hide()
        # add widgets to layout.
        layout.addWidget(region)
        layout.addWidget(additionalInfo)
        area.setLayout(layout)
        self.cityAndRegion = cityAndRegion
        self.coords = coords
        self.country = country
        self.population = population

        return area

    def copyCurrentWeatherJSON(self):
        pass

    def copyCurrentWeatherImage(self):
        """copy current weather icon"""
        self.__copied_pixmap = self.tempIcon.pixmap()
        QApplication.clipboard().setPixmap(self.__copied_pixmap)

    def copyCurrentWeatherString(self):
        if self.apiData is not None:
            weather = self.apiData["weather"]
            desc = weather["desc"]
            tempCStr = weather["temp"]["C"]+"°C"
            tempFStr = weather["temp"]["F"]+"°F"
            feelsLikeC = weather["feels_like"]["C"]+"°C"
            feelsLikeF = weather["feels_like"]["F"]+"°F"
            weatherString = f"{desc}\n{tempCStr} ({tempFStr})\nfeels like {feelsLikeC} ({feelsLikeF})"
            QApplication.clipboard().setText(weatherString)

    def exportCurrentWeatherJSON(self):
        pass

    def exportForecastCSV(self):
        pass

    def contextMenuEvent(self, event):
        self.contextMenu = QMenu()
        self.contextMenu.addAction(
            FigD.Icon("widget/weather/copy.svg"), 
            "Copy weather string", self.copyCurrentWeatherString
        )
        self.contextMenu.addAction(
            FigD.Icon("widget/weather/copy.svg"), 
            "Copy weather JSON", self.copyCurrentWeatherJSON
        )
        self.contextMenu.addAction(
            FigD.Icon("widget/weather/copy_image.svg"), 
            "Copy weather icon", self.copyCurrentWeatherImage
        )
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(
            FigD.Icon("widget/weather/export_json.svg"), 
            "Save weather JSON", self.exportCurrentWeatherJSON
        )
        # self.contextMenu.addAction(
        #     FigD.Icon("widget/weather/export_csv.svg"), 
        #     "Save weekly forecast CSV", self.exportForecastCSV
        # )
        self.contextMenu.addSeparator()
        # build the view side of the things.
        groupNames = [name+"Group" for name in ["wind", "rain", "misc"]]
        groupNames.append("additionalInfo")
        actionNames = [name+" group" for name in ["wind", "rain", "miscellaneous"]]
        actionNames.append("additional area info")
        iconList = ["wind_speed.svg", "rain.png", None, "location.svg"]
        for name, title, icon in zip(groupNames, actionNames, iconList):
            group = getattr(self, name)
            if icon:
                iconObj = FigD.Icon(f"widget/weather/{icon}")
            else: iconObj = QIcon("")
            if group.isVisible():
                self.contextMenu.addAction(
                    iconObj, f"Hide {title}", 
                    partial(self.toggleGroup, name)
                )
            else:
                self.contextMenu.addAction(
                    iconObj, f"Show {title}", 
                    partial(self.toggleGroup, name)
                ) 
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
        self.contextMenu.popup(event.globalPos())
    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()

    # def mouseMoveEvent(self, event):
    #     try:
    #         delta = QPoint(event.globalPos() - self.oldPos)
    #         self.move(self.x() + delta.x(), self.y() + delta.y())
    #         self.oldPos = event.globalPos()
    #     except Exception as e:
    #         print("\x1b[31;1mtitlebar.mouseMoveEvent\x1b[0m", e)

    def reportProgress(self, weather: str, area: str, forecast: str):
        # show message for 2 secs.
        self.showMessage(f"    data fetch finished, fetched {len(weather)+len(area)} bytes", msecs=1000) 
        area = json.loads(area)
        weather = json.loads(weather)
        self.apiData = {
            "area": area, "weather": weather, 
            "forecast": forecast
        }
        self.dataReceived.emit(str(forecast))
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
        
        desc = weather["desc"].lower().strip()
        print("desc:", desc)
        path_day, path_night = WEATHER_WIDGET_ICON_MAP.get(desc, ("",""))
        hour = int(datetime.datetime.now().strftime("%H"))
        # print(f"\x1b[34;1mpath_day: {path_day}, path_night: {path_night}\x1b[0m")
        if 6 <= hour <= 12+7:
            # day weather logo.
            self.weatherPixmap = QPixmap(path_day).scaledToHeight(
                150, mode=Qt.SmoothTransformation
            )
            # print("\x1b[33;1mday\x1b[0m")
        else:
            # night weather logo.
            self.weatherPixmap = QPixmap(path_night).scaledToHeight(
                150, mode=Qt.SmoothTransformation
            )
            # print("\x1b[32;1mnight\x1b[0m")
        self.tempIcon.setPixmap(self.weatherPixmap)

        countryName = area["country"]
        countryIcon = WEATHER_WIDGET_FLAG_MAP.get(countryName,'')
        self.country.setIcon(FigD.Icon(
            f"flags/{countryIcon}"
        ))
        
        # self.weatherGif = QMovie(path)
        # self.weatherGif.setScaledSize(QSize(150,150))
        # self.tempIcon.setMovie(self.weatherGif)
        # self.weatherGif.start()
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
        btn.setStatusTip(tip)
        btn.setIcon(FigD.Icon(icon))
        btn.setIconSize(QSize(20,20))
        btn.setObjectName("AreaButton")
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        return btn

# forecast widget: splitter: 3 days + hourly forecast plot.
class ForecastWeatherWidget(QSplitter):
    def __init__(self, accent_color: str="yellow", 
                 parent: Union[None, QWidget]=None):
        super(ForecastWeatherWidget, self).__init__(Qt.Vertical)
        self.accent_color = accent_color
        self.forecastData = None
        # sub-widget forecast tiles.
        self.forecast_tiles = self.initForecastTiles()
        # sub-widget hourly plots.
        self.hourly_plots = self.initHourlyPlots()
        self.addWidget(self.forecast_tiles)
        self.addWidget(self.hourly_plots)

    def connectCurrentWeather(self, widget: QWidget):
        self.current_weather = widget
        self.current_weather.dataReceived.connect(self.setForecastFromString)

    def setForecastFromString(self, forecastString: dict):
        """load forecast json from serialized json string"""
        print("\x1b[31;1mreceived forecast info!\x1b[0m")
        # print(forecastString)
        forecastData = json.loads(forecastString)
        self.setForecastData(forecastData)

    def setForecastData(self, forecastData: dict):
        """set the forecast data json"""
        self.forecastData = forecastData
        for daily_data in forecastData:
            print(daily_data.keys())

    def initForecastTiles(self):
        forecast_tiles = QWidget()
        forecast_tiles.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
            font-family: "Be Vietnam Pro";
        }""")
        self.forecast_tiles_layout = QHBoxLayout()
        self.forecast_tiles_layout.setContentsMargins(5, 5, 5, 5)
        self.forecast_tiles_layout.setSpacing(10)
        forecast_tiles.setLayout(self.forecast_tiles_layout)

        return forecast_tiles

    def initHourlyPlots(self):
        plot_widget = QWidget()
        plot_widget.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
            font-family: "Be Vietnam Pro";
        }""")
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        # sub widgets.
        self.plot_canvas = QLabel()
        # build layout.
        layout.addWidget(self.plot_canvas)
        plot_widget.setLayout(layout)

        return plot_widget

    def connectWeatherWidget(self, widget: QWidget):
        self.weather_widget = widget

# final fig-dash weather widget.
class WeatherWidget(QMainWindow):
    def __init__(self, accent_color: str="orange", 
                 parent: Union[None, QWidget]=None):
        super(WeatherWidget, self).__init__(parent)
        self.accent_color = accent_color
        centralWidget = self.initCentralWidget() 
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(centralWidget)

    def update(self, *args, **kwargs):
        self.current_weather.update(*args, **kwargs)

    def initCentralWidget(self):
        # central widget.
        centralWidget = QWidget()
        # init layout: contains menu + scroll area.
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        # splitter: current weather + forecast.
        self.__splitter = QSplitter(Qt.Horizontal)
        # scroll area.
        self.__scroll_area = QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__scroll_area.setStyleSheet(DASH_WIDGET_SCROLL_AREA.render())
        self.__scroll_area.setAttribute(Qt.WA_TranslucentBackground)
        self.__scroll_area.setWidget(self.__splitter)
        # init sub widgets.
        # current weather
        self.current_weather = CurrentWeatherWidget(
            accent_color=self.accent_color
        )
        self.current_weather.connectWeatherWidget(self)
        # weather forecast.
        self.forecast_weather = ForecastWeatherWidget(
            accent_color=self.accent_color,
        )
        self.forecast_weather.connectCurrentWeather(
            self.current_weather
        )
        # self.weather_forecast.connectWeatherWidget(self) 
        self.__splitter.addWidget(self.current_weather)
        self.__splitter.addWidget(self.forecast_weather)

        self.menu = WeatherWidgetMenu(accent_color=self.accent_color)
        self.menu.setFixedHeight(120)
        self.menu.connectCurrentWeather(self.current_weather)
        # self.simpleMenu = WeatherWidgetSimpleMenu()
        # self.simpleMenu.hide()
        # build layout.
        layout.addWidget(self.menu)
        # layout.addWidget(self.simpleMenu)
        layout.addWidget(self.__scroll_area)
        centralWidget.setLayout(layout)

        return centralWidget

def test_weather_widget():
    import sys, time
    FigD("/home/atharva/GUI/fig-dash/resources")
    # figD app container.
    app = FigDAppContainer(sys.argv)
    s = time.time()
    # args.
    where = "front"
    icon = FigDSystemAppIconMap["weather"]
    accent_color = FigDAccentColorMap["weather"]
    # main widget.
    weather = WeatherWidget(accent_color=accent_color)
    window = wrapFigDWindow(
        weather, title="Weather", icon=icon,
        accent_color=accent_color, width=650,
        height=500, where=where,
    )
    window = styleWindowStatusBar(window, font_color="#eb5f34")
    # needed just for this widget.
    try: weather.statusbar = window.statusbar
    except AttributeError as e: print(e)
    # show the window.
    window.show()
    try:
        weather.update(region=sys.argv[1])
    except IndexError as e:
        print(e)
        weather.update()
    # report time needed.
    print(time.time()-s)
    app.exec()

def launch_weather():
    FigD("/home/atharva/GUI/fig-dash/resources")
    # args.
    where = "front"
    icon = FigDSystemAppIconMap["weather"]
    accent_color = FigDAccentColorMap["weather"]
    # accent_color = "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #e95900, stop : 0.091 #ed6600, stop : 0.182 #f17300, stop : 0.273 #f58000, stop : 0.364 #f88c00, stop : 0.455 #fa9900, stop : 0.545 #fca500, stop : 0.636 #feb100, stop : 0.727 #febe00, stop : 0.818 #ffca00, stop : 0.909 #ffd600, stop : 1.0 #fee200)"
    # main widget.
    weather = WeatherWidget(accent_color=accent_color)
    window = wrapFigDWindow(
        weather, title="Weather", icon=icon,
        accent_color=accent_color, width=650,
        height=500, where=where,
    )
    window = styleWindowStatusBar(window, font_color="#eb5f34")
    # needed just for this widget.
    try: weather.statusbar = window.statusbar
    except AttributeError as e: print(e)
    # show the window.
    window.show()
    try:
        weather.update(region=sys.argv[1])
    except IndexError as e:
        print(e)
        weather.update()

    return window


if __name__ == '__main__':
    test_weather_widget()