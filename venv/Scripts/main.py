from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import sys
import time
from datetime import date
import pandas as pd

#############################
finviz_stock_list = []
finviz_web_page_url = 'https://finviz.com/screener.ashx?v=111&f=ta_pattern_channelup2&ft=4'
CSV_file_name = "Channel_Up_Stock_List_from_Finviz_"+ str(date.today()).replace('-','') + ".csv"

#############################
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="D:\\Downloads\\chromedriver_win32\\chromedriver.exe", options=chrome_options)
driver.get(finviz_web_page_url)

total_num_of_stocks = driver.find_elements_by_class_name("screener-pages")
total_page = int(total_num_of_stocks[-1].text)

for page_num in range(1,total_page+1):
    new_finviz_web_page_url = "https://finviz.com/screener.ashx?v=111&f=ta_pattern_channelup2&ft=4&r=" + str((page_num-1)*20+1)
    driver.get(new_finviz_web_page_url)

    cell = driver.find_elements_by_class_name("screener-link-primary")

    for i in range(len(cell)):
        finviz_stock_list.append(cell[i].text)

print("Stock List download completed")
#################################################

with open(CSV_file_name,"w+") as filehandle:
    filehandle.write("Stock Symbol"+"\n")
    for stocks in finviz_stock_list:
        filehandle.write(stocks + "\n")

df_stocks = pd.read_csv(CSV_file_name)
df_stocks["Stars in Guru"] = None

########################################
for i in range(len(df_stocks)):
    try:
        new_guru_web_page_url = "https://www.gurufocus.com/stock/" + df_stocks.at[i,"Stock Symbol"] + "/summary"
        driver.get(new_guru_web_page_url)

        total_star_element = driver.find_element_by_class_name("el-rate")

        number_of_stars_for_stock = total_star_element.get_attribute("aria-valuenow")

        df_stocks.at[i,"Stars in Gura"] = number_of_stars_for_stock

        print(str(i + 1) + " of " + str(len(df_stocks)) + " completed")
    except:
        print(str(df_stocks.at[i,"Stock Symbol"]) + " failed" )

df_stocks.to_csv(CSV_file_name, index=False)