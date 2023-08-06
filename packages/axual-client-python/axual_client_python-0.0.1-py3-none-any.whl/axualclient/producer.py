# -*- coding: utf-8 -*-
#
#      Copyright (C) 2020 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import threading
from time import sleep

from confluent_kafka import Producer as KafkaProducer

from axualclient.discovery import DiscoveryClientRegistry, DiscoveryClient, BOOTSTRAP_SERVERS_KEY, TIMESTAMP_KEY, \
    DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY
from axualclient.patterns import resolve_topic
from axualclient.util import filter_axual_configuration, calculate_producer_switch_timeout

logger = logging.getLogger(__name__)


class Producer(DiscoveryClient):

    def __init__(self,
                 configuration: dict,
                 *args, **kwargs):
        """
        Instantiate a producer for Axual. The _producer attribute is the confluent_kafka Producer class.

        Parameters
        ----------
        configuration : dict
            Configuration properties including Axual Configuration. All producer Configuration can be found at:
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        *args and **kwargs :
            Other parameters that can be passed to confluent_kafka Producer.
        """
        self._producer = None  # no discovery result yet

        self.init_args = args
        self.init_kwargs = kwargs

        self.configuration = configuration
        # bootstrap servers & key/value serializers are not available at this point yet
        self.configuration['security.protocol'] = 'SSL'
        if 'partitioner' not in self.configuration.keys():
            self.configuration['partitioner'] = 'murmur2_random'

        self.switch_lock = threading.Lock()
        self.init_lock = threading.Lock()

        self.discovery_result = {}
        self.discovery_fetcher = DiscoveryClientRegistry.register_client(
            self.configuration, self
        )

    def wait_for_initialization(self) -> None:
        if self._producer is not None:
            return
        with self.init_lock:
            self.discovery_fetcher.wait_for_discovery_result()

    def _do_with_switch_lock(self, func):
        self.wait_for_initialization()
        with self.switch_lock:
            return func()

    def on_discovery_properties_changed(self, discovery_result: dict) -> None:
        """ A new discovery result has been received, need to switch """
        with self.switch_lock:
            self.discovery_result = discovery_result
            # plug in the new bootstrap servers
            self.configuration['bootstrap.servers'] = discovery_result[BOOTSTRAP_SERVERS_KEY]

            # Switch producer
            if self._producer is not None:
                self._producer.flush()
                switch_timeout = calculate_producer_switch_timeout(
                    self._is_keeping_order(),
                    int(discovery_result[DISTRIBUTOR_TIMEOUT_KEY]),
                    int(discovery_result[DISTRIBUTOR_DISTANCE_KEY]),
                    discovery_result[TIMESTAMP_KEY]
                )
                sleep(switch_timeout)

            kafka_properties = filter_axual_configuration(self.configuration)
            self._producer = KafkaProducer(kafka_properties, *self.init_args, **self.init_kwargs)

    def _is_keeping_order(self):
        return self.configuration.get('max.in.flight.requests.per.connection') in [1, '1']

    def produce(self, topic: str, value=None, *args, **kwargs) -> None:
        """
        Produce message to topic. Wrapper around confluent_kafka's Producer.produce() method.

        Parameters
        ----------
        :param topic: Topic to produce to, as it appears on Self Service
        :param str|bytes value: Message payload
        *args and **kwargs :
            Arguments to pass to Producer.produce(). value, key, ...

        Returns
        -------
        None.
        """
        self._do_with_switch_lock(
            lambda:
            self._producer.produce(resolve_topic(self.discovery_result, topic), *args, value, *args, **kwargs)
        )

    def abort_transaction(self, *args, **kwargs):
        self._do_with_switch_lock(
            lambda: self._producer.abort_transaction(*args, **kwargs)
        )

    def begin_transaction(self, *args, **kwargs):
        self._do_with_switch_lock(
            lambda: self._producer.begin_transaction(*args, **kwargs)
        )

    def commit_transaction(self, *args, **kwargs):
        self._do_with_switch_lock(
            lambda: self._producer.commit_transaction(*args, **kwargs)
        )

    def flush(self, *args, **kwargs) -> int:
        return self._do_with_switch_lock(
            lambda: self._producer.flush(*args, **kwargs)
        )

    def init_transactions(self, *args, **kwargs) -> None:
        self._do_with_switch_lock(
            lambda: self._producer.init_transactions(*args, **kwargs)
        )

    def list_topics(self, topic=None, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._producer.list_topics(resolve_topic(self.discovery_result, topic), *args, **kwargs)
        )

    def poll(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._producer.poll(*args, **kwargs)
        )

    def send_offsets_to_transaction(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._producer.send_offsets_to_transaction(*args, **kwargs)
        )

    def __class__(self, *args, **kwargs):
        return self._producer.__class__(*args, **kwargs)

    def __dir__(self, *args, **kwargs):
        return self._producer.__dir__(*args, **kwargs)

    def __doc__(self, *args, **kwargs):
        return self._producer.__doc__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self._producer.__eq__(*args, **kwargs)

    def __format__(self, *args, **kwargs):
        return self._producer.__format__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self._producer.__ge__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self._producer.__gt__(*args, **kwargs)

    def __hash__(self, *args, **kwargs):
        return self._producer.__hash__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self._producer.__le__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._producer.__len__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self._producer.__lt__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self._producer.__ne__(*args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        return self._producer.__reduce__(*args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        return self._producer.__reduce_ex__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self._producer.__repr__(*args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        return self._producer.__sizeof__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self._producer.__str__(*args, **kwargs)
