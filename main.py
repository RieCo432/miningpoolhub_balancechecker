import requests
import json
import time

api_key = "e798d89ba8e4debc2f3904f23e0fbaa99dc3c3a85b63924d63375b2057231a3b"

request_string = "https://miningpoolhub.com/index.php?page=api&action=getuserallbalances&api_key=" + api_key

bittrex_getticker_request_string = "https://bittrex.com/api/v1.1/public/getticker?market=BTC-"

symbol_dict = {"auroracoin-qubit": "AUR",
               "bitcoin-cash": "BCC",
               "bitcoin-gold": "BTG",
               "dash": "DASH",
               "digibyte-skein": "DGB",
               "ethereum": "ETH",
               "ethereum-classic": "ETC",
               "expanse": "EXP",
               "feathercoin": "FTC",
               "gamecredits": "GAME",
               "geocoin": "GEO",
               "groestlcoin": "GRS",
               "litecoin": "LTC",
               "monacoin": "MONA",
               "monero": "XMR",
               "musicoin": "MUSIC",
               "myriadcoin": "XMY",
               "startcoin": "START",
               "verge-scrypt": "XVG",
               "vertcoin": "VTC",
               "zcash": "ZEC",
               "zclassic": "ZCL",
               "zcoin": "XZC",
               "zencash": "ZEN"}


def calculate_btc_equivalent(coin_id, amount):
    coinmarkedcap_json = json.loads(requests.get("https://api.coinmarketcap.com/v1/ticker/").text)

    poloniex_json = json.loads(requests.get("https://poloniex.com/public?command=returnTicker").text)

    current_coin_data_coinmarketcap = filter(lambda coin: coin["id"] == coin_id, coinmarkedcap_json)
    if coin_id in symbol_dict:
        current_coin_data_bittrex = json.loads(
            requests.get(bittrex_getticker_request_string + symbol_dict[coin_id]).text)
    if coin_id in symbol_dict and current_coin_data_bittrex["success"]:
        exchange_rate = current_coin_data_bittrex["result"]["Last"]
        coin_btc_equivalent = amount * float(exchange_rate)
        print("Coin: " + str(coin_id))
        print("Amount: " + str(amount))
        print("Exchange rate: " + str(exchange_rate))
        print("BTC equiv. : " + str(coin_btc_equivalent) + "\n")
        return coin_btc_equivalent
    elif coin_id in symbol_dict and "BTC_" + symbol_dict[coin_id] in poloniex_json:
        current_coin_data_poloniex = poloniex_json["BTC_" + symbol_dict[coin_id]]
        exchange_rate = current_coin_data_poloniex["last"]
        coin_btc_equivalent = amount * float(exchange_rate)
        print("Coin: " + str(coin_id))
        print("Amount: " + str(amount))
        print("Exchange rate: " + str(exchange_rate))
        print("BTC equiv. : " + str(coin_btc_equivalent) + "\n")
        return coin_btc_equivalent
    elif len(current_coin_data_coinmarketcap) is not 0:
        exchange_rate = current_coin_data_coinmarketcap[0]["price_btc"]
        coin_btc_equivalent = amount * float(exchange_rate)
        print("Coin: " + str(coin_id))
        print("Amount: " + str(amount))
        print("Exchange rate: " + str(exchange_rate))
        print("BTC equiv. : " + str(coin_btc_equivalent) + "\n")
        return coin_btc_equivalent
    else:
        print("Coin: " + str(coin_id))
        print("Amount: " + str(amount))
        print("Error: No information on exchange rate!\n")
        return 0.0


def check_balance_btc_equivalent():
    total_btc_value = 0.0

    miningpoolhub_json = json.loads(requests.get(request_string).text)

    for coin_balance in miningpoolhub_json["getuserallbalances"]["data"]:
        combined_coin_balance = coin_balance["confirmed"] + coin_balance["unconfirmed"] + coin_balance["ae_confirmed"] + \
                                coin_balance["ae_unconfirmed"] + coin_balance["exchange"]
        coin_id = coin_balance["coin"]
        total_btc_value = total_btc_value + calculate_btc_equivalent(coin_id, combined_coin_balance)

    total_btc_value = format(float(round(total_btc_value * 100000000)) / 100000000, ".8f")
    print("Total BTC equiv.: " + str(total_btc_value))

    return total_btc_value


def log_btc_equivalent(amount):
    with open("file.log", "a") as logfile:
        logfile.write(time.strftime("%Y/%m/%d-%H:%M:%S\t") + amount + "\n")


while True:
    total_btc_equivalent = check_balance_btc_equivalent()
    log_btc_equivalent(total_btc_equivalent)
    time.sleep(10*60)
