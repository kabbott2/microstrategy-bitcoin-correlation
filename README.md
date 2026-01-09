# What is the Correlation Between (Micro)Strategy and Bitcoin?
## Background
Strategy (MSTR), f.k.a. Microstrategy, is a digital asset treasury company (DATCO) that holds 673,783 Bitcoin (BTC) worth approximately $61b dollars. MSTR began to purcahse Bitcoin on August 11th, 2020 and has since acquired over 3% of the world's total supply of BTC at the time of writing (1/8/26). 

## Guiding Question
What is the correlation between the share price of MSTR and the spot price of BTC in dollar terms? Does MTSR truly give investors "leveraged BTC" exposure as many espouse?

## Analysis Steps
1. #### Install dependencies
* Pandas, NumPy, MatPlotLib, yfinance, and SciPy
* For the most part, this is present in all modules.
2. #### Fetch and clean data.
* Source MSTR and BTC data from yfinance (open, close, high, low, volume [adj. for splits/dividends]) from August 10, 2020 (marks the date MSTR first acquired BTC). 
* Remove BTC data on weekends, as MSTR only trades on weekdays.
* Calculate daily return for MSTR and BTC, as raw prices are non-stationary, voiding the use of correlation analysis.
* fetch_mstr.py, fetch_btc.py
3. #### Merge datasets.
* Load MSTR and BTC data into Pandas dataframes and merge them on the date index so they are aligned.
* evaluate.py
4. #### Create visualizations
* Use MatPlotLib to visaulize the results.

## Findings
####

## Visualizations
### 1. 
<img width="1197" height="306" alt="Screenshot 2026-01-08 at 2 29 27 PM" src="https://github.com/user-attachments/assets/ebdd145d-efe1-4b71-9944-a934f59c4bbe" />


## Disclosure
This project is in no way investment advice. The author of this project is therein not responsible for any financial risk, be it through the purchase or sale short of MSTR, BTC, or any other kind of financial instrument/security, taken after viewing this project.
