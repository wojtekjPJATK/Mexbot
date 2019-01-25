import random
import math
from LimitOrder import LimitOrder


class Cords:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ScaledOrder:
    def __init__(self, total_amount, order_count, price_low, price_high, amount_variance, price_variance, distribution):
        self.total_amount = int(total_amount)
        self.order_count = int(order_count)
        self.price_low = int(price_low)
        self.price_high = int(price_high)
        self.amount_variance = int(amount_variance)
        self.price_variance = int(price_variance)
        self.orders = []
        if type(distribution) is list:
            self.distribution = self.get_distribution(distribution)

        else:
            self.distribution = 1

        self.get_orders()

    def get_orders(self):
        order_size = self.total_amount / self.order_count
        sum = 0
        price_jump = (self.price_high - self.price_low) / \
            (self.order_count - 1)
        last_price = self.price_low
        for i in range(0, self.order_count):
            if i == 0:
                price = self.price_low

            elif i == self.order_count - 1:
                price = self.price_high

            else:
                price = last_price
                rng = random.randint(
                    0-self.price_variance, self.price_variance)
                variance = price_jump + rng
                price = math.floor(price + variance)

            size = order_size * (self.distribution[i].y / 100)
            rng = random.randint(0 - self.amount_variance,
                                 self.amount_variance)
            size += size * (rng / 100)
            size = math.ceil(size)
            sum += size
            last_price = price
            self.orders.append(LimitOrder(size, price))

        dif = self.total_amount - sum
        while dif > 0:
            chips = dif / self.order_count
            if chips > dif:
                chips = dif
            for i in range(0, self.order_count):
                amount = math.ceil(chips * (self.distribution[i].y / 100))
                self.orders[i].amount += amount
                sum += amount
                if sum >= self.total_amount:
                    break

            dif = self.total_amount - sum

    def get_distribution(self, distribution):
        distribution_cords = []
        order_cords = []
        for i in range(0, 5):
            distribution_cords.append(Cords(i * 25, distribution[i]))

        for i in range(0, self.order_count):
            for j in range(0, 5):
                if distribution_cords[j].x > i * (100 / self.order_count):
                    start = distribution_cords[j - 1]
                    end = distribution_cords[j]
                    break

            order_x = i * (100 / (self.order_count - 1))
            # y=(((yB-yA)(x-xA))/(xB-xA))+yA
            order_y = (((end.y - start.y) * (order_x - start.x)) /
                       (end.x - start.x)) + start.y
            order_cords.append(Cords(order_x, order_y))

        return order_cords
