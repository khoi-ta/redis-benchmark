import time
import json
from util import *
from speed_redis import *

class Scenarios():
    '''
        ===================== Inserting\n
        Insert order to redis\n
        Insert transaction to redis\n
        Update position in redis\n
        ===================== Getting\n
        Get order by orderId in redis\n
        Get transaction by transaction id in redis => Get position in redis by this transaction hash
    '''
    def __init__(self) -> None:
        self.client = SpeedRedis()
        with open("order_mock.json") as f:
            self.orders = json.load(f)


    def benchmark_string(self):
        start = time.time() * 1000
        for order in self.orders:
            self.client.set_message(order["client_order_id"], json.dumps(order), 10)
            
        for order in self.orders:
            value = self.client.get_message(order["client_order_id"])
            transaction = {
                "transaction_id": value["client_order_id"],
                "ticker_symbol": value["ticker_symbol"],
                "exchange_id": "HNX",
                "portfolio_id": value["portfolio_id"],
                "order_id": value["client_order_duid"],
                "side": value["order_side"],
                "matched_quantity": value["matched_quantity"],
                "matched_price": value["avg_price"],
                "matched_datetime": time.time(),
                "transaction_type": "trading",
                "fee": 0.07,
                "delivery_date": "null",
            }
            self.client.set_message(order['client_order_duid'], json.dumps(transaction), expired=10)

        for order in self.orders:
            transaction = self.client.get_message(order["client_order_duid"])
            position = self.client.get_message("POSITION")
            if position is not None:
                position = update_position(position, transaction)
            else:
                newPosition = {}
                position = update_position(newPosition, transaction)
            self.client.set_message("POSITION", json.dumps(position), expired=10)

        for order in self.orders:
            transaction = self.client.get_message(order["client_order_duid"])
            position = self.client.get_message("POSITION")
            key = f"{transaction['exchange_id']}:{transaction['ticker_symbol']}"
            value = position[key]["long"][f"{transaction['matched_price']}"] if transaction["side"] == "BUY" else \
                    position[key]["short"][f"{transaction['matched_price']}"] 
            
            if value != transaction["transaction_id"]:
                raise Exception("Wrong Transaction")

        end = time.time() * 1000
        print(f"String test: {end - start}")


    def benchmark_json(self):
        start = time.time() * 1000
        for order in self.orders:
            self.client.set_json(order["client_order_id"], order, expired=10)
            
        for order in self.orders:
            value = self.client.get_json(order["client_order_id"])
            transaction = {
                "transaction_id": value["client_order_id"],
                "ticker_symbol": value["ticker_symbol"],
                "exchange_id": "HNX",
                "portfolio_id": value["portfolio_id"],
                "order_id": value["client_order_duid"],
                "side": value["order_side"],
                "matched_quantity": value["matched_quantity"],
                "matched_price": value["avg_price"],
                "matched_datetime": time.time(),
                "transaction_type": "trading",
                "fee": 0.07,
                "delivery_date": "null",
            }
            self.client.set_json(order['client_order_duid'], transaction, expired=10)

        for order in self.orders:
            transaction = self.client.get_json(order["client_order_duid"])
            position = self.client.get_json("POSITION")
            if position is not None:
                position = update_position(position, transaction)
            else:
                newPosition = {}
                position = update_position(newPosition, transaction)
            self.client.set_json("POSITION", position, expired=10)

        for order in self.orders:
            transaction = self.client.get_json(order["client_order_duid"])
            position = self.client.get_json("POSITION")
            key = f"{transaction['exchange_id']}:{transaction['ticker_symbol']}"
            value = position[key]["long"][f"{transaction['matched_price']}"] if transaction["side"] == "BUY" else \
                    position[key]["short"][f"{transaction['matched_price']}"] 
            
            if value != transaction["transaction_id"]:
                raise Exception("Wrong Transaction")

        end = time.time() * 1000
        print(f"Json test: {end - start}")

    def run(self):
        self.benchmark_string()
        time.sleep(10)
        self.benchmark_json()
        time.sleep(10)

if __name__ == "__main__":
    scenarios_test = Scenarios()
    scenarios_test.run()
