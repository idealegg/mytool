# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import pprint

find_key = None


class BookMarks:
    def __init__(self, html_file):
        self.html_file = html_file
        self.handle = None
        self.lines = None
        self.soup = None
        #self.fix_lines = ['<DT><A HREF=', '</DL><p>']
        self.pattern = re.compile(r'<DT><A HREF=|</DL><p>') #|</H3>
        self.href_map = {}

    def get_lines(self):
        self.handle = open(self.html_file, 'r')
        self.lines = self.handle.readlines()
        self.handle.close()

    def get_soup(self):
        self.soup = BeautifulSoup(''.join(self.lines), 'lxml', from_encoding='UTF-8')

    def add_dt_tag(self, str):
        return "".join([str, '</DT>'])

    def delete_dt_tag(self, str):
        return str[0:str.rindex('</DT>')]

    def fix_html_format(self):
        last_modified_index = 0
        for index in range(len(self.lines)):
            if re.search(self.pattern, self.lines[index]):
                last_modified_index = index
                self.lines[index] = self.add_dt_tag(self.lines[index])
        # the last line can not be fixed
        self.lines[last_modified_index] = self.delete_dt_tag(self.lines[last_modified_index])

    def create_instance(self):
        self.get_lines()
        self.fix_html_format()
        self.get_soup()
        return self.soup

    def print_html(self):
        if self.soup:
            print self.soup.prettify(encoding='UTF-8')
        else:
            print "the item is none"

    def get_all_href(self):
        if not self.href_map:
            for item in soup.find_all('a'):
                self.href_map[item['href']] = item
                for tmp_parent in item.parents:
                    if tmp_parent.h3 and tmp_parent.h3.string != u'书签栏':
                        self.href_map[tmp_parent.h3.string] = tmp_parent
        return self.href_map

    @staticmethod
    def get_dl_tag_with_text(tag):
        global find_key
        return tag.name == 'dl' and tag.h3 and tag.h3.string == find_key

    @staticmethod
    def get_all_child_dl_tag(tag):
        global find_key
        flag = False
        if tag.name != 'dl':
            return flag
        for tmp_parent in tag.parents:
            #if tag.name != 'dl' tmp_parent.h3 and tmp_parent.h3.string != u'书签栏':
            pass
        while tag.name == 'dl' and tag.parent.h3 and tag.parent.h3.string == find_key:
            pass

    def insert_new_item(self, key, o_bm):
        global find_key
        # -- find the item in source book mark
        tmp_list = o_bm.soup.find_all('a', href=key)
        if len(tmp_list) > 1:
            print "Warning, the key [%s] has 2 book marks.\n" % key
        item = tmp_list[0]

        # -- find the existed parent content in target book mark
        tmp_parent = item.parent
        while tmp_parent.h3 and tmp_parent.h3.string not in self.href_map:
            item = tmp_parent.h3.string
            tmp_parent = tmp_parent.parent

        # -- get the parent item
        find_key = tmp_parent.h3.string
        tmp_list2 = self.soup.find_all(BookMarks.get_dl_tag_with_text)
        target_item = tmp_list2[0]

        # -- add the new item to target item
        target_item.append(o_bm.get_all_href()[item])

        # -- update href map
        key_list = item.find_all('a')
        key_list.extend(item.find_all(BookMarks.get_dl_tag_with_text))
        self.href_map[item] = o_bm.get_all_href()[item]

    def merge(self, o_bm):
        for (key, value) in o_bm.get_all_href():
            if key not in self.href_map:
                self.insert_new_item(key, o_bm)


if __name__ == '__main__':
    bm = BookMarks('bookmarks.html')
    soup = bm.create_instance()
    bm.print_html()
    #pprint.pprint(soup.find_all('a'))
    '''
    for item in soup.find_all('a'):
        parent = []
        #tmp_parent = item.parent
        #wh#ile tmp_parent:#or tmp_parent.string != u'书签栏':
        #    parent.insert(0, tmp_parent)
        #    if tmp_parent.h3:
        #        print tmp_parent.h3.string
        #    tmp_parent = tmp_parent.parent
        for tmp_parent in item.parents:
            if tmp_parent.h3 and tmp_parent.h3.string != u'书签栏':
                parent.insert(0, tmp_parent.h3.string)
            print tmp_parent.name
        pprint.pprint(parent)
        print len(parent)
        print item
        break
    '''



