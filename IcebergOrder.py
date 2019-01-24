import random
import math
from LimitOrder import LimitOrder


def orderCompare(order):
    return order.amount


class IcebergOrder:
    def __init__(self, total_amount, order_count, price, variance):
        self.total_amount = total_amount
        self.order_count = order_count
        self.price = price
        self.variance = variance/100
        self.orders = []
        self.get_orders()

    def get_orders(self):
        sum = 0
        size = 0
        for i in range(0, self.order_count):
            randomVariance = random.uniform(0 - self.variance, self.variance)
            size = (self.total_amount / self.order_count)
            size += randomVariance * size
            size = math.floor(size)
            sum += size
            self.orders.append(LimitOrder(size, self.price))

        dif = self.total_amount - sum

        while dif != 0:

            if dif > 0:
                self.orders.sort(key=orderCompare)
                self.orders[0].amount += 1
                dif -= 1
            elif dif < 0:
                self.orders.sort(key=orderCompare, reverse=True)
                self.orders[0].amount -= 1
                dif += 1

        sum = 0
        for order in self.orders:
            print("order size: " + str(format(order.amount, '.2f')) +
                  ", price: " + str(format(order.price, '.2f')))
            sum += order.amount

        print("sum: " + str(format(sum, '.2f')))


#total_amount, order_count, price, variance
#io = IcebergOrder(100000, 100, 123, 55)
#print(io)
