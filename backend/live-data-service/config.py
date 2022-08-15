from redis_om import get_redis_connection

redis = get_redis_connection(
    host='redis_server',
    port=6379
)