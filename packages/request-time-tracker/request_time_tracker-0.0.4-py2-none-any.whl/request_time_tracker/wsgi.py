import logging
import threading
from datetime import datetime, timedelta
from django.conf import settings
import boto3


logger = logging.getLogger('django.time_in_queue')


def notify_cloudwatch_time_queue(namespace, time_in_queue):
    client = boto3.client(
        'cloudwatch',
        aws_access_key_id=settings.CLOUDWATCH_QUEUE_TIME_ACCESS_KEY,
        aws_secret_access_key=settings.CLOUDWATCH_QUEUE_TIME_SECRET_KEY,
        region_name=settings.CLOUDWATCH_QUEUE_TIME_REGION,
    )
    response = client.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': 'TimeInQueue',
                'Timestamp': datetime.utcnow(),
                'Value': time_in_queue.total_seconds(),
                'Unit': 'Seconds',
                'StorageResolution': 1,
            }
        ]
    )
    try:
        status_code = response['ResponseMetadata']['HTTPStatusCode']
    except KeyError:
        logger.warning('TimeInQueue export failing. Unable to find status code in response')
        return

    if status_code != 200:
        logger.warning('TimeInQueue export failing. Status code: {0}'.format(status_code))


class QueueTimeTracker:
    def __init__(self, parent_application, send_stats_every_seconds=5):
        self.parent_application = parent_application
        self.send_stats_every_seconds = send_stats_every_seconds
        self.last_notified = datetime.now() - timedelta(seconds=self.send_stats_every_seconds + 1)

    def __call__(self, environ, start_response):
        try:
            if settings.CLOUDWATCH_QUEUE_TIME_HEADER in environ:
                request_timestamp, millis = environ[settings.CLOUDWATCH_QUEUE_TIME_HEADER].split('.')
                request_started_at = datetime.fromtimestamp(int(request_timestamp)).replace(microsecond=int(millis) * 1000)

                request_in_queue = datetime.now() - request_started_at

                if datetime.now() > self.last_notified + timedelta(seconds=self.send_stats_every_seconds):
                    self.last_notified = datetime.now()
                    threading.Thread(
                        target=notify_cloudwatch_time_queue,
                        args=[settings.CLOUDWATCH_QUEUE_TIME_NAMESPACE, request_in_queue],
                    ).start()
        except AttributeError as ex:
            logger.warning('Improperly configured. {0}'.format(ex))

        return self.parent_application(environ, start_response)
