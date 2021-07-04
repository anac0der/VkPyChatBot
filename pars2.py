import bs4
import requests
import random


class Parse:
    def parse_top2(self, url):
        request = requests.get(url)
        b = bs4.BeautifulSoup(request.text, "html.parser")

        tables = b.find_all('div', attrs={'class': 'table'})
        bars = b.find_all('div', attrs={'class': 'bar2'})
        home_teams = []
        away_teams = []
        scores = []
        texts = []
        for table in tables:
            home_teams.append(table.find_all('td', attrs={'class': 'team2'}))
            away_teams.append(table.find_all('td', attrs={'class': 'team3'}))
            scores.append(table.find_all('td', attrs={'class': 'dash'}))
        for bar in bars:
            texts.append(bar.find('div', attrs={'class': 'bartext'}))
        result = ''
        for i in range(len(tables)):
            result += '\n'
            result += texts[i].text
            result += ':'
            result += '\n'
            result += '\n'
            for j in range(len(home_teams[i])):
                result += home_teams[i][j].text
                result += ' '
                result += scores[i][j].text
                result += ' '
                result += away_teams[i][j].text
                result += '\n'
        return result

    def parse_bets(self, url2):
        request = requests.get(url2)
        soup = bs4.BeautifulSoup(request.text, "html.parser")

        matches = soup.find_all('div', attrs={'class': 'live-match alt2 is-not-started'})
        while True:
            i = random.choice(matches)
            home_team = i.find('div', attrs={'class': 'team1'}).text
            away_team = i.find('div', attrs={'class': 'team2'}).text
            bets = i.find_all('a', attrs={'class': 'live-odds-value'})
            if len(bets)-1 < 1:
                continue
            else:
                rand = random.randint(0, len(bets)-1)
                coeff = bets[rand].text
                bet = ''
                if rand == 0:
                    bet = 'П1'
                if rand == 1:
                    bet = 'Ничья'
                if rand == 2:
                    bet = 'П2'
                result = ''
                result += home_team
                result += ' - '
                result += away_team
                result += '\n'
                result += 'Ставка:'
                result += bet
                result += ' '
                result += coeff
                break

        return result

    def parse_facts(self, url3):
        request = requests.get(url3)
        soup = bs4.BeautifulSoup(request.text, "html.parser")

        content = soup.find('div', attrs={'id': 'content'})
        fact = random.choice(content.find_all('p', attrs={'class': 'content'})).text

        return fact

    def parse_weather(self, city="москва"):
        url3 = city.replace(" ", "-")
        url4 = 'https://sinoptik.com.ru/погода-' + url3
        request = requests.get(url4)
        soup = bs4.BeautifulSoup(request.text, "html.parser")

        str1 = ""
        desc = soup.find('div', attrs={'class': 'weather__article_description-text'}).text
        cur = soup.find('div', attrs={'class': 'table__col current'})
        current_temp = cur.find('div', attrs={'class': 'table__temp'}).text
        str1 += "Текущая температура : {}\n{}".format(current_temp, desc)

        return str1

    def parse_problems(self, tupe="4"):
        types = {'4': 'https://math-ege.sdamgia.ru/test?theme=166&sort=',
                 '11': 'https://math-ege.sdamgia.ru/test?theme=88&sort=',
                 }
        sorts = ['', 'hardr', 'hard', 'fav', 'ids', 'idsr']
        url = types.get(tupe) + random.choice(sorts)

        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text, "html.parser")


        prob = random.choice(soup.find_all('div', attrs={'class': 'problem_container'}))
        problem = prob.find('div', attrs={'class': 'prob_maindiv'})
        text = problem.find('p', attrs={'class': 'left_margin'})
        sol = prob.find('div', attrs={'class': 'answer'})
        stroka = text.text.replace("\xad", "")

        return stroka, sol.text


