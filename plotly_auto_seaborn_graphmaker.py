import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.express as px
from datetime import date
from itertools import cycle


statelist = list(['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'NYC', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'])

today = date.today()
dnow = today.strftime("%Y-%m-%d")

for state in statelist:
    source = ("  directory  /dateparsed/temp_data_sorted_" + state + ".csv")    #This gets the state strfed, date parsed and ordered csv file
    
    def graphmaker(maindata, mult):
        # maindata = case / death
        # mult = 0:total / 1:new / 2:rate

        # section-1. Naming.
        maindata = str(maindata)
        mult = int(mult)
        data_temp = pd.read_csv(source)         # pull the full csv

        multmaindata = (maindata + 's')

        if maindata == 'case':                  # defining the relevant data based on initial function input
            maindata = ('tot_' + multmaindata)
        elif maindata == 'death':
            maindata = ('tot_' + maindata)
        else:
            pass

        global data_main
        data_main = data_temp[[maindata]]       # getting the relevant data from the full
        #naming system for each int
        if mult ==1:
            ddiff = data_main.diff()                                                                    # Getting weekly average
            data_main = ddiff                                                                           # I GET IT this is horrible but hey it's easy
            yaxisname = ('New ' + str.title(multmaindata))
            titlename = ('COVID-19 New ' + str.title(multmaindata) + ', ' + state)                      # Title. self-explanatory.
            widthint = 5                                                                                # Line thickness
        elif mult ==2:
            ddiff = data_main.diff()
            ddiff = ddiff.diff()
            data_main = ddiff
            yaxisname = ('Rate of Increase of New ' + str.title(multmaindata))
            titlename = ('COVID-19 Rate of Change of New ' + str.title(multmaindata) + ', ' + state)
            widthint = 5
        else:
            yaxisname = ('Total Number of ' + str.title(multmaindata))
            titlename = ('COVID-19 Total ' + str.title(multmaindata) + ', ' + state)
            widthint = 15                                                                               # Thicker for total graphs
            pass
        
        # section-2. Date. date column to datetime and diff-7day-average if mult=1 or 2
        data_date = data_temp[['date_parsed']].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
        df_dd = pd.concat([data_main, data_date], axis=1, join='inner')
        df_dd.columns = [maindata, 'date']
        df_dd['diff_rolling_avg'] = df_dd[maindata].rolling( 7).mean()                                  # Rolling average per 1 week from diff added as column
        print(df_dd)

        # section-3. Max. finding the maximum value for each csv.
        maindatalist = list(maindata)
        maindatalist = ''.join(maindatalist)

        maxcolumn1 = df_dd[maindata].max()
        print(maxcolumn1)
        maxcolumn1 = int(maxcolumn1)
        
        maxcolumnid = df_dd[maindata].idxmax()
        print(maxcolumnid)
        maxcolumn2 = df_dd.iloc[maxcolumnid]['date']
        maxcolumn2 = str(maxcolumn2)
        
        # section-4. Graphing. pulling the graph out of thin air
            # I love well-documented libraries
            # Thank you Plotly
            # Refer to them for further details and how to personalize your graph
        if mult == 0:   #total. no diff.
            fig1 = px.line(df_dd, x = 'date', y = maindata, width=2560, height=1440, labels={'date':'Time', maindata:(yaxisname)})
            fig1.update_layout(title_text=(titlename), title_font_size=60, font_size=30, margin_t=200, margin_l=150, margin_b=100)
            fig1.update_traces(line=dict(color="red", width=widthint))                              # Thick red line
            fig1.update_layout(xaxis_range=['2020-01-01', '2021-08-01'])
            fig1.add_annotation(x=maxcolumn2, y=maxcolumn1,                                         # The words at the end of the graph line        # Data found in section-3
                        text=("Current: " + str(maxcolumn1) + " " + multmaindata),                                                                  # The actual text in the box
                        showarrow=False,                                                                                                            # No arrow from the box to the data point
                        bgcolor= "red",                                                                                                             # Text box color
                        yshift=10,                                                                                                                  # Cha cha real smooth (up)
                        xshift=-75)                                                                                                                 # Mooove to the left
            fig1.show()
            filetail = ("_total_" + multmaindata)                                                                                                   # Added into the name of the file
            oneuploc = ("total")                                                                                                                    # Name of folder containing these graphs in the multmaindata folder
        elif mult == 1 or 2:    #1=new, 2=rate
            fig1 = px.line(df_dd, x = 'date', y = [maindata, 'diff_rolling_avg'], width=2560, height=1440, labels={'date':'Time', maindata:(yaxisname)})
            fig1.update_layout(title_text=(titlename), title_font_size=60, font_size=30, margin_t=200, margin_l=150, margin_b=100)
            names = cycle([yaxisname, 'Weekly Average'])
            fig1.for_each_trace(lambda t:  t.update(name = next(names)))
            fig1.for_each_trace(
                lambda trace: trace.update(line=dict(color="red", width=widthint)) if trace.name == 'Weekly Average' else (),
                )
            fig1.update_layout(xaxis_range=['2020-01-01', '2021-08-01'])
            fig1.update_layout(legend_title_text='Legend')
            fig1.update_layout(xaxis_title='Date', yaxis_title=yaxisname)
            fig1.add_annotation(x=maxcolumn2, y=maxcolumn1,
                        text=("Maximum: " + str(maxcolumn1) + " " + multmaindata),
                        showarrow=False,
                        yshift=10)
            fig1.show()
            if mult == 1:
                filetail = ("_new_" + multmaindata)
                oneuploc = ("new")
            elif mult == 2:
                filetail = ("_rate_new_" + multmaindata)
                oneuploc = ("rate")
        newfile = ("  directory  /chart_results/" + multmaindata + "/" + oneuploc + "/2021_07_total_" + state + filetail + ".png")  # output
        
        import os
        if not os.path.exists(newfile):
            file1 = open(newfile, "w+")
            file1.close
        fig1.write_image(newfile)

    graphmaker('case', 0)
    graphmaker('case', 1)
    graphmaker('case', 2)
    graphmaker('death', 0)
    graphmaker('death', 1)
    graphmaker('death', 2)