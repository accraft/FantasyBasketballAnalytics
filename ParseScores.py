import os
import sys
import csv
from bs4 import BeautifulSoup

#Point of this program is to scrape webpage that displays fantasy bball results

#this function takes the webpage as input and returns 2 dimensional python list with the results
def scrape_scores(HTML_Page,header_row=False):
    line_string=""

    espn_page = BeautifulSoup(open(HTML_Page),'lxml')
    scoreboard_matchups = espn_page.find("div", {"id": "scoreboardMatchups"})

    results = [[]]
    header_reached = 0
    row_counter = 0
    matchup_counter = 0
    all_TR = scoreboard_matchups.find_all('tr')
    for tr in all_TR:
        if tr.has_attr('class'):  # necessary because trying to pull a class that doesn't exist causes an error
            if tr['class'][0] == 'tableSubHead' and header_reached == 0 and header_row==True:
                header_reached = 1
                td_counter = 0
                results[row_counter].append('Week Name') # adds the title of the matchup in the first column
                results[row_counter].append('Matchup Number')
                for th in tr.find_all('th'):
                    results[row_counter].append(th.text)

            if tr['class'][0] == 'linescoreTeamRow':
                if len(results[0]) > 1:
                    results.append([])
                    row_counter += 1
                results[row_counter].append(espn_page.find_all('h1')[1].text)
                results[row_counter].append(matchup_counter)
                for td in tr.find_all('td'):
                    if td.text:
                        results[row_counter].append(td.text)

            if tr['class'][
                0] == 'tableSubHead':  # need to add one to the matchup counter every time there is a table subhead
                matchup_counter += 1

    return results

#samplecall
#scrape_scores("C:\\Users\\accra_000\\PycharmProjects\\AnalyseBBallLeague\\JaVale Vindicated Scoreboard_ Matchup 11 (Dec 25 - 31) - ESPN.html")

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

        if a==1:
            output_list = scrape_scores(html_file_name,header_row=True)
        else:
            output_list = scrape_scores(html_file_name)
        with open(final_csv, 'a+') as final_file:
            for row in output_list:
                wr = csv.writer(final_file, quoting=csv.QUOTE_ALL, lineterminator='\n')
                wr.writerow(row)
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







