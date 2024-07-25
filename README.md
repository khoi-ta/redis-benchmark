# Benchmark storing method in Redis
- [x] Storing object by json.dump, json.loads
- [x] Storing object by hash of redis
- [x] Storing object by json module of redis
- [x] Storing object by protocol buffer
- [x] Storing object by pickle
- [x] Storing object by message package  
# Redis installation
Redis stack is used for benchmarking. To install the redis stack with docker, use the command below
```
docker run -d --name speed-redis -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
# Set up
- Object data is stored at ```mock.json``` file, we create more than 1000 orders for testing. An example of an order:
```
{
    "orderId": "66a0f9d28c7a97ac474ce5c4",
    "externalId": "91286431-ac65-46c9-b149-0b0b5214c9d1",
    "side": "BUY",
    "price": "$1,395.66",
    "amount": 1,
    "status": "NEW",
    "orderType": "MARKET",
    "rawText": "Excepteur quis anim ullamco amet deserunt est nisi irure non."
}
```

- The benchmark testing is created on Mac Pro Intel 2019, 2.4 GHz Quad-Core with 8GB RAM
- The objects will be sequencially stored in redis and then sequecially get by its key
- The result is calculated in milisecond
# Benchmark result
The exact milisecond is depend on each execution but for most of the testing times json parsing is slower than others serialization/deserialization method. hset and json module of redis are the two slowest with more than a second
```
string parser: 740.43115234375
hset duration: 1118.1689453125
json module redis: 1121.400634765625
Protocol buffer: 722.647216796875
Message package: 728.159912109375
Pickle: 729.4521484375
```
