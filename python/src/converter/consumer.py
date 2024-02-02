import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3


def main():
    # we are using the mongo client installed in our local machine
    # we did not deployed in cluster
    client = MongoClient("host.minikube.internal", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s

    #gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    #configure rabbit mq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()


    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)

        # if there is error , we have to send the negative acknowledgement
        if err:
            # delivery tag is used to uinquely identify the delivery of the channel
            ch.basic_nack(delivery_tag=method.delivery_tag)
            # rabbit mq based on negative ack it removes the message from the queue
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)


    # on_message_callback is excuted when video is pull backed from the queue
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)