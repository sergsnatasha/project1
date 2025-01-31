# -*- coding: utf-8 -*-
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty,StringProperty
from kivymd.uix.widget import MDWidget
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivy.graphics import *
from kivy.core.window import Window
from kivymd.uix.controllers import WindowController
from kivy.uix.scatter import ScatterPlane
from kivy.metrics import dp
import math
from geopy.geocoders import Nominatim
import swisseph as swe
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from kivy.config import Config
import re
Config.set('kivy', 'keyboard_mode', 'systemanddock')

divider = 3
Window.size = (1080/divider, 2000/divider)
class Container(MDScreenManager):
    my_widget = ObjectProperty()
    input_date_year_natal = ObjectProperty()
    input_date_mount_natal = ObjectProperty()
    input_date_day_natal = ObjectProperty()
    input_time_hour_natal = ObjectProperty()
    input_time_minute_natal = ObjectProperty()
    input_time_sec_natal = ObjectProperty()
    input_city_natal = ObjectProperty()
    input_country_natal = ObjectProperty()
    input_latitude_grad_natal = ObjectProperty()
    input_latitude_min_natal = ObjectProperty()
    input_latitude_sec_natal = ObjectProperty()
    input_longitude_grad_natal = ObjectProperty()
    input_longitude_sec_natal = ObjectProperty()
    input_longitude_min_natal = ObjectProperty()
    label_date_natal = ObjectProperty()
    button_natal_minus_min_text = ObjectProperty()
    button_natal_minus_hour_text = ObjectProperty()
    button_natal_plus_min_text = ObjectProperty()
    button_natal_plus_hour_text = ObjectProperty()

    dates = datetime.now()
    latitude_grad_natal = 47
    latitude_min_natal = 45
    latitude_sec_natal = 0
    longitude_grad_natal = 29
    longitude_min_natal = 32
    longitude_sec_natal = 0
    city_natal = 'Подільськ'
    country_natal = 'Україна'
    item_natal_hour = 1
    item_natal_min = 1

    drop_item_menu: MDDropdownMenu = None

    def open_drop_item_menu(self, item):
        items = ['1м', '5м', '10м', '30м', '50м', '1ч', '5ч', '10ч', '12ч', '24ч']
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            }
            for i in items
        ]
        if not self.drop_item_menu:
            self.drop_item_menu = MDDropdownMenu(
                caller=item, items=menu_items, position="center"
            )
        self.drop_item_menu.open()

    def menu_callback(self, text_item):
        self.ids.drop_text.text = text_item
        if text_item == '1м':
            self.item_natal_min = 1
            self.button_natal_plus_min_text.text = text_item
            self.button_natal_minus_min_text.text = text_item
        elif text_item == '5м':
            self.item_natal_min = 5
            self.button_natal_plus_min_text.text = text_item
            self.button_natal_minus_min_text.text = text_item
        elif text_item == '10м':
            self.item_natal_min = 10
            self.button_natal_plus_min_text.text = text_item
            self.button_natal_minus_min_text.text = text_item
        elif text_item == '30м':
            self.item_natal_min = 30
            self.button_natal_plus_min_text.text = text_item
            self.button_natal_minus_min_text.text = text_item
        elif text_item == '50м':
            self.item_natal_min = 50
            self.button_natal_plus_min_text.text = text_item
            self.button_natal_minus_min_text.text = text_item
        elif text_item == '1ч':
            self.item_natal_hour = 1
            self.button_natal_plus_hour_text.text = text_item
            self.button_natal_minus_hour_text.text = text_item
        elif text_item == '5ч':
            self.item_natal_hour = 5
            self.button_natal_plus_hour_text.text = text_item
            self.button_natal_minus_hour_text.text = text_item
        elif text_item == '10ч':
            self.item_natal_hour = 10
            self.button_natal_plus_hour_text.text = text_item
            self.button_natal_minus_hour_text.text = text_item
        elif text_item == '12ч':
            self.item_natal_hour = 12
            self.button_natal_plus_hour_text.text = text_item
            self.button_natal_minus_hour_text.text = text_item
        elif text_item == '24ч':
            self.item_natal_hour = 24
            self.button_natal_plus_hour_text.text = text_item
            self.button_natal_minus_hour_text.text = text_item
        self.drop_item_menu.dismiss()

    def disabled_widgets(self):
        self.root.ids.drop_item.disabled = not self.root.ids.drop_item.disabled

    def get_time(self):
        hour = self.item_natal_hour
        min = self.item_natal_min
        return hour, min


    def starting_app(self):
        latitude = self.my_widget.convert_time_to_decimals([self.latitude_grad_natal, self.latitude_min_natal, self.latitude_sec_natal])
        longitude = 29.67584
        ctime = dt_utc = datetime(self.dates.year, self.dates.month, self.dates.day, self.dates.hour, self.dates.minute, self.dates.second)
        tf = TimezoneFinder()
        timz = tf.timezone_at(lng=longitude, lat=latitude)
        tz = pytz.timezone(timz)
        ctime = tz.localize(ctime)
        offset = ctime.utcoffset().seconds
        offsets = int(offset / 3600)

        date_natal = [self.dates.year, self.dates.month, self.dates.day]
        time_natal = [self.dates.hour - offsets, self.dates.minute, self.dates.second]
        self.my_widget.update_natal_data(date_natal, time_natal, latitude, longitude)
        self.input_date_year_natal.text = str(self.dates.year)
        self.input_date_mount_natal.text = str(self.dates.month)
        self.input_date_day_natal.text = str(self.dates.day)
        self.input_time_hour_natal.text = str(self.dates.hour)
        self.input_time_minute_natal.text = str(self.dates.minute)
        self.input_time_sec_natal.text = str(self.dates.second)
        self.input_city_natal.text = self.city_natal
        self.input_country_natal.text = self.country_natal
        self.input_latitude_grad_natal.text = str(self.latitude_grad_natal)
        self.input_latitude_min_natal.text = str(self.latitude_min_natal)
        self.input_latitude_sec_natal.text = str(self.latitude_sec_natal)
        self.input_longitude_grad_natal.text = str(self.longitude_grad_natal)
        self.input_longitude_min_natal.text = str(self.longitude_min_natal)
        self.input_longitude_sec_natal.text = str(self.longitude_sec_natal)
        self.label_date_natal.text = str(self.dates.year) + '-' + str(self.dates.month) + '-' + str(
            self.dates.day) + '  ' + str(self.dates.hour) + ':' + str(self.dates.minute) + ':' + str(self.dates.second)
    def update_time_check(self, date_year_natal, date_mount_natal, date_day_natal, time_hour_natal, time_minute_natal, hour, min):
        moun_thirty_one_days = [1, 3, 5, 7, 8, 10, 12]
        moun_thirty_days = [4, 6, 9, 11]
        moun_thirty_one_days_minus = [2, 4, 6, 8, 9, 11]
        moun_thirty_days_minus = [5, 7, 10, 12]
        time_minute_natal = time_minute_natal + min
        time_hour_natal = time_hour_natal + hour

        if time_minute_natal > 59:
            time_hour_natal += 1
            time_minute_natal = time_minute_natal - 60
        if time_minute_natal  < 0:
            time_hour_natal -= 1
            time_minute_natal = 60 + time_minute_natal

        if time_hour_natal > 23:
            date_day_natal += 1
            time_hour_natal = time_hour_natal - 24
        if time_hour_natal < 0:
            date_day_natal -= 1
            time_hour_natal = 24 + time_hour_natal

        if date_day_natal > 28 and date_mount_natal == 2 and date_year_natal % 4 != 0:
            date_mount_natal += 1
            date_day_natal = 1

        if date_day_natal > 29 and date_mount_natal == 2 and date_year_natal % 4 == 0:
            date_mount_natal += 1
            date_day_natal = 1

        if date_day_natal > 30:
            for mount in moun_thirty_days:
                if date_mount_natal == mount:
                    date_mount_natal += 1
                    date_day_natal = 1

        if date_day_natal > 31:
            for mount in moun_thirty_one_days:
                if date_mount_natal == mount:
                    date_mount_natal += 1
                    date_day_natal = 1

        if  date_day_natal < 1 and date_mount_natal == 3:
            if date_year_natal % 4 == 0:
                date_mount_natal -= 1
                date_day_natal = 29
            if date_year_natal % 4 != 0:
                date_mount_natal -= 1
                date_day_natal = 28


        if date_day_natal < 1:
            for mount in moun_thirty_one_days_minus:
                if date_mount_natal == mount:
                    date_mount_natal -= 1
                    date_day_natal = 31

        if date_day_natal < 1:
            for mount in moun_thirty_days_minus:
                if date_mount_natal == mount:
                    date_mount_natal -= 1
                    date_day_natal = 30

        if  date_day_natal < 1 and date_mount_natal == 1:
            date_mount_natal = 12
            date_day_natal = 31
            date_year_natal -= 1

        if  date_mount_natal > 12:
            date_mount_natal = 1
            date_year_natal += 1

        return date_year_natal, date_mount_natal, date_day_natal, time_hour_natal, time_minute_natal

    def check_data(self, hour, min, flag):
        moun_thirty_one_days = [1, 3, 5, 7, 8, 10, 12]
        moun_thirty_days = [4, 6, 9, 11]
        date_year_natal = self.dates.year
        date_mount_natal = self.dates.month
        date_day_natal = self.dates.day
        time_hour_natal = self.dates.hour
        time_minute_natal = self.dates.minute
        time_sec_natal = self.dates.second
        city_natal = self.city_natal
        country_natal = self.country_natal
        latitude_grad_natal = 47
        latitude_min_natal = 45
        latitude_sec_natal = 0
        longitude_grad_natal = 29
        longitude_min_natal = 32
        longitude_sec_natal = 0
        #date natal chek
        if  re.fullmatch(r'\d\d\d\d', self.input_date_year_natal.text, flags=re.ASCII) and 3000 > int(self.input_date_year_natal.text) >= 0:
            date_year_natal = int(self.input_date_year_natal.text)
        if  re.fullmatch(r'\d|\d\d', self.input_date_mount_natal.text, flags=re.ASCII) and 13 > int(self.input_date_mount_natal.text) >= 0:
            date_mount_natal = int(self.input_date_mount_natal.text)
        if  re.fullmatch(r'\d|\d\d', self.input_date_day_natal.text, flags=re.ASCII) and 29 > int(self.input_date_day_natal.text) >= 0 and date_mount_natal == 2 and date_year_natal % 4 != 0 :
            date_day_natal = int(self.input_date_day_natal.text)
        if  re.fullmatch(r'\d|\d\d', self.input_date_day_natal.text, flags=re.ASCII) and 30 > int(self.input_date_day_natal.text) >= 0 and date_mount_natal == 2 and date_year_natal % 4 == 0:
            date_day_natal = int(self.input_date_day_natal.text)
        if  re.fullmatch(r'\d|\d\d', self.input_date_day_natal.text, flags=re.ASCII) and 31 > int(self.input_date_day_natal.text) >= 0:
            for mount in moun_thirty_days:
                if date_mount_natal == mount:
                    date_day_natal = int(self.input_date_day_natal.text)
        if  re.fullmatch(r'\d|\d\d', self.input_date_day_natal.text, flags=re.ASCII) and 32 > int(self.input_date_day_natal.text) >= 0:
            for mount in moun_thirty_one_days:
                if date_mount_natal == mount:
                    date_day_natal = int(self.input_date_day_natal.text)
        date_natal = [date_year_natal, date_mount_natal, date_day_natal]
        # time natal chek
        if  re.fullmatch(r'\d|\d\d', self.input_time_hour_natal.text, flags=re.ASCII) and 24 > int(self.input_time_hour_natal.text) >= 0:
            time_hour_natal = int(self.input_time_hour_natal.text)
        if  re.fullmatch(r'\d|\d\d', self.input_time_minute_natal.text, flags=re.ASCII) and 60 > int(self.input_time_minute_natal.text) >= 0:
            time_minute_natal = int(self.input_time_minute_natal.text)
        if  re.fullmatch(r'\d|\d\d', self.input_time_sec_natal.text, flags=re.ASCII) and 60 > int(self.input_time_sec_natal.text) >= 0:
            time_sec_natal = int(self.input_time_sec_natal.text)
        # city natal chek
        if  re.fullmatch(r'\w+', self.input_city_natal.text, flags=re.ASCII):
            print(self.input_city_natal.text)

        # country natal chek
        if re.fullmatch(r'\w+', self.input_country_natal.text, flags=re.ASCII):
            print(self.input_country_natal.text)

        # lattitude natal chek
        if  re.fullmatch(r'[-+]?\d+', self.input_latitude_grad_natal.text, flags=re.ASCII) and 90 > int(self.input_latitude_grad_natal.text) > -90:
            latitude_grad_natal = int(self.input_latitude_grad_natal.text)

        if  re.fullmatch(r'\d|\d\d', self.input_latitude_min_natal.text, flags=re.ASCII) and 60 > int(self.input_latitude_min_natal.text) >= 0:
            latitude_min_natal = int(self.input_latitude_min_natal.text)

        if  re.fullmatch(r'\d|\d\d', self.input_latitude_sec_natal.text, flags=re.ASCII) and 60 > int(self.input_latitude_sec_natal.text) >= 0:
            latitude_sec_natal = int(self.input_latitude_sec_natal.text)

            # longitude natal chek
        if re.fullmatch(r'[-+]?\d+', self.input_longitude_grad_natal.text, flags=re.ASCII) and 180 > int(self.input_longitude_grad_natal.text) > -180:
            longitude_grad_natal = int(self.input_longitude_grad_natal.text)

        if re.fullmatch(r'\d|\d\d', self.input_longitude_min_natal.text, flags=re.ASCII) and 60 > int(self.input_longitude_min_natal.text) >= 0:
            longitude_min_natal = int(self.input_longitude_min_natal.text)

        if re.fullmatch(r'\d|\d\d', self.input_longitude_sec_natal.text, flags=re.ASCII) and 60 > int(self.input_longitude_sec_natal.text) >= 0:
            longitude_sec_natal = int(self.input_longitude_sec_natal.text)


        latitude = self.my_widget.convert_time_to_decimals([latitude_grad_natal, latitude_min_natal, latitude_sec_natal])
        longitude = self.my_widget.convert_time_to_decimals([longitude_grad_natal, longitude_min_natal, longitude_sec_natal])
        ctime = dt_utc = datetime(date_year_natal, date_mount_natal, date_day_natal, time_hour_natal, time_minute_natal, time_sec_natal)
        tf = TimezoneFinder()
        timz = tf.timezone_at(lng=longitude, lat=latitude)
        tz = pytz.timezone(timz)
        ctime = tz.localize(ctime)
        offset = ctime.utcoffset().seconds
        offsets = int(offset / 3600)

        time_natal = [time_hour_natal - offsets, time_minute_natal, time_sec_natal]
        if flag:
            time_hour_natal = int(self.input_time_hour_natal.text)
            time_check = self.update_time_check(date_year_natal, date_mount_natal, date_day_natal, time_hour_natal,
                              time_minute_natal, hour, min)

            self.input_time_hour_natal.text = str(time_check[3])
            self.input_time_minute_natal.text = str(time_check[4])
            self.input_date_day_natal.text = str(time_check[2])
            self.input_date_mount_natal.text = str(time_check[1])
            self.input_date_year_natal.text = str(time_check[0])
            date_natal = [time_check[0], time_check[1], time_check[2]]
            time_natal = [time_check[3] - offsets, time_check[4], time_sec_natal]
            self.label_date_natal.text = str(date_natal[0])+'-'+str(date_natal[1])+'-'+str(date_natal[2])+'  '+str(time_natal[0]+offsets)+':'+str(time_natal[1])+':'+str(time_natal[2])
        self.my_widget.update_natal_data(date_natal, time_natal, latitude, longitude)
        if flag == False:
            self.label_date_natal.text = str(date_year_natal) + '-' + str(date_mount_natal) + '-' + str(
                date_day_natal) + '  ' + str(time_hour_natal) + ':' + str(time_minute_natal) + ':' + str(time_sec_natal)

            self.current = 'screen_app'


    '''
        nominaltim = Nominatim(user_agent='user')
        location = nominaltim.geocode('Подільськ, Україна')
        print((location.latitude, location.longitude))
     '''

