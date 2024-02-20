import json
from datetime import date, datetime, time, timedelta
from uuid import UUID

import pytest

from kiota_serialization_form.form_parse_node import FormParseNode

from tests.helpers import TestEntity, TestEnum

TEST_USER_FORM: str = (
    "displayName=Megan+Bowen&"
    "numbers=one,two,thirtytwo&"
    "givenName=Megan&"
    "accountEnabled=true&"
    "createdDateTime=2017-07-29T03:07:25Z&"
    "jobTitle=Auditor&"
    "mail=MeganB@M365x214355.onmicrosoft.com&"
    "mobilePhone=null&"
    "officeLocation=null&"
    "preferredLanguage=en-US&"
    "surname=Bowen&"
    "workDuration=PT1H&"
    "startWorkTime=08:00:00.0000000&"
    "endWorkTime=17:00:00.0000000&"
    "userPrincipalName=MeganB@M365x214355.onmicrosoft.com&"
    "birthDay=2017-09-04&"
    "deviceNames=device1&deviceNames=device2&" #collection property
    "otherPhones=123456789&otherPhones=987654321&" #collection property for additionalData
    "id=48d31887-5fad-4d73-a9f5-3c356e68a038"
)

def test_get_str_value():
    parse_node = FormParseNode("Megan+Bowen")
    result = parse_node.get_str_value()
    assert result == "Megan Bowen"


def test_get_int_value():
    parse_node = FormParseNode("1454")
    result = parse_node.get_int_value()
    assert result == 1454


def test_get_bool_value():
    parse_node = FormParseNode("false")
    result = parse_node.get_bool_value()
    assert result is False


def test_get_float_value():
    parse_node = FormParseNode("44.6")
    result = parse_node.get_float_value()
    assert result == 44.6


def test_get_uuid_value():
    parse_node = FormParseNode("f58411c7-ae78-4d3c-bb0d-3f24d948de41")
    result = parse_node.get_uuid_value()
    assert result == UUID("f58411c7-ae78-4d3c-bb0d-3f24d948de41")


def test_get_datetime_value():
    parse_node = FormParseNode('2022-01-27T12:59:45.596117')
    result = parse_node.get_datetime_value()
    assert isinstance(result, datetime)


def test_get_date_value():
    parse_node = FormParseNode('2015-04-20')
    result = parse_node.get_date_value()
    assert isinstance(result, date)
    assert str(result) == '2015-04-20'


def test_get_time_value():
    parse_node = FormParseNode('12:59:45.596117')
    result = parse_node.get_time_value()
    assert isinstance(result, time)
    assert str(result) == '12:59:45.596117'


def test_get_timedelta_value():
    parse_node = FormParseNode('PT30S')
    result = parse_node.get_timedelta_value()
    assert isinstance(result, timedelta)
    assert str(result) == '0:00:30'


# def test_get_collection_of_primitive_values():
#     parse_node = FormParseNode([12.1, 12.2, 12.3, 12.4, 12.5])
#     result = parse_node.get_collection_of_primitive_values(float)
#     assert result == [12.1, 12.2, 12.3, 12.4, 12.5]


# def test_get_collection_of_primitive_values_no_type():
#     parse_node = FormParseNode(["One", "Two", "Three", "Four", "Five"])
#     result = parse_node.get_collection_of_primitive_values(None)
#     assert result == ["One", "Two", "Three", "Four", "Five"]


def test_get_bytes_value():
    parse_node = FormParseNode('U2Ftd2VsIGlzIHRoZSBiZXN0')
    result = parse_node.get_bytes_value()
    assert isinstance(result, bytes)


# def test_get_collection_of_enum_values():
#     parse_node = FormParseNode(["dunhill", "oval"])
#     result = parse_node.get_collection_of_enum_values(OfficeLocation)
#     assert isinstance(result, list)
#     assert result == [OfficeLocation.Dunhill, OfficeLocation.Oval]


# def test_get_enum_value():
#     parse_node = FormParseNode("dunhill")
#     result = parse_node.get_enum_value(OfficeLocation)
#     assert isinstance(result, OfficeLocation)
#     assert result == OfficeLocation.Dunhill


# def test_get_object_value(user1_json):
#     parse_node = FormParseNode(json.loads(user1_json))
#     result = parse_node.get_object_value(User)
#     assert isinstance(result, User)
#     assert result.id == UUID("8f841f30-e6e3-439a-a812-ebd369559c36")
#     assert result.office_location == OfficeLocation.Dunhill
#     assert isinstance(result.updated_at, datetime)
#     assert isinstance(result.birthday, date)
#     assert result.business_phones == ["+1 205 555 0108"]
#     assert result.is_active is True
#     assert result.mobile_phone is None


