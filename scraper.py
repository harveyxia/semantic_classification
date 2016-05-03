import urllib2
from bs4 import BeautifulSoup

def run(n):
    url = "http://www.npr.org/sections/goatsandsoda/2016/05/02/467247415/should-the-u-s-reconsider-its-stand-on-foreign-aid-for-abortion-clinics"
    document_tag_dict = {}
    file_number = 1
    for i in xrange(n):
        try:
            res = urllib2.urlopen(url)
        except:
            print "error"
            continue
        if res.getcode() == 200:
            soup = BeautifulSoup(res.read(), 'html.parser')
            tags = parse_tags(soup)
            # tags exist for the article
            if tags is not None:
                text = parse_page(soup)
                document_tag_dict[file_number] = tags
                write_file(file_number, text)
                file_number += 1
            # navigate to the next article
            url = soup.find(id='prev_nav')['href']
    write_document_tag_dict(document_tag_dict)
    return document_tag_dict


# grab all p elements from id=storytext
def parse_page(soup):
    paragraphs = soup.find(id="storytext").findAll('p')
    p_text = []
    for p in paragraphs:
        for s in p.stripped_strings:
            p_text.append(s)
    return " ".join(p_text)

# return the tags for the article
def parse_tags(soup):
    tags = soup.findAll("div", { "class" : "tags" })
    if len(tags) == 0:
        return None
    else:
        tags = tags[0].text.strip().split("\n")
        return ",".join(tags)

def write_document_tag_dict(document_tag_dict):
    with open( "documents/tags.txt", "w" ) as output:
        for i in document_tag_dict:
            output.write(str(i) + ':' + document_tag_dict[i] + '\n')


def write_file(file_number, text):
    with open( "documents/" + str(file_number) + ".txt", "w" ) as output:
        output.write(text.encode('utf-8'))
