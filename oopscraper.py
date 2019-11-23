import requests
import pandas as pd
from bs4 import BeautifulSoup


class GetLiveScores():
    """
    Class: fetches football scores from livescores.com within
            a specified time interval
    """

    URL_ = "http://www.livescores.com/soccer/"

    def __init__(self, starttime, endtime, filename):
        self.starttime = starttime
        self.endtime = endtime
        self.filename = filename

    def prepare_dates(self):
        self.daterange = pd.date_range(
                            start=self.starttime,
                            end=self.endtime
                            ).astype(str)
        return self.daterange

    def save_to_excel(self):
        with pd.ExcelWriter(f"{self.filename}.xlsx") as writer:
            for i in range(len(self.prepare_dates())):
                date_i = self.prepare_dates()[i]
                footdates = f"{self.URL_}{date_i.split(' ')[0]}"
                webdata = requests.get(footdates)
                soup = BeautifulSoup(webdata.content, 'lxml')
                find_home_team = soup.findAll(class_='ply tright name')
                find_scores = soup.findAll(class_='sco')
                find_away_team = soup.findAll(class_='ply name')

                home_team = [date_i.text for date_i in find_home_team]
                scores = [date_i.text for date_i in find_scores]
                away_team = [date_i.text for date_i in find_away_team]
                df = pd.DataFrame({})
                df['Home Team'] = home_team
                df['Scores'] = scores
                df['Away Team'] = away_team
                df.to_excel(
                    writer,
                    index=False,
                    sheet_name=date_i.split(" ")[0]
                )


if __name__ == '__main__':
    GetLiveScores('9/1/2019', '9/20/2019', 'oopfootball').save_to_excel()
