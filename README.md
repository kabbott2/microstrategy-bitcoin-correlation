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
### Figure 1. Daily Returns of MSTR and BTC (08/11/20 - Present)
<img width="1400" height="600" alt="daily_returns_btc_mstr" src="https://github.com/user-attachments/assets/0c7265bd-da41-4b1d-924c-6f17ac50c7df" />
### What this shows:
* MSTR (blue) consistently shows larger spikes than BTC (orange)
* BTC rarely exceeds + or - 15% swings, where as MSTR regularly hits + or - 20%.
* Volatility clustering is evident, especially in early 2021 (institutional acquisition), mid-2022 (beginning of the "Crypto Winter"), March 2023 (banking crisis, particularly Silicon Valley Bank), late 2024 (more institutional adoption and Trump's 2024 win), and early-to-mid 2025 (legislation and GENIUS Act).

### Figure 2. MSTR vs BTC Returns Correlation
<img width="1000" height="800" alt="daily_returns_correlation" src="https://github.com/user-attachments/assets/1c844b77-3d08-43d4-a7a1-fccebe7736bc" />
### What this shows:
* Pearson (0.686) and Spearman (0.681) are nearly identical, which confirms that the correlation is profound and not distorted by outliers.
* MSTR moves roughly 1.1% for every 1% BTC moves which differs from the approximate "2.5x" volatility ratio that sources purport.
* When BTC moves + or - 10% or more, MSTR's response becomes less predictable, meaning MSTR amplifies or lags BTC's move. 

### Figure 3. MSTR vs BTC Daily Returns by Year
<img width="1400" height="500" alt="relationship_overtime" src="https://github.com/user-attachments/assets/9290f284-d618-4eec-bfcf-bf0d1f0de993" />
#### What this shows:
* 2021: The flattest regression line of all which suggests that MSTR was less correlated to BTC when MSTR first began acquiring BTC.
* 2022: During what is now known as the "Crypto Winter," MSTR became heavily correlated to BTC, with the highest Spearman and Pearson ratios out of all FY trading years to date.
* 2023: A compressed range on both axes, as BTC rarely exceeded >10% returns or losses and MSTR >20% returns or losses. Tight clustering near the origin.
* 2024: A wild year. The steepest regression line and the widest scatter. Several outlier days shows MSTR making big moves on moderate BTC moves.
* 2025: Similar story to 2024 but with a narrower BTC range (+ or - 10%), perhaps due to the law of large numbers effect (larger market cap for BTC, more liquidity, and institutional participation).

### Figure 4. Pearson, Spearman, and Beta by Year
<img width="1375" height="717" alt="returns_by_year" src="https://github.com/user-attachments/assets/e519a420-21b6-4fa6-83e7-75f9b29bcdbd" />
#### What this shows:
* Pearson and Spearman correlations are roughly even, indicating MSTR-BTC are tightly correlated.
* 2022 showed the strongest correlation perhaps due to loss of faith in any security that was crypto-exposed, including DATCOs, BTC, Ethereum, etc.
* Beta has jumped +.53 since 2021! MSTR has become more leveraged to BTC over time, which figures as MSTR has acquired significantly more BTC since 2021, turning from a software company with ~some~ exposure to a DATCO with software exposure.

## Disclosure
Nothing in this project should be construed as financial advice. Do your own diligence prior to implementing any trading strategy.

## Easter Egg (Feel the AGI!)
<img width="388" height="747" alt="Screenshot 2026-01-09 at 5 03 08 PM" src="https://github.com/user-attachments/assets/56cf58f7-b358-404c-a4f3-d1add6742f93" />

