# Web scraping problem

In this project, we are going to scrape the Tesla revenue data and store it in a dataframe, and also in a sqlite database.

To know whether a website allows web scraping or not, you can look at the website’s “robots.txt” file. You can find this file by appending “/robots.txt” to the URL that you want to scrape.

**Step 1:** Make sure you have sqlite3 and pandas installed. In case they are not installed, you can use the following command in the terminal:

```py
pip install pandas
```

and 

```py
pip install sqlite3
```

**Step 2:** Import necessary libraries


```python
# import packages

import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3

```

**Step 3:** Use the requests library to download the webpage https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue. Save the text of the response as a variable named html_data.


```python
 
url = " https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

```

**Step 4:** Parse the html data using beautiful_soup


```python
soup = BeautifulSoup(html_data,"html.parser")
```

**Step 5:** Use beautiful soup or the read_html function to extract the table with Tesla Quarterly Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column.


```python
#find all tables
tables = soup.find_all('table')

for index,table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index

#create a dataframe        
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        Tesla_revenue = Tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


#using read_html

#tesla_revenue=pd.read_html(url, match="Tesla Quarterly Revenue", flavor='bs4')[0]
#tesla_revenue = tesla_revenue.rename(columns={"Tesla Quarterly Revenue(Millions of US $)":"Date","Tesla Quarterly Revenue(Millions of US $).1":"Revenue"}) #Rename df columns to 'Date' and 'Revenue'
#tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"") # remove the comma and dollar sign from the 'Revenue' column
#tesla_revenue.head()
```

**Step 6:** Remove the rows in the dataframe that are empty strings or are NaN in the Revenue column. Print the entire tesla_revenue DataFrame to see if you have any.


```python
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-03-31</td>
      <td>18756</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021-12-31</td>
      <td>17719</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021-09-30</td>
      <td>13757</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2021-06-30</td>
      <td>11958</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2021-03-31</td>
      <td>10389</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2020-12-31</td>
      <td>10744</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2020-09-30</td>
      <td>8771</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2020-06-30</td>
      <td>6036</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2020-03-31</td>
      <td>5985</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2019-12-31</td>
      <td>7384</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2019-09-30</td>
      <td>6303</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2019-06-30</td>
      <td>6350</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2019-03-31</td>
      <td>4541</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2018-12-31</td>
      <td>7226</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2018-09-30</td>
      <td>6824</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2018-06-30</td>
      <td>4002</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2018-03-31</td>
      <td>3409</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2017-12-31</td>
      <td>3288</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2017-09-30</td>
      <td>2985</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2017-06-30</td>
      <td>2790</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2017-03-31</td>
      <td>2696</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2016-12-31</td>
      <td>2285</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2016-09-30</td>
      <td>2298</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2016-06-30</td>
      <td>1270</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2016-03-31</td>
      <td>1147</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2015-12-31</td>
      <td>1214</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2015-09-30</td>
      <td>937</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2015-06-30</td>
      <td>955</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2015-03-31</td>
      <td>940</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2014-12-31</td>
      <td>957</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2014-09-30</td>
      <td>852</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2014-06-30</td>
      <td>769</td>
    </tr>
    <tr>
      <th>32</th>
      <td>2014-03-31</td>
      <td>621</td>
    </tr>
    <tr>
      <th>33</th>
      <td>2013-12-31</td>
      <td>615</td>
    </tr>
    <tr>
      <th>34</th>
      <td>2013-09-30</td>
      <td>431</td>
    </tr>
    <tr>
      <th>35</th>
      <td>2013-06-30</td>
      <td>405</td>
    </tr>
    <tr>
      <th>36</th>
      <td>2013-03-31</td>
      <td>562</td>
    </tr>
    <tr>
      <th>37</th>
      <td>2012-12-31</td>
      <td>306</td>
    </tr>
    <tr>
      <th>38</th>
      <td>2012-09-30</td>
      <td>50</td>
    </tr>
    <tr>
      <th>39</th>
      <td>2012-06-30</td>
      <td>27</td>
    </tr>
    <tr>
      <th>40</th>
      <td>2012-03-31</td>
      <td>30</td>
    </tr>
    <tr>
      <th>41</th>
      <td>2011-12-31</td>
      <td>39</td>
    </tr>
    <tr>
      <th>42</th>
      <td>2011-09-30</td>
      <td>58</td>
    </tr>
    <tr>
      <th>43</th>
      <td>2011-06-30</td>
      <td>58</td>
    </tr>
    <tr>
      <th>44</th>
      <td>2011-03-31</td>
      <td>49</td>
    </tr>
    <tr>
      <th>45</th>
      <td>2010-12-31</td>
      <td>36</td>
    </tr>
    <tr>
      <th>46</th>
      <td>2010-09-30</td>
      <td>31</td>
    </tr>
    <tr>
      <th>47</th>
      <td>2010-06-30</td>
      <td>28</td>
    </tr>
    <tr>
      <th>48</th>
      <td>2010-03-31</td>
      <td>21</td>
    </tr>
    <tr>
      <th>50</th>
      <td>2009-09-30</td>
      <td>46</td>
    </tr>
    <tr>
      <th>51</th>
      <td>2009-06-30</td>
      <td>27</td>
    </tr>
  </tbody>
</table>
</div>



**Step 7:** Make sure tesla_revenue is still a dataframe


```python
type(tesla_revenue)
```




    pandas.core.frame.DataFrame



**Step 8:** Insert the data into sqlite3 by converting the dataframe into a list of tuples


```python

