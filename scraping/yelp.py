
import requests


import re
import util
import bs4
import queue
import json
import sys
import csv

url = "https://www.yelp.com/biz/alinea-chicago?osq=Restaurants"

request = requests.get(url)
encoding = request.encoding
html = request.text.encode(encoding)
soup = bs4.BeautifulSoup(html, "html5lib")
aggregateRating = soup.find_all("div", itemprop="aggregateRating")
aggregateRating_tag = aggregateRating[0]
meta = aggregateRating_tag.find_all("meta")
meta_tag = meta[0]


        
def extract_links(page, limiting_domain, course_map_filename, data):
    
    queue = data["queue"]
    links_visited = data["links visited"]
    index = data['index']

    
    if util.is_url_ok_to_follow(page, limiting_domain) and page not in links_visited:
        request_page = util.get_request(page)
        if request_page is None:
            return data
        html_page = util.read_request(request_page)
        url = util.get_request_url(request_page)
        new_index= create_index_entry(html_page, course_map_filename, index)
        index = new_index

        
        if util.is_url_ok_to_follow(url, limiting_domain) and url not in links_visited:
            links_visited.append(url)
            if url != page:
                links_visited.append(page)
            soup = bs4.BeautifulSoup(html_page, "html5lib")
            links = soup.find_all("a")

            for tag in links:
                i = links.index(tag)
                if tag.has_attr("href"):
                    links[i] = tag["href"]
                else:
                    links[i] = "link"

            for link in links:
                link = util.remove_fragment(link)
                if util.is_absolute_url(link) == False:
                    link = util.convert_if_relative_url(page, link)
                if util.is_url_ok_to_follow(link, limiting_domain) and link not in links_visited and link not in queue:
                    queue.append(link)
    data = {"queue": queue, "links visited": links_visited, "index": index}
    return data



def create_index_entry(html, course_map_filename, index):
    '''
    Creates appropriate entries given html of a webpage that will be entered into 
    the index CSV file later. 

    Inputs:
        html: the html to pull entries from
        course_map_filename: a JSON file
        index: an ongoing list of entries into Indexer, added to under this function

    Outputs: 
        Index: an ongoing list of entries containing the index
    '''
    
    soup = bs4.BeautifulSoup(html, "html5lib")
    main = soup.find_all("div", class_="courseblock main")
    json_data=open(course_map_filename).read()
    course_map = json.loads(json_data)

    for course in main:
        pattern = r'([A-Z]{4})(.)([0-9]{5})'
        seq_list = util.find_sequence(course)
        seq_list.append(course)
        code_list = []
        main_title_tags = course.find_all("p", class_="courseblocktitle")
        t = main_title_tags[0]
        main_title = t.text

        for seq in seq_list:
            title = seq.find_all("p", class_="courseblocktitle")
            t = title[0]
            course_title = t.text
        
            match = re.findall(pattern, course_title)
            title = (str(match[0][0])+" "+str(match[0][2]))
            course_code = course_map[title]
            if course_code not in code_list:
                code_list.append(course_code)
        
        desc = course.find_all("p", class_="courseblockdesc")
        t = desc[0]
        desc = t.text + " " + str(main_title)
        word = r'([A-Za-z][A-Za-z0-9]+)'
        match = re.findall(word, desc)

        for word in match:
            word = word.lower()
            if word not in INDEX_IGNORE:
                for code in code_list:
                    entry = (word, code)
                    if entry not in index:
                        index.append(entry)     
    return index
    
def write_into_csv(index_filename, index):
    '''
    Writes a given index into a csv file of name index_filename

    Inputs:
        index_filename: the name for the CSV of the index.
        index: list of entries into the Index

    Outputs: 
        CSV file of the index index.
    '''
    index.sort()
 
    with open(index_filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in index:
            entry = str(row[1]) + "|" + row[0]
            entry = [str(entry)]
            writer.writerow(entry)







if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 1000
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)    
        sys.exit(0)


go(num_pages_to_crawl, course_map_filename, index_filename)




