from flask import Flask, render_template, request
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# api
cg = CoinGeckoAPI()


time_now = datetime.now().replace(microsecond=0)


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



def converter(unix_delta):
#converting 13 numbers to 13 string numbers to 10 string to 10 integers
    good_delta = str(unix_delta)
    good_delta = good_delta[0:10]
    with_date = datetime.utcfromtimestamp(int(good_delta)).strftime('%Y-%m-%d %H:%M:%S')
    without_date = with_date[10:]
    return without_date

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
                           trendy_coins=lijst_trendy_coins, names=names, prices=prices, thumbs=thumbs,
                           list_coins=coin_list_a,time=time_now
                           )


@app.route('/coin', methods=['POST'])
def coin():
    list_of_times = []
    list_of_prices = []
    try:
        crypto_search = request.form['crypto'].lower()
    except ValueError:
        print('invalid input')
    # 0 = time unix timestamp. maybe convert it?
    # 1 = the price
    price_market_volume = cg.get_coin_market_chart_by_id(id=crypto_search, vs_currency='eur', days=0.1)
    first_timedelta = price_market_volume['prices'][0][0]

    for num in range(0, 10):
        price_time_data = price_market_volume['prices'][num][0]
        price = price_market_volume['prices'][num][1]
        time = converter(price_time_data)
        list_of_times.append(time)
        list_of_prices.append(price)

    plt.plot(list_of_times, list_of_prices)
    plt.title(f"{crypto_search.title()} by Thijs Geertman. DATA: CoinGecko" )
    plt.xlabel('Time')
    plt.xlim(0, 5)
    plt.ylabel('Price in EUR')
    pic = plt.savefig('static/img/coin.png')



    return render_template(f'coin.html', crypto_search=crypto_search,pic=pic)


if __name__ == "__main__":
    app.run(debug=True)
