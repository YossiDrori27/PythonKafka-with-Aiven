from faker import Faker
import json
from kafka import KafkaProducer
import time
import sys
import os
import random
import argparse
from stockproducer import StockProvider


# Creating a Faker instance and seeding to have the same results every time we execute the script
fake = Faker()
Faker.seed(4321)

# function produce_msgs starts producing messages with Faker
def produce_msgs(cert_folder = 'Stocks',
                 hostname = 'kafka-stock-tickets-drori-a69e.aivencloud.com',
                 port = '28003',
                 topic_name = 'stock-indexs',
                 nr_messages = -1,
                 max_waiting_time_in_sec = 5,
                 subject = 'stock'):
        
        rootdir = os.getcwd()
        my_ssl_cafile = f"{rootdir}\\{cert_folder}\\ca.pe"
        my_ssl_certfile = f"{rootdir}\\{cert_folder}\\service.ce"
        my_ssl_keyfile = f"{rootdir}\\{cert_folder}\\service.key"
        print(my_ssl_keyfile)
        producer = KafkaProducer(
            bootstrap_servers='kafka-stock-tickets-drori-a69e.aivencloud.com:28003',
            security_protocol='SSL',
            ssl_cafile=my_ssl_cafile,
            ssl_certfile=my_ssl_certfile,
            ssl_keyfile=my_ssl_keyfile,
            value_serializer=lambda v: json.dumps(v).encode('ascii'),
            key_serializer=lambda v: json.dumps(v).encode('ascii'))

        if nr_messages <= 0:
            nr_messages = float('inf')
        i = 0
    
        fake.add_provider(StockProvider)

        while i < nr_messages:
            message, key = fake.produce_msg()
            print('Sending...key:{key} message:{message}'.format(key=key,message=message))

            #sending the message to Kafka
            producer.send(topic_name,
                          key=key,
                          value=message)
        
            # Sleeping time
            sleep_time = random.randint(0, int(max_waiting_time_in_sec * 10000))/10000
            print('Sleeping for...'+str(sleep_time)+'s')
            time.sleep(sleep_time)

            # Force flushing of all messages
            if (i % 100) == 0:
                producer.flush()
            i = i + 1
        producer.flush()

# calling the main produce_msgs function: parameters are:
#   * nr_messages: number of messages to produce
#   * max_waiting_time_in_sec: maximum waiting time in sec between messages

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cert-folder', help='Path to folder containing required Kafka certificates. Required --security-protocol equal SSL', required=False)
    parser.add_argument('--host', help='Kafka Host (obtained from Aiven console)', required=True)
    parser.add_argument('--port', help='Kafka Port (obtained from Aiven console)', required=True)
    parser.add_argument('--topic-name', help='Topic Name', required=True)
    parser.add_argument('--nr-messages', help='Number of messages to produce (0 for unlimited)', required=True)
    parser.add_argument('--max-waiting-time', help='Max waiting time between messages (0 for none)', required=True)
    args = parser.parse_args()
    p_cert_folder =args.cert_folder
    p_hostname =args.host
    p_port =args.port
    p_topic_name=args.topic_name
    print(args)
    produce_msgs(cert_folder=p_cert_folder,
                 hostname=p_hostname,
                 port=p_port,
                 topic_name=p_topic_name,
                 nr_messages=int(args.nr_messages),
                 max_waiting_time_in_sec=float(args.max_waiting_time)
                 )
    print(args.nr_messages)

if __name__ == '__main__':
    main()
