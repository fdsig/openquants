import time
import plotext as plt
import yfinance as yf
import pandas as pd
import sys
import select
import tty
import termios

def get_key():
    """Detects key presses without waiting for Enter."""
    if not sys.stdin.isatty():
        return None
    fd = sys.stdin.fileno()
    try:
        old_settings = termios.tcgetattr(fd)
    except termios.error:
        return None
        
    try:
        tty.setraw(fd)
        # Use select to check if input is available
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            if key == '\x1b': # Potential arrow key
                # Read next two characters for arrow keys
                rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                if rlist:
                    key += sys.stdin.read(2)
            return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def streaming_chart(tickers, duration_minutes=60, interval_seconds=30):
    current_index = 0
    num_tickers = len(tickers)
    
    plt.theme('dark')
    start_time = time.time()
    last_fetch_time = 0
    df = pd.DataFrame()
    
    print("Initializing Interactive Streaming Chart (Last 2 Weeks, Hourly)...")
    print("Controls: 'n' or '>' (Next) | 'b' or '<' (Back) | 'q' (Quit)")
    time.sleep(2)
    
    try:
        while time.time() - start_time < duration_minutes * 60:
            # 1. Fetch data every interval_seconds
            if time.time() - last_fetch_time > interval_seconds:
                # Fetch 2 weeks of hourly data
                df = yf.download(tickers, period='2wk', interval='1h', progress=False)
                last_fetch_time = time.time()
            
            if not df.empty:
                ticker = tickers[current_index]
                
                plt.clf()
                plt.clt() # Clear terminal
                
                # 2. Extract price data
                try:
                    if isinstance(df['Close'], pd.Series):
                        prices = df['Close'].dropna()
                    else:
                        prices = df['Close'][ticker].dropna()
                        
                    if not prices.empty:
                        price_values = prices.tolist()
                        time_labels = [d.strftime('%m-%d %H:00') for d in prices.index]
                        
                        # 3. Build the Single Chart
                        plt.title(f"STOCK: {ticker} - LAST 2 WEEKS (HOURLY)")
                        plt.plot(price_values, label=f"{ticker} Price", marker="braille", color="cyan")
                        
                        # Format X-axis: Increment by 6 hours
                        indices = list(range(len(time_labels)))
                        # Since interval='1h', a step of 6 gives 6-hour increments
                        step = 6
                        plt.xticks(indices[::step], time_labels[::step])
                        
                        plt.xlabel("Date & Hour (6h Increments)")
                        plt.ylabel("Price (USD)")
                        plt.canvas_color('black')
                        plt.axes_color('black')
                        plt.ticks_color('white')
                        
                        # Show navigation help in the chart area
                        plt.show()
                        print(f"\n[Ticker {current_index + 1}/{num_tickers}] Viewing: {ticker}")
                        print("Controls: 'b' Back | 'n' Next | 'q' Quit")
                except Exception as e:
                    print(f"Error processing {ticker}: {e}")

            # 4. Handle Keyboard Input
            key = get_key()
            # Support arrows, n/b, and shevrons
            if key in ['\x1b[D', 'b', 'B', '<', ',']: # Left/Back
                current_index = (current_index - 1) % num_tickers
            elif key in ['\x1b[C', 'n', 'N', '>', '.']: # Right/Next
                current_index = (current_index + 1) % num_tickers
            elif key in ['q', 'Q', '\x03']: # 'q' or Ctrl+C
                break
                
            # Short sleep to prevent CPU spiking while still being responsive
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
    finally:
        plt.clt()

if __name__ == "__main__":
    # Core Tech + AI Cloud/Compute + Commodities (Oil, Gas, Gold)
    tickers = [
        "AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "CRWV", 
        "NVDA", "AMD", "ORCL", "META", "SMCI", "VRT",
        "CL=F", "NG=F", "GC=F"
    ]
    streaming_chart(tickers)
