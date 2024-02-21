import redis

client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

client.set('example_key', 'example_value')
print(client.get('example_key'))
