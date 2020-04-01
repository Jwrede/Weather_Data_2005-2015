import pandas as pd
import matplotlib.pyplot as plt
import calendar

import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

def leaflet_plot_stations(hashid):
    '''
    _________________________________________________________________________________________________
    
    Plots the Longitude and Latitude of the weather stations that we take the weather data from.
    The input is a hashid that translates to the location you want to inspect.
    _________________________________________________________________________________________________

    '''
    df = pd.read_csv(r'C:\Users\Jonathan\Desktop\coursera\Data science\visualization ass1\data.csv')
    print(df.describe())
    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)
    
    plt.title("Longitude and Latitude of the underlying weather stations")
    
    plt.gca().spines["bottom"].set_visible(False)
    plt.gca().spines["right"].set_visible(False) 
    plt.gca().spines["left"].set_visible(False) 
    
    plt.show()
    
    return df

df = leaflet_plot_stations('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')

#This is a Dataset that contains the minimum and maximum daily temperature different stations have observed.
#The Dataset has the columns "ID", "Date", "Element" and "data_value", where the "ID" marks the
#ID of the station, the "Date" marks the Date at which the observation was made, the "Element" labels
#wether the given observation was a maximum or minimum temperature and the "Data_Value" contains its value.
df2 = pd.read_csv(r'C:\Users\Jonathan\Desktop\coursera\Data science\visualization ass1\data2.csv')

def toPivotTable():
    '''
    _________________________________________________________________________________________________
    
    Converts the dataset into a pivot table thats needed for the plotMinMaxTemp function.
    Returns a Dataframe with the dates as its columns and the station ID and the value label wether 
    an element is a max temperature or a min temperature.
    _________________________________________________________________________________________________

    '''
    df2.sort_values(["ID","Date"], inplace = True)

    data = df2.pivot_table(values = ["Data_Value"], columns = ["Date"], index = ["ID", "Element"])
    
    data.columns = data.columns.get_level_values(1)
    
    data /= 10
    
    #eliminates the leap days
    for i in range(2005, 2015):
        if f"{i}-02-29" in data.columns: 
            data.drop(f"{i}-02-29", axis = 1, inplace = True)
    
    return data

ye = toPivotTable()

def plotMinMaxTemp():
    '''
    _________________________________________________________________________________________________
    
    Plots two lines, a red one for the maximum temperatures over the years till 2014 and a blue one 
    for the minimum temperatures till 2014 and then shades the area in between.
    _________________________________________________________________________________________________

    '''
    data = toPivotTable()
    
    min_series = data.apply(lambda x: x.min())
    min_series_to_2014 = min_series.iloc[:3652]

    dates = min_series_to_2014.index.to_list()
    
    ax = plt.subplot(1,1,1)
    
    plt.title("Weather Data Ann Arbor, Michigan, United States")
    
    ax.plot(dates, min_series_to_2014, linewidth = 0.25)

    max_series = data.apply(lambda x: x.max())
    max_series_to_2014 = max_series.iloc[:3652]

    ax.plot(dates, max_series_to_2014, linewidth = 0.25)

    plt.xticks(dates[::365], rotation=45)
    
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False) 
    ax.spines["left"].set_visible(False) 
    
    ax.set_ylabel('Temperature ($^\circ$C)')
    
    ax.fill_between(range(len(dates)), min_series_to_2014, max_series_to_2014, facecolor = "green", alpha = 0.3)
    
    plt.show()

plotMinMaxTemp()

def compare_2015_to_past():
    '''
    _________________________________________________________________________________________________
    
    Plots two lines, a red one for the maximum temperatures for each day of the year gathered from
    the data from the years 2005 to 2014 and a blue one that does the same for the minimum temperature.
    Then it scatters the maximum and minimum temperatures of the year 2015 over the graph where the
    red points are the temperatures that were hotter than the red line and the blue points are the 
    temperatures that were colder than the blue line.
    _________________________________________________________________________________________________

    '''
    #uses the original Dataset not the toPivotTabel one
    data = df2.copy()
    
    data["Data_Value"] /= 10
    
    data["Date"] = pd.to_datetime(data["Date"])
    
    data["year"], data["month"], data["day"] = data["Date"].dt.year, data["Date"].dt.month, data["Date"].dt.day
    
    data_to_2015 = data[data["year"] != 2015]
    
    max_temp_till_2015 = data_to_2015.pivot_table(index=["month", "day"], values = ["Data_Value"], aggfunc = "max")
    min_temp_till_2015 = data_to_2015.pivot_table(index=["month", "day"], values = ["Data_Value"], aggfunc = "min")
    
    max_min_till_2015 = pd.merge(max_temp_till_2015, min_temp_till_2015, how = "outer", left_index = True, right_index = True)
    
    dates = ["" + str(i[1]) +"," + calendar.month_name[i[0]] for i in max_temp_till_2015.index]
    
    ax = plt.subplot(1,1,1)
    ax.plot(dates, max_temp_till_2015, linewidth = 0.5, c = "r")
    ax.plot(dates, min_temp_till_2015, linewidth = 0.5, c = "b")
        
    plt.xticks([i for i in dates if i[0:2] == str(1)+","], rotation = 45)
    
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False) 
    ax.spines["left"].set_visible(False) 
    
    ax.set_ylabel('Temperature ($^\circ$C)')
    
    ax.fill_between(range(len(dates)), min_temp_till_2015.iloc[:,0], max_temp_till_2015.iloc[:,0], facecolor = "green", alpha = 0.3)
    
    data_2015 = data_to_2015 = data[data["year"] == 2015]
    
    max_temp_2015 = data_2015.pivot_table(index=["month", "day"], values = ["Data_Value"], aggfunc = "max")
    min_temp_2015 = data_2015.pivot_table(index=["month", "day"], values = ["Data_Value"], aggfunc = "min")
    
    max_min_2015 = pd.merge(max_temp_2015, min_temp_2015, how = "outer", left_index = True, right_index = True)
    
    _ = pd.merge(max_min_till_2015, max_min_2015, how = "outer", left_index = True, right_index = True)
    
    max_xvalues_2015 = _.where(_.iloc[:,2] > _.iloc[:,0]).dropna()
    min_xvalues_2015 = _.where(_.iloc[:,3] < _.iloc[:,1]).dropna()
    
    dates_max_2015 = ["" + str(i[1]) +"," + calendar.month_name[i[0]] for i in max_xvalues_2015.index]
    dates_min_2015 = ["" + str(i[1]) +"," + calendar.month_name[i[0]] for i in min_xvalues_2015.index]
    
    plt.scatter(dates_max_2015, max_xvalues_2015.iloc[:, 2], s = 2, c = "r")
    plt.scatter(dates_min_2015, min_xvalues_2015.iloc[:, 3], s = 2,c = "b")
    
    plt.show()  