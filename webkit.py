#!/usr/bin/python
# -*- coding: utf -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class Webkit():
    '''an AppleWebKit browser implementation'''

    class Page(QWebPage):
        '''QWebPage implementation with a custom user agent string'''

        def userAgentForUrl(self, url):
            return "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.7; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2"

    class PostData(QByteArray):
        '''QByteArray implementation used when POSTing data from a dict'''

        def __init__(self, dict=None):
            QByteArray.__init__(self)

            if dict:
                i = len(dict)
                for key, value in dict.items():
                    i -= 1
                    if i > 0: div = '&'
                    self.append("%s=%s%s" % (key, value, div))

    def get(self, url):
        '''GET'''
        self.__run(url, 'GET')

    def post(self, url, dict=None):
        '''POST'''
        self.__run(url, 'POST', dict)

    def __run(self, url, method, dict=None):
        self.qapp = QApplication([])
        
        req = QNetworkRequest()
        req.setUrl(QUrl(url))

        self.qweb = QWebView()
        self.qweb.setPage(self.Page())
        self.qweb.loadFinished.connect(self.finished_loading)

        if method == 'POST': self.qweb.load(req, operation=4, body=self.PostData(dict))
        else: self.qweb.load(req)

        #self.qweb.show()
        self.qapp.exec_()

    def finished_loading(self):
        '''save the result after page has finished loading'''
        self.html_result = self.qweb.page().mainFrame().toHtml()
        self.qapp.quit()

if __name__ == '__main__':
    w = Webkit()

    # parse arguments
    dict = {}
    for argument in sys.argv:
        arg = argument.split('=')
        if len(arg) == 2:
            if arg[0] == 'form':
                if 'form' not in dict: dict['form'] = {}
                arg = arg[1].split(':')
                dict['form'][arg[0]] = arg[1]
            else:
                dict[arg[0]] = arg[1]
    for key in dict.keys(): exec(key + " = dict['" + key + "']")

    if method == 'POST':
        w.post(url, form)
    else:
        w.get(url)

    # output result
    print w.html_result