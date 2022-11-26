# %%
# Initialize Otter
import otter
grader = otter.Notebook("project2.ipynb")

# %% [markdown]
# # Project 2: Climate Change—Temperatures and Precipitation
# 
# In this project, you will investigate data on climate change, or the long-term shifts in temperatures and weather patterns!

# %%
# Run this cell to set up the notebook, but don't change it.
from datascience import *
import numpy as np

%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
np.set_printoptions(legacy='1.13')

import warnings
warnings.simplefilter('ignore')

# %% [markdown]
# ## Part 1: Temperatures

# %% [markdown]
# In the following analysis, we will investigate one of the 21st century's most prominent issues: climate change. While the details of climate science are beyond the scope of this course, we can start to learn about climate change just by analyzing public records of different cities' temperature and precipitation over time.
# 
# We will analyze a collection of historical daily temperature and precipitation measurements from weather stations in 210 U.S. cities. The dataset was compiled by Yuchuan Lai and David Dzombak [1]; a description of the data from the original authors and the data itself is available [here](https://kilthub.cmu.edu/articles/dataset/Compiled_daily_temperature_and_precipitation_data_for_the_U_S_cities/7890488). 
# 
# [1] Lai, Yuchuan; Dzombak, David (2019): Compiled historical daily temperature and precipitation data for selected 210 U.S. cities. Carnegie Mellon University. Dataset.

# %% [markdown]
# ### Part 1, Section 1: Cities

# %% [markdown]
# Run the following cell to load information about the `cities` and preview the first few rows.

# %%
cities = Table.read_table('city_info.csv', index_col=0)
cities.show(3)

# %% [markdown]
# The `cities` table has one row per weather station and the following columns:
# 
# 1. `"Name"`: The name of the US city
# 2. `"ID"`: The unique identifier for the US city
# 3. `"Lat"`: The latitude of the US city (measured in degrees of latitude)
# 4. `"Lon"`: The longitude of the US city (measured in degrees of longitude)
# 4. `"Stn.Name"`: The name of the weather station in which the data was collected
# 5. `"Stn.stDate"`: A string representing the date of the first recording at that particular station
# 6. `"Stn.edDate"`: A string representing the date of the last recording at that particular station
# 
# The data lists the weather stations at which temperature and precipitation data were collected. Note that although some cities have multiple weather stations, only one is collecting data for that city at any given point in time. Thus, we are able to just focus on the cities themselves.

# %% [markdown]
# a scatter plot that plots the latitude and longitude of every city in the `cities` table so that the result places northern cities at the top and western cities at the left.
# 

# %%
cities.scatter("Lon","Lat")

# %% [markdown]
# <!-- END QUESTION -->
# 
# 
# 
# These cities are all within the continental U.S., and so the general shape of the U.S. should be visible in your plot. The shape will appear distorted compared to most maps for two reasons: the scatter plot is square even though the U.S. is wider than it is tall, and this scatter plot is an [equirectangular projection](https://en.wikipedia.org/wiki/Equirectangular_projection) of the spherical Earth. A geographical map of the same data uses the common [Pseudo-Mercator projection](https://en.wikipedia.org/wiki/Web_Mercator_projection).

# %%
# Just run this cell
Marker.map_table(cities.select('Lat', 'Lon', 'Name').relabeled('Name', 'labels'))

# %% [markdown]
# Assign `num_unique_cities` to the number of unique cities that appear in the `cities` table.

# %%
num_unique_cites = cities.group("Name").num_rows

# Do not change this line
print(f"There are {num_unique_cites} unique cities that appear within our dataset.")

# %%
grader.check("q1_1_3")

# %% [markdown]
# In order to investigate further, it will be helpful to determine what region of the United States each city was located in: Northeast, Northwest, Southeast, or Southwest. For our purposes, we will be using the following geographical boundaries:
# 
# <img src= "usa_coordinates.png" alt="USA Coordinate Map" width="600"/>
# 
# 1. A station is located in the `"Northeast"` region if its latitude is above or equal to 40 degrees and its longtitude is greater than or equal to -100 degrees.
# 2. A station is located in the `"Northwest"` region if its latitude is above or equal to 40 degrees and its longtitude is less than -100 degrees.
# 3. A station is located in the `"Southeast"` region if its latitude is below 40 degrees and its longtitude is greater than or equal to -100 degrees.
# 4. A station is located in the `"Southwest"` region if its latitude is below 40 degrees and its longtitude is less than -100 degrees.