# def test_get_collection_of_object_values(users_json):
#     parse_node = FormParseNode(json.loads(users_json))
#     result = parse_node.get_collection_of_object_values(User)
#     assert isinstance(result[0], User)
#     assert result[0].id == UUID("8f841f30-e6e3-439a-a812-ebd369559c36")
#     assert result[0].office_location == OfficeLocation.Dunhill
#     assert isinstance(result[0].updated_at, datetime)
#     assert isinstance(result[0].birthday, date)
#     assert result[0].business_phones == ["+1 205 555 0108"]
#     assert result[0].is_active is True
#     assert result[0].mobile_phone is None

def test_gets_entity_properties_from_form_data():
    parse_node = FormParseNode(TEST_USER_FORM)
    result = parse_node.get_object_value(TestEntity)
    assert isinstance(result, TestEntity)
    assert result.id == UUID("48d31887-5fad-4d73-a9f5-3c356e68a038")
    assert result.device_names == ["device1", "device2"]
    assert result.numbers == [TestEnum.One, TestEnum.Two]
    assert result.work_duration == timedelta(hours=1)
    assert result.birthday == date(2017, 9, 4)
    assert result.start_work_time == time(8, 0)
    assert result.end_work_time == time(17, 0)
    assert isinstance(result.created_date_time, datetime)
    assert result.office_location == None
    assert result.additional_data["otherPhones"]
    assert result.additional_data["otherPhones"] == "123456789,987654321"
    assert result.additional_data["mobilePhone"]
    assert result.additional_data["accountEnabled"] == "true"
    assert result.additional_data["jobTitle"] == "Auditor"
    
def test_get_collection_of_numerical_primitive_values():
    TEST_FORM_DATA = "numbers=1&numbers=2&numbers=3&"
    parse_node = FormParseNode(TEST_FORM_DATA)
    number_node = parse_node.get_child_node("numbers")
    
    result = number_node.get_collection_of_primitive_values(int)
    assert result == [1, 2, 3]
    
    result = number_node.get_collection_of_primitive_values(str)
    assert result == ["1", "2", "3"]
    
    result = number_node.get_collection_of_primitive_values(float)
    assert result == [1.0, 2.0, 3.0]
    
def test_get_collection_of_boolean_primitive_values():
    TEST_FORM_DATA = "booleans=true&booleans=false&booleans=true&"
    parse_node = FormParseNode(TEST_FORM_DATA)
    boolean_node = parse_node.get_child_node("booleans")
    
    result = boolean_node.get_collection_of_primitive_values(bool)
    assert result == [True, False, True]
    
    result = boolean_node.get_collection_of_primitive_values(str)
    assert result == ["true", "false", "true"]
    
def test_get_collection_of_uuid_primitive_values():
    TEST_FORM_DATA = "uuids=8f841f30-e6e3-439a-a812-ebd369559c36&uuids=8f841f30-e6e3-439a-a812-ebd369559c36&uuids=8f841f30-e6e3-439a-a812-ebd369559c36&"
    parse_node = FormParseNode(TEST_FORM_DATA)
    uuid_node = parse_node.get_child_node("uuids")
    
    result = uuid_node.get_collection_of_primitive_values(UUID)
    assert result == [UUID("8f841f30-e6e3-439a-a812-ebd369559c36"), UUID("8f841f30-e6e3-439a-a812-ebd369559c36"), UUID("8f841f30-e6e3-439a-a812-ebd369559c36")]
    
    result = uuid_node.get_collection_of_primitive_values(str)
    assert result == ["8f841f30-e6e3-439a-a812-ebd369559c36", "8f841f30-e6e3-439a-a812-ebd369559c36", "8f841f30-e6e3-439a-a812-ebd369559c36"]
    
def test_get_collection_of_object_values():
    parse_node = FormParseNode(TEST_USER_FORM)
    with pytest.raises(Exception) as excinfo:
        result = parse_node.get_collection_of_object_values(TestEntity)
    assert "Collection of object values is not supported " in str(excinfo.value)
    
def returns_default_if_child_node_does_not_exist():
    parse_node = FormParseNode(TEST_USER_FORM)
    result = parse_node.get_child_node("nonExistent")
    assert result == None