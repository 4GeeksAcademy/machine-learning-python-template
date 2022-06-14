# Web scraping problem

In this project, we are going to scrape the Tesla revenue data and store it in a dataframe, and also in a sqlite database.

To know whether a website allows web scraping or not, you can look at the website’s “robots.txt” file. You can find this file by appending `/robots.txt` to the URL that you want to scrape.

## Step 1: Setup and installation

Make sure you have sqlite3 and pandas installed. 

In case they are not installed, you can use the following command in the terminal:

```py
pip install pandas sqlite3 requests
```

Note: this will install both libraries and libraries

## Step 2: Create app.py 

Open the `./src` folder and create a new app.py file and add the following content to it:

```py
print("Hello world")
```

Run the file using the command `python ./src/app.py`


### Step 3: Download the data using request library

Use the [requests library](https://requests.readthedocs.io/en/latest/user/quickstart/) to download the data.

The following website contains the tesla revenue data from the past few years:
https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue

Save the text of the response as a variable named html_data.

### Step 4: Parse the html data using beautiful_soup

Create a new intance of BeautifulSoup with the html_data.

Use beautiful soup or the read_html function to extract the table with Tesla Quarterly Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column. Inspect the html code to know what parts of the table should be found.

1. find all tables
2. find table with Tesla quarterly revenue
3. create the dataframe        
4. Iterate over the table rows to get the values and remove the `$` and `comma` 

## Step 5: Clean rows

Remove the rows in the dataframe that are empty strings or are `NaN` in the Revenue column. 

Print the entire `tesla_revenue` DataFrame to see if you have any.


### Step 6: Insert the data into sqlite3

Make sure tesla_revenue is still a dataframe

Insert the data into sqlite3 by converting the dataframe into a list of tuples


### Step 7: Connect to SQLite

Now let's create a SQLite3 database. Use the connect() function of sqlite3 to create a database. It will create a connection object. In case the databse does not exist, it will create it.


Use the `sqlite3.connect()` function of sqlite3 to create a database. It will create a connection object.


### Step 8: Let's create a table in our database to store our revenue values:

1. Create table
2. Insert the values
3. Save (commit) the changes

### Step 9: Now retrieve the data from the database

Our database name is “Tesla.db”. We saved the connection to the connection object.

Next time we run this file, it just connects to the database, and if the database is not there, it will create one.

### Step 10: Finally create a plot to visualize the data

What kind of visualizations show we do?

Source:

https://github.com/bhavyaramgiri/Web-Scraping-and-sqlite3/blob/master/week%209-%20web%20scraping%20sqlite.ipynb

https://coderspacket.com/scraping-the-web-page-and-storing-it-in-a-sqlite3-database

https://gist.github.com/elifum/09dcaecfbc6c6e047222db3fcfe5f3b8