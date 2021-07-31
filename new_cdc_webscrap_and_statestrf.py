#"  directory  " is where you should insert your own directory locations


from selenium import webdriver
from time import sleep
from datetime import date
import shutil

import csv
import pandas as pd


#getting the file from the CDC website

url = "https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36"

def down_csv():
    driver = webdriver.Chrome(executable_path=r"  directory  ") #location for chromedriver
    driver.get("https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD")
    sleep(5)
    driver.close
down_csv()

today = date.today()
dnow = today.strftime("%Y-%m-%d")


#making new files to prepare for state strfing

orig = ("  directory  /United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv") #original csv file
dest1 = ("  directory  /United_States_COVID-19_Cases_and_Deaths_by_State_over_Time_downloaded_" + dnow + ".csv") #backup copy of orig; this file is intended to come up empty after running
dest2 = ("  directory  /WORKING_COPY_"  + dnow + ".csv") #extracted backup of dest1; this file should be complete

shutil.move(orig, dest1)

with open(dest1, newline='') as f:
    reader = csv.reader(f)
    df = list(reader)
fileVariable = open(dest1, 'r+')
fileVariable.truncate(0)
fileVariable.close()
with open(dest2, "w+", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(df)
    f.close()

    
#filtering the huge csv by state and making separate csv files for each

statelist = list(['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'NYC', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'])

for state in statelist:
    document = ("  directory  /state_strf/temp_data_sorted_" + state + "location" + dnow + ".csv") #
    fr = pd.read_csv(dest2)
    fr = fr.loc[fr['state'] == state]
    fr.to_csv(document, index=False)