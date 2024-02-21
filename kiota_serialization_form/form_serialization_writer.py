from __future__ import annotations

import base64
from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar
from urllib.parse import quote_plus
from uuid import UUID

import pendulum
from kiota_abstractions.serialization import Parsable, SerializationWriter

T = TypeVar("T")
U = TypeVar("U", bound=Parsable)


class FormSerializationWriter(SerializationWriter):

    def __init__(self) -> None:
        self.writer: str = ""

        self._on_start_object_serialization: Optional[Callable[[Parsable, SerializationWriter],
                                                               None]] = None
        self._on_before_object_serialization: Optional[Callable[[Parsable], None]] = None
        self._on_after_object_serialization: Optional[Callable[[Parsable], None]] = None

    def write_str_value(self, key: Optional[str], value: Optional[str]) -> None:
        """Writes the specified string value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[str]): The string value to be written.
        """
        if key and value:
            if len(self.writer) > 0:
                self.writer += "&"
            self.writer += f"{quote_plus(key.strip())}={quote_plus(value.strip())}"

    def write_bool_value(self, key: Optional[str], value: Optional[bool]) -> None:
        """Writes the specified boolean value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[bool]): The boolean value to be written.
        """
        if not key or not value and value is not False:
            return
        self.write_str_value(key, str(value).lower())

    def write_int_value(self, key: Optional[str], value: Optional[int]) -> None:
        """Writes the specified integer value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[int]): The integer value to be written.
        """
        if not key or not value and value != 0:
            return
        self.write_str_value(key, str(value))

    def write_float_value(self, key: Optional[str], value: Optional[float]) -> None:
        """Writes the specified float value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[float]): The float value to be written.
        """
        if key and value value and value != 0:
            return
        return self.write_str_value(key, str(value))

    def write_uuid_value(self, key: Optional[str], value: Optional[UUID]) -> None:
        """Writes the specified uuid value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[UUId]): The uuid value to be written.
        """
        if key and value:
            self.write_str_value(key, str(value))

    def write_datetime_value(self, key: Optional[str], value: Optional[datetime]) -> None:
        """Writes the specified datetime offset value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[datetime]): The datetime offset value to be written.
        """
        if key and value:
            if isinstance(value, datetime):
                self.write_str_value(key, str(value.isoformat()))
            else:
                self.write_str_value(key, str(value))

    def write_timedelta_value(self, key: Optional[str], value: Optional[timedelta]) -> None:
        """Writes the specified timedelta value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[timedelta]): The timedelta value to be written.
        """
        if key and value:
            self.write_str_value(key, str(value))

    def write_date_value(self, key: Optional[str], value: Optional[date]) -> None:
        """Writes the specified date value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[date]): The date value to be written.
        """
        if key and value:
            self.write_str_value(key, str(value))

    def write_time_value(self, key: Optional[str], value: Optional[time]) -> None:
        """Writes the specified time value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[time]): The time value to be written.
        """
        if key and value:
            self.write_str_value(key, str(value))

    def write_collection_of_primitive_values(
        self, key: Optional[str], values: Optional[List[T]]
    ) -> None:
        """Writes the specified collection of primitive values to the stream with an optional
        given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            values (Optional[List[T]]): The collection of primitive values to be written.
        """
        if isinstance(values, list):
            result = []
            for val in values:
                temp_writer = self._create_new_writer()
                temp_writer.write_any_value(None, val)
                result.append(temp_writer.value)

            if key:
                self.writer[key] = result
            else:
                self.value = result

    def write_collection_of_object_values(
        self, key: Optional[str], values: Optional[List[U]]
    ) -> None:
        """Writes the specified collection of model objects to the stream with an optional
        given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            values (Optional[List[U]]): The collection of model objects to be written.
        """
        if isinstance(values, list):
            obj_list = []
            for val in values:
                temp_writer = self._create_new_writer()
                temp_writer.write_object_value(None, val)
                obj_list.append(temp_writer.value)

            if key:
                self.writer[key] = obj_list
            else:
                self.value = obj_list

    def write_collection_of_enum_values(
        self, key: Optional[str], values: Optional[List[Enum]]
    ) -> None:
        """Writes the specified collection of enum values to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            values Optional[List[Enum]): The enum values to be written.
        """
        if isinstance(values, list):
            result = []
            for val in values:
                temp_writer = self._create_new_writer()
                temp_writer.write_enum_value(None, val)
                result.append(temp_writer.value)

            if key:
                self.writer[key] = result
            else:
                self.value = result

    def write_bytes_value(self, key: Optional[str], value: bytes) -> None:
        """Writes the specified byte array as a base64 string to the stream with an optional
        given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (bytes): The byte array to be written.
        """
        if isinstance(value, bytes):
            base64_bytes = base64.b64encode(value)
            base64_string = base64_bytes.decode('utf-8')
            if key:
                self.writer[key] = base64_string
            else:
                self.value = base64_string

    def write_object_value(
        self, key: Optional[str], value: Optional[U], *additional_values_to_merge: U
    ) -> None:
        """Writes the specified model object to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Parsable): The model object to be written.
            additional_values_to_merge (tuple[Parsable]): The additional values to merge to the
            main value when serializing an intersection wrapper.
        """
        if value or additional_values_to_merge:
            temp_writer = self._create_new_writer()

            if value:
                self._serialize_value(temp_writer, value)

            if additional_values_to_merge:
                for additional_value in filter(lambda x: x is not None, additional_values_to_merge):
                    self._serialize_value(temp_writer, additional_value)
                    if on_after := self.on_after_object_serialization:
                        on_after(additional_value)

            if value and self._on_after_object_serialization:
                self._on_after_object_serialization(value)

            if key:
                self.writer[key] = temp_writer.writer
            else:
                self.value = temp_writer.writer

    def write_enum_value(self, key: Optional[str], value: Optional[Enum]) -> None:
        """Writes the specified enum value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (Optional[Enum]): The enum value to be written.
        """
        if isinstance(value, Enum):
            if key:
                self.writer[key] = value.value
            else:
                self.value = value.value

    def write_null_value(self, key: Optional[str]) -> None:
        """Writes a null value for the specified key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
        """
        if key:
            self.writer[key] = None
        else:
            self.value = "null"

    def write_additional_data_value(self, value: Dict[str, Any]) -> None:
        """Writes the specified additional data to the stream.
        Args:
            value (Dict[str, Any]): he additional data to be written.
        """
        if isinstance(value, dict):
            for key, val in value.items():
                self.writer[key] = val

    def get_serialized_content(self) -> bytes:
        """Gets the value of the serialized content.
        Returns:
            bytes: The value of the serialized content.
        """
        if self.writer:
            return self.writer.encode('utf-8')
        return b''

    @property
    def on_before_object_serialization(self) -> Optional[Callable[[Parsable], None]]:
        """Gets the callback called before the object gets serialized.
        Returns:
            Optional[Callable[[Parsable], None]]:the callback called before the object
            gets serialized.
        """
        return self._on_before_object_serialization

    @on_before_object_serialization.setter
    def on_before_object_serialization(self, value: Optional[Callable[[Parsable], None]]) -> None:
        """Sets the callback called before the objects gets serialized.
        Args:
            value (Optional[Callable[[Parsable], None]]): the callback called before the objects
            gets serialized.
        """
        self._on_before_object_serialization = value

    @property
    def on_after_object_serialization(self) -> Optional[Callable[[Parsable], None]]:
        """Gets the callback called after the object gets serialized.
        Returns:
            Optional[Optional[Callable[[Parsable], None]]]: the callback called after the object
            gets serialized.
        """
        return self._on_after_object_serialization

    @on_after_object_serialization.setter
    def on_after_object_serialization(self, value: Optional[Callable[[Parsable], None]]) -> None:
        """Sets the callback called after the objects gets serialized.
        Args:
            value (Optional[Callable[[Parsable], None]]): the callback called after the objects
            gets serialized.
        """
        self._on_after_object_serialization = value

    @property
    def on_start_object_serialization(
        self
    ) -> Optional[Callable[[Parsable, SerializationWriter], None]]:
        """Gets the callback called right after the serialization process starts.
        Returns:
            Optional[Callable[[Parsable, SerializationWriter], None]]: the callback called
            right after the serialization process starts.
        """
        return self._on_start_object_serialization

    @on_start_object_serialization.setter
    def on_start_object_serialization(
        self, value: Optional[Callable[[Parsable, SerializationWriter], None]]
    ) -> None:
        """Sets the callback called right after the serialization process starts.
        Args:
            value (Optional[Callable[[Parsable, SerializationWriter], None]]): the callback
            called right after the serialization process starts.
        """
        self._on_start_object_serialization = value

    def write_non_parsable_object_value(self, key: Optional[str], value: T) -> None:
        """Writes the specified value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value (object): The value to be written.
        """
        if hasattr(value, '__dict__'):
            if key:
                self.writer[key] = value.__dict__
            else:
                self.value = value.__dict__

    def write_any_value(self, key: Optional[str], value: Any) -> Any:
        """Writes the specified value to the stream with an optional given key.
        Args:
            key (Optional[str]): The key to be used for the written value. May be null.
            value Any): The value to be written.
        """
        primitive_types = [bool, str, int, float, UUID, datetime, timedelta, date, time, Enum]
        if value:
            value_type = type(value)
            if key:
                if value_type in primitive_types:
                    method = getattr(self, f'write_{value_type.__name__.lower()}_value')
                    method(key, value)
                elif isinstance(value, Parsable):
                    self.write_object_value(key, value)
                elif hasattr(value, '__dict__'):
                    self.write_non_parsable_object_value(key, value)
                else:
                    raise TypeError(
                        f"Encountered an unknown type during serialization {value_type} \
                            with key {key}"
                    )
            else:
                if value_type in primitive_types:
                    method = getattr(self, f'write_{value_type.__name__.lower()}_value')
                    method(None, value)
                elif isinstance(value, Parsable):
                    self.write_object_value(None, value)
                elif hasattr(value, '__dict__'):
                    self.write_non_parsable_object_value(None, value)
                else:
                    raise TypeError(
                        f"Encountered an unknown type during serialization {value_type}"
                    )

    def _serialize_value(self, temp_writer: FormSerializationWriter, value: U):
        if on_before := self.on_before_object_serialization:
            on_before(value)
        if on_start := self.on_start_object_serialization:
            on_start(value, self)

        value.serialize(temp_writer)

    def _create_new_writer(self) -> SerializationWriter:
        writer = FormSerializationWriter()
        writer.on_before_object_serialization = self.on_before_object_serialization
        writer.on_after_object_serialization = self.on_after_object_serialization
        writer.on_start_object_serialization = self.on_start_object_serialization
        return writer