# %% [markdown]
# Define the `coordinates_to_region` function below. It should take in two arguments, a city's latitude (`lat`) and longitude (`lon`) coordinates, and output a string representing the region it is located in.
# 

# %%
def coordinates_to_region(lat, lon):
    if lat >= 40 and lon >= -100:
        return "Northeast"
    elif lat >= 40 and lon < -100:
        return "Northwest"
    elif lat <40 and lon>= -100:
        return "Southeast"
    elif lat <40 and lon <-100:
        return "Southwest"
        

# %%


# %% [markdown]
# Add a new column in `cities` labeled `Region` that contains the region in which the city is located. use the `coordinates_to_region` function defined rather than reimplementing its logic.
# 

# %%
regions_array = cities.apply(coordinates_to_region, 'Lat','Lon')
cities = cities.with_column('Region', regions_array)
cities.show(5)

# %%


# %% [markdown]
# To confirm that you've defined your `coordinates_to_region` function correctly and successfully added the `Region` column to the `cities` table, run the following cell. Each region should have a different color in the result.

# %%
# Just run this cell
cities.scatter("Lon", "Lat", group="Region")

# %% [markdown]
# Create a new table called `cities_nearest`. It contains the same columns as the `cities` table and an additional column called `"Nearest"` that contains the **name of the nearest city** that is in a different region from the city described by the row.
# 
# To approximate the distance between two cities, take the square root of the sum of the squared difference between their latitudes and the square difference between their longitudes.

# %%
def distance(lat0, lon0, lat1, lon1):
    "Approximate the distance between point (lat0, lon0) and (lat1, lon1) pairs in the arrays."
    return np.sqrt((lat0 - lat1) * (lat0 - lat1) + (lon0 - lon1) * (lon0 - lon1))

...

cities_nearest = ...
# Note: remove the comment(#) on the next line if you choose to do this question
#cities_nearest.show(5)

# %% [markdown]
# ### Part 1, Section 2: Welcome to Phoenix, Arizona

# %% [markdown]
# Each city has a different CSV file full of daily temperature and precipitation measurements. The file for Phoenix, Arizona is included with this project as `phoenix.csv`. The files for other cities can be downloaded [here](https://kilthub.cmu.edu/articles/dataset/Compiled_daily_temperature_and_precipitation_data_for_the_U_S_cities/7890488) by matching them to the ID of the city in the `cities` table.
# 
# Since Phoenix is located on the upper edge of the Sonoran Desert, it has some impressive temperatures.
# 
# Run the following cell to load in the `phoenix` table. It has one row per day and the following columns:
# 
# 1. `"Date"`: The date (a string) representing the date of the recording in **YYYY-MM-DD** format
# 2. `"tmax"`: The maximum temperature for the  day (°F)
# 3. `"tmin"`: The minimum temperature for the day (°F)
# 4. `"prcp"`: The recorded precipitation for the day (inches)

# %%
phoenix = Table.read_table("phoenix.csv", index_col=0)
phoenix.show(3)

# %% [markdown]
# Assign the variable `largest_2010_range_date` to the date of the **largest temperature range** in Phoenix, Arizona for any day between January 1st, 2010 and December 31st, 2010.

# %%

phoenix_with_ranges_2010 = phoenix.where('Date',are.containing('2010'))
phoenix_with_ranges_2010.with_column('abs_diff', abs(phoenix_with_ranges_2010.column('tmax') - phoenix_with_ranges_2010.column('tmin'))).sort('abs_diff', descending=True)
largest_2010_range_date = phoenix_with_ranges_2010.column('Date').item(0)


# %%


# %% [markdown]
# We can look back to our `phoenix` table to check the temperature readings for our `largest_2010_range_date` to see if anything special is going on. Run the cell below to find the row of the `phoenix` table that corresponds to the date we found above. 

# %%
# Just run this cell
phoenix.where("Date", largest_2010_range_date)

# %% [markdown]
# ZOO WEE MAMA! Look at the maximum temperature for that day. That's hot.

# %% [markdown]
# The function `extract_year_from_date` takes a date string in the **YYYY-MM-DD** format and returns an integer representing the **year**. The function `extract_month_from_date` takes a date string and returns a string describing the month. Run this cell, but you do not need to understand how this code works or edit it.

