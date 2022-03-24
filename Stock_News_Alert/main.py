import requests
from twilio.rest import Client
from datetime import date, timedelta
import os

STOCK_SYMBOL = "AAPL"
COMPANY_NAME = "APPLE"
alphavantage_api_key = os.environ.get('ALPHAVANTAGE_KEY')
newsapi_key = os.environ.get('NEWSAPI_KEY')

my_twilio_number = os.environ.get('MY_TWILIO_NUMBER')
receive_number = os.environ.get('MY_RECEIVE_NUMBER')
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# API parameters
check_for = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_SYMBOL,
    "apikey": alphavantage_api_key
}

# request
response = requests.get(url="https://www.alphavantage.co/query", params=check_for)
response.raise_for_status()

# get date for yesterday and 2 days ago using datetime module
today = date.today()
_yesterday = today - timedelta(days=1)
_two_days_ago = today - timedelta(days=2)

# calculate percentage difference
yesterday = float(response.json()["Time Series (Daily)"][str(_yesterday)]['4. close'])
two_days_ago = float(response.json()["Time Series (Daily)"][str(_two_days_ago)]['4. close'])
diff = round((yesterday - two_days_ago), 4)
percentage_diff = round(((diff/two_days_ago) * 100), 2)
print(percentage_diff)

if percentage_diff > 0:
    the_symbol = "🔺"
else:
    the_symbol = "🔻"

# if percentage diff meets the criteria in the if statement below, fetch top news from the company
# also send sms notification
if percentage_diff > 4 or percentage_diff < -4:
    check_for_news = {
        "q": "tesla",
        "from": str(_yesterday),
        "to": str(today),
        "sortBy": "popularity",
        "apikey": newsapi_key
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=check_for_news)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    # list with first 3 articles
    three_articles = articles[:3]

    list_articles = [f"{STOCK_SYMBOL}: {the_symbol} {percentage_diff}%\nHeadline: {article['title']}\nBrief: {article['description']}" for article in three_articles]

    # send each article via sms
    client = Client(account_sid, auth_token)
    for article in list_articles:
        message = client.messages.create(
            body=article,
            from_=my_twilio_number,
            to=receive_number
        )
