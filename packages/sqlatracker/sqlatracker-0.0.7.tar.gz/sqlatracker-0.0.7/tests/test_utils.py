import json

from sqlalchemy import MetaData
from hypothesis import given, strategies as st

from sqlatracker import utils
from sqlatracker.field_tracker import FieldTracker


def test_merge_metadata():
    metadata = utils.merge_metadata(FieldTracker.metadata)
    assert isinstance(metadata, MetaData)


@given(st.booleans())
def test_booleans_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.characters())
def test_characters_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.dates())
def test_dates_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.datetimes())
def test_datetimes_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.decimals())
def test_decimals_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.floats())
def test_floats_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.integers())
def test_integers_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.none())
def test_none_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.times())
def test_times_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.tuples())
def test_tuples_can_json(value):
    json.dumps(utils.can_json(value))


@given(st.uuids())
def test_uuids_can_json(value):
    json.dumps(utils.can_json(value))