# %%
# Just run this cell
import calendar

def extract_year_from_date(date):
    """Returns an integer corresponding to the year of the input string's date."""
    return int(date[:4])

def extract_month_from_date(date):
    "Return an abbreviation of the name of the month for a string's date."
    month = date[5:7]
    return f'{month} ({calendar.month_abbr[int(date[5:7])]})'


# Example
print('2022-04-01 has year', extract_year_from_date('2022-04-01'),
      'and month', extract_month_from_date('2022-04-01'))

# %% [markdown]
# Add two new columns called `Year` and `Month` to the `phoenix` table that contain the year as an **integer** and the month as a **string** (such as `"04 (Apr)"`) for each day, respectively. 
# 

# %%
years_array = phoenix.apply(extract_year_from_date, 'Date')
months_array = phoenix.apply(extract_month_from_date, 'Date')
phoenix = phoenix.with_columns('Year', years_array, 'Month',months_array)
phoenix.show(5)

# %%


# %% [markdown]
# Using the `phoenix` table, create an overlaid line plot of the **average maximum temperature** and **average minimum temperature** for each year between 1900 and 2020 (inclusive). 
# 

# %%
phoenix.group('Year',np.mean).select('Year','tmax mean','tmin mean').plot('Year')

# %% [markdown]
# Although still hotly debated (pun intended), many climate scientists agree that the effects of climate change began to surface in the early 1960s as a result of elevated levels of greenhouse gas emissions.

# %% [markdown]
# 

# %% [markdown]
# 

# %% [markdown]
# Create a `monthly_increases` table with one row per month and the following four columns in order: 
# 1. `"Month"`: The month (such as `"02 (Feb)"`)
# 2. `"Past"`: The average max temperature in that month from 1900-1960 (inclusive)
# 3. `"Present"`: The average max temperature in that month from 2019-2021 (inclusive)
# 4. `"Increase"`: The difference between the present and past average max temperatures in that month
# 
# First make a copy of the `phoenix` table and add a new column containing the corresponding **period** for each row. You may find the `period` function helpful. Then, use this new table to construct `monthly_increases`. Feel free to use as many lines as you need.

# %%
def period(year):
    "Output if a year is in the Past, Present, or Other."
    if 1900 <= year <= 1960:
        return "Past"
    elif 2019 <= year <= 2021:
        return "Present"
    else:
        return "Other"
    
phoenix_copy = phoenix 

monthly_increases = phoenix_copy.with_column('period',phoenix.apply(period,'Year'))
                                                                                         
monthly_increases=monthly_increases.where('period','Past').group('Month',np.mean).join( 'Month',monthly_increases.where('period','Present').group('Month',np.mean)).drop(
'Date mean','tmin mean','prcp mean','Year mean','period mean','Date mean_2','tmin mean_2','prcp mean_2','Year mean_2','period mean_2').relabeled( 'tmax mean','Past').relabeled(
'tmax mean_2','Present')
monthly_increases=monthly_increases.with_columns('Increase',monthly_increases.column('Present')-monthly_increases.column('Past'))

monthly_increases.show()

# %%


# %% [markdown]
# ### February in Phoenix

# %% [markdown]
# The `"Past"` column values are averaged over many decades, and so they are reliable estimates of the average high temperatures in those months before the effects of modern climate change. However, the `"Present"` column is based on only three years of observations. February, the shortest month, has the fewest total observations: only 85 days. Run the following cell to see this.

# %%
# Just run this cell
feb_present = phoenix.where('Year', are.between_or_equal_to(2019, 2021)).where('Month', '02 (Feb)')
feb_present.num_rows

# %% [markdown]
# Look back to your `monthly_increases` table. Compared to the other months, the increase for the month of February is quite small; the February difference is very close to zero. Run the following cell to print out our observed difference.

# %%
# Just run this cell
print(f"February Difference: {monthly_increases.row(1).item('Increase')}")

# %% [markdown]
# Complete the implementation of the function `ci_lower`, which takes a one-column table `t` containing sample observations and a confidence `level` percentage such as 95 or 99. It returns the lower bound of a confidence interval for the population mean constructed using 5,000 bootstrap resamples.
# 
# After defining `ci_lower`, we have provided a line of code that calls `ci_lower` on the present-day February max temperatures to output the lower bound of a 99% confidence interval for the February average max temperature. The result should be around 67 degrees.
# 

