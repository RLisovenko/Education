print(0.1 + 0.2)
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))
print(Decimal(2) ** Decimal('0.5'))
#-----------------------------------
from fractions import Fraction  #дроби модель
print(Fraction(1,3))
#-----------------------------------
import datetime
curTime = datetime.datetime.now()
print(curTime)
#curTime = (curTime * 5) -1
print(curTime )
some_day = datetime.datetime(year=1975, month=3, day=10,hour=22,minute=50,second=9)
print(some_day)
some_day += datetime.timedelta(days=(48*365 + 48/4 ))
print(some_day)
some_day -= datetime.timedelta(days=(1*365  ))
print(some_day)
print(some_day.isoweekday())
print(some_day.weekday())
