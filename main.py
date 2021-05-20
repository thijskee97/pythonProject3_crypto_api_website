from flask import Flask, render_template, request
from pycoingecko import CoinGeckoAPI
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# api
cg = CoinGeckoAPI()

# datetime
now = datetime.datetime.now()
t = now.strftime("%d/%m/%Y, %H:%M:%S")

# populair homepage coins
coins = cg.get_price(ids=['bitcoin', 'ethereum', 'litecoin', 'dogecoin'], vs_currencies='eur')
bitcoin = coins['bitcoin']['eur']
eth = coins['ethereum']['eur']
lite = coins['litecoin']['eur']
doge = coins['dogecoin']['eur']

bitcoin = f"€{bitcoin}"
eth = f"€{eth}"
lite = f"€{lite}"
doge = f"€{doge}"

coins = cg.get_search_trending()
list_coins = cg.get_coins_list()
coin_list_a = []

# all coins list
for coin in list_coins:
    c = coin['id']
    coin_list_a.append(c)

# lists
lijst_trendy_coins = []
names = []
prices = []
thumbs = []

# get 7 trendy coins
for num in range(0, 6):
    name = coins['coins'][num]["item"]['name']
    price = coins['coins'][num]["item"]['price_btc']
    thumb = coins['coins'][num]["item"]['large']
    new_coin = (name, price, thumb)
    names.append(name)
    prices.append(price)
    thumbs.append(thumb)
    lijst_trendy_coins.append(name)
    lijst_trendy_coins.append(thumb)


# backend website

@app.route('/')
def home():
    return render_template('index.html', bitcoin=bitcoin, lite=lite, eth=eth, doge=doge,
                           trendy_coins=lijst_trendy_coins, names=names, prices=prices, thumbs=thumbs, time=t,
                           list_coins=coin_list_a
                           )


@app.route('/test', methods=['POST'])
def test():
    crypto_search = request.form['crypto'].lower()
    sc = cg.get_coin_market_chart_by_id(id=crypto_search, vs_currency='eur', days=24)
    list_sc_prices = sc['prices'][0:10][0]
    print(list_sc_prices)

    return render_template(f'test.html', crypto_search=crypto_search, data=sc)


if __name__ == "__main__":
    app.run(debug=True)
