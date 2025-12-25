import yfinance as yf
import plotext as plt

class Stocks:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_stock_price(self):
        stock = yf.Ticker(self.ticker)
        return stock.info.get('regularMarketPrice') or stock.info.get('currentPrice')
    
    def get_stock_notes(self):
        stock = yf.Ticker(self.ticker)
        return stock.info.get('longBusinessSummary', 'No notes available')

    def get_stock_chart(self):
        stock = yf.Ticker(self.ticker)
        data = stock.history(period='5d')  # Last week (5 trading days)
        
        if data.empty:
            print(f"No data found for {self.ticker}")
            return

        plt.clf()
        plt.theme('dark')
        
        prices = data['Close'].tolist()
        # Use indices for x-axis and set labels manually to avoid date parsing errors
        x = list(range(len(prices)))
        xticks_labels = [d.strftime('%m-%d') for d in data.index]
        
        plt.plot(x, prices, label=f"{self.ticker} Close")
        plt.xticks(x, xticks_labels)
        
        plt.title(f"{self.ticker} Stock Chart (Last Week)")
        
        # Black terminal styling with white text
        plt.canvas_color('black')
        plt.axes_color('black')
        plt.ticks_color('white')
        
        plt.show()
