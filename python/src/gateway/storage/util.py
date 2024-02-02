import pika, json

#Upload method take inputs file , gridfs instance, rabbitMQ channel, user access
def upload(f, fs, channel, access):
    try:
        #mongo db return the file id
        fid = fs.put(f)
    except Exception as err:
        # print(err)
        return "Internal Server Error in putting file" + str(err), 500

    # After successfully uploading file
    # create a message for a queue

    message = {
            "video_fid": str(fid),
            "mp3_fid": None,
            "username": access['username'],            
            }
    # Put the message into the queue

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        """
        This part is very important messages are persisted in our queue in the event of a pod crash or restart of a pod
Pod for rabbitmq is stateful pod with the kubernates cluster
The messages are added to the queue. This is acutually persisted the message. If the pod is restart or crash when it come back up still the message is there
If we don't set this (delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE), if the pod crash or restart the messages are gone which means it is not persisted

Simply pod is restored to its original state. The queue retains the messages. It is durable 
"""
    except Exception as err:
        # we need to delete the file from our mongo db
        # If there is no message for the queue for the file, the file present in the db never going to be processed | Stale video file simply occupy space in db
        # If the file is failed to added in the message queue we should delete that
        print(err)
        fs.delete(fid)
        return "Internal Server Error in last line" + str(err), 500