# %%
def ci_lower(t, level):
    """Compute a lower bound of a level% confidence interval of the 
    average of the population for which column 0 of Table t contains a sample.
    """
    percent=(100-level)/2
    stats = make_array()
    for k in np.arange(5000):
        t_replacement = t.sample(with_replacement=True)
        stat = np.mean(t_replacement.column(0))
        stats = np.append(stats,stat)
    print(stats)
    return percentile(percent,stats)
 

# Call ci_lower on the max temperatures in present-day February to find the lower bound of a 99% confidence interval.
feb_present_ci = ci_lower(feb_present.select('tmax'), 99)


# %%
grader.check("q1_2_6")

# %% [markdown]
#  The lower bound of the `feb_present_ci` 99% confidence interval is below the observed past February average maximum temperature of 68.8485 (from the `monthly_increases` table). What conclusion can you draw about the effect of climate change on February maximum temperatures in Phoenix from this information? Use a 1% p-value cutoff.
# 

# %% [markdown]
# <!-- END QUESTION -->
# 
# 
# 
# ### All Months

# %% [markdown]
# Repeat the process of comparing the **lower bound of a 99% confidence interval** to the **past average** for each month. For each month, print out the name of the month (e.g., `02 (Feb)`), the observed past average, and the lower bound of a confidence interval for the present average.
# 
# Use the provided call to `print` in order to format the result as one line per month.

# %%
comparisons = make_array()
months = make_array('01 (Jan)', '02 (Feb)', '03 (Mar)', '04 (Apr)', '05 (May)', '06 (Jun)', '07 (Jul)', '08 (Aug)', '09 (Sep)','10 (Oct)','11 (Nov)', '12 (Dec)')
for month in months:
    past_average = monthly_increases.where("Month", month).column(1).item(0)
    present_observations = phoenix.where('Year', are.between_or_equal_to(2019,2021)).where("Month",month)
    present_lower_bound = ci_lower(present_observations.select('tmax'),99)
    
    # Do not change the code below this line
    below = past_average < present_lower_bound
    if below:
        comparison = '**below**'
    else:
        comparison = '*above*'
    comparisons = np.append(comparisons, comparison)
    
    print('For', month, 'the past avg', round(past_average, 1), 
          'is', comparison, 
          'the lower bound', round(present_lower_bound, 1),
          'of the 99% CI of the present avg. \n')

# %%


# %% [markdown]
# Summarize your findings. After comparing the past average to the 99% confidence interval's lower bound for each month, what conclusions can we make about the monthly average maximum temperature in historical (1900-1960) vs. modern (2019-2021) times in the twelve months? In other words, what null hypothesis should you consider, and for which months would you reject or fail to reject the null hypothesis? Use a 1% p-value cutoff.

# %% [markdown]
# The code above calculates the past average and present lower bound for a given month. The past average is calculated by taking average of the observations for that month. The present lower bound is calculated by taking the lower bound of 99% confidence interval for the present month. If the past average is below the present lower bound, it will result in below. If the past average is above the present lower bound, it will result in above. Then, the comparison is appended to the comparison array. 
# 

# %%


# %%
# Run this cell to set up the notebook, but please don't change it.
from datascience import *
import numpy as np

%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
np.set_printoptions(legacy='1.13')

import warnings
warnings.simplefilter('ignore')

# %% [markdown]
# # Part 2: Drought

# %% [markdown]
# According to the [United States Environmental Protection Agency](https://www.epa.gov/climate-indicators/southwest), "Large portions of the Southwest have experienced drought conditions since weekly Drought Monitor records began in 2000. For extended periods from 2002 to 2005 and from 2012 to 2020, nearly the entire region was abnormally dry or even drier." 
# 
# Assessing the impact of drought is challenging with just city-level data because so much of the water that people use is transported from elsewhere, but we'll explore the data we have and see what we can learn.
# 
# Let's first take a look at the precipitation data in the Southwest region. The `southwest.csv` file contains total annual precipitation for 13 cities in the southwestern United States for each year from 1960 to 2021. This dataset is aggregated from the daily data and includes only the Southwest cities from the original dataset that have consistent precipitation records back to 1960.

