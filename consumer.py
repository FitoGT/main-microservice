import pika
import json
from main import Product, db

params = pika.URLParameters(
    "amqps://xjjbbkgb:Vyt7GaMax2oyyBkMiuWUln5OY9HCb0vh@moose.rmq.cloudamqp.com/xjjbbkgb")

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('recieved in main')
    data = json.loads(body)
    if properties.content_type == 'product_created':
        product = Product(
            id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')


channel.basic_consume(
    queue="main", on_message_callback=callback, auto_ack=True)

print("consuming")

channel.start_consuming()

channel.close()
