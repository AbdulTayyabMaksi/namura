from __future__ import annotations

import re
from typing import Any

MARKET_KEYWORDS = [
    "stock", "share", "shares", "price", "nifty", "sensex", "market cap",
    "dividend", "pe ratio", "p/e", "ipo", "bse", "nse", "trading",
    "portfolio", "mutual fund", "etf", "equity", "company", "ticker",
    "reliance", "tcs", "infosys", "hdfc", "wipro", "apple", "google",
    "microsoft", "tesla", "amazon", "bitcoin", "crypto",
]

INDIAN_TICKER_MAP: dict[str, str] = {
    "reliance": "RELIANCE.NS",
    "ril": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS",
    "hdfc": "HDFCBANK.NS",
    "hdfc bank": "HDFCBANK.NS",
    "icici": "ICICIBANK.NS",
    "sbi": "SBIN.NS",
    "wipro": "WIPRO.NS",
    "bharti": "BHARTIARTL.NS",
    "airtel": "BHARTIARTL.NS",
    "itc": "ITC.NS",
    "tata motors": "TATASTEEL.NS",
    "tata steel": "TATASTEEL.NS",
    "maruti": "MARUTI.NS",
    "asian paints": "ASIANPAINT.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "kotak": "KOTAKBANK.NS",
    "axis bank": "AXISBANK.NS",
    "l&t": "LT.NS",
    "sun pharma": "SUNPHARMA.NS",
    "adani": "ADANIENT.NS",
    "zomato": "ZOMATO.NS",
    "paytm": "PAYTM.NS",
    "mrf": "MRF.NS",
    "mrf tyres": "MRF.NS",
    "hindustan unilever": "HINDUNILVR.NS",
    "hul": "HINDUNILVR.NS",
    "bajaj auto": "BAJAJ-AUTO.NS",
    "asian paints": "ASIANPAINT.NS",
    "nestle": "NESTLEIND.NS",
    "hcl": "HCLTECH.NS",
    "tech mahindra": "TECHM.NS",
    "sun pharma": "SUNPHARMA.NS",
    "ongc": "ONGC.NS",
    "ntpc": "NTPC.NS",
    "power grid": "POWERGRID.NS",
    "coal india": "COALINDIA.NS",
    "jio financial": "JIOFIN.NS",
    "titan": "TITAN.NS",
    "mahindra": "M&M.NS",
}

US_TICKER_MAP: dict[str, str] = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META",
    "facebook": "META",
    "nvidia": "NVDA",
    "netflix": "NFLX",
}


def is_market_query(message: str) -> bool:
    msg = message.lower()
    return any(k in msg for k in MARKET_KEYWORDS)


def _extract_tickers(message: str) -> list[str]:
    msg = message.lower()
    found: list[str] = []

    for name, ticker in {**INDIAN_TICKER_MAP, **US_TICKER_MAP}.items():
        if name in msg and ticker not in found:
            found.append(ticker)

    # Raw NSE-style symbols e.g. RELIANCE, TCS (2-12 uppercase letters)
    for match in re.findall(r"\b([A-Z]{2,12})\b", message):
        candidate = match if "." in match else f"{match}.NS"
        if candidate not in found:
            found.append(candidate)

    return found[:5]


def _fetch_ticker_info(ticker: str) -> dict[str, Any] | None:
    try:
        import yfinance as yf

        stock = yf.Ticker(ticker)
        info = stock.info or {}
        hist = stock.history(period="5d")

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        if current_price is None and not hist.empty:
            current_price = float(hist["Close"].iloc[-1])

        return {
            "ticker": ticker,
            "name": info.get("longName") or info.get("shortName") or ticker,
            "price": current_price,
            "currency": info.get("currency", "INR"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE") or info.get("forwardPE"),
            "dividend_yield": info.get("dividendYield"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "description": (info.get("longBusinessSummary") or "")[:400],
        }
    except Exception:
        return None


def fetch_market_context(message: str) -> str:
    if not is_market_query(message):
        return ""

    tickers = _extract_tickers(message)
    if not tickers:
        # Try nifty/sensex
        msg = message.lower()
        if "nifty" in msg:
            tickers = ["^NSEI"]
        elif "sensex" in msg:
            tickers = ["^BSESN"]

    if not tickers:
        return ""

    lines = ["LIVE MARKET DATA (fetched just now):"]
    for ticker in tickers:
        data = _fetch_ticker_info(ticker)
        if not data:
            continue
        price_str = f"{data['currency']} {data['price']:,.2f}" if data.get("price") else "N/A"
        lines.append(f"\n• {data['name']} ({data['ticker']})")
        lines.append(f"  Price: {price_str}")
        if data.get("pe_ratio"):
            lines.append(f"  P/E Ratio: {data['pe_ratio']:.2f}")
        if data.get("market_cap"):
            lines.append(f"  Market Cap: {data['currency']} {data['market_cap']:,.0f}")
        if data.get("dividend_yield") and data["dividend_yield"] < 0.5:
            lines.append(f"  Dividend Yield: {data['dividend_yield']:.2%}")
        if data.get("52w_high") and data.get("52w_low"):
            lines.append(f"  52W Range: {data['52w_low']:,.2f} – {data['52w_high']:,.2f}")
        if data.get("sector"):
            lines.append(f"  Sector: {data['sector']}")
        if data.get("description"):
            lines.append(f"  About: {data['description']}")

    return "\n".join(lines) if len(lines) > 1 else ""
