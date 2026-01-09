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
* Modules: fetch_mstr.py, fetch_btc.py
3. #### Merge datasets.
* Load MSTR and BTC data into Pandas dataframes and merge them on the date index so they are aligned.
* Modules: evaluate.py
4. #### Analyze the data and create visualizations.
* Use the time-series data, compare daily returns.
* Calculate the Pearson and Spearman coefficients, as well as the Beta of MSTR to BTC. 
* Use MatPlotLib to visaulize the results.

## Findings and Charts
### Figure 1. Share Price of MSTR and BTC (08/11/20 - Present)
<img width="1197" height="306" alt="Screenshot 2026-01-08 at 2 29 27 PM" src="https://github.com/user-attachments/assets/ebdd145d-efe1-4b71-9944-a934f59c4bbe" />
### What this shows:
* The price action of MSTR and BTC is similar,

### Figure 2. Daily Returns of MSTR and BTC (08/11/20 - Present)
<img width="1400" height="600" alt="daily_returns_btc_mstr" src="https://github.com/user-attachments/assets/0c7265bd-da41-4b1d-924c-6f17ac50c7df" />
### What this shows:
* MSTR (blue) consistently shows larger spikes than BTC (orange)
* BTC rarely exceeds + or - 15% swings, where as MSTR regularly hits + or - 20%.
* Volatility clustering is evident, especially in late 2021, March 2023 (bank crisis, particularly Silicon Valley Bank), and late 2024 (institutional adoption and Trump's 2024 win)

### Figure 3. MSTR vs BTC Returns Correlation
<img width="1000" height="800" alt="daily_returns_correlation" src="https://github.com/user-attachments/assets/1c844b77-3d08-43d4-a7a1-fccebe7736bc" />
### What this shows:
* Pearson (0.686) and Spearman (0.681) are nearly identical, which confirms that the correlation is profound and not distorted by outliers.
* MSTR moves roughly 1.1% for every 1% BTC moves which differs from the approximate "2.5x" volatility ratio that sources purport.
* When BTC moves + or - 10% or more, MSTR's response becomes less predictable, meaning MSTR amplifies or lags BTC's move. 

### 4.
<img width="1400" height="500" alt="relationship_overtime" src="https://github.com/user-attachments/assets/9290f284-d618-4eec-bfcf-bf0d1f0de993" />
#### What this shows:
* 2021: The flattest regression line of all which suggests that MSTR was less correlated to BTC when MSTR first began acquiring BTC.
* 2022: During what is now known as the "Crypto Winter," MSTR became heavily correlated to BTC, with the highest Spearman and Pearson ratios out of all FY trading years to date. Shared by Figure 1

### 5. 
<img width="1375" height="717" alt="returns_by_year" src="https://github.com/user-attachments/assets/e519a420-21b6-4fa6-83e7-75f9b29bcdbd" />

## Disclosure
Nothing in this project should be construed as financial advice. Do your own diligence prior to implementing any trading strategy.
