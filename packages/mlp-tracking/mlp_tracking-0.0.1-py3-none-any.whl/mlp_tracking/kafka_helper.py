# pip install confluent-kafka
from confluent_kafka import Producer
from functools import lru_cache


SECURITY_PROTOCOL = "SASL_PLAINTEXT"
# SECURITY_PROTOCOL = "SASL_SSL"

SASL_MECHANISM = "PLAIN"


@lru_cache(maxsize=None)
def get_kafka_producer(
    kafka_servers:str,
    kafka_username:str,
    kafka_password:str,
):
    conf = {
        'bootstrap.servers': kafka_servers,
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.mechanisms': SASL_MECHANISM,
        'sasl.username': kafka_username,
        'sasl.password': kafka_password,
    }
    return Producer(conf)
