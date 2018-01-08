import os

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
def main():
    path_to_script = os.path.realpath(__file__)
    script_directory = os.path.dirname(path_to_script)

    #sample call below
    full_test_file_path = os.path.join(script_directory, 'JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html')
    print scrapeScores(full_test_file_path)

if __name__ == '__main__':
    main()


#Below code is not yet wrapped in a function, right now it just attempts to print the title 
#also requires the browsercookie package and a reasonable up to date version of sqlite3
#now define a function that pulls the hmtl content associated with a generic URL
import urllib2
from bs4 import BeautifulSoup
import browsercookie

#uncomment the below if you want to see the results of the page without including chrome cookies
#page = urllib2.urlopen('http://games.espn.com/fba/scoreboard?leagueId=73636&matchupPeriodId=12')

#below lines read in the URL with cookies
br = browsercookie.chrome()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(br))
page = opener.open('http://games.espn.com/fba/scoreboard?leagueId=73636&matchupPeriodId=12')

#loops through and only displayes lines between the Title HTML tags
page_bs = BeautifulSoup(page.read(),'lxml')
i = 0
p = -1
for line in page_bs.prettify().split('\n'):
    i = i + 1
    if i <= 40:
        if 'title>' in line.lower():
            p = p * -1
        if p == 1:
            print i
            print line
    else: break


