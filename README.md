
# Mike Swithers' Python Project

## Introduction:

This portfolio project reads in stock data from a file, takes user input to add or update it and saves the updated files.  Also, it gets the most recent stock price from yahoo! finance and creates a gain/loss report. 

The goal of this project is for me to learn how to develop a program in the object oriented programming style using Python.  I wanted to learn how to automate working with Excel files and obtain infomation from the web.  

I decided to save the data to csv files, since Excel works with them easily.  Also, in order to save the data directly to Excel I need to learn more about pandas DataFrames, and time did not permit this.  My next version I will learn the ins and outs of the pandas library and refactor my project to work with DataFrames.  

## Installation:

The main.py file contains all the code needed to run the program.  The only 3rd party library used is yfinance, which gets the current prices from yahoo finance's website.   

## Get Started:

Run the main.py file and follow the menu step by step.  

The output files are saved to the same directory as the main.py file is run.
The files are:

    portfolio.csv   - contains the stock holdings
    transactions.cvs - all the transactions
    gain_loss_report.csv - the unrealized gain or loss on each stock holding

Currrently the portfolio and gain_loss_report files are overwritten each time the program is run.  The transactions file is appended if it exists or created if it does not.    

I have not yet implemented the dividend report or the data validation, exception handling, or testing.
 


## Documentation:

I started a UML diagram: [UML Diagram](UMLPorfolioLink.url) a screen shot is included in the project folder if the link does not work. 