records = tesla_revenue.to_records(index=False)
list_of_tuples = list(records)
list_of_tuples
```




    [('2022-03-31', '18756'),
     ('2021-12-31', '17719'),
     ('2021-09-30', '13757'),
     ('2021-06-30', '11958'),
     ('2021-03-31', '10389'),
     ('2020-12-31', '10744'),
     ('2020-09-30', '8771'),
     ('2020-06-30', '6036'),
     ('2020-03-31', '5985'),
     ('2019-12-31', '7384'),
     ('2019-09-30', '6303'),
     ('2019-06-30', '6350'),
     ('2019-03-31', '4541'),
     ('2018-12-31', '7226'),
     ('2018-09-30', '6824'),
     ('2018-06-30', '4002'),
     ('2018-03-31', '3409'),
     ('2017-12-31', '3288'),
     ('2017-09-30', '2985'),
     ('2017-06-30', '2790'),
     ('2017-03-31', '2696'),
     ('2016-12-31', '2285'),
     ('2016-09-30', '2298'),
     ('2016-06-30', '1270'),
     ('2016-03-31', '1147'),
     ('2015-12-31', '1214'),
     ('2015-09-30', '937'),
     ('2015-06-30', '955'),
     ('2015-03-31', '940'),
     ('2014-12-31', '957'),
     ('2014-09-30', '852'),
     ('2014-06-30', '769'),
     ('2014-03-31', '621'),
     ('2013-12-31', '615'),
     ('2013-09-30', '431'),
     ('2013-06-30', '405'),
     ('2013-03-31', '562'),
     ('2012-12-31', '306'),
     ('2012-09-30', '50'),
     ('2012-06-30', '27'),
     ('2012-03-31', '30'),
     ('2011-12-31', '39'),
     ('2011-09-30', '58'),
     ('2011-06-30', '58'),
     ('2011-03-31', '49'),
     ('2010-12-31', '36'),
     ('2010-09-30', '31'),
     ('2010-06-30', '28'),
     ('2010-03-31', '21'),
     ('2009-09-30', '46'),
     ('2009-06-30', '27')]



**Step 9:** Now let's create a SQLite3 database. Use the connect() function of sqlite3 to create a database. It will create a connection object. In case the databse does not exist, it will create it.


```python
# Use the connect() function of sqlite3 to create a database. It will create a connection object.

connection = sqlite3.connect('Tesla.db')
```

**Step 10:** Let's create a table in our database to store our revenue values.


```python
c = connection.cursor()

# Create table
c.execute('''CREATE TABLE revenue
             (Date, Revenue)''')
```




    <sqlite3.Cursor at 0x7f6fd433e2d0>




```python
# Insert the values
c.executemany('INSERT INTO revenue VALUES (?,?)', list_of_tuples)
# Save (commit) the changes
connection.commit()
```

**Step 11:** Now retrieve the data from the database


```python
for row in c.execute('SELECT * FROM revenue'):
    print(row)
```

    ('2022-03-31', '18756')
    ('2021-12-31', '17719')
    ('2021-09-30', '13757')
    ('2021-06-30', '11958')
    ('2021-03-31', '10389')
    ('2020-12-31', '10744')
    ('2020-09-30', '8771')
    ('2020-06-30', '6036')
    ('2020-03-31', '5985')
    ('2019-12-31', '7384')
    ('2019-09-30', '6303')
    ('2019-06-30', '6350')
    ('2019-03-31', '4541')
    ('2018-12-31', '7226')
    ('2018-09-30', '6824')
    ('2018-06-30', '4002')
    ('2018-03-31', '3409')
    ('2017-12-31', '3288')
    ('2017-09-30', '2985')
    ('2017-06-30', '2790')
    ('2017-03-31', '2696')
    ('2016-12-31', '2285')
    ('2016-09-30', '2298')
    ('2016-06-30', '1270')
    ('2016-03-31', '1147')
    ('2015-12-31', '1214')
    ('2015-09-30', '937')
    ('2015-06-30', '955')
    ('2015-03-31', '940')
    ('2014-12-31', '957')
    ('2014-09-30', '852')
    ('2014-06-30', '769')
    ('2014-03-31', '621')
    ('2013-12-31', '615')
    ('2013-09-30', '431')
    ('2013-06-30', '405')
    ('2013-03-31', '562')
    ('2012-12-31', '306')
    ('2012-09-30', '50')
    ('2012-06-30', '27')
    ('2012-03-31', '30')
    ('2011-12-31', '39')
    ('2011-09-30', '58')
    ('2011-06-30', '58')
    ('2011-03-31', '49')
    ('2010-12-31', '36')
    ('2010-09-30', '31')
    ('2010-06-30', '28')
    ('2010-03-31', '21')
    ('2009-09-30', '46')
    ('2009-06-30', '27')


Our database name is “Tesla.db”. We saved the connection to the connection object.

Next time we run this file, it just connects to the database, and if the database is not there, it will create one.

Source:

https://github.com/bhavyaramgiri/Web-Scraping-and-sqlite3/blob/master/week%209-%20web%20scraping%20sqlite.ipynb

https://coderspacket.com/scraping-the-web-page-and-storing-it-in-a-sqlite3-database

https://gist.github.com/elifum/09dcaecfbc6c6e047222db3fcfe5f3b8