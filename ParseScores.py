from bs4 import BeautifulSoup
LineString=""
FantasyBBallPage = 'C:\Users\\accra_000\Desktop\JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html'

CC_Data = BeautifulSoup(open(FantasyBBallPage),'lxml')
Header_TR = CC_Data.find("tr",class_="tableSubHead")
All_TR = CC_Data.find_all("tr",class_="linescoreTeamRow")





for TR in All_TR:
    All_TD = TR.find_all("td")
    for TD in All_TD:
        LineString = LineString + "," + TD.text
    print LineString
    LineString=""
quit()

