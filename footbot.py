from pars2 import Parse
import bs4
import random
import requests
from schedule import *


class Bot(Parse):
    def __init__(self, user_id):
        print(f'\nСоздан бот,id пользователя: {user_id}')

        self.CURR_PROB = None
        self.CURR_PROB_TYPE = None
        self.CURR_ANSWER = None
        self.PREV_ANSWER = None
        self.RIGHT_PROBS = 0
        self.WRONG_PROBS = 0

        self._USER_ID = user_id

        self.RESOURCES = {
            "МАТЕМАТИКА":
            f'https://vk.cc/2mp7sV - сайт с крупнейшим в интернете набором вычислительных алгоритмов\n'
            f'https://vk.cc/L2Oms - построение графиков функций онлайн\n '
            f'https://vk.cc/9jrx1n - все формулы школьного курса математики и геометрии\n'
            f'https://vk.cc/1gQkHg - теория и практика для подготовки к олимпиадам и части С ЕГЭ\n'
            f'https://vk.cc/a95XDA - поиск числовой последовательности в числе Пи',

            "РУССКИЙ":
            f'https://vk.cc/58YmjE - задания ЕГЭ по русскому языку\n'
            f'https://vk.cc/cN1eO - один из самых известных справочных порталов по русскому языку\n'
            f'https://vk.cc/7O9ADk - анализ вашего текста и проверка на уникальность\n'
            f'https://vk.cc/ab2mKe - словарь смыслов русского языка\n'
            f'https://vk.cc/8VbiqO - ресурс с множеством полезных материалов для школьников\n',

            "ИНФОРМАТИКА":
            f'https://vk.cc/735DBG - решение задач по программированию с возможностью проверки в проверяющей системе\n'
            f'https://vk.cc/5CX86f - подготовка к ЕГЭ по информатике\n'
            f'https://vk.cc/1XPRBb - сайт автора школьного учебника по информатике\n'
            f'https://vk.cc/2ytdyh - "Проект Эйлера" - сайт с задачами на математику и программирование\n'
            f'https://vk.cc/95zZxP - ведущий в России портал о технологиях и IT\n'
            }



        self.DEFKEYWORDS = {

             "weather": ["weather"],
             "foot_results": ["get_res"],
             "curr_lesson": ["get_lesson"],
             "problems": ['return_problem', 'check_answer', "type_change"],
             "resources": ["resources"]

             }

        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = [["ПРИВЕТ", "ХАЙ", "Q", "КУ", "ЗДОРОВО", "ПРИВ"],
                          ["РЕЗУЛЬТАТЫ МАТЧЕЙ", "РЕЗЫ", "РЕЗУЛЬТАТЫ", "ФУТБОЛ"],
                          ["ЗАДАЧИ", "ЕГЭ", "ЗАДАЧА", "РЕШАТЬ"],
                          ["ПОКА", "ББ"],
                          ["ДАЙ ФАКТ", "ФАКТ"],
                          ["ПОГОДА"],
                          ["УРОК"],
                          ["САЙТЫ", "РЕСУРСЫ", "ССЫЛКИ"]]

        self.WELCOME_MESS = f'Привет, {self._USERNAME}!\n' \
            f'Перед тем как продолжить разговор со мной, ' \
            f'прочитай правила отправки сообщений, чтобы избежать недопониманий.' \
            f'' \
            f'\n Уже прочитал? Тогда погнали!'

        self.IS_WELCOME_MESS = False

        self._IDKCOMMANDS_NUM = 0

        self.URLS = ['https://www.futbol24.com/national/England/Premier-League/2019-2020/',
                     'https://www.futbol24.com/national/Spain/Primera-Division/2019-2020/',
                     'https://www.futbol24.com/national/Italy/Serie-A/2019-2020/',
                     'https://www.futbol24.com/national/Germany/Bundesliga/2019-2020/',
                     'https://www.futbol24.com/national/Russia/Premier-Liga/2019-2020/',
                     'https://www.futbol24.com/national/France/Ligue-1/2019-2020/',
                     'https://www.futbol24.com/national/Holland/Eredivisie/2019-2020/',
                     'http://muzey-factov.ru/tag/football',
                     'https://www.liveresult.ru/']

        self.LEAGUES = {self.URLS[0]: ['АПЛ', 'АНГЛИЯ'],
                        self.URLS[1]: ['ЛА ЛИГА', 'ИСПАНИЯ'],
                        self.URLS[2]: ['СЕРИЯ А', 'ИТАЛИЯ'],
                        self.URLS[3]: ['БУНДЕСЛИГА', 'ГЕРМАНИЯ', 'БУНДЕС'],
                        self.URLS[4]: ['РПЛ', 'РОССИЯ', 'РФПЛ'],
                        self.URLS[5]: ['ЛИГА 1', 'ФРАНЦИЯ'],
                        self.URLS[6]: ['ЭРЕДИВИЗИ', 'ЭРЕДИВИЗИЯ', 'ГОЛЛАНДИЯ', 'НИДЕРЛАНДЫ']
                        }

        self._IDKCOMMANDS = ["Не знаю о чем вы...",
                             "Меня такому еще не учили...",
                             "Повторите, я не расслышал",
                             "Может, вы неправильно написали? Я вас не понимаю",
                             "Не понимаю. Напишите моему создателю:@amsel228"]

        self.USER_INPUT = "read_command"

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = bs.find_all("title")[0].text

        return user_name.split()[0]

    @staticmethod
    def compare(string, array):
        for i in array:
            if string.upper() == i:
                return True
        return False

    def welcome_msg(self):
        self.IS_WELCOME_MESS = True
        return self.WELCOME_MESS

    def curr_lesson(self, message="11е"):
        if self.USER_INPUT == "read_command":
            self.USER_INPUT = "get_lesson"
            return "Введите ваш класс"
        elif self.USER_INPUT == "get_lesson":
            try:
                if CurrentLesson(message):
                    self.USER_INPUT = "read_command"
                    return f"Ваш следующий урок: {CurrentLesson(message)}"
                else:
                    self.USER_INPUT = "read_command"
                    return "У вас нет уроков"
            except TypeError:
                return "Проверьте ввод"

    def resources(self, message="математика"):
        if self.USER_INPUT == 'read_command':
            self.USER_INPUT = 'resources'
            return "Какая область науки вас интересует?"
        elif self.USER_INPUT == "resources":
            if self.RESOURCES.get(message.upper()):
                self.USER_INPUT = 'read_command'
                return self.RESOURCES.get(message.upper())
            else:
                return "Проверьте ввод"

    def foot_results(self, message="АПЛ"):
        if self.USER_INPUT == 'read_command':
            self.USER_INPUT = 'get_res'
            return "Выберите лигу"
        elif self.USER_INPUT == 'get_res':
            for i in range(len(self.URLS)):
                if self.compare(message, self.LEAGUES.get(self.URLS[i])):
                    self.USER_INPUT = 'read_command'
                    return self.parse_top2(self.URLS[i])

    def get_weather(self, message='москва'):
        if self.USER_INPUT == 'read_command':
            self.USER_INPUT = 'weather'
            return "Введите город"
        elif self.USER_INPUT == 'weather':
            try:
                self.USER_INPUT = 'read_command'
                return self.parse_weather(message.lower())
            except AttributeError:
                self.USER_INPUT = 'weather'
                return "Проверьте ввод!"

    def problems(self, message=""):
        if message.upper() == "ВЫЙТИ" or message.upper() == "ВСЕ":
            self.USER_INPUT = 'read_command'
            ans = "Статистика сессии: \nРешено верно: " + str(self.RIGHT_PROBS) + "\n"
            ans += "Решено неверно: " + str(self.WRONG_PROBS) + "\n" + "Вы вышли из режима решения задач"
            return ans

        if message.upper() == "СМЕНА":
            self.USER_INPUT = "type_change"
            return "Выберите новый тип задач"

        if self.USER_INPUT == 'read_command':
            self.RIGHT_PROBS = 0
            self.WRONG_PROBS = 0
            self.USER_INPUT = 'return_problem'
            return "Введите тип задачи"

        elif self.USER_INPUT == 'return_problem':
            self.CURR_PROB_TYPE = message
            try:
                self.USER_INPUT = 'check_answer'
                self.CURR_PROB = self.parse_problems(self.CURR_PROB_TYPE)
                self.CURR_ANSWER = self.CURR_PROB[1][7:]
                return self.CURR_PROB[0]
            except TypeError:
                self.USER_INPUT = 'return_problem'
                return "Проверьте ввод"

        elif self.USER_INPUT == 'check_answer':
            self.PREV_ANSWER = self.CURR_ANSWER
            self.CURR_PROB = self.parse_problems(self.CURR_PROB_TYPE)
            self.CURR_ANSWER = self.CURR_PROB[1][7:]
            if message == self.PREV_ANSWER:
                self.RIGHT_PROBS += 1
                return "Верно! "+"Ответ: " + self.PREV_ANSWER + "\n" + self.CURR_PROB[0]
            else:
                self.WRONG_PROBS += 1
                return "Неверно! " + "Ответ: " + self.PREV_ANSWER + "\n" + self.CURR_PROB[0]
        elif self.USER_INPUT == "type_change":
            self.CURR_PROB_TYPE = message
            self.USER_INPUT = "check_answer"
            self.CURR_PROB = self.parse_problems(self.CURR_PROB_TYPE)
            self.CURR_ANSWER = self.CURR_PROB[1]
            return self.CURR_PROB[0]

    def read_command(self, message):
        if self.compare(message, self._COMMANDS[0]):
            return f"Привет - привет,{self._USERNAME}!"
        elif message in ["😚", "😍", "😙", "😗", "😘", "❤"]:
            return random.choice(["&#128522;", "&#128540;", "&#128139;", "&#128563;"])

        elif message.upper() == "НАЧАТЬ" and not self.IS_WELCOME_MESS:
            return self.welcome_msg()

        elif self.compare(message, self._COMMANDS[1]):
            return self.foot_results()

        elif self.compare(message, self._COMMANDS[2]):
            return self.problems()

        elif self.compare(message, self._COMMANDS[3]):
            return f"Пока - пока, {self._USERNAME}!"

        elif self.compare(message, self._COMMANDS[4]):
            return self.parse_facts(self.URLS[-2])

        elif self.compare(message, self._COMMANDS[5]):
            return self.get_weather()

        elif self.compare(message, self._COMMANDS[6]):
            return self.curr_lesson(message)

        elif self.compare(message, self._COMMANDS[7]):
            return self.resources(message)
        else:
            if self._IDKCOMMANDS_NUM < 2:
                self._IDKCOMMANDS_NUM += 1
                return "Такой команды я пока что не знаю... Но вы можете написать моему создателю: @amsel228"
            elif self._IDKCOMMANDS_NUM == 2:
                self._IDKCOMMANDS_NUM += 1
                return "Либо я не слишком умен, либо вы очень плохо знаете русский!"
            elif self._IDKCOMMANDS_NUM == 3:
                self._IDKCOMMANDS_NUM += 1
                return "Не могу вас понять...Видимо мы не созданы друг для друга"
            else:
                return random.choice(self._IDKCOMMANDS)

    def update_screen(self, message):
        if self.USER_INPUT == "read_command":
            return self.read_command(message)
        elif self.USER_INPUT in self.DEFKEYWORDS.get("foot_results"):
            return self.foot_results(message)
        elif self.USER_INPUT in self.DEFKEYWORDS.get("weather"):
            return self.get_weather(message)
        elif self.USER_INPUT in self.DEFKEYWORDS.get("curr_lesson"):
            return self.curr_lesson(message)
        elif self.USER_INPUT in self.DEFKEYWORDS.get("problems"):
            return self.problems(message)
        elif self.USER_INPUT in self.DEFKEYWORDS.get("resources"):
            return self.resources(message)















