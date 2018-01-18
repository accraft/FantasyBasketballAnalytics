import os
import sys
from bs4 import BeautifulSoup

#Point of this program is to scrape webpage that displays fantasy bball results
def scrape_scores(HTML_Page):
    line_string=""

    CC_Data = BeautifulSoup(open(HTML_Page),'lxml')
    header_TR = CC_Data.find("tr",class_="tableSubHead")
    all_TR = CC_Data.find_all("tr",class_="linescoreTeamRow")

    #first add headers
    header_TR = header_TR.find_all("th")
    for TD in header_TR:
        line_string = line_string + "," + TD.text
    combined_results = line_string + "\n"
    line_string=""

    #now populate the scores for the given week
    for TR in all_TR:
        all_TD = TR.find_all("td")
        line_string = CC_Data.find_all('h1')[1].text #adds the title of the matchup in the first column
        for TD in all_TD:
            line_string = line_string + "," + TD.text
        combined_results = combined_results + line_string.replace(",,",",")  + "\n"
        line_string=""



    return combined_results
#samplecall
#scrape_scores("C:\\Users\\accra_000\\PycharmProjects\\AnalyseBBallLeague\\JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html")

#CC_Data = BeautifulSoup(open("C:\\Users\\accra_000\\PycharmProjects\\AnalyseBBallLeague\\JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html"), 'lxml')

#Below code requires the browsercookie package and a reasonably up to date version of sqlite3
#create new function, will take 2 arguments: URL of the site (required), UseChromeCookies (optional, TRUE if you want to use cookies from your chrome browser)
#will return a string
def pull_page(URL,use_chrome_cookies=False):
    #type: (str, bool) -> str
    import urllib2
    from bs4 import BeautifulSoup
    
    if use_chrome_cookies==True:
        import browsercookie
        br = browsercookie.chrome()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(br))
        page = opener.open(URL)
    else:
        page = urllib2.urlopen(URL)
    return page.read()

#sample call
#PullPage('http://games.espn.com/fba/scoreboard?leagueId=73636&matchupPeriodId=12',UseChromeCookies=True)

#below code ties it all together,
def main(weeks,final_csv):
    a=1
    while a <= weeks:
        html_file_contents = pull_page('http://games.espn.com/fba/scoreboard?leagueId=73636&matchupPeriodId='+str(a),use_chrome_cookies=True)
        html_file_name = 'matchup' + str(a) + '.html'
        text_file = open('matchup' + str(a) + '.html', "w+")
        text_file.write(html_file_contents)
        text_file.close()

        final_file = open(final_csv,'a+')
        final_file.write(scrape_scores(html_file_name)+ "\n")
        final_file.close()
        print "Week " , a , " parsed."
        a = a + 1

#main pulls all 16 weeks
if __name__ == '__main__':
    main(16, 'C:\\Users\\accra_000\\PycharmProjects\\AnalyseBBallLeague\\all_scores.csv')







#sample call below
# def main():
#     path_to_script = os.path.realpath(__file__)
#     script_directory = os.path.dirname(path_to_script)
#
#     #sample html file already downloaded
#     full_test_file_path = os.path.join(script_directory, 'JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html')
#     print scrape_scores(full_test_file_path)
