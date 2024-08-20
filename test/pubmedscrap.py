from selenium import webdriver
from selenium.webdriver.common.by import By

# pmid = "32484110"
# articles = get_data(pmid)
#
# src = FindIt(pmid)
# print(src.url)
# print(src.reason)

url = "https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/32484110/"

driver = webdriver.Chrome()
driver.get(url)
title = driver.title
print(title)

page_source = driver.page_source
print(page_source)

driver.implicitly_wait(0.5)
# text_box = driver.find_element(by=By.NAME, value="Background")
# print(text_box)
pageSource = driver.find_element(by=By.TAG_NAME, value="body").text
print(pageSource)

