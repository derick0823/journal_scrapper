import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def get_issues():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    start_issue = 100
    end_issue = 112
    

    
    for now_issue in range(start_issue, end_issue):
        vol = 1
        has_next_vol = True

        while has_next_vol:
            print("===================")
            print(f"Issue: {now_issue}, Vol: {vol}")
            url_link = f"https://dl.sciencesocieties.org/publications/aj/tocs/{now_issue}/{vol}"
            resp = requests.get(url_link)
            soup = BeautifulSoup(resp.text, 'html.parser')

            checkboxes = soup.find_all("input",class_="article_checkbox")
            cnt = 0
            for ele in checkboxes:
                cnt+= 1
                parent_li = ele.parent
                authors = str(parent_li.contents[0])
                #print(authors.strip())
            
            print('total:',cnt)
            if cnt:
                print('寫入db')
                insert_sql = f"INSERT INTO agronomy_journal (`sn`,`issue`,`vol`,`url`,`html`,`is_complete`) VALUES ( NULL, '{now_issue}', '{vol}', '{url_link}', '', 0 );"
                print(insert_sql)
                cursor.execute(insert_sql)
                conn.commit()
                vol += 1
                with open( f"./aj_html/aj_{now_issue}_vol_{vol}.html","w", encoding="utf-8" ) as f:
                    f.write(resp.text)
            else:
                has_next_vol = False
                print('進入下個issue')

    conn.close()



def get_articles():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    issues_sql = "SELECT * FROM agronomy_journal WHERE is_complete = 0"
    cursor.execute(issues_sql)
    ret = cursor.fetchall()

    for row in ret:
        issue = row['issue']
        vol = row['vol']
        html_file = f"./aj_html/aj_{issue}_vol_{vol+1}.html"
        with open( html_file,"r", encoding="utf-8" ) as f:
            html_code = f.read()
            soup = BeautifulSoup(html_code, 'html.parser')

            #拿到年月資訊
            wrap_div = soup.find("div",class_="acsMarkLogicWrapper")
            first_p = wrap_div.find("p")
            yearmonth_str = first_p.get_text().strip().split(',')[1]
            #print(yearmonth_str.split(' '))
            month = yearmonth_str.split(' ')[1]
            year = yearmonth_str.split(' ')[2]
            #print(month)
            #利用checkbox定位出每則文章
            checkboxes = soup.find_all("input",class_="article_checkbox")
            cnt = 0
            for ele in checkboxes:

                
                parent_li = ele.parent
                #print(parent_li.contents)
                # s = 0
                # for x in parent_li.contents:
                #     print('number:',s)
                #     print(x)
                #     s += 1
                abstract_ele = parent_li.find("abstract")
                span_eles = parent_li.find_all("span")

                #print(abstract_ele)
                authors = str(parent_li.contents[0]) #作者
                author = authors.strip()
                title = span_eles[1].get_text().strip().replace('\n',' ')
                abstract = ""
                try:
                    abstract = abstract_ele.get_text()
                except:
                    c = parent_li.find(id=f"abstract{cnt}")
                    abstract = c.get_text()
                    #return False
                #print(abstract)
                doi = ""
                pattern = r'doi:(?P<doi_str>.*?)<br/>'
                r1 = re.compile(pattern)
                for bsTag in parent_li.contents:
                    text_pool = str(bsTag)
                    d2 = r1.search(text_pool) 
                    if d2:
                        doi = d2.group('doi_str')
                        break
                
                if not doi:
                    for bsTag in parent_li.contents:
                        text_pool = str(bsTag)
                        if 'doi:' in text_pool:
                            doi = text_pool.replace('doi:','')
                

                journal = "agronomy journal"
                print("-----------------------------------------------")
                print(year,month)
                print('Author:',author)
                print('Title:',title)
                print('Abstract:',abstract)
                print('doi:',doi)
                #insert_sql = f"INSERT INTO journal_articles (`sn`,`title`,`author`,`abstract`,`doi`,`issue`,`vol`,`year`,`month`,`journal`) VALUES ( NULL, '{title}', '{author}', '{abstract}', '{doi}', '{issue}', '{vol}', '{year}', '{month}', 'Agronomy Journal' );"
                insert_sql = f"INSERT INTO journal_articles (`sn`,`title`,`author`,`abstract`,`doi`,`issue`,`vol`,`year`,`month`,`journal`) VALUES ( NULL, ?, ?, ?, ?, ?, ?, ?, ?, 'Agronomy Journal' );"
                
                cursor.execute( insert_sql, (title,author,abstract,doi,issue,vol,year,month) )
                conn.commit()
                cnt+= 1

    conn.close()



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d














if __name__ == "__main__":
    #print('ok')
    #get_issues()
    get_articles()