# %%
southwest = Table.read_table('southwest.csv')
southwest.show(5)

# %% [markdown]
# Create a table `totals` that has one row for each year in chronological order. It should contain the following columns:
# 1. `"Year"`: The year (a number)
# 2. `"Precipitation"`: The total precipitation in all 13 southwestern cities that year

# %%
southwest.sort("Year")

# %%
totals = southwest.group("Year", np.sum).relabel("Total Precipitation sum","Precipitation").drop("City", "City sum")
                                                                            

# %% [markdown]
# Run the cell below to plot the total precipitation in these cities over time, so that we can try to spot the drought visually. As a reminder, the drought years given by the EPA were  (2002-2005) and (2012-2020).

# %%
# Just run this cell
totals.plot("Year", "Precipitation")

# %% [markdown]
# This plot isn't very revealing. Each year has a different amount of precipitation, and there is quite a bit of variability across years, as if each year's precipitation is a random draw from a distribution of possible outcomes. 
# 
# Could it be that these so-called "drought conditions" from 2002-2005 and 2012-2020 can be explained by chance? In other words, could it be that the annual precipitation amounts in the Southwest for these drought years are like **random draws from the same underlying distribution** as for other years? Perhaps nothing about the Earth's precipitation patterns has really changed, and the Southwest U.S. just happened to experience a few dry years close together. 
# 
# To assess this idea, let's conduct an A/B test in which **each year's total precipitation** is an outcome, and the condition is **whether or not the year is in the EPA's drought period**.

# %% [markdown]
# This `drought_label` function distinguishes between drought years as described in the U.S. EPA statement above (2002-2005 and 2012-2020) and other years. Note that the label "other" is perhaps misleading, since there were other droughts before 2000, such as the massive [1988 drought](https://en.wikipedia.org/wiki/1988%E2%80%9390_North_American_drought) that affected much of the U.S. However, if we're interested in whether these modern drought periods (2002-2005 and 2012-2020) are *normal* or *abnormal*, it makes sense to distinguish the years in this way. 

# %%
def drought_label(n):
    """Return the label for an input year n."""
    if 2002 <= n <= 2005 or 2012 <= n <= 2020:
        return 'drought'
    else:
        return 'other'

# %% [markdown]
#  Define null and alternative hypotheses for an A/B test that investigates whether drought years are drier (have less precipitation) than other years.
# 

# %% [markdown]
# Drought years are drier than other years
# 
# Drought years are not drier than other years

# %% [markdown]
# First, define the table `drought`. It should contain one row per year and the following two columns:
# - `"Label"`: Denotes if a year is part of a `"drought"` year or an `"other"` year
# - `"Precipitation"`: The sum of the total precipitation in 13 Southwest cities that year
# 
# Then, construct an overlaid histogram of two observed distributions: the total precipitation in drought years and the total precipitation in other years. 

# %%
bins = np.arange(85, 215+1, 13)
totals_copy = totals
drought = totals_copy.with_columns("Label", totals.apply(drought_label, "Year")).select("Label", "Precipitation")
drought.hist("Precipitation", unit="Year", bins=bins, group="Label")


# %% [markdown]
# <!-- END QUESTION -->
# 
# 
# 
# Before you continue, inspect the histogram you just created and try to guess the conclusion of the A/B test. Building intuition about the result of hypothesis testing from visualizations is quite useful for data science applications. 

# %% [markdown]
# Our next step is to choose a test statistic based on our alternative hypothesis in Question 2.2. Which of the following options are valid choices for the test statistic? Assign `ab_test_stat` to an array of integers corresponding to valid choices. Assume averages and totals are taken over the total precipitation sums for each year.
# 
# 1. The difference between the **total** precipitation in **drought** years and the **total** precipitation in **other** years.
# 2. The difference between the **total** precipitation in **others** years and the **total** precipitation in **drought** years.
# 3. The **absolute** difference between the **total** precipitation in others years and the **total** precipitation in drought years.
# 1. The difference between the **average** precipitation in **drought** years and the **average** precipitation in **other** years.
# 2. The difference between the **average** precipitation in **others** years and the **average** precipitation in **drought** years.
# 3. The **absolute** difference between the **average** precipitation in others years and the **average** precipitation in drought years.
# 

