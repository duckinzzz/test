import requests
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from plyer import gps
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.clock import Clock

Window.size = (338, 600)

kv = '''
MDFloatLayout:
    md_bg_color: 1, 1, 1, 1

    Image:
        source: "assets/location.png"
        size_hint: .1, .1
        pos_hint: {"center_x": .5, "center_y": .95}

    Button:
        size_hint: .1, .1
        pos_hint: {"center_x": .9, "center_y": .95}
        background_color: 1,1,1,0
        on_release: app.gps_location_weather()
    Image:
        source: "assets/get_location.png"
        size_hint: .1, .1
        pos_hint: {"center_x": .9, "center_y": .95}

    Button:
        size_hint: .1, .1
        pos_hint: {"center_x": .1, "center_y": .95}
        background_color: 1,1,1,1
        on_release: app.button_test() 
    Image:
        source: "assets/settings.png"
        size_hint: .1, .1
        pos_hint: {"center_x": .1, "center_y": .95}

    MDLabel:
        id: location
        text: ""
        pos_hint: {"center_x": .5, "center_y": .89  }
        halign: "center"
        font_size:  "20sp"
        font_name: "BPoppins"
    Image:
        id: weather_image
        source: "assets/partlyclouds.png"
        pos_hint: {"center_x": .5, "center_y": .77}
    MDLabel:
        id: temperature
        text: ""
        markup: True
        pos_hint: {"center_x": .5, "center_y": .62}
        halign: "center"
        font_size:  "60sp"
    MDLabel:
        id: weather
        text: ""
        markup: True
        pos_hint: {"center_x": .5, "center_y": .54}
        halign: "center"
        font_size:  "20sp"
        font_name: "Poppins"

    MDFloatLayout:
        pos_hint: {"center_x": .25, "center_y": .45}
        size_hint: .22, .1
        Image:
            source: "assets/humidity.png"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: humidity
            text: "  %"
            pos_hint: {"center_x": 1, "center_y": .7}
            font_size:  "18sp"
            font_name: "Poppins"
        MDLabel:
            text: "Humidity"
            pos_hint: {"center_x": 1, "center_y": .3}
            font_size:  "14sp"
            font_name: "Poppins"    

    MDFloatLayout:
        pos_hint: {"center_x": .7, "center_y": .45}
        size_hint: .22, .1
        Image:
            source: "assets/wind.png"
            pos_hint: {"center_x": .1, "center_y": .5}

        MDLabel:
            id: wind_speed
            text: "   m/s"
            pos_hint: {"center_x": 1.1, "center_y": .7}
            font_size:  "18sp"
            font_name: "Poppins"
        MDLabel:
            text: "Wind"
            pos_hint: {"center_x": 1.1, "center_y": .3}
            font_size:  "14sp"
            font_name: "Poppins"

    MDFloatLayout:
        size_hint_y: .12
        canvas:
            Color:
                rgb: rgba(121, 86, 162) # цвет фона нижней панели
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [30,30,0,0]

        MDFloatLayout:
            pos_hint: {"center_x": .38, "center_y": .5}
            size_hint: .7, .7
            canvas:
                Color:
                    rgb: rgba(181, 159, 242) # цвет кнопки
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [6]
            TextInput:
                id: city_name
                hint_text: "Enter city name"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                multiline: False
                font_name: "BPoppins"
                font_size: "20sp"
                hint_text_color: 1,1,1,1
                foreground_color: 1,1,1,1
                background_color: 1,1,1,0
                padding: 15
                halign: "center"
                cursor_color: 1,1,1,1
                cursor_width: "2sp"

        Button:
            id: get_weather_button
            # text: "G"
            font_name: "BPoppins"
            font_size: "20sp"
            size_hint: .2, .7
            pos_hint: {"center_x": .87, "center_y": .5}
            background_color: 1,1,1,0
            color: rgba(148, 117, 255, 255)
            on_release: app.search_weather()
            canvas.before:
                Color:
                    rgb: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [6]
        Image:
            source: "assets/search_icon.png"
            size_hint: .3, .3
            pos_hint: {"center_x": .87, "center_y": .5}

    MDFloatLayout:
        pos_hint: {"center_x": .5, "center_y": .25}
        size_hint: .9, .2
        canvas:
            Color:
                rgb: rgba(133, 95, 185)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [40,40,40,40]

        MDFloatLayout:
            pos_hint: {"center_x": .11, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]

            MDLabel:
                id: d1_date
                text: "01"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"
            MDLabel:
                id: d1_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d1_img
                source: "assets/sun.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9

        MDFloatLayout:
            pos_hint: {"center_x": .305, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d2_date
                text: "02"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"        
            MDLabel:
                id: d2_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d2_img
                source: "assets/snow.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9        

        MDFloatLayout:
            pos_hint: {"center_x": .5, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d3_date
                text: "03"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"
            MDLabel:
                id: d3_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d3_img
                source: "assets/wind.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9        

        MDFloatLayout:
            pos_hint: {"center_x": .695, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d4_date
                text: "04"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"        
            MDLabel:
                id: d4_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d4_img
                source: "assets/storm.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9        
        MDFloatLayout:
            pos_hint: {"center_x": .89, "center_y": .5}
            size_hint: .17, .9
            canvas:
                Color:
                    rgb: rgba(255,255,255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25,25,25,25]
            MDLabel:
                id: d5_date
                text: "05"
                pos_hint: {"center_x": 0.5, "center_y": .875}
                halign: "center"
                font_size:  "15sp"
                font_name: "Poppins"   
            MDLabel:
                id: d5_temp
                text: "15°"
                pos_hint: {"center_x": 0.5, "center_y": .2}
                halign: "center"
                font_size:  "18sp"
                font_name: "Poppins"
            Image:
                id: d5_img
                source: "assets/haze.png"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: .9,.9
'''


