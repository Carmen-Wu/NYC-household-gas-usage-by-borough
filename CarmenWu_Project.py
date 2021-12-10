"""
Name: Carmen Wu 
Title: NYC household gas usage by borough 
URl: https://carmenwu876.wixsite.com/nyc-household-gas-us
Resources: Listed below
	⁃	This dataset includes the borough of zip codes in NYC: https://data.ny.gov/Government-Finance/New-York-State-ZIP-Codes-County-FIPS-Cross-Referen/juva-r6g2/data
	⁃	This dataset shows gas usage of households/industries during 2010: https://data.cityofnewyork.us/w/uedp-fegm/25te-f2tw?cur=zh_ETNBDGVA&from=root
	⁃	This dataset shows the population of each borough: https://data.ny.gov/widgets/xywu-7bv9
Email: Carmen.Wu01@myhunter.cuny.edu
"""

import pandas as pd 
import pandasql as psql 
import matplotlib.pyplot as plt


#cleans data for just residential buildings
gas_df = pd.read_csv('Natural_Gas_Consumption_by_ZIP_Code_-_2010.csv')
new_gas_df = gas_df[(gas_df['Building type (service class'] == 'Residential') | 
        (gas_df['Building type (service class'] == 'Small residential') | 
        (gas_df['Building type (service class'] == 'Large residential')]

#groupby zipcode to get average consumption. 
q1 = 'SELECT DISTINCT("Zip Code") as "ZIP Code", AVG(" Consumption (GJ) ") as Avg_con FROM new_gas_df GROUP BY "Zip Code"'
zipcode_df = psql.sqldf(q1)
zipcode_df['ZIP Code'] = zipcode_df['ZIP Code'].str[:5]
zipcode_df['ZIP Code'] = zipcode_df['ZIP Code'].astype(int)


#top 5 zipcodes with largest usage, plots using matplotlib.pyplot
zipcodedf_large = zipcode_df.nlargest(5, ['Avg_con'])
zipcode_Df_large = zipcodedf_large.reset_index()
zipcode_Df_large = zipcode_Df_large.drop(['index'], axis = 1)

zipcode_Df_large['ZIP Code'] = zipcode_Df_large['ZIP Code'].astype(str)
plt.bar(zipcode_Df_large['ZIP Code'], zipcode_Df_large['Avg_con'])
plt.title('Zip Code with highest Average_usage (Gj)')
plt.xlabel('Zip Code')
plt.ylabel('Average_usage (Gj)')
plt.show()


#5 zipcode with lowest usage, plots using matplotlib.pyplot 
zipcodedf_small = zipcode_df.nsmallest(5, ['Avg_con'])
zipcode_Df_small = zipcodedf_small.reset_index()
zipcode_Df_small = zipcode_Df_small.drop(['index'], axis = 1)


zipcode_Df_small['ZIP Code'] = zipcode_Df_small['ZIP Code'].astype(str)
plt.bar(zipcode_Df_small['ZIP Code'], zipcode_Df_small['Avg_con'])
plt.title('Zip Code with smallest Average_usage (Gj)')
plt.xlabel('Zip Code')
plt.ylabel('Average_usage (Gj)')
plt.show()


#cleans data for population 
pop_df = pd.read_csv('New_York_City_Population_by_Borough__1950_-_2040.csv')
popdf = pop_df.drop(['Age Group','1950', '1950 - Boro share of NYC total', '1960', '1960 - Boro share of NYC total', '1970', '1970 - Boro share of NYC total', '1980', '1980 - Boro share of NYC total', '1990', '1990 - Boro share of NYC total', '2000', '2000 - Boro share of NYC total', '2020', '2020 - Boro share of NYC total', '2030', '2030 - Boro share of NYC total', '2040', '2040 - Boro share of NYC total','2010 - Boro share of NYC total',], axis = 1)
pop_Df = popdf.drop([0])
pop_Df['2010'] = pop_Df['2010'].str.replace(',', '')
pop_Df['2010'] = pop_Df['2010'].astype(int)


#plots population data of each borough
plt.bar(pop_Df['Borough'], pop_Df['2010'])
plt.title('Borough Population')
plt.xlabel('Borough')
plt.ylabel('Population')
plt.show()



#cleans data for borough/county name dataset
county_df = pd.read_csv('New_York_State_ZIP_Codes-County_FIPS_Cross-Reference.csv')
county_DF = county_df.drop(['State FIPS','County FIPS', 'File Date', 'County Code'], axis = 1)
county_DF = county_DF[['ZIP Code', 'County Name']]


#merge zipcode and county/borough datasets together
merge_borough_zipcode = pd.merge(zipcode_df, county_DF, how = "inner", on = ["ZIP Code"])


#average gas usage by borough
q2 = 'SELECT ("County Name") as "County Name", AVG("Avg_con") as Average_usage FROM merge_borough_zipcode GROUP BY "County Name"'
borough_avg = psql.sqldf(q2)


#plot borough gas usage average 
plt.bar(borough_avg['County Name'], borough_avg['Average_usage'])
plt.title('Borough/County Name Vs Average_usage (Gj)')
plt.xlabel('Borough/County Name')
plt.ylabel('Average_usage (Gj)')
plt.show()


#find gas usage of an average person per borough
pop_Df['persons avg usage'] = pop_Df['2010']/ borough_avg['Average_usage']
staten_island = 468730/529220 #staten island calculation (population of SI /average usage of SI)

#make a new df to manually enter staten island  
Data = {'County Name': ['Bronx', 'Kings', 'Manhattan', 'Queens', 'Richmond'], 'usage_per_person': ['1.376754', '20.863404', '4.255317', '4.251544', staten_island]}
usage_per_person_df = pd.DataFrame(data = Data)
usage_per_person_df['usage_per_person'] = usage_per_person_df['usage_per_person'].astype(float)


# plot average usage per person per borough
plt.bar(usage_per_person_df['County Name'], usage_per_person_df['usage_per_person'])
plt.title('Borough/County Name Vs Average_usage_per_person(Gj)')
plt.xlabel('Borough/County Name')
plt.ylabel('Average_usage_per_person (Gj)')
plt.show()


