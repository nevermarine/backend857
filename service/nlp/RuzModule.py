from datetime import date
import re
from dateutil.relativedelta import relativedelta
from service.ruz.ruz import Ruz
from validator.ActiveUser import CurrentUser
from dateutil.parser import parse
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
        return parse(request)

    def parse_question(self, request):
        if request.find("сегодня") != -1:
            time_now = date.today()
            return str(time_now).replace("-", ".")
        elif request.find("послезавтра") != -1:
            time_aftertomorrow = date.today() + relativedelta(days=+2)
            return str(time_aftertomorrow).replace("-", ".")
        elif request.find("завтра") != -1:
            time_tomorrow = date.today() + relativedelta(days=+1)
            return str(time_tomorrow).replace("-", ".")
        else:
            regex = r'(?:(\d{1,2}) (.+) (\d{4}))'
            match = re.search(regex, request, flags=re.IGNORECASE)
            if match is None:
                time_now = date.today()
                return str(time_now).replace("-", ".")
            return self.multiple_replace(match[1] + match[2] + match[3], self.replace_months)

    def get_data(self):
        self.schedule = Ruz.get_schedule_by_name_and_date(str(CurrentUser), self.date, CurrentUser.position)

    def read_data(self):
        if not CurrentUser:
            return 'для того чтобы я мог рассказать вам о расписании подойдите ко мне'
        if self.date==None:
            return 'я не понимаю на какую дату вы хотите узнать свое расписание'
        self.get_data()
        if not self.schedule:
            return 'Занятий нет'
        else:
            answer_ruz = ''
            for i in range(len(self.schedule)):
                if i!=len(self.schedule)-1:
                    answer_ruz = answer_ruz + 'с ' + self.schedule[i]['beginLesson'] + ' до '+ self.schedule[i]['endLesson'] + ' будет ' + self.schedule[i]['discipline'][:-5] + ', затем'
                else:
                    answer_ruz = answer_ruz + 'с ' + self.schedule[i]['beginLesson'] + ' до '+self.schedule[i]['endLesson'] + ' будет ' + self.schedule[i]['discipline'][:-5]
        return answer_ruz
