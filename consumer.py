import queue
import pika

params = pika.URLParameters(
    "amqps://xjjbbkgb:Vyt7GaMax2oyyBkMiuWUln5OY9HCb0vh@moose.rmq.cloudamqp.com/xjjbbkgb")

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('recieved in main')
    print(body)


channel.basic_consume(queue="main", on_message_callback=callback)

print("consuming")

channel.start_consuming()

channel.close()
