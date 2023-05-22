#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:35:41 2023

@author: ropger
"""
import numpy as np 
import pandas as pd 
import mysql.connector
import matplotlib.pyplot as plt
import pyodbc


#######################################

# Try + SQL error

import mysql.connector
from mysql.connector import Error
try:
    cnx = mysql.connector.connect(user='root', 
                                  password='plymouth96',
                                  host='localhost',
                                  port='3306',
                                  database='health_income')
 
    if cnx.is_connected():
        print("Connected to MySQL database")
 
except Error as e:
    print("Error while connecting to MySQL", e)
 
finally:
    if (cnx.is_connected()):
        cnx.close()
        print("MySQL connection is closed")
        
######################################
######################################
######################################


cxn = mysql.connector.connect(user='root', 
                              password='plymouth96',
                              host='localhost',
                              port='3306',
                              database='health_income')

# Print connection object (check if connection was succesfull)
print(cxn)

# Close connection when needed
# cxn.close()

cursor = cxn.cursor(buffered=True)

# In case of disconnect
# cursor.reset()

######################################
######################################
######################################
######################################

# EXECUTE QUERIES


# Execute query
cursor.execute("SELECT * FROM health_income WHERE country = 'Albania'")


# Fetch one result
row = cursor.fetchall() # Or 'fetchone()'
print(row)


######################################
# CREATE Data Frame from country = Albania

Albania = pd.read_sql("""SELECT * 
                      FROM health_income 
                      WHERE country = 'Albania'""", cxn)

Albania


Albania.head()
Albania.describe()

# GET life_expectancy for Albania (via SQL query and Python summary statistics)

Albania_e = Albania["life_expectancy"].mean()
Albania_e 

Albania_e = pd.read_sql(""" SELECT AVG(life_expectancy)
                       
                            FROM health_income
                            WHERE COUNTRY = 'Albania'""", cxn)
Albania_e          
######################################

# Plot life expectancy over the years for Albania


Albania_e_fy = pd.read_sql("""SELECT life_expectancy, 
                           year,
                           country
                       FROM health_income
                       WHERE COUNTRY = 'Albania'""", cxn)
                       
Albania_e_fy

Albania_e_fy.pivot_table(index=['year'] ,values=['life_expectancy'], columns=['country']).plot(figsize=(12,5),title='Life Expectancy Over the Years')

######################################

# Plot life expectancy comparison between Albania and Algeria

Albania_Algeria_e = pd.read_sql("""SELECT life_expectancy, 
                           year,
                           country
                       FROM health_income
                       WHERE COUNTRY in ('Albania', 'Algeria') """, cxn)
                       
Albania_Algeria_e

Albania_Algeria_e.pivot_table(index=['year'] ,values=['life_expectancy'], columns=['country']).plot(figsize=(12,5),title='Life Expectancy Over the Years (Albania and Algeria)')

######################################

