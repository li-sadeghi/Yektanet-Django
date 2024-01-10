import json
from Yektanet.settings import KAFKA_BOOTSTRAP_SERVERS
from advertiser_mangement.constants import VIEW_TRANSACTION_TOPIC
from advertiser_mangement.models import Transaction
from kafka import KafkaProducer, KafkaConsumer


def view_transaction_producer(transaction):
    transaction_data = {
        'ad_id': transaction.ad.id,
        "time": transaction.time.isoformat(),
        "type": transaction.type,
        "cost": transaction.cost,
    }

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    producer.send(VIEW_TRANSACTION_TOPIC, transaction_data)


def view_transaction_consumer():
    pass