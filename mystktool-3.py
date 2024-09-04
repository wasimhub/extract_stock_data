import yfinance as yf
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from datetime import timedelta

def analyze_stock(ticker: str, years: int, threshold: float = 0.9):
    # Download stock data for the specified time period
    stock_data = yf.download(ticker, period=f"{years}y")
    
    if stock_data.empty:
        print("No data found for the given ticker and time period.")
        return

    # Use the 'Adj Close' price for analysis
    prices = stock_data['Adj Close'].values
    dates = stock_data.index

    # Find the crests (peaks) in the stock price data
    crests, _ = find_peaks(prices)
    
    # Find the troughs (negative peaks) in the stock price data
    troughs, _ = find_peaks(-prices)
    
    # Sort crests and troughs
    crests = sorted(crests)
    troughs = sorted(troughs)
    
    results = []
    trough_index = 0
    time_differences = []
    
    for crest in crests:
        # Find the next trough after the crest
        while trough_index < len(troughs) and troughs[trough_index] <= crest:
            trough_index += 1
        if trough_index >= len(troughs):
            break
        trough = troughs[trough_index]
        crest_value = prices[crest]
        trough_value = prices[trough]
        crest_date = dates[crest].strftime('%Y-%m-%d')
        trough_date = dates[trough].strftime('%Y-%m-%d')
        
        # Check for the threshold difference
        if trough_value <= crest_value * threshold:
            results.append((crest_date, crest_value, trough_date, trough_value))
            time_diff = dates[trough] - dates[crest]
            time_differences.append(time_diff)
            # Move to the next trough to avoid overlapping
            trough_index += 1

    # Print the results in a formatted table
    if results:
        print(f"\nCrest and Trough pairs for {ticker.upper()} over the past {years} year(s) with at least {(1 - threshold)*100}% difference:\n")
        print(f"{'Crest Date':<15} {'Crest Value':<15} {'Trough Date':<15} {'Trough Value':<15}")
        print("-" * 60)
        for crest_date, crest, trough_date, trough in results:
            print(f"{crest_date:<15} {crest:<15.2f} {trough_date:<15} {trough:<15.2f}")
    else:
        print("\nNo crest and trough pairs found with the specified difference threshold.")

    # Predicting the next correction
    if time_differences:
        avg_time_diff = sum(time_differences, timedelta(0)) / len(time_differences)
        last_crest_date = dates[crests[-1]]
        predicted_next_correction_date = last_crest_date + avg_time_diff
        print(f"\nThe average time between corrections is approximately {avg_time_diff.days} days.")
        print(f"Based on historical data, the next 10% correction is estimated to occur around {predicted_next_correction_date.strftime('%Y-%m-%d')}.")
    else:
        print("\nNot enough data to predict the next correction.")

# Example usage:
if __name__ == "__main__":
    ticker_symbol = input("Enter the stock ticker symbol: ").strip().upper()
    try:
        time_period = int(input("Enter the time period in years: "))
        if time_period <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input for time period. Please enter a positive integer value.")
        exit(1)
    analyze_stock(ticker_symbol, time_period)
