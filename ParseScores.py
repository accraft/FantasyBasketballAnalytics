import os

#Point of this program is to scrape webpage that displays fantasy bball results
def scrape_scores(HTML_Page):
    from bs4 import BeautifulSoup
    line_string=""

    CC_Data = BeautifulSoup(open(HTML_Page),'lxml')
    header_TR = CC_Data.find("tr",class_="tableSubHead")
    all_TR = CC_Data.find_all("tr",class_="linescoreTeamRow")

    #first add headers
    header_TR = header_TR.find_all("th")
    for TD in header_TR:
        LineString = line_string + "," + TD.text
    combined_results = line_string
    line_string=""

    #now populate the scores for the given week
    for TR in all_TR:
        all_TD = TR.find_all("td")
        for TD in all_TD:
            line_string = line_string + "," + TD.text
        combined_results = combined_results + "\n" + line_string.replace(",,",",")
        line_string=""


    return combined_results

#sample call below 
def main():
    path_to_script = os.path.realpath(__file__)
    script_directory = os.path.dirname(path_to_script)

    #sample call below
    full_test_file_path = os.path.join(script_directory, 'JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html')
    print scrape_scores(full_test_file_path)

if __name__ == '__main__':
    main()


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

#below is a nice little utility to print all lines (within the top 40 lines) between the title tags of a BeautifulSoup object
def ReturnTitle(BS4_Object):
    i = 0
    p = -1
    for line in BS4_Object.prettify().split('\n'):
        i = i + 1
        if i <= 40:
            if 'title>' in line.lower():
                p = p * -1
            if p == 1:
                print i
                print line
        else: break

from bs4 import BeautifulSoup
ReturnTitle(BeautifulSoup(pull_page('http://games.espn.com/fba/scoreboard?leagueId=73636&matchupPeriodId=12',use_chrome_cookies=True),'lxml'))
    #JaVale Vindicated Scoreboard: Matchup 12 (Jan 1 - 7) -  ESPN
ReturnTitle(BeautifulSoup(pull_page('http://games.espn.com/fba/scoreboard?leagueId=73636&matchupPeriodId=12',use_chrome_cookies=False),'lxml'))
    # Log In -  ESPN


#not sure how I"m going to tie this together, the below code does NOT work because pull_page returns a string and scare_scores expects a file path.
scrape_scores(pull_page('http://games.espn.com/fba/scoreboard?leagueId=73636&matchupPeriodId=1',use_chrome_cookies=True))
#maybe adjust scrape_scores to accept a string?



