import re
import requests
from bs4 import BeautifulSoup
import os.path
from os import path

classPrereqs = {}
tree_top = None

class Node:
    def __init__(self, data, operation=None):
        self.data = data
        # self.operation = operation
        # self.group = []
        self.parent = None
    #
    # def add_to_me(self, other_node):
    #     self.group.append(other_node)
    #     other_node.operation = self.operation
    #
    # def add_to_you(self, other_node):
    #     other_node.group.add_to_me(self)

    def link_parent(self, parent):
        self.parent = parent


def format_text(stri):
    stri = re.sub(" ? ?a? minimum grade of \\d.\\d in", "", stri)  # remove min grade
    stri = re.sub("( ?or)? ?(permission of instructor|Instructor permission) ?(or)? ?\\.?", "",
                  stri)  # remove instructor permissions
    stri = re.sub(",? (or)? (equivalent)[.,]?", "", stri)  # removes "or equivalent"
    stri = re.sub(";? ?(exposure) ?.+", "", stri)
    stri = re.sub(".+ ?(majors|major|minors|minor) ?(and|or)? ?(only)?[,.;]?", "",
                  stri)  # removes major/minor requirements
    stri = re.sub(" ?Offered: .*?\\.", "", stri)  # remove joint offers
    stri = re.sub(";? (recommended|Recommended):? .+", "", stri)  # removes recommended
    stri = re.sub("[.,;]?(</p>)", "", stri)  # removes paragraph closings
    stri = re.sub("( ?and either)", "either", stri)
    stri = re.sub(",? ?(and|or)? ?(graduate standing).+", "", stri)
    stri = re.sub(".+ ?(knowledge|calculus) ?.+", "", stri)  # removes prereq of knowledge
    stri = re.sub("(a score of) ?.+", "", stri)
    stri = re.sub(" ?(which may be taken concurrently) ?[.,]", "", stri)
    stri = re.sub("Either", "either", stri)
    # beautify
    stri = re.sub("[.?,!;] ?$", "", stri)
    stri = re.sub(" +", " ", stri)
    stri = re.sub(";", " and", stri)
    stri = re.sub(",", " or", stri)
    stri = re.sub(" or or", " or", stri)
    stri = re.sub(" and and", " and", stri)
    stri = re.sub("^ +", "", stri)
    return stri



def online_load():
    page = requests.get("https://www.cs.washington.edu/education/courses/")
    if page.status_code != 200:
        print("Status code [",page.status_code,"]")
        exit(1)

    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('div', class_='views-row')

    for i in range(len(rows)):
        row = rows[i]
        links = row.find_all('a')
        link = str(links[1])
        title = link[link.find(">")+1:link.find(": ")]
        rt = str(row)
        text = rt[rt.find("</span>")+12:rt.find("</a></span></div>")]
        psplit = text.split("Prerequisite:")
        if len(psplit) > 1:
            preqs = format_text(psplit[1].split(". ")[0])
            # print(title, preqs)
            classPrereqs[title] = preqs
        else:
            classPrereqs[title] = ""


def write_prereqs():
    print("NYI")


def offline_load():
    print("NYI")


def build_root(root_name):
    tree_top = Node("TOP")
    build_tree(root_name, tree_top)

def build_tree(class_name, parent_node):
    print(class_name)
    node = Node(class_name)
    node.link_parent(parent_node)
    if class_name in classPrereqs.keys():
        questioned = classPrereqs[class_name]
        questioned = re.sub(" ?(either|or|and) ?", "_", questioned)
        questioned = re.sub("_+", "_", questioned)
        questioned = re.sub("^_*", "", questioned)
        prereqs = questioned.split("_")
        for course in prereqs:
            build_tree(course, node)





hasPath = path.exists("ClassData/UW-Class-Dependency.txt")
if hasPath:
    offline_load()
else:
    online_load()
    build_root("CSE 311")
    write_prereqs()
#print (hasPath)