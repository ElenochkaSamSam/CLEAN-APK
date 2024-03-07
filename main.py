from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class CalcLabel(Button):
    @staticmethod
    def to_num(s):
        try:
            float(s)
            return float(s)
        except ValueError:
            return 0


Builder.load_string("""
<ScreenManagement>:
    Screen1:
        id: screen1
        name: 'screen1'
    Screen2:
        id: screen2
        name: 'screen2'
<Screen1>:
    background_color: "blue"
    orientation: 'vertical'
    font_name: 'Roboto'

    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'screen1.jpg'
    GridLayout:
        rows:2
        cols:2
        size_hint: 1,0.1
        spacing: 2,2
        Button:
            disabled: True
            background_disabled_normal: "fone_car.png"
            color: 'black'
            italic: True
            text: "Бюджет расходов:"
        CalcLabel:
            disabled: True
            background_disabled_normal: "fone_car.png"
            color: 'black'
            id: losted
            bold: True
            font_size: 20
            text: str(self.to_num(root.stored_data.get('mydata')['text_car'])).split('.')[0]
        Button:
            disabled: True
            background_disabled_normal: "fone_car.png"
            color: 'black'
            italic: True
            text: "Потрачено:"
        CalcLabel:
            disabled: True
            background_disabled_normal: "fone_car.png"
            color: 'black'
            bold: True
            font_size: 20
            text: str((self.to_num(root.stored_data.get('mydata')['lost_past_car']))*100/self.to_num(losted.text)).split('.')[0]+"%" if self.to_num(losted.text)!=0 else "0"

    GridLayout:
        rows:1
        cols:3
        spacing: 2,2
        size_hint: 1,0.08
        Button:
            background_normal: "car.png"
            on_release:
                root.manager.current = 'screen2'
        Button:
            disabled: True
            background_disabled_normal: "stocent.png" 
            color: 'black'
            id: lb_car
            bold: True
            font_size: 20
            text: root.stored_data.get('mydata')['cent_car']
        Button:
            disabled: True
            background_disabled_normal: "fone_car.png" 
            color: 'black'
            id: lbl_car
            bold: True
            font_size: 20       
            text: root.stored_data.get('mydata')['text_car']

<Screen2>:
    txtinput_car: txtinput_car
    day_car: day_car
    lost_car: lost_car
    cent_car: cent_car
    orientation: 'vertical'
    font_name: 'Roboto'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'screen2.jpg'
    GridLayout:
        size_hint: 1,0.3
        cols:2
        rows:4
        Label:
            color: 'black'
            italic: True
            text: "Ежемесячный лимит:"
        TextInput:
            color: 'black'
            id: txtinput_car
            italic: True
            bold: True
            font_size: 20
            text: root.stored_data.get('mydata')['text_car'] if root.stored_data.exists('mydata') else '0'

        Label:
            color: 'black'
            italic: True
            text: "Потратили сегодня:"
        TextInput:
            color: 'black'
            id: day_car
            bold: True
            font_size: 20
            text: root.stored_data.get('mydata')['days_car'] if root.stored_data.exists('mydata') else ''

    GridLayout: 
        size_hint: 1,0.2
        cols:3
        rows:1
        Button:
            disabled: True
            background_disabled_normal: "fone_car.png"
            color: 'black'
            italic: True
            size_hint: 0.5,0.2
            text: "Всего потрачено:"
        CalcLabel:
            disabled: True
            background_disabled_normal: "fone_car.png"
            color: 'black'
            size_hint: 0.25,0.2
            id: cent_car
            bold: True
            font_size: 20
            text: str((self.to_num(day_car.text)+self.to_num(root.stored_data.get('mydata')['lost_past_car']))*100/self.to_num(txtinput_car.text)).split('.')[0]+"%" if self.to_num(txtinput_car.text) and self.to_num(day_car.text)!=0 else str(self.to_num(root.stored_data.get('mydata')['lost_past_car'])*100/self.to_num(root.stored_data.get('mydata')['text_car'])).split('.')[0]+"%" if self.to_num(root.stored_data.get('mydata')['text_car'])!=0 else "0"     

        CalcLabel:
            disabled: True
            background_disabled_normal: "fone_car.png"
            color: 'black'
            size_hint: 0.25,0.2
            id: lost_car
            bold: True
            font_size: 20
            text: str(self.to_num(root.stored_data.get('mydata')['lost_car'])+ self.to_num(day_car.text)).split('.')[0]   

    GridLayout:
        size_hint: 1,0.2
        cols:3
        rows:1
        Label:
            text: ""
        Button:
            italic: True
            background_normal: "car.png"
            #text: "На главную"
            on_press:
                root.stored_data.put('mydata', text_car=txtinput_car.text,days_car="0",days_past_car=day_car.text,lost_car=lost_car.text,lost_past_car=lost_car.text,cent_car=cent_car.text)
            on_release:
                root.manager.current = 'screen1'
        Label:
            text: ""
""")


class Screen1(BoxLayout, Screen):
    stored_data = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Screen1, self).__init__(*args, **kwargs)
        self.stored_data = JsonStore('storage.json')


class Screen2(BoxLayout, Screen):
    stored_data = ObjectProperty(None)

    # def to_num(self):
    # try:
    # float(self)
    # return float(self)
    # except ValueError:
    # return 0

    def __init__(self, *args, **kwargs):
        super(Screen2, self).__init__(*args, **kwargs)
        self.stored_data = JsonStore('storage.json')

    def on_leave(self, *args):
        self.manager.ids.screen1.ids.lbl_car.text = self.txtinput_car.text
        self.manager.ids.screen1.ids.lb_car.text = self.cent_car.text


class ScreenManagement(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    MyApp().run()
