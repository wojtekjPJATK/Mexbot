from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.config import Config


from kivy.core.window import Window
Config.set('graphics', 'resizable', False)
Config.write()

Window.size = (200, 800)


class UI(App):
    def build(self):
        f = FloatLayout()
        f.add_widget(spinner1)
        f.add_widget(spinner2)
        return f

def show_selected_value(spinner, text):
    print('The spinner', spinner, 'have text', text)


if __name__ == "__main__":
    spinner1 = Spinner(
        text='Pick order type',
        values=('Order 1', 'Order 2', 'Order 3', 'Order 4'),
        size_hint=(1, None),
        size=(200, 30),
        pos_hint={'x': 0, 'y': 0.3})

    spinner2 = Spinner(
        text='XBTUSD',
        values=('XBTETH', 'ETHUSD'),
        size_hint=(1, None),
        size=(200, 30),
        pos_hint={'x': 0, 'y':  0.7})

    spinner1.bind(text=show_selected_value)
    spinner2.bind(text=show_selected_value)
    UI().run()


