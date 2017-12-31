#Point of this program is to scrape webpage that displays fantasy bball results
def scrapeScores(HTML_Page):
    from bs4 import BeautifulSoup
    LineString=""
    FantasyBBallPage = HTML_Page

    CC_Data = BeautifulSoup(open(FantasyBBallPage),'lxml')
    Header_TR = CC_Data.find("tr",class_="tableSubHead")
    All_TR = CC_Data.find_all("tr",class_="linescoreTeamRow")

    #first add headers
    Header_TH = Header_TR.find_all("th")
    for TD in Header_TH:
        LineString = LineString + "," + TD.text
    CombinedResults = LineString
    LineString=""

    #now populate the scores for the given week
    for TR in All_TR:
        All_TD = TR.find_all("td")
        for TD in All_TD:
            LineString = LineString + "," + TD.text
        CombinedResults = CombinedResults + "\n" + LineString.replace(",,",",")
        LineString=""


    return CombinedResults;

#sample call below
print scrapeScores('C:\Users\\accra_000\Desktop\JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html')

