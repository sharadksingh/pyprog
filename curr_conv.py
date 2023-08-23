from forex_python.converter import CurrencyRates
import datetime

c = CurrencyRates()

print(c.get_rate('USD', 'INR'))
print(c.get_rate('GBP', 'INR'))
print(c.get_rate('EUR', 'INR'))
print(c.get_rate('JPY', 'INR'))
print(c.get_rate('RUB', 'INR'))
print(c.get_rate('AUD', 'INR'))
print(c.get_rate('CAD', 'INR'))


dt = datetime.datetime(2022, 12, 19, 13, 30)
print(c.get_rate('USD', 'INR', dt))

dt = datetime.datetime(2022, 12, 18, 13, 30)
print(c.get_rate('USD', 'INR', dt))

dt = datetime.datetime(2022, 12, 17, 13, 30)
print(c.get_rate('USD', 'INR', dt))

dt = datetime.datetime(2022, 12, 16, 13, 30)
print(c.get_rate('USD', 'INR', dt))

dt = datetime.datetime(2022, 12, 1, 13, 30)
print(c.get_rate('USD', 'INR', dt))


