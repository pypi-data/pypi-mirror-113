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
from datetime import datetime
from time import sleep
from typing import List

from confluent_kafka import Consumer as KafkaConsumer

from axualclient.discovery import DiscoveryClient, DiscoveryClientRegistry, BOOTSTRAP_SERVERS_KEY, TIMESTAMP_KEY, \
    DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY, TTL_KEY
from axualclient.patterns import resolve_group, resolve_topic, resolve_topics
from axualclient.util import filter_axual_configuration

logger = logging.getLogger(__name__)

DEFAULT_POLL_SPEED = 0.2


class Consumer(DiscoveryClient):
    """Simple balanced consumer class.
    Implements __iter__ to be able to create a for loop on the consumer
     to iterate through messages: for msg in Consumer. Set pause
     attribute to break from loop.
    Set poll_speed attribute to change the polling speed (default: 0.2 [secs])."""

    def __init__(self,
                 configuration: dict = None,
                 *args, **kwargs):
        """
        Instantiate a consumer for Axual. Derives from confluent_kafka
         Consumer class.
        Note that auto-commit is set to False, so received messages must
         be committed by your script's logic.

        Parameters
        ----------
        configuration: dict
            Configuration properties including Axual Configurations. All consumer Configurations can be found at:
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        *args and **kwargs:
            Other parameters that can be passed to confluent_kafka Consumer.
        """
        self.unresolved_topics = []
        self.unresolved_group_id = configuration.get('application_id')
        self._consumer = None
        self.init_args = args
        self.init_kwargs = kwargs

        self.configuration = configuration
        # bootstrap servers & key/value serializers are not available at this point yet
        self.configuration['security.protocol'] = 'SSL'

        self.poll_speed = DEFAULT_POLL_SPEED
        self.initialized = False
        self.switch_lock = threading.Lock()
        self.init_lock = threading.Lock()

        self.discovery_result = {}
        self.discovery_fetcher = DiscoveryClientRegistry.register_client(
            self.configuration, self
        )

    def wait_for_initialization(self) -> None:
        if self.initialized:
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
            # plug in the resolved group.id
            self.configuration['group.id'] = resolve_group(discovery_result, self.unresolved_group_id)
            logger.debug(f'group.id: {self.configuration["group.id"]}')

            # Switch consumer
            if self.initialized:
                assignment = self._consumer.assignment()
                # sleep(self.poll_speed)  # Wait outstanding polls before closing consumer
                self._consumer.close()

                # Calculate switch time-out
                if len(assignment) > 0:
                    switch_timeout = self._calculate_switch_timeout(discovery_result)
                    sleep(switch_timeout / 1000)

            kafka_properties = filter_axual_configuration(self.configuration)
            self._consumer = KafkaConsumer(kafka_properties, *self.init_args, **self.init_kwargs)
            # subscribe to previously subscribed-to topics, on new cluster
            if self.unresolved_topics:
                resolved_topics = resolve_topics(self.discovery_result, self.unresolved_topics)
                self._consumer.subscribe(resolved_topics)
            self.initialized = True

    def _calculate_switch_timeout(self, discovery_result: dict):
        if self._is_at_least_once():
            return int(discovery_result[TIMESTAMP_KEY])
        return max(int(discovery_result[DISTRIBUTOR_TIMEOUT_KEY]) *
                   int(discovery_result[DISTRIBUTOR_DISTANCE_KEY]) -
                   (datetime.utcnow() - discovery_result[TIMESTAMP_KEY]).total_seconds() * 1000,
                   int(discovery_result[TTL_KEY]))

    def _is_at_least_once(self) -> bool:
        return self.configuration.get('auto.offset.reset') in ['earliest', 'smallest', 'begin', 'start']

    def __iter__(self):
        """Continuously loop through messages until self.pause is set to True"""
        self.pause = False
        while not self.pause:
            msg = self.poll(self.poll_speed)
            yield msg

    # KafkaConsumer interface
    def assign(self, partitions, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.assign(partitions, *args, **kwargs)
        )

    def assignment(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.assignment(*args, **kwargs)
        )

    def close(self, *args, **kwargs):
        DiscoveryClientRegistry.deregister_client(self.unresolved_group_id, self)
        return self._do_with_switch_lock(
            lambda: self._consumer.close(*args, **kwargs)
        )

    def commit(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.commit(*args, **kwargs)
        )

    def committed(self, partitions, timeout=None):
        return self._do_with_switch_lock(
            lambda: self._consumer.committed(partitions, timeout)
        )

    def consume(self, num_messages=1, *args,
                **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.consume(num_messages, *args, **kwargs)
        )

    def consumer_group_metadata(self):
        return self._do_with_switch_lock(
            lambda: self._consumer.consumer_group_metadata()
        )

    def get_watermark_offsets(self, partition, timeout=None, *args,
                              **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.get_watermark_offsets(partition, timeout, *args, **kwargs)
        )

    def list_topics(self, topic=None, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.list_topics(resolve_topic(self.discovery_result, topic), *args, **kwargs)
        )

    def offsets_for_times(self, partitions, timeout=None):
        return self._do_with_switch_lock(
            lambda: self._consumer.assign(partitions, timeout)
        )

    def pause(self, partitions):
        return self._do_with_switch_lock(
            lambda: self._consumer.pause(partitions)
        )

    def poll(self, timeout=-1):
        return self._do_with_switch_lock(
            lambda: self._consumer.poll(timeout=timeout)
        )

    def position(self, partitions):
        return self._do_with_switch_lock(
            lambda: self._consumer.position(partitions)
        )

    def resume(self, partitions):
        return self._do_with_switch_lock(
            lambda: self._consumer.resume(partitions)
        )

    def seek(self, partition):
        return self._do_with_switch_lock(
            lambda: self._consumer.seek(partition)
        )

    def store_offsets(self, message=None, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.store_offsets(message, *args, **kwargs)
        )

    def subscribe(self, topics: List[str], *args, **kwargs):
        self.unresolved_topics = list(set(self.unresolved_topics + topics))
        return self._do_with_switch_lock(
            lambda: self._consumer.subscribe(
                resolve_topics(self.discovery_result, topics),
                *args, **kwargs
            )
        )

    def unassign(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.unassign(*args, **kwargs)
        )

    def unsubscribe(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._consumer.unsubscribe(*args, **kwargs)
        )
