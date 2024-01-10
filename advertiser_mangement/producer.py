from confluent_kafka import Producer
import json


class KafkaTransactionProducer:
    def __init__(self, bootstrap_servers='localhost:29092'):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def produce_transaction(self, transaction_data):
        topic = "transaction-consumer"
        self.producer.produce(topic, key=str(
            transaction_data['ad_id']), value=json.dumps(transaction_data))
        self.producer.flush()