# %% [markdown]
# Fellow climate scientists Will and Nicole point out that there are more **other** years than **drought** years, and so measuring the difference between total precipitation will always favor the **other** years. They conclude that all of the options above involving **total** precipitation are invalid test statistic choices.

# %% [markdown]
# <!-- END QUESTION -->
# 
# 
# 
# Before going on, check your `drought` table. It should have two columns `Label` and `Precipitation` with 61 rows, 13 of which are for `"drought"` years.

# %%
drought.show(3)

# %%
drought.group('Label')

# %% [markdown]
# For our A/B test, we'll use the difference between the average precipitation in drought years and the average precipitation in other years as our test statistic:
# 
# $$\text{average precipitation in "drought" years} - \text{average precipitation in "other" years}$$
# 
# First, complete the function `test_statistic`. It should take in a two-column table `t` with one row per year and two columns:
# - `Label`: the label for that year (either `'drought'` or `'other'`)
# - `Precipitation`: the total precipitation in the 13 Southwest cities that year. 
# 
# Then, use the function you define to assign `observed_statistic` to the observed test statistic.
# 

# %%
def test_statistic(t):
    drought_years = t.where("Label", "drought").column("Precipitation")
    other_years = t.where("Label", "other").column("Precipitation")
    return np.average(drought_years) - np.average(other_years)

observed_statistic = test_statistic(drought)

# %% [markdown]
# Now that we have defined our hypotheses and test statistic, we are ready to conduct our hypothesis test. We’ll start by defining a function to simulate the test statistic under the null hypothesis, and then call that function 5,000 times to construct an empirical distribution under the null hypothesis.

# %% [markdown]
# Write a function to simulate the test statistic under the null hypothesis. The `simulate_precipitation_null` function should simulate the null hypothesis once (not 5,000 times) and return the value of the test statistic for that simulated sample.

# %%
def simulate_precipitation_null():
    # return np.round(sample_proportions(61, [13/61, 48/61]) * 61).item(0) - np.round(sample_proportions(61, [13/61, 48/61]) * 61).item(1)
    random_labels = drought.sample(with_replacement=False).column('Label')
    random_sample_table = drought.select('Precipitation').with_column(
        'Label', random_labels)
    return test_statistic(random_sample_table)
 
simulate_precipitation_null()

# %% [markdown]
# Fill in the blanks below to complete the simulation for the hypothesis test. Your simulation should compute 5,000 values of the test statistic under the null hypothesis and store the result in the array `sampled_stats`.

# %%
sampled_stats = make_array()

repetitions = 5000
for i in np.arange(repetitions):
    sampled_stats = np.append(sampled_stats, simulate_precipitation_null())

# Do not change these lines
Table().with_column('Difference Between Means', sampled_stats).hist()
plt.scatter(observed_statistic, 0, c="r", s=50);
plt.ylim(-0.01);

# %% [markdown]
# Compute the p-value for this hypothesis test, and assign it to the variable `precipitation_p_val`.

# %%
precipitation_p_val = np.count_nonzero(sampled_stats <= observed_statistic) / repetitions



# %% [markdown]
# State a conclusion from this test using a p-value cutoff of 5%. What have you learned about the EPA's statement on drought?
# 

# %% [markdown]
# The p-value was 2.92% which is below the cutoff showing that there was a statistically significant difference between the two periods. this shows that there have been significant climate changes in recent times

# %% [markdown]
# Does your conclusion from Question 2.10 apply to the entire Southwest region of the U.S.? Why or why not?
# 

# %% [markdown]
# There may be some relation because the cities are naturally randomly selected but it does not definitively claim so

# %% [markdown]
# <!-- END QUESTION -->
# 
# 
# 
# # Conclusion

# %% [markdown]
# Data science plays a central role in climate change research because massive simulations of the Earth's climate are necessary to assess the implications of climate data recorded from weather stations, satellites, and other sensors. [Berkeley Earth](http://berkeleyearth.org/data/) is a common source of data for these kinds of projects.
# 
# In this project, we found ways to apply our statistical inference technqiues that rely on random sampling even in situations where the data were not generated randomly, but instead by some complicated natural process that appeared random. We made assumptions about randomness and then came to conclusions based on those assumptions. Great care must be taken to choose assumptions that are realistic, so that the resulting conclusions are not misleading. However, making assumptions about data can be productive when doing so allows inference techniques to apply to novel situations.


