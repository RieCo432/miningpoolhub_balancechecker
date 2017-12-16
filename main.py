import requests
import json

api_key = "e798d89ba8e4debc2f3904f23e0fbaa99dc3c3a85b63924d63375b2057231a3b"

request_string = "https://miningpoolhub.com/index.php?page=api&action=getuserallbalances&api_key=" + api_key

miningpoolhub_json = json.loads(requests.get(request_string).text)

coinmarkedcap_json = json.loads(requests.get("https://api.coinmarketcap.com/v1/ticker/").text)

total_btc_equivalent = 0.0


def calculate_btc_equivalent(coin_id, amount):
    current_coin_data = filter(lambda coin: coin["id"] == coin_id, coinmarkedcap_json)
    if len(current_coin_data) is not 0:
        exchange_rate = current_coin_data[0]["price_btc"]
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


for coin_balance in miningpoolhub_json["getuserallbalances"]["data"]:
    combined_coin_balance = coin_balance["confirmed"] + coin_balance["unconfirmed"] + coin_balance["ae_confirmed"] + \
                            coin_balance["ae_unconfirmed"] + coin_balance["exchange"]
    coin_id = coin_balance["coin"]
    total_btc_equivalent = total_btc_equivalent + calculate_btc_equivalent(coin_id, combined_coin_balance)


total_btc_equivalent = format(float(round(total_btc_equivalent*100000000)) / 100000000, ".8f")
print("Total BTC equiv.: " + str(total_btc_equivalent))
