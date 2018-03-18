#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileenconding=utf8 :

"""This scraper is made to get specific data from the web packtpub. It
finds the title, description and the list of contents and lessons (not
available in all books) of the daily free book and stores it in a text
file."""

import urllib2

import bs4


class Scraper(object):
    """The class of the scraper, containing all functions."""

    def get_web(self, url):
        """Gets and returns the html page of the specified link."""

        data = urllib2.urlopen(url)
        html = data.read()
        data.close()

        return html

    def run(self):
        """Uses the html code to find the desired content, which is the title,
        description and the overall lessons list. The raw data is then
        normalized and finally saved in a text file."""

        # Get web page
        html = self.get_web("https://www.packtpub.com/packt/offers/free-learning")
        # Parse
        soup = bs4.BeautifulSoup(html, "lxml")
        content = soup.find("div", "dotd-main-book-summary float-left")
        elements = content.find_all("div")
        # Title
        title = (elements[1].text.strip())
        # Description
        description = (elements[2].text.strip())
        # Learning list
        learning_raw = elements[3].find_all("li")
        learning = []
        for learns in learning_raw:
            learning.append(">" + learns.text.strip())

        # Write everything in a text file
        w_file = open("book_data.txt", "w")
        w_file.write(title.encode("ascii", "ignore").decode("ascii") + "\n")
        w_file.write(description.encode("ascii", "ignore").decode("ascii") + "\n")
        for learns in learning:
            w_file.write(learns.encode("ascii", "ignore").decode("ascii") + "\n")

        w_file.close()

if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
