# CS122: Course Search Engine Part 1
#
# Austin Herrick & Camille Choe
#

import re
import util
import bs4
import queue
import json
import sys
import csv

INDEX_IGNORE = set(['a',  'also',  'an',  'and',  'are', 'as',  'at',  'be',
                    'but',  'by',  'course',  'for',  'from',  'how', 'i',
                    'ii',  'iii',  'in',  'include',  'is',  'not',  'of',
                    'on',  'or',  's',  'sequence',  'so',  'social',  'students',
                    'such',  'that',  'the',  'their',  'this',  'through',  'to',
                    'topics',  'units', 'we', 'were', 'which', 'will', 'with', 'yet'])

def go(num_pages_to_crawl, course_map_filename, index_filename):
    '''
    Crawl the college catalog and generates a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs: 
        CSV file of the index.
    '''

    starting_url = "http://www.classes.cs.uchicago.edu/archive/2015/winter/12200-1/new.collegecatalog.uchicago.edu/index.html"
    limiting_domain = "classes.cs.uchicago.edu"
    
    with open("course_map.json") as f:
        course_map = json.load(f)    

    index = crawler(starting_url, limiting_domain, 1000, course_map)

    # Creates the index to write the csv file
    csv_index = []
    for word in sorted(index.keys()):
        for course_identifier in index[word]:
            word_map = str(course_identifier) + "|" + word
            csv_index.append(word_map)
    
    # Write Data to File
    csv_file = open(index_filename,'w')
    writer = csv.writer(csv_file, delimiter = ',')
    for map_row in csv_index:
        writer.writerow([map_row])

    return csv_file

def crawler(starting_url, limiting_domain, max_visits, course_map):
    '''
    Produces the word index, by traversing all relevant sites

    Inputs:
        starting_url: The initial page from which to begin crawling
        limiting_domain: A domain which restricts valid urls
        max_visits: Max number of unique pages to visit before halting
        course_map: A dictionary which translates course codes

    Outputs:
        Finished word_index, containing our word:course mapping
    '''

    url_queue = queue.Queue()
    visited_sites = []
    word_index = {}

    # Convert starting URL to https
    starting_url = util.get_request(starting_url)
    starting_url = util.get_request_url(starting_url)
    url_queue.put(starting_url)

    # Tracks queued urls to avoid adding duplicates to the queue
    queued_urls = [starting_url]

    while not url_queue.empty():
        # Verify max_visits hasn't been exceeded
        if len(visited_sites) < max_visits:
            visit_url = url_queue.get()

            if visit_url not in visited_sites:
                # Pull request from a url and translate back to url
                # This ensures links are not redirects to invalid locations
                request_url = util.get_request(visit_url)
                visit_url = util.get_request_url(request_url)
                if util.is_url_ok_to_follow(visit_url, limiting_domain):
                    visited_sites.append(visit_url)
                    soup = cook_soup(request_url)
                    # If webpage is valid, return list of unique, valid urls
                    # Also updates our word_index, if relevant
                    if soup:
                        url_list = get_links(visit_url, limiting_domain, soup)
                        word_index = update_index(soup, word_index, course_map)

                    # For each url, append to queue if it is unique
                    for url in url_list:
                        if url not in visited_sites:
                            if url not in queued_urls:
                                queued_urls.append(url)
                                url_queue.put(url)
        else:
            break

    return word_index

def cook_soup(request_url):
    '''
    Creates a soup object from the request of a url.

    Inputs:
        request_url: A request return from a given url_list

    Outputs:
        A soup file
    '''

    html = util.read_request(request_url)
    if html:
        soup = bs4.BeautifulSoup(html, "html5")
        return soup

def get_links(url, limiting_domain, soup):
    '''
    Generates a list of all unique, valid urls found on a page

    Inputs:
        url: The page to search for links 
        limiting_domain: A domain which restricts valid urls
        soup: A soup file for the given web page

    Outputs:
        A list of all unique, valid urls
    '''

    url_list = []
    a_tags = soup.find_all("a")
    
    for tag in a_tags:
        # Verify tag is a web link
        if tag.has_attr("href"):
            href_url = tag["href"]
            new_url = util.convert_if_relative_url(url, href_url)
            if new_url not in url_list:
                # Check if url is a valid web link
                if util.is_url_ok_to_follow(new_url, limiting_domain):
                    url_list.append(new_url)

    return url_list

def update_index(soup, word_index, course_map):
    '''
    Generates a list of all unique, valid urls found on a page

    Inputs:
        soup: The soup file for the given web page
        word_index: The current version of our word index
        course_map: A dictionary which translates course codes

    Outputs:
        word_index, updated with all any relevant additions
    '''

    course_main = soup.find_all("div", class_= "courseblock main")
    
    for course_tag in course_main:
        subsequences = util.find_sequence(course_tag)
        courses = []

        # Check for subsequences, and add them to courses if relevant
        subseq_desc = ''
        if subsequences:
            for subtext in course_tag.find_all('p', class_ = "courseblocktitle"):
                subseq_desc += subtext.text + ' '
            for subtext in course_tag.find_all('p', class_ = "courseblockdesc"):
                subseq_desc += subtext.text + ' '
            courses += subsequences

        else:
            courses += [course_tag]

        for course in courses:
            for child in course.children:
                if type(child) == bs4.element.Tag and child.has_attr("class"):
                    if child["class"] == ["courseblocktitle"]:
                        # Extract title of course, and construct/translate
                        # course code
                        title = child.text
                        code_1 = re.search("^[A-Z]{4}", title)
                        code_2 = re.search("[0-9]{5}", title)
                        code = code_1.group() + ' ' + code_2.group()
                        code = course_map[code]
                    
                    elif child["class"] == ["courseblockdesc"]:
                        # Pull description from course description,
                        # Update our word_index based on description and title
                        # words, including subsequence parent text
                        description = child.text
                        word_list = make_word_list(subseq_desc + ' ' + 
                            title + ' ' + description)
                        for word in word_list:
                            word_index.setdefault(word, [])
                            if code not in word_index[word]:
                                word_index[word].append(code)

    return word_index


def make_word_list(text):
    '''
    Helper function to generate all unique words from a text block

    Inputs:
        text: The text to from which to identify words

    Outputs:
        A list of all valid words appearing in the text
    '''
    lower_text = text.lower()
    word_list = []

    words = re.findall("[A-Za-z]\w*", lower_text)
    for word in words:
        if word not in INDEX_IGNORE:
            word_list.append(word)

    return word_list


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
