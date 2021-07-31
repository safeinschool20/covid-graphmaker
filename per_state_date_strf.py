import csv
import pandas as pd
from datetime import date
import shutil

statelist = list(['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'NYC', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'])

today = date.today()
dnow = today.strftime("%Y-%m-%d")

for state in statelist:

    document = ("  directory  /state_strf/temp_data_sorted_" + state + "_" + dnow + ".csv")

    # saving the csv into a new one while clipping the beginning part of the pandas read
    with open(document, newline='') as f:
        reader = csv.reader(f)
        df = list(reader)

    fileVariable = open(document, 'r+')
    fileVariable.truncate(0)
    fileVariable.close()

    with open(document, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(df)
        f.close()
    print(df)

    # reading the date column of the csv and converting to datetime format
    datereader = pd.read_csv(document)
    datereader['date_parsed'] = pd.to_datetime(datereader['submission_date'], format = "%m/%d/%Y")
    datereader.to_csv(document, index=False)

    df1 = pd.read_csv(document)
    sorted_df1 = df1.sort_values(by=["date_parsed"], ascending=True)
    sorted_df1.to_csv(document, index=False)

    # saving again
    shutil.copyfile(document, "  directory  /dateparsed/temp_data_sorted_" + state + ".csv")

