from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.label import Label

import threading
from Mexbot import Mexbot
from IcebergOrder import IcebergOrder
from MarketOrder import MarketOrder
from LimitOrder import LimitOrder


Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 10)
Config.set('graphics', 'top',  50)

Config.set('graphics', 'resizable', False)


Window.size = (200, 800)


class RootWidget(FloatLayout):
    order_alert = StringProperty()
    def __init__(self):
        super().__init__()
        self.order_alert = "Witaj przywoływaczu"
    
    spinner1 = Spinner(
        text='Pick order type',
        values=('Limit Order', 'Market Order', 'Scaled Order', 'Iceberg Order'),
        size_hint=(1, None),
        size=(200, 30),
        pos_hint={'x': 0, 'y': 0.5},
    )

    spinner2 = Spinner(
        text='XBTUSD',
        values=('XBTUSD', 'XBTJPY', 'ADAH19', 'BCHH19', 'EOSH19', 'ETHXBT', 'LTCH19', 'TRXH19', 'XRPH19', 'XBTKRW'),
        size_hint=(1, None),
        size=(200, 30),
        pos_hint={'x': 0, 'y': 0.7})

    def show_selected_pair(self, pair):
        print('Pair: ' + pair)
        #mex = Mexbot(pair)
        return pair

    def show_selected_value(self, orderType):

        content = GridLayout()
        input_number = TextInput(
            id='number',
            height='30',
            width='80',
            multiline='false',
            hint_text='Number',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 360)
        )

        input_price = TextInput(
            id='price',
            height='30',
            width='80',
            multiline='false',
            hint_text='Price',
            input_filter='int',
            size_hint=(None, None),
            pos=(100, 360)
        )

        input_total_amount = TextInput(
            id='total_amount',
            height='30',
            width='80',
            multiline='false',
            hint_text='Total',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 320)
        )

        input_order_count = TextInput(
            id='order_count',
            height='30',
            width='80',
            multiline='false',
            hint_text='Order count',
            input_filter='int',
            size_hint=(None, None),
            pos=(100, 320)
        )

        input_low_price = TextInput(
            id='price_low',
            height='30',
            width='80',
            multiline='false',
            hint_text='Low price',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 360)
        )

        input_high_price = TextInput(
            id='price_high',
            height='30',
            width='80',
            multiline='false',
            hint_text='High price',
            input_filter='int',
            size_hint=(None, None),
            pos=(100, 360)
        )

        input_variance_amount = TextInput(
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

        input_variance_price = TextInput(
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

        input_variance = TextInput(
            id='variance',
            height='30',
            width='80',
            multiline='false',
            hint_text='Variance',
            input_filter='int',
            size_hint=(None, None),
            pos=(10, 360)
        )

        popup_alert = Popup(title='',
                separator_height= 0,
                content=Label(text='Success!'),
                size_hint=(None, None), size=(150, 100))

        def buy(self):
            print("buy")
            print(input_variance.text)
            print(orderType)


            if (orderType == "Iceberg Order"):
                total_amount = int(input_total_amount.text)
                order_count = int(input_order_count.text)
                price = int(input_price.text)
                variance = int(input_variance.text)


                if(total_amount > 0 and order_count > 0 and price > 0 and variance > 0):
                    #total_amount, order_count, price, variance
                    #io = IcebergOrder(100000, 100, 123, 55)
                    order = IcebergOrder(total_amount, order_count, price, variance)
                    #result = mexbot.executeOrder(order)
                    popup_alert.open()
                    popup.dismiss()


            elif (orderType == "Market Order"):
                number = int(input_number.text)
                if(number > 0 and number):
                    order = MarketOrder(number)
                    #result = mexbot.executeOrder(order)
                    popup_alert.open()
                    popup.dismiss()

            elif (orderType == "Limit Order"):
                number = int(input_number.text)
                price = int(input_price.text)
                if(number > 0 and price > 0):
                    order = LimitOrder(number, price)
                    #result = mexbot.executeOrder(order)
                    popup_alert.open()
                    popup.dismiss()

        def sell(self):
            print("sell")
    
            if (orderType == "Iceberg Order"):
                total_amount = int(input_total_amount.text)
                total_amount = -total_amount
                order_count = int(input_order_count.text)
                price = int(input_price.text)
                variance = int(input_variance.text)


                if(total_amount < 0 and order_count > 0 and price > 0 and variance > 0):
                    #total_amount, order_count, price, variance
                    #io = IcebergOrder(100000, 100, 123, 55)
                    order = IcebergOrder(total_amount, order_count, price, variance)
                    #result = mexbot.executeOrder(order)
                    popup_alert.open()
                    popup.dismiss()


            elif (orderType == "Market Order"):
                number = int(input_number.text)
                number = -number
                if(number < 0):
                    order = MarketOrder(number)
                    #result = mexbot.executeOrder(order)
                    popup_alert.open()
                    popup.dismiss()

            elif (orderType == "Limit Order"):
                number = int(input_number.text)
                number = -number
                price = int(input_price.text)
                if(number < 0 and price > 0):
                    order = LimitOrder(number, price)
                    #result = mexbot.executeOrder(order)
                    popup_alert.open()
                    popup.dismiss()




    

        button_buy = Button(
            id='buy',
            font_size=10,
            text='Buy',
            pos=(10, 270),
            height=35,
            width=80,
            background_color = (0, 1, 0, 1),
            on_press = buy
        )

        button_sell = Button(
            id='sell',
            font_size=10,
            text='Sell',
            pos=(100, 270),
            height=35,
            width=80,
            background_color=(1, 0, 0, 1),
            on_press = sell
        )

        if(orderType == 'Limit Order'):
            content.add_widget(input_number)
            content.add_widget(input_price)
        elif (orderType == 'Market Order'):
            content.add_widget(input_number)
        elif(orderType == 'Scaled Order'):
            content.add_widget(input_total_amount)
            content.add_widget(input_order_count)
            content.add_widget(input_low_price)
            content.add_widget(input_high_price)
            content.add_widget(input_variance_amount)
            content.add_widget(input_variance_price)
        elif (orderType == 'Iceberg Order'):
            content.add_widget(input_price)
            content.add_widget(input_total_amount)
            content.add_widget(input_order_count)
            content.add_widget(input_variance)

        content.add_widget(button_buy)
        content.add_widget(button_sell)
        popup = Popup(title=orderType,
                      content=content,
                      size_hint=(None, None), size=(200, 300))

        print('Spinner: ' + orderType)
        popup.open()

    spinner1.bind(text=show_selected_value)
    spinner2.bind(text=show_selected_pair)


class UI(App):
    def build(self):
        root = RootWidget()
        root.add_widget(root.spinner1)
        root.add_widget(root.spinner2)
        return root


if __name__ == "__main__":
    app = UI()
    def newThread():
        app.run()

    thread = threading.Thread(target=newThread, args=())
    thread.start()
    
