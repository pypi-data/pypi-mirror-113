from ml_platform_client.context import request_context
from typing import Optional
import json
from .kafka_helper import get_kafka_producer
from .log_helper import get_logger
from .util import get_current_time


class MlpTracker:
    def __init__(self,
        pipe_type,
        issue_module,
        event_name='issue_track',
        kafka_servers:str='',
        kafka_username:str='',
        kafka_password:str='',
    ):
        self.pipe_type = pipe_type
        self.issue_module = issue_module
        self.event_name = event_name
        if kafka_servers:
            self.kafka_producer = get_kafka_producer(
                kafka_servers=kafka_servers,
                kafka_username=kafka_username,
                kafka_password=kafka_password,
            )
        else:
            self.kafka_producer = None
        self.logger = get_logger(__name__)


    def send(
        self,
        message:str,
        reason:str,
        issue_time:Optional[str]=None,
        issue_module:Optional[str]=None,
        pipe_type:Optional[str]=None,
        uuid:Optional[str]=None,
    ):
        data= {
            'uuid': uuid or getattr(request_context, 'uuid', None),
            'issue_time': issue_time or get_current_time(),
            'issue_message': message,
            'issue_reason': reason,
            'issue_module': issue_module or self.issue_module,
            'pipe_type': pipe_type or self.pipe_type,
        }
        data = json.dumps(data, ensure_ascii=False)
        if self.kafka_producer is not None:
            try:
                self.kafka_producer.produce(self.event_name, data.encode('utf-8'))
            except BufferError:
                self.logger.info(f"{self.event_name}:[{data}]")
            self.kafka_producer.poll(0)
        else:
            self.logger.info(f"{self.event_name}:[{data}]")
        return
