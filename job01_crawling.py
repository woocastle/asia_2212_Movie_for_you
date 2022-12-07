from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchFrameException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?year=2022&page=1'

