# Python Fake Data Producer for Apache Kafka®

## Description

**Python Fake Data Producer for Apache Kafka®** is a complete demo app allowing you to quickly produce a Python fake Pizza-based streaming dataset and push it to an Apache Kafka® topic. It gives an example on how easy is to create great fake streaming data to feed Apache Kafka.

* **Apache Kafka**: a [distributed streaming platform](https://kafka.apache.org/)
* **Topic**: all Apache Kafka records are organised into topics, you can think of a topic like an event log or a table if you're familiar with databases.
* **Apache Kafka Producer**: an entity/application that publishes data to Apache Kafka

An Apache Apache Kafka cluster can be created in minutes in any cloud of your choice using [Aiven.io console](https://console.aiven.io/signup?utm_source=github&utm_medium=organic&utm_campaign=blog_art&utm_content=post).

For more informations about the code building blogs check the [blog post](https://aiven.io/blog/create-your-own-data-stream-for-kafka-with-python-and-faker?utm_source=github&utm_medium=organic&utm_campaign=blog_art&utm_content=post)


## Installation
This demo app is relying on [Faker](https://faker.readthedocs.io/en/master/) and [kafka-python](https://kafka-python.readthedocs.io/en/master/usage.html) which the former requiring Python 3.5 and above.
The installation can be done via

```bash
pip install -r requirements.txt
```

## Usage

The Python code can be run in bash with the following,
in SSL security protocol:
```bash
python main.py \
  --cert-folder \
  --host \
  --port 13041 \
  --topic-name  \
  --nr-messages 0 \
  --max-waiting-time 0
```

Where
* `cert-folder`: points to the folder containing the Apache Kafka certificates (see [blog post](https://aiven.io/blog/create-your-own-data-stream-for-kafka-with-python-and-faker?utm_source=github&utm_medium=organic&utm_campaign=blog_art&utm_content=post) for more)
* `host`: the Apache Kafka host
* `port`: the Apache Kafka port
* `topic-name`: the Apache Kafka topic name to write to (the topic needs to be pre-created or `kafka.auto_create_topics_enable` parameter enabled)
* `nr-messages`: the number of messages to send
* `max-waiting-time`: the maximum waiting time in seconds between messages
* `subject`: select amongst various subjects: `pizza` is the default one, but you can generate also `userbehaviour`, `bet`, `stock`, `realstock` (using the yahoo finance apis) and `metric`.

If successfully connected to a Apache Kafka cluster, the command will output a number of messages (`nr-messages` parameter) that are been sent to Apache Kafka in the form

```json
{
  "id": 0,
  "shop": "Circular Pi Pizzeria",
  "name": "Jason Brown",
  "phoneNumber": "(510)290-7469",
  "address": "2701 Samuel Summit Suite 938\nRyanbury, PA 62847",
  "pizzas": [{
    "pizzaName": "Diavola",
    "additionalToppings": []
  }, {
    "pizzaName": "Mari & Monti",
    "additionalToppings": ["olives", "garlic", "anchovies"]
  }, {
    "pizzaName": "Diavola",
    "additionalToppings": ["onion", "anchovies", "mozzarella", "olives"]
  }]
}
```

With
* `id`: being the order number, starting from `0` until `nr-messages -1`
* `shop`: is the pizza shop name receiving the order, you can check and change the full list of shops in the `pizza_shop` function within [pizzaproducer.py](pizzaproducer.py)
* `name`: the caller name
* `phoneNumber`: the caller phone number
* `address`: the caller address
* `pizzas`: an array or pizza orders made by
  * `pizzaName`: the name of the basic pizza in the range from 1 to `MAX_NUMBER_PIZZAS_IN_ORDER` defined in [main.py](main.py), the list of available pizzas can be found in the `pizza_name` function within [pizzaproducer.py](pizzaproducer.py)
  * `additionalToppings`: an optional number of additional toppings added to the pizza in the range from 0 to `MAX_ADDITIONAL_TOPPINGS_IN_PIZZA` , the list of available toppings can be found in the `pizza_topping` function within [pizzaproducer.py](pizzaproducer.py)

# Starting your Apache Kafka Service with Aiven.io

If you don't have a Apache Kafka Cluster available, you can easily start one in [Aiven.io console](https://console.aiven.io/signup?utm_source=github&utm_medium=organic&utm_campaign=blog_art&utm_content=post).

Once created your account you can start your Apache Kafka service with [Aiven.io's cli](https://github.com/aiven/aiven-client)

Set your variables first:
```bash
KAFKA_INSTANCE_NAME=fafka-my
PROJECT_NAME=my-project
CLOUD_REGION=aws-eu-south-1
AIVEN_PLAN_NAME=business-4
DESTINATION_FOLDER_NAME=~/kafkacerts
```
Parameters:
* `KAFKA_INSTANCE_NAME`: the name you want to give to the Apache Kafka instance
* `PROJECT_NAME`: the name of the project created during sing-up
* `CLOUD_REGION`: the name of the Cloud region where the instance will be created. The list of cloud regions can be found
 with
```bash
avn cloud list
```
* `AIVEN_PLAN_NAME`: name of Aiven's plan to use, which will drive the resources available, the list of plans can be found with
```bash
avn service plans --project <PROJECT_NAME> -t kafka --cloud <CLOUD_PROVIDER>
```
* `DESTINATION_FOLDER_NAME`: local folder where Apache Kafka certificates will be stored (used to login)

You can create the Apache Kafka service with

```bash
avn service create  \
  -t kafka $KAFKA_INSTANCE_NAME \
  --project $PROJECT_NAME \
  --cloud  $CLOUD_PROVIDER \
  -p $AIVEN_PLAN_NAME \
  -c kafka_rest=true \
  -c kafka.auto_create_topics_enable=true \
  -c schema_registry=true
```

---

You can download the required SSL certificates in the `<DESTINATION_FOLDER_NAME>` with

```bash
avn service user-creds-download $KAFKA_SERVICE_NAME \
  --project $PROJECT_NAME    \
  -d $DESTINATION_FOLDER_NAME \
  --username avnadmin
```

And retrieve the Apache Kafka Service URI with

```bash
avn service get $KAFKA_SERVICE_NAME \
  --project $PROJECT_NAME \
  --format '{service_uri}'
```
The Apache Kafka Service URI is in the form `hostname:port` and provides the `hostname` and `port` needed to execute the code.
You can wait for the newly created Apache Kafka instance to be ready with

```bash
avn service wait $KAFKA_SERVICE_NAME --project $PROJECT_NAME
```
For a more detailed description of services and required credentials, check the [blog post](blogs.aiven.io)


The code is based on [Faker](https://faker.readthedocs.io/en/master/), an Open Source Python library to generate fake data.

To modify the data generated, change the `produce_pizza_order` function within the `main.py` file. The output of the function should be two python dictionaries, containing the event `key` and `message`


To customise your dataset, you can check Faker's providers in the [related doc](https://faker.readthedocs.io/en/master/providers.html)

**Edit**:
Now with the ``subject`` parameter you can start generating:

* fake `stock` data

```
{'stock_name': 'Pita Pan', 'stock_value': 11.311429500055635, 'timestamp': 1634221435718}
{'stock_name': 'Deja Brew', 'stock_value': 9.956550461386884, 'timestamp': 1634221435877}
{'stock_name': 'Thai Tanic', 'stock_value': 27.227119819515632, 'timestamp': 1634221436180}
{'stock_name': 'Lawn & Order', 'stock_value': 20.625166423466904, 'timestamp': 1634221436285}
{'stock_name': 'Indiana Jeans', 'stock_value': 24.598295127977412, 'timestamp': 1634221436491}
```


Apache Kafka is either a registered trademark or trademark of the Apache Software Foundation in the United States and/or other countries. Aiven has no affiliation with and is not endorsed by The Apache Software Foundation.
