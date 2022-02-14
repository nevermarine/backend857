from dateutil.parser import parse
from datetime import datetime, date
import re
from dateutil.relativedelta import relativedelta
from service.ruz.ruz import Ruz
from validator.ActiveUser import CurrentUser
class RUZ:
  def __init__(self, quest):
    self.date = self.parse_question(quest)
    self.replace_months = {
      "января": "january",
      "февраля": "february",
      "марта": "march",
      "апреля": "april",
      "мая": "may",
      "июня": "june",
      "июля": "july",
      "августа": "august",
      "сентября": "september",
      "октября": "october",
      "ноября": "november",
      "декабря": "december"
  }

  def multiple_replace(self, request, replace_values):
      for i, j in replace_values.items():
          if request.find(i) != -1:
              request = request.replace(i, j)
              break
      #print(parse(request))
      return parse(request)

  def parse_question(self, request):
      if request.find("расписание") != -1 and request.find("сегодня") != -1:
          time_now = date.today()
          return str(time_now).replace("-",".")
      elif request.find("расписание") != -1 and request.find("послезавтра") != -1:
          time_aftertomorrow = date.today() + relativedelta(days=+2)
          return str(time_aftertomorrow).replace("-",".")
      elif request.find("расписание") != -1 and request.find("завтра") != -1:
          time_tomorrow = date.today() + relativedelta(days=+1)
          return str(time_tomorrow).replace("-",".")
      else:
          regex = r'какое расписание будет (?:(\d{1,2}) (.+) (\d{4}))'
          match = re.search(regex, request, flags=re.IGNORECASE)
          if match is None:
              return None
          return self.multiple_replace(match[1] + match[2] + match[3], self.replace_months)

  def get_data(self):
    #print('здесь мы должны получить данные в формате json, я просто написала сама')
    self.schedule = Ruz.get_schedule_by_name_and_date(str(CurrentUser), self.date)

  def read_data(self):
    if self.date==None:
      return None
    self.get_data()
    if not self.schedule:
      return 'Занятий нет'
    else:
      answer_ruz = ''
      for i in range(len(self.schedule)):
          if i!=len(self.schedule)-1:
              answer_ruz = answer_ruz + 'с ' + self.schedule[i]['beginLesson'] + ' до '+ self.schedule[i]['endLesson'] + ' будет ' + self.schedule[i]['discipline'][:-5] + ', затем'
          else:
              answer_ruz= answer_ruz + 'с ' + self.schedule[i]['beginLesson'] + ' до '+self.schedule[i]['endLesson'] + ' будет ' + self.schedule[i]['discipline'][:-5]
    return answer_ruz
