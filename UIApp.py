from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 10)
Config.set('graphics', 'top',  50)

Config.set('graphics', 'resizable', False)


Window.size = (200, 800)


class RootWidget(FloatLayout):


    spinner1 = Spinner(
        text='Pick order type',
        values=('Limit Order', 'Market Order', 'Scaled Order', 'Iceberg Order'),
        size_hint=(1, None),
        size=(200, 30),
        pos_hint={'x': 0, 'y': 0.5},
    )

    spinner2 = Spinner(
        text='XBTUSD',
        values=('XBTETH', 'ETHUSD'),
        size_hint=(1, None),
        size=(200, 30),
        pos_hint={'x': 0, 'y': 0.7})

    def show_selected_value(spinner, orderType):
        content = GridLayout()
        input1 = TextInput(
            id='number',
            height='30',
            width='80',
            multiline='false',
            hint_text='Number',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 360)
        )

        input2 = TextInput(
            id='price',
            height='30',
            width='80',
            multiline='false',
            hint_text='Price',
            input_filter='int',
            size_hint=(None, None),
            pos=(100, 360)
        )

        input3 = TextInput(
            id='total_amount',
            height='30',
            width='80',
            multiline='false',
            hint_text='Total',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 320)
        )

        input4 = TextInput(
            id='order_amount',
            height='30',
            width='80',
            multiline='false',
            hint_text='Order',
            input_filter='int',
            size_hint=(None, None),
            pos=(100, 320)
        )

        input5 = TextInput(
            id='price_low',
            height='30',
            width='80',
            multiline='false',
            hint_text='Low price',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 360)
        )

        input6 = TextInput(
            id='price_high',
            height='30',
            width='80',
            multiline='false',
            hint_text='High price',
            input_filter='int',
            size_hint=(None, None),
            pos=(100, 360)
        )

        input7 = TextInput(
            id='amount_variance',
            height='30',
            width='80',
            multiline='false',
            hint_text='Variance_amount',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 400),
            font_size=10
        )

        input8 = TextInput(
            id='price_variance',
            height='30',
            width='80',
            multiline='false',
            hint_text='Variance_price',
            input_filter='int',
            size_hint=(None, None),
            pos=(100, 400),
            font_size=10
        )

        input9 = TextInput(
            id='variance',
            height='30',
            width='80',
            multiline='false',
            hint_text='Variance',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 360)
        )


        button1 = Button(
            id='buy',
            font_size=10,
            text='Buy',
            pos=(10, 270),
            height=35,
            width=80,
            background_color = (0, 1, 0, 1)
        )

        button2 = Button(
            id='sell',
            font_size=10,
            text='Sell',
            pos=(100, 270),
            height=35,
            width=80,
            background_color=(1, 0, 0, 1)
        )

        if(orderType == 'Limit Order'):
            content.add_widget(input1)
            content.add_widget(input2)
        elif (orderType == 'Market Order'):
            content.add_widget(input1)
        elif(orderType == 'Scaled Order'):
            content.add_widget(input3)
            content.add_widget(input4)
            content.add_widget(input5)
            content.add_widget(input6)
            content.add_widget(input7)
            content.add_widget(input8)
        elif (orderType == 'Iceberg Order'):
            content.add_widget(input2)
            content.add_widget(input3)
            content.add_widget(input4)
            content.add_widget(input9)

        content.add_widget(button1)
        content.add_widget(button2)
        popup = Popup(title=orderType,
                      content=content,
                      size_hint=(None, None), size=(200, 300))

        print('Spinner: ' + orderType)
        popup.open()
        button1.bind(on_press=popup.dismiss)
        button2.bind(on_press=popup.dismiss)

    spinner1.bind(text=show_selected_value)


class UI(App):
    def build(self):
        root = RootWidget()
        print(root.x)
        root.add_widget(root.spinner1)
        root.add_widget(root.spinner2)
        return root



if __name__ == "__main__":
    UI().run()