class WeatherApp(MDApp):
    api_key = "API_KEY"
    gps_city_memory = ''
    last_call_coord = {'lon': 10., 'lat': 10.}

    gps_location = StringProperty()
    gps_status = StringProperty('=)')

    def button_test(self):
        print("Button pressed")

    def forecast_display_clear(self):
        self.root.ids.d1_img.source = "assets/no_data.png"
        self.root.ids.d1_temp.text = '-°'
        self.root.ids.d2_img.source = "assets/no_data.png"
        self.root.ids.d2_temp.text = '-°'
        self.root.ids.d3_img.source = "assets/no_data.png"
        self.root.ids.d3_temp.text = '-°'
        self.root.ids.d4_img.source = "assets/no_data.png"
        self.root.ids.d4_temp.text = '-°'
        self.root.ids.d5_img.source = "assets/no_data.png"
        self.root.ids.d5_temp.text = '-°'

    def no_connection(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "No connection"
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/notconnected.png"
        self.forecast_display_clear()

    def city_notfound(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "City Not Found"
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/notfound.png"
        self.forecast_display_clear()

    def waiting_for_gps(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "Waiting for GPS..."
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/waiting_for_gps.png"
        self.forecast_display_clear()

    def gps_not_allowed(self):
        self.root.ids.temperature.text = "[b]--[/b]°"
        self.root.ids.weather.text = "GPS was not allowed"
        self.root.ids.humidity.text = "--%"
        self.root.ids.wind_speed.text = "-- m/s"
        self.root.ids.location.text = ""
        self.root.ids.weather_image.source = "assets/gps_not_allowed.png"
        self.forecast_display_clear()

    def gps_location_weather(self):
        print('ща буду искать тут: ', self.last_call_coord)
        self.get_weather(self.last_call_coord)

    def get_weather(self, coordinates):
        try:
            print('пишу погоде...')
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates['lat']}&lon={coordinates['lon']}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            x = response.json()
            print('получил рез\n', x)
            if x["cod"] != "404":
                self.root.ids.city_name.text = ''
                temperature = round(x['main']['temp'])
                humidity = x['main']['humidity']
                weather = x['weather'][0]['main']
                weather_id = str(x['weather'][0]['id'])
                wind_speed = round(x['wind']['speed'])
                location = x["name"] + ', ' + x['sys']['country']
                self.root.ids.temperature.text = f"[b]{temperature}[/b]°"
                self.root.ids.weather.text = str(weather)
                self.root.ids.humidity.text = f"{humidity}%"
                self.root.ids.wind_speed.text = f"{wind_speed} m/s"
                self.root.ids.location.text = location
                if weather_id == '800':
                    self.root.ids.weather_image.source = "assets/sun.png"
                elif '200' <= weather_id <= '232':
                    self.root.ids.weather_image.source = "assets/storm.png"
                elif '300' <= weather_id <= '321' or '500' <= weather_id <= '531':
                    self.root.ids.weather_image.source = "assets/rain.png"
                elif '600' <= weather_id <= '622':
                    self.root.ids.weather_image.source = "assets/snow.png"
                elif '701' <= weather_id <= '781':
                    self.root.ids.weather_image.source = "assets/haze.png"
                elif '801' <= weather_id <= '804':
                    self.root.ids.weather_image.source = "assets/clouds.png"
                self.forecast(coordinates)
            else:
                self.city_notfound()
                print("city not found")
        except requests.ConnectionError:
            self.no_connection()
            print("no connection")

    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name != '':
            print('пишу геокоду...')
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            x = response.json()
            if x['cod'] == '200':
                print('получил рез\n', x['coord'])
                coorditanes = x['coord']
                self.get_weather(coorditanes)
            else:
                self.city_notfound()
        else:
            self.gps_location_weather()

    def forecast(self, coordinates):
        print('получаю прогноз...')
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coordinates['lat']}&lon={coordinates['lon']}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        x = response.json()
        print('получил прогноз:\n', x)

        def choose_img(weather_id):
            if weather_id == '800':
                return "assets/sun.png"
            elif '200' <= weather_id <= '232':
                return "assets/storm.png"
            elif '300' <= weather_id <= '321' or '500' <= weather_id <= '531':
                return "assets/rain.png"
            elif '600' <= weather_id <= '622':
                return "assets/snow.png"
            elif '701' <= weather_id <= '781':
                return "assets/haze.png"
            elif '801' <= weather_id <= '804':
                return "assets/clouds.png"

        self.root.ids.d1_img.source = choose_img(str(x["list"][1]['weather'][0]['id']))
        self.root.ids.d1_temp.text = str(round(x['list'][1]['main']['temp'])) + '°'
        self.root.ids.d1_date.text = x["list"][1]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d2_img.source = choose_img(str(x["list"][9]['weather'][0]['id']))
        self.root.ids.d2_temp.text = str(round(x['list'][9]['main']['temp'])) + '°'
        self.root.ids.d2_date.text = x["list"][9]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d3_img.source = choose_img(str(x["list"][17]['weather'][0]['id']))
        self.root.ids.d3_temp.text = str(round(x['list'][17]['main']['temp'])) + '°'
        self.root.ids.d3_date.text = x["list"][17]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d4_img.source = choose_img(str(x["list"][25]['weather'][0]['id']))
        self.root.ids.d4_temp.text = str(round(x['list'][25]['main']['temp'])) + '°'
        self.root.ids.d4_date.text = x["list"][25]['dt_txt'].split()[0].split('-')[2]

        self.root.ids.d5_img.source = choose_img(str(x["list"][33]['weather'][0]['id']))
        self.root.ids.d5_temp.text = str(round(x['list'][33]['main']['temp'])) + '°'
        self.root.ids.d5_date.text = x["list"][33]['dt_txt'].split()[0].split('-')[2]

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
                self.gps_start(1000, 0)
                Clock.schedule_once(lambda dt: self.get_weather(self.last_call_coord), 7)
            else:
                print("callback. Some permissions refused.")
                self.gps_not_allowed()

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)

    def gps_start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = f"lat: {kwargs['lat']}  lon: {kwargs['lon']}"
        self.last_call_coord['lat'] = kwargs['lat']
        self.last_call_coord['lon'] = kwargs['lon']

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_start(self):
        # self.gps_start(1000, 0)
        self.gps_not_allowed()

    def build(self):
        if platform == "android":
            try:
                gps.configure(on_location=self.on_location,
                              on_status=self.on_status)
            except NotImplementedError:
                import traceback
                traceback.print_exc()
                self.gps_status = 'GPS is not implemented for your platform'
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return Builder.load_string(kv)


if __name__ == "__main__":
    LabelBase.register(name="Poppins", fn_regular="fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="fonts/Poppins-SemiBold.ttf")
    WeatherApp().run()