class BaseMDNavigationItem(MDNavigationItem):
    text = StringProperty()
    icon = StringProperty()
class ResizableDraggable(ScatterPlane):
    def on_touch_down(self, touch):
        # Override Scatter's `on_touch_down` behavior for mouse scroll
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                if self.scale < 10:
                    self.scale = self.scale * 1.1
            elif touch.button == 'scrollup':
                if self.scale > 1:
                    self.scale = self.scale * 0.8
        # If some other kind of "touch": Fall back on Scatter's behavior
        else:
            super(ResizableDraggable, self).on_touch_down(touch)
class MyWidget(MDWidget):
    swe.set_ephe_path('ephe')
    scale_value_x = NumericProperty(1)
    scale_value_y = NumericProperty(1)
    scale_value_z = NumericProperty(1)

    radius_3 = 125
    center_circle_x = 300
    center_circle_y = 800
    radius_1 = 255
    radius_2 = 300
    radius_4 = (radius_2 + 20)
    radius_5 = (radius_3 + 20)
    radius_6 = (radius_5 + 30)
    radius_circle_zodiac = (radius_2 - radius_1)/2 + radius_1
    radius_circle_asc = radius_4 + 20


    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

    def update_natal_data(self, date_natal, time_natal, latitude, longitude):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            #self.rect = Rectangle(pos=self.pos, size=self.size)
            time = self.convert_time_to_decimals((time_natal[0], time_natal[1], time_natal[2]))

            width_color_zodiak = (self.radius_2 - self.radius_1)/2
            radius_color_zodiak = width_color_zodiak + self.radius_1

            width_color_circcle = (self.radius_1 - self.radius_3)/2
            radius_color_circle = width_color_circcle + self.radius_3

            degrees_circle = [(330, 360), (300, 330), (270, 300), (240, 270),
                              (210, 240), (180, 210), (150, 180), (120, 150),
                              (90, 120), (60, 90), (30, 60), (0, 30)]

            color_zodiac = [(0.98, 0.74, 0.72), (0.99, 0.86, 0.74), (0.99, 0.99, 0.74), (0.86, 0.99, 0.74),
                            (0.74, 0.99, 0.74), (0.67, 0.85, 0.72), (0.7, 0.99, 0.99), (0.74, 0.86, 0.98),
                            (0.74, 0.74, 0.99), (0.86, 0.74, 0.99), (0.98, 0.72, 0.98), (0.98, 0.74, 0.86)]

            jd = swe.julday(date_natal[0], date_natal[1], date_natal[2], time)
            houses = swe.houses(jd, latitude, longitude, b'K')
            print(jd)
            print(houses)

            planet = {}
            planet_coordin = []
            retrogr_planet = []
            planet_name = ['TRUE_NODE' ,'SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN',
                           'URANUS', 'NEPTUNE', 'PLUTO', 'Selena', 'Proserpina',
                           'hiron','Lilit']
            planet_int = [11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 56, 57, 15, 12]

            for name, coord in zip(planet_name, planet_int):
                coordinate = swe.calc_ut(jd, coord, swe.FLG_SPEED)
                planet[name] = coordinate[0][0]
                planet_coordin.append(coordinate[0][0])
                if coordinate[0][3] < 0:
                    retrogr_planet.append('R')
                else:
                    retrogr_planet.append('D')

            planet_coordin.insert(1, planet_coordin[0] + 180)
            retrogr_planet.insert(1, retrogr_planet[0])

            print(planet)

            swe.close()

            Color(0.88, 0.92, 0.98)
            size_house_image = 15
            Line(circle=(self.center_circle_x, self.center_circle_y, radius_color_circle), width=width_color_circcle)

            lines_hous_coordinates = self.convert_degrees_to_coordinates(houses[0][0], houses[0], self.center_circle_x,
                                                                    self.center_circle_y, self.radius_3,
                                                                    self.radius_4)
            houses_image = ['images/one.png', 'images/two.png', 'images/three.png', 'images/four.png',
                            'images/five.png', 'images/six.png', 'images/seven.png', 'images/eight.png',
                            'images/nine.png', 'images/ten.png', 'images/eleven.png', 'images/twelve.png']

            Color(1., 0, 0)
            for lines_coordinate in lines_hous_coordinates:
                Line(points=(lines_coordinate[0], lines_coordinate[1], lines_coordinate[2],
                             lines_coordinate[3]), width=1, cap='square')

            hous_image_coor = []
            for coordinate in houses[0]:
                hous_image_coor.append(coordinate - 2)


            lines_hous_image_coordinates = self.convert_degrees_to_coordinates(houses[0][0], hous_image_coor, self.center_circle_x,
                                                                         self.center_circle_y, self.radius_3,
                                                                         self.radius_4)


            for coord, name_hous in zip(lines_hous_image_coordinates, houses_image):
                Rectangle(source=name_hous, pos=(coord[2]-size_house_image/2, coord[3]-size_house_image/2), size=(size_house_image, size_house_image))

            lines_asc_coordinates = self.convert_degrees_to_coordinates(houses[0][0], houses[0], self.center_circle_x,
                                                                    self.center_circle_y, self.radius_3,
                                                                    self.radius_circle_asc)
            Line(points=(lines_asc_coordinates[0][0], lines_asc_coordinates[0][1], lines_asc_coordinates[0][2],
                         lines_asc_coordinates[0][3]), width=1.3, cap='square')
            Line(points=(lines_asc_coordinates[6][0], lines_asc_coordinates[6][1], lines_asc_coordinates[6][2],
                         lines_asc_coordinates[6][3]), width=1.3, cap='square')
            Color(0, 0, 1)
            Line(points=(lines_asc_coordinates[3][0], lines_asc_coordinates[3][1], lines_asc_coordinates[3][2],
                         lines_asc_coordinates[3][3]), width=1.3, cap='square')
            Line(points=(lines_asc_coordinates[9][0], lines_asc_coordinates[9][1], lines_asc_coordinates[9][2],
                         lines_asc_coordinates[9][3]), width=1.3, cap='square')

            for col, degre in zip(color_zodiac, degrees_circle):
                Color(col[0], col[1], col[2])
                Line(circle=(self.center_circle_x, self.center_circle_y, radius_color_zodiak, degre[0]-90+houses[0][0],
                             degre[1]-90+houses[0][0] , 8), width=width_color_zodiak, cap='none')

            Color(0, 0, 1, 1, mode='rgba')
            Line(circle=(self.center_circle_x, self.center_circle_y, self.radius_3), width=1)
            Line(circle=(self.center_circle_x, self.center_circle_y, self.radius_1), width=1)
            Line(circle=(self.center_circle_x, self.center_circle_y, self.radius_2), width=1)

            degrees_circle_line = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
            lines_zodiac_coordinates = self.convert_degrees_to_coordinates(houses[0][0]-90, degrees_circle_line, self.center_circle_x,
                                                                    self.center_circle_y, self.radius_1,
                                                                    self.radius_2)

            for coord in lines_zodiac_coordinates:
                Line(points=(coord[0], coord[1], coord[2], coord[3]), width=1/divider, cap='square')


            zodiac_images = ['images/Cancer.png', 'images/Leo.png', 'images/Virgo.png','images/Libra.png',
                             'images/Scorpio.png', 'images/Sagittarius.png', 'images/Capricorn.png','images/Aquarius.png',
                             'images/Pisces.png', 'images/Aries.png', 'images/Taurus.png', 'images/Gemini.png']

            degrees_circle_zodiac = [15, 45, 75, 105, 135, 165, 195, 225, 255, 285, 315, 345]
            size_zodiac_image = 25
            lines_coordinates_zodiac = self.convert_degrees_to_coordinates(houses[0][0] - 90, degrees_circle_zodiac,
                                                                    self.center_circle_x,
                                                                    self.center_circle_y, self.radius_1,
                                                                    self.radius_circle_zodiac)
            for coordinate, zodiac_image in zip(lines_coordinates_zodiac, zodiac_images):
                Rectangle(source=zodiac_image, pos=(coordinate[2]-size_zodiac_image/2, coordinate[3]-size_zodiac_image/2), size=(size_zodiac_image, size_zodiac_image))

            planet_coordinates = self.convert_degrees_to_coordinates(houses[0][0], planet_coordin, self.center_circle_x,
                                                                     self.center_circle_y, self.radius_2,
                                                                     self.radius_5)

            planet_image = ['images/south node.png', 'images/north node.png', 'images/sun.png', 'images/moon.png',
                            'images/mercury.png', 'images/venus.png', 'images/mars.png', 'images/jupiter.png',
                            'images/saturn.png', 'images/uranus.png', 'images/neptune.png', 'images/pluto.png',
                            'images/selena.png', 'images/proserpine.png', 'images/hiron.png', 'images/lilith.png']
            planet_retrog_image = ['images/south_node_retrog.png', 'images/north_node_retrog.png', 'images/sun_retrog.png', 'images/moon_retrog.png',
                            'images/mercury_retrog.png', 'images/venus_retrog.png', 'images/mars_retrog.png', 'images/jupiter_retrog.png',
                            'images/saturn_retrog.png', 'images/uranus_retrog.png', 'images/neptune_retrog.png', 'images/pluto_retrog.png',
                            'images/selena_retrog.png', 'images/proserpine_retrog.png', 'images/hiron_retrog.png', 'images/lilith_retrog.png']
            planet_image_n = ['images/south node_N.png', 'images/north node_N.png', 'images/sun_N.png', 'images/moon_N.png',
                            'images/mercury_N.png', 'images/venus_N.png', 'images/mars_N.png', 'images/jupiter_N.png',
                            'images/saturn_N.png', 'images/uranus_N.png', 'images/neptune_N.png', 'images/pluto_N.png',
                            'images/selena_N.png', 'images/proserpine_N.png', 'images/hiron_N.png', 'images/lilith_N.png']
            planet_retrog_image_n = ['images/south_node_retrog_N.png', 'images/north_node_retrog_N.png', 'images/sun_retrog_N.png', 'images/moon_retrog_N.png',
                                   'images/mercury_retrog_N.png', 'images/venus_retrog_N.png', 'images/mars_retrog_N.png', 'images/jupiter_retrog_N.png',
                                   'images/saturn_retrog_N.png', 'images/uranus_retrog_N.png', 'images/neptune_retrog_N.png', 'images/pluto_retrog_N.png',
                                   'images/selena_retrog_N.png', 'images/proserpine_retrog_N.png', 'images/hiron_retrog_N.png', 'images/lilith_retrog_N.png']

            size_planet_image = 15
            index_aspect = 0
            for coord_planet in planet_coordinates:
                aspect = self.get_position_planet(planet_coordin, houses, retrogr_planet, index_aspect)

                coord_planet_x = coord_planet[2]-10
                coord_planet_y = coord_planet[3]-10
                planet_coordinat = self.convert_degrees_to_coordinate(houses[0][0], aspect[3],
                                                                         self.center_circle_x,
                                                                         self.center_circle_y, self.radius_2,
                                                                         self.radius_6)

                if aspect[4]:
                    coord_planet_x = planet_coordinat[0][2] - size_planet_image/2
                    coord_planet_y = planet_coordinat[0][3] - size_planet_image/2

                if aspect[1] == 'D' and aspect[2]:
                    Color(1, 0, 0)
                    Line(ellipse=(aspect[0][2]-2, aspect[0][3]-2, 4, 4), width=1)
                    Rectangle(source=planet_image_n[index_aspect], pos=(coord_planet_x, coord_planet_y), size=(size_planet_image, size_planet_image))
                elif aspect[1] == 'R' and aspect[2]:
                    Color(1, 0, 0)
                    Line(ellipse=(aspect[0][2]-2, aspect[0][3]-2, 4, 4), width=1)
                    Rectangle(source=planet_retrog_image_n[index_aspect], pos=(coord_planet_x, coord_planet_y), size=(size_planet_image, size_planet_image))
                elif aspect[1] == 'D' and aspect[2] == False:
                    Color(0, 1, 0)
                    Line(ellipse=(aspect[0][2]-2, aspect[0][3]-2, 4, 4), width=1)
                    Rectangle(source=planet_image[index_aspect], pos=(coord_planet_x, coord_planet_y), size=(size_planet_image, size_planet_image))
                elif aspect[1] == 'R' and aspect[2] == False:
                    Color(0, 1, 0)
                    Line(ellipse=(aspect[0][2]-2, aspect[0][3]-2, 4, 4), width=1)
                    Rectangle(source=planet_retrog_image[index_aspect], pos=(coord_planet_x, coord_planet_y), size=(size_planet_image, size_planet_image))
                index_aspect += 1

    def get_position_planet(self,plan_pos, houses, retrog, index,  trans=False):
        south_node = plan_pos[0]
        north_node = plan_pos[1]
        sun = plan_pos[2]
        moon = plan_pos[3]
        mercury = plan_pos[4]
        venus = plan_pos[5]
        mars = plan_pos[6]
        jupiter = plan_pos[7]
        saturn = plan_pos[8]
        uranus = plan_pos[9]
        neptune = plan_pos[10]
        pluto = plan_pos[11]
        selena = plan_pos[12]
        proserpine = plan_pos[13]
        hiron = plan_pos[14]
        lilith = plan_pos[15]

        tenson = False
        tenson_yes = 0
        tenson_no = 0

        planets = [south_node, north_node, sun,  moon, mercury, venus, mars, jupiter, saturn, uranus, neptune,
                  pluto, selena, proserpine, hiron, lilith]

        planet_coord = planet_coordinates = self.convert_degrees_to_coordinates(houses[0][0], plan_pos, self.center_circle_x,
                                                                     self.center_circle_y, self.radius_3,
                                                                     self.radius_3)


        a = 0
        opposition_a = 0
        opposition_b = 0
        quadrature_a = 0
        quadrature_b = 0
        trigon_a = 0
        trigon_b = 0
        sextile_a = 0
        sextile_b = 0
        сompound_a = 0
        сompound_b = 0
        if index == 0: # south_node
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 1
            quadrature_b = 1
            trigon_a = 5
            trigon_b = 5
            sextile_a = 5
            sextile_b = 5
            a = 1
        elif index == 1: # north_node
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 1
            quadrature_b = 1
            trigon_a = 5
            trigon_b = 5
            sextile_a = 5
            sextile_b = 5
            a = 1
        elif index == 2: # SUN
            сompound_a = 12
            сompound_b = 12
            opposition_a = 12
            opposition_b = 12
            quadrature_a = 10
            quadrature_b = 10
            trigon_a = 12
            trigon_b = 12
            sextile_a = 6.5
            sextile_b = 6.5
            a = 5
        elif index == 3: # moon
            сompound_a = 10
            сompound_b = 10
            opposition_a = 10
            opposition_b = 10
            quadrature_a = 8
            quadrature_b = 8
            trigon_a = 8
            trigon_b = 8
            sextile_a  = 6
            sextile_b = 6
            a = 4
        elif index == 4: # mercury
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 5
            quadrature_b = 5
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 2
        elif index == 5: # venus
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 5
            quadrature_b = 5
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 2
        elif index == 6: # mars
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 5
            quadrature_b = 5
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 2
        elif index == 7: # jupiter
            сompound_a = 8
            сompound_b = 8
            opposition_a = 8
            opposition_b = 8
            quadrature_a = 7
            quadrature_b = 7
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 3
        elif index == 8: # saturn
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 5
            quadrature_b = 5
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 2
        elif index == 9: # uranus
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 5
            quadrature_b = 5
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 2
        elif index == 10: # neptune
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 5
            quadrature_b = 5
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 2
        elif index == 11: # pluto
            сompound_a = 0.1
            сompound_b = 0.1
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 5
            quadrature_b = 5
            trigon_a = 5
            trigon_b = 5
            sextile_a  = 5
            sextile_b = 5
            a = 1
        elif index == 12: # selena
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 1
            quadrature_b = 1
            trigon_a = 5
            trigon_b = 5
            sextile_a = 5
            sextile_b = 5
            a = 0
        elif index == 13:  # prozerpina
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 1
            quadrature_b = 1
            trigon_a = 5
            trigon_b = 5
            sextile_a = 5
            sextile_b = 5
            a = 0
        elif index == 14: # hiron
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 1
            quadrature_b = 1
            trigon_a = 5
            trigon_b = 5
            sextile_a = 5
            sextile_b = 5
            a = 0
        elif index == 15: # lilith
            сompound_a = 5
            сompound_b = 5
            opposition_a = 5
            opposition_b = 5
            quadrature_a = 1
            quadrature_b = 1
            trigon_a = 5
            trigon_b = 5
            sextile_a = 5
            sextile_b = 5
            a = 0


        planet = planets.pop(index)
        planet_coor = planet_coord.pop(index)
        retr = retrog[index]
        planets_name = ['north_NODE', 'south_NODE',  'SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN',
                       'URANUS', 'NEPTUNE', 'PLUTO', 'Selena', 'Proserpina', 'hiron', 'Lilit']
        c = 0
        orb = False
        planet_name = planets_name.pop(index)
        for pl, pc, pn in zip(planets, planet_coord, planets_name):
            b = 0
            opposition_a_o = 0
            opposition_b_o = 0
            quadrature_a_o = 0
            quadrature_b_o = 0
            trigon_a_o = 0
            trigon_b_o = 0
            sextile_a_o = 0
            sextile_b_o = 0
            сompound_b_o = 0
            if pn == 'north_NODE':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 1
                quadrature_b_o = 1
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 1
            elif pn == 'south_NODE':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 1
                quadrature_b_o = 1
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 1
            elif pn == 'SUN':
                сompound_a_o = 12
                сompound_b_o = 12
                opposition_a_o = 12
                opposition_b_o = 12
                quadrature_a_o = 10
                quadrature_b_o = 10
                trigon_a_o = 12
                trigon_b_o = 12
                sextile_a_o  = 6.5
                sextile_b_o = 6.5
                b = 5
            elif pn == 'MOON':
                сompound_a_o = 10
                сompound_b_o = 10
                opposition_a_o = 10
                opposition_b_o = 10
                quadrature_a_o = 8
                quadrature_b_o = 8
                trigon_a_o = 8
                trigon_b_o = 8
                sextile_a_o  = 6
                sextile_b_o = 6
                b = 4
            elif pn == 'MERCURY':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 5
                quadrature_b_o = 5
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o  = 5
                sextile_b_o = 5
                b = 2
            elif pn == 'VENUS':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 5
                quadrature_b_o = 5
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 2
            elif pn == 'MARS':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 5
                quadrature_b_o = 5
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 2
            elif pn == 'JUPITER':
                сompound_a_o = 8
                сompound_b_o = 8
                opposition_a_o = 8
                opposition_b_o = 8
                quadrature_a_o = 7
                quadrature_b_o = 7
                trigon_a_o = 5
                trigon_b_o = 7
                sextile_a_o = 5
                sextile_b_o = 5
                b = 3
            elif pn == 'SATURN':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 5
                quadrature_b_o = 5
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 2
            elif pn == 'URANUS':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 6
                quadrature_a_o = 5
                quadrature_b_o = 5
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 2
            elif pn == 'NEPTUNE':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 6
                quadrature_a_o = 5
                quadrature_b_o = 5
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 2
            elif pn == 'PLUTO':
                сompound_a_o = 0.1
                сompound_b_o = 0.1
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 5
                quadrature_b_o = 5
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 1
            elif pn == 'Selena':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 1
                quadrature_b_o = 1
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 0
            elif pn == 'hiron':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 1
                quadrature_b_o = 1
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 0
            elif pn == 'Proserpina':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 1
                quadrature_b_o = 1
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 0
            elif pn == 'Lilit':
                сompound_a_o = 5
                сompound_b_o = 5
                opposition_a_o = 5
                opposition_b_o = 5
                quadrature_a_o = 1
                quadrature_b_o = 1
                trigon_a_o = 5
                trigon_b_o = 5
                sextile_a_o = 5
                sextile_b_o = 5
                b = 0

            diferent = abs(planet - pl)
            if diferent < 6 and planet - pl < 0:
                c = planet
                orb = True

            if diferent > 180:
                dif = diferent - 180
                diferent = 180 - dif - (dif * 0.001)

            if diferent >= 180 - (opposition_a + opposition_a_o)/2 and diferent <= 180 + (opposition_b + opposition_b_o)/2:
                Color(0, 0, 1)
                Line(points=(planet_coor[0], planet_coor[1], pc[2], pc[3]), width=0.4, cap='square')
                tenson_yes += 1
            elif diferent >= 90 - (quadrature_a + quadrature_a_o)/2 and diferent <= 90 + (quadrature_b + quadrature_b_o)/2:
                Color(1, 0, 0)
                Line(points=(planet_coor[0], planet_coor[1], pc[2], pc[3]), width=0.4, cap='square')
                tenson_yes += 1
            elif diferent >= 120 - (trigon_a + trigon_a_o)/2 and diferent <= 120 + (trigon_b + trigon_b_o)/2:
                Color(0, 0.5, 0)
                Line(points=(planet_coor[0], planet_coor[1], pc[2], pc[3]), width=0.4, cap='square')
                tenson_no += 1
            elif diferent >= 60 - (sextile_a + sextile_a_o)/2 and diferent <= 60 + (sextile_b + sextile_b_o)/2:
                Color(0.5, 0.5, 0.5)
                Line(points=(planet_coor[0], planet_coor[1], pc[2], pc[3]), width=0.4, cap='square')
            elif diferent >= 0 and diferent <= (сompound_b + сompound_b_o)/2:
                Color(0, 0, 1)
                Line(points=(planet_coor[0], planet_coor[1], pc[2], pc[3]), width=0.4, cap='square')

        if tenson_yes > tenson_no:
            tenson = True
        else:
            tenson = False

        return planet_coor , retr, tenson, c, orb
    def convert_degrees_to_coordinates(self, ascendent, degreses, center_circle_x, center_circle_y, radius_1, radius_2):
        coordinates = []
        for degres in degreses:
            degres -= ascendent
            x1 = center_circle_x - radius_1 * math.cos(degres * math.pi / 180.)
            y1 = center_circle_y - radius_1 * math.sin(degres * math.pi / 180.)
            x2 = center_circle_x - radius_2 * math.cos(degres * math.pi / 180.)
            y2 = center_circle_y - radius_2 * math.sin(degres * math.pi / 180.)
            coordinates.append([x1, y1, x2, y2])

        return coordinates
    def convert_degrees_to_coordinate(self, ascendent, degres, center_circle_x, center_circle_y, radius_1, radius_2):
        coordinates = []

        degres -= ascendent
        x1 = center_circle_x - radius_1 * math.cos(degres * math.pi / 180.)
        y1 = center_circle_y - radius_1 * math.sin(degres * math.pi / 180.)
        x2 = center_circle_x - radius_2 * math.cos(degres * math.pi / 180.)
        y2 = center_circle_y - radius_2 * math.sin(degres * math.pi / 180.)
        coordinates.append([x1, y1, x2, y2])

        return coordinates
    def convert_time_to_decimals(self, time):
        hours = time[0]
        minutes = time[1]
        seconds = time[2]

        decimals = (seconds / 60 + minutes) / 60 + hours
        return decimals
    def convert_decimals_to_time(self, decimals):
        hours = int(decimals)
        minutes = (decimals - hours) * 60
        seconds = (minutes - int(minutes)) * 60
        time = (hours, int(minutes), int(seconds))

        return time


class MyApp(MDApp):
    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    def build(self):
        return Container()
        #return Builder.load_file('my.kv')


if __name__ == '__main__':
    MyApp().run()
