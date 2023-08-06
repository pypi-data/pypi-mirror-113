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
import os
import threading
from time import sleep

from confluent_kafka import SerializingProducer as KafkaSerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

from axualclient.discovery import DiscoveryClient, BOOTSTRAP_SERVERS_KEY, TIMESTAMP_KEY, DiscoveryClientRegistry, \
    SCHEMA_REGISTRY_URL_KEY, DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY
from axualclient.patterns import resolve_topic
from axualclient.util import first_of_string_list, filter_axual_configuration, calculate_producer_switch_timeout

logger = logging.getLogger(__name__)


class SerializingProducer(DiscoveryClient):

    def __init__(self,
                 configuration: dict,
                 schema_value: str,
                 schema_key: str = None,
                 value_to_dict: callable = None,
                 key_to_dict: callable = None,
                 *args, **kwargs):
        """
        Instantiate an AVRO producer for Axual. The _producer attribute is
         the confluent_kafka SerializingProducer class.

        Parameters
        ----------
        configuration: dict
            App config information
        schema_value: str
            AVRO schema to use to serialize value, either the AVSC string, or
             a path to the AVSC file containing the schema.
        schema_key: str, (optional)
            AVRO schema to use to serialize value, either the AVSC string, or
             a path to the AVSC file containing the schema. The default assumes
        value_to_dict: callable (optional) must be callable with the signature:
             to_dict(value_object, SerializationContext) -> dict
        key_to_dict: callable (optional) must be callable with the signature:
             to_dict(key_object, SerializationContext) -> dict
        *args and **kwargs:
            Other parameters that can be passed to confluent_kafka Producer.

        """
        self._producer = None                    # has not received discovery result yet
        self._schema_registry_client = None      # no url available yet

        self.init_schema_key = schema_key
        self.init_schema_value = schema_value
        self.key_to_dict = key_to_dict
        self.value_to_dict = value_to_dict

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

            # initialize serializers against new schema registry
            sr_url = first_of_string_list(discovery_result[SCHEMA_REGISTRY_URL_KEY])
            self._schema_registry_client = SchemaRegistryClient(
                {
                    'url': sr_url,
                    'ssl.ca.location': self.configuration['ssl.ca.location'],
                    'ssl.key.location': self.configuration['ssl.key.location'],
                    'ssl.certificate.location': self.configuration['ssl.certificate.location']
                }
            )
            self.configuration['key.serializer'] = self._create_key_serializer()
            self.configuration['value.serializer'] = self._create_value_serializer()

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
            self._producer = KafkaSerializingProducer(
                kafka_properties, *self.init_args, **self.init_kwargs
            )

    def _is_keeping_order(self):
        return self.configuration.get('max.in.flight.requests.per.connection') in [1, '1']

    def _create_key_serializer(self):
        if self.init_schema_key is not None:
            if os.path.isfile(self.init_schema_key):
                with open(self.init_schema_key, 'r') as f:
                    schema_key_str = f.read()
            else:
                schema_key_str = self.init_schema_key
            return AvroSerializer(
                schema_registry_client=self._schema_registry_client,
                schema_str=schema_key_str,
                to_dict=self.key_to_dict,
                # Converts input to dict, but should not be needed when supplying dicts
                conf={'auto.register.schemas': False}
            )
        else:
            return StringSerializer('utf-8')

    def _create_value_serializer(self):
        if os.path.isfile(self.init_schema_value):
            with open(self.init_schema_value, 'r') as f:
                schema_str = f.read()
        else:
            schema_str = self.init_schema_value
        return AvroSerializer(
            schema_registry_client=self._schema_registry_client,
            schema_str=schema_str,
            to_dict=self.value_to_dict,
            # Converts input to dict, but should not be needed when supplying dicts
            conf={'auto.register.schemas': False}
        )

    def produce(self, *args, topic: str, key=None, value=None, **kwargs) -> None:
        """
        Produce message to topic. Wrapper around confluent_kafka's
         SerializingProducer.produce() method.

        Parameters
        ----------
        :param topic: Topic to produce to, as it appears on Self Service
        :param object key:   Message key
        :param object value: Message payload
        *args and **kwargs :
            Arguments to pass to Producer.produce().

        Returns
        -------
        None.

        """
        resolved_topic = resolve_topic(self.discovery_result, topic)
        self._do_with_switch_lock(
            lambda:
            self._producer.produce(
                resolved_topic, *args, key, value, **kwargs
            )
        )

    # producer interface
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

    # obj interface
    def __class__(self, *args, **kwargs):
        return self._producer.__class__(*args, **kwargs)

    def __dict__(self, *args, **kwargs):
        return self._producer.__dict__(*args, **kwargs)

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

    def __module__(self, *args, **kwargs):
        return self._producer.__module__(*args, **kwargs)

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

    def __weakref__(self, *args, **kwargs):
        return self._producer.__weakref__(*args, **kwargs)
