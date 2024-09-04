# extract_stock_data
This program provides the crest and trough occurances for a stock for the given number of years. 
The crest and trough reflects 10% corection between crest and trough. It does so by analyzing the 
yahoo finance data.
So for a given year, it will look for all the time span where the 10% or more corrections occured.

The program also predicts the next coming correction.

Program run and output:

>>python mystktool-3.py
Enter the stock ticker symbol: amzn
Enter the time period in years: 1
[*********************100%***********************]  1 of 1 completed

Crest and Trough pairs for AMZN over the past 1 year(s) with at least 9.999999999999998% difference:

Crest Date      Crest Value     Trough Date     Trough Value

------------------------------------------------------------
2023-09-13      144.85          2023-09-22      129.12
2024-07-31      186.98          2024-08-05      161.02

The average time between corrections is approximately 7 days.
Based on historical data, the next 10% correction is estimated to occur around 2024-09-06.

----------------------------------



