#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, asyncio
from PyQt5.QtGui import *
from PyQt5.QtCore import QUrl
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QTabWidget, QStatusBar, QToolBar, QLineEdit, QAction, QMainWindow, QApplication

# main window
class BossWindow(QMainWindow):
	'''constructor'''
	def __init__(self, init_url='https://pypi.org/project/bossweb/0.0.1/', *args, **kwargs):
		super(BossWindow, self).__init__(*args, **kwargs)
		self.tabs = QTabWidget() # tab widget
		self.tabs.setDocumentMode(True) # making document mode true
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick) # adding action when double clicked		
		self.tabs.currentChanged.connect(self.current_tab_changed) # adding action when tab is changed		
		self.tabs.setTabsClosable(True) # making tabs closeable		
		self.tabs.tabCloseRequested.connect(self.close_current_tab) # adding action when tab close is requested
		self.setCentralWidget(self.tabs) # making tabs as central widget
		self.status = QStatusBar() # creating a status bar
		self.setStatusBar(self.status) # setting status bar to the main window
		navtb = QToolBar("Navigation") # creating a tool bar for navigation
		self.addToolBar(navtb) # adding tool bar tot he main window
		back_btn = QAction("Back", self) # creating back action
		back_btn.setStatusTip("Back to previous page") # setting status tip
		# adding action to back button
		# making current tab to go back
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		navtb.addAction(back_btn) # adding this to the navigation tool bar
		# similarly adding next button
		next_btn = QAction("Forward", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)
		# similarly adding reload button
		reload_btn = QAction("Reload", self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)
		# creating home action
		home_btn = QAction("Home", self)
		home_btn.setStatusTip("Go home")
		# adding action to home button
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)
		navtb.addSeparator() # adding a separator
		self.urlbar = QLineEdit() # creating a line edit widget for URL
		self.urlbar.returnPressed.connect(self.navigate_to_url) # adding action to line edit when return key is pressed		
		navtb.addWidget(self.urlbar) # adding line edit to tool bar
		# similarly adding stop action
		stop_btn = QAction("Stop", self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)
		self.add_new_tab(QUrl(init_url), 'Homepage') # creating first tab
		self.show() # showing all the components
		self.setWindowTitle("BossWeb") # setting window title

	'''method for adding new tab'''
	def add_new_tab(self, qurl = None, label ="Blank"):
		if qurl is None: # if url is blank
			qurl = QUrl('http://www.google.com') # show bossweb homepage
		browser = QWebEngineView() # creating a QWebEngineView object
		browser.setUrl(qurl) # setting url to browser
		# setting tab index
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)
		# adding action to the browser when url is changed
		# update the url
		browser.urlChanged.connect(lambda qurl, browser = browser:
								self.update_urlbar(qurl, browser))
		# adding action to the browser when loading is finished
		# set the tab title
		browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.tabs.setTabText(i, browser.page().title()))

	'''when double clicked is pressed on tabs'''
	def tab_open_doubleclick(self, i):
		# checking index i.e
		# No tab under the click
		if i == -1:
			self.add_new_tab() # creating a new tab

	'''when tab is changed'''
	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url() # get the curl
		self.update_urlbar(qurl, self.tabs.currentWidget()) # update the url 
		self.update_title(self.tabs.currentWidget()) # update the title

	'''when tab is closed'''
	def close_current_tab(self, i):
		# if there is only one tab
		if self.tabs.count() < 2:
			return # do nothing
		self.tabs.removeTab(i) # else remove the tab

	'''method for updating the title'''
	def update_title(self, browser):
		# if signal is not from the current tab
		if browser != self.tabs.currentWidget():
			return # do nothing
		title = self.tabs.currentWidget().page().title() # get the page title
		self.setWindowTitle("% s - Geek PyQt5" % title) # set the window title

	'''action to go to home'''
	def navigate_home(self):
		# go to bossweb pypi page
		self.tabs.currentWidget().setUrl(QUrl("https://pypi.org/project/bossweb/0.0.1/"))

	'''method for navigate to url'''
	def navigate_to_url(self):
		# get the line edit text
		# convert it to QUrl object
		q = QUrl(self.urlbar.text())
		# if scheme is blank
		if q.scheme() == "":
			q.setScheme("http") # set the scheme to
		self.tabs.currentWidget().setUrl(q) # set the url

	'''method to update the url'''
	def update_urlbar(self, q, browser = None):
		# If this signal is not from the current tab, ignore
		if browser != self.tabs.currentWidget():
			return
		# set text to the url bar
		self.urlbar.setText(q.toString())
		# set cursor position
		self.urlbar.setCursorPosition(0)


def launchWindow(url=None):
    bossApp = QApplication(sys.argv) # create the PyQt5 application
    bossApp.setApplicationName("Hello World") # set name to the application
    if url: window = BossWindow(init_url=url)
    else: window = BossWindow() # create the BossWindow object
    sys.exit(bossApp.exec()) # main event loop


if __name__ == "__main__":
    server.run(debug=True, use_reloader=True)