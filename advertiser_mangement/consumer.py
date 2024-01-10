from confluent_kafka import Consumer, KafkaError
import json
from .models import Click, View, Transaction


class KafkaTransactionConsumer:
    def __init__(self, bootstrap_servers='localhost:29092', group_id='my_consumer_group'):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

    def consume_transactions(self):
        topic = "transaction-consumer"
        self.consumer.subscribe([topic])

        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            transaction_data = json.loads(msg.value().decode('utf-8'))

            Transaction.objects.create(**transaction_data)
