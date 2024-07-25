import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import msgpack
import pickle
from protocol_buffers.message_pb2 import *
from speed_redis import *

class Benchmark():
    def __init__(self) -> None:
        self.client = SpeedRedis()
        with open("mock.json") as f:
            self.orders = json.load(f)
    
    def benchmark_string(self):
        start = time.time() * 1000
        for order in self.orders:
            self.client.set_message(order["orderId"], json.dumps(order))

        for order in self.orders:
            value = self.client.get_message(order["orderId"])
        end = time.time() * 1000
        duration = end - start
        print(f"string parser: {duration}")
        return duration

    def benchmark_hset(self):
        start = time.time() * 1000
        for order in self.orders:
            self.client.hset(order["orderId"], order)
        
        keys=["orderId", "externalId", "side", "price", "amount", "status", "orderType", "rawText"]
        for order in self.orders:
            value = self.client.hmget(order["orderId"], keys=keys)
        end = time.time() * 1000
        duration = end - start
        print(f"hset duration: {duration}")
        return duration

    def benchmark_json(self):
        start = time.time() * 1000
        for order in self.orders:
            self.client.set_json(f"{order['orderId']}:json", order)

        for order in self.orders:
            self.client.get_json(order["orderId"])
        
        end = time.time() * 1000
        duration = end - start
        print(f"json module redis: {duration}")
        return duration

    def benchmark_protocol_buffers(self):
        start = time.time() * 1000
        message = OrderMessage()
     
        for order in self.orders:
            message.orderId = order["orderId"]
            message.externalId = order["externalId"]
            message.side = BUY if order["side"] == "BUY" else SELL
            message.amount = order["amount"]
            message.price = order["price"]
            
            if order["status"] == "NEW": 
                message.status = NEW
            elif order["status"] == "PENDING":
                message.status = PENDING
            else:
                message.status = FILL
            message.orderType = MARKET if order["orderType"] == "MARKET" else LIMIT
            message.rawText = order["rawText"]
            serialized_message = message.SerializeToString()
            self.client.set_message(message.orderId, serialized_message)
       
        for order in self.orders:
            value = self.client.get_message(message.orderId, is_json=False)
            retrieved = OrderMessage()
            retrieved.ParseFromString(value)
        end = time.time() * 1000
        duration = end - start
        print(f"Protocol buffer: {duration}")
        return duration
    
    def benchmark_pickle(self):
        start = time.time() * 1000
        for order in self.orders:
          serilized_value = pickle.dumps(order)
          self.client.set_message(order["orderId"], serilized_value)
        
        for order in self.orders:
          value = self.client.get_message(order["orderId"], is_json=False)
          deserialized_value = pickle.loads(value)
        
        end = time.time() * 1000
        duration = end - start
        print(f"Pickle: {duration}")
        return duration

    def benchmark_msgpack(self):
        start = time.time() * 1000
        for order in self.orders:
          packed_value = msgpack.packb(order)
          self.client.set_message(order["orderId"], packed_value)
        
        for order in self.orders:
          value = self.client.get_message(order["orderId"], is_json=False)
          unpk = msgpack.unpackb(value)
        
        end = time.time() * 1000
        duration = end - start
        print(f"Message package: {duration}")
        return duration

    def run(self):
        values = []
        for i in range(10):
            print(f"iter {i + 1}")
            dt = self.benchmark_string()
            time.sleep(2)
            dhs = self.benchmark_hset()
            time.sleep(2)
            djs = self.benchmark_json()
            time.sleep(2)
            dpb = self.benchmark_protocol_buffers()
            time.sleep(2)
            dmp = self.benchmark_msgpack()
            time.sleep(2)
            dp = self.benchmark_pickle()
            values.append([dt, dhs, djs, dpb, dmp, dp])
    
        df = pd.DataFrame(values, columns=["string", "hset", "json", "protocol buffers", "message package", "pickle"])
        ax = df.plot(title='Redis benchmark', xlabel='Iteration', ylabel='Mili seconds')
        ax.legend(title='Columns')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.savefig('benchmark.png')
        plt.show()

if __name__ == "__main__":
    bm = Benchmark()
    bm.run()
    

    