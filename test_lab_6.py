import pytest
from pydantic import ValidationError
from lab_6 import Block, Source, Person, Vote

def test_valid_block():
    block = Block(hexString="0x1a2b3c4d", id=1001, view=101, desc="First Block", img="img.png")
    assert block.hexString == "0x1a2b3c4d"

def test_invalid_block_hex():
    with pytest.raises(ValidationError):
        Block(hexString="invalid", id=1001, view=101, desc="First Block", img="img.png")

def test_negative_view():
    with pytest.raises(ValidationError):
        Block(hexString="0x1a2b3c4d", id=1001, view=-1, desc="First Block", img="img.png")

def test_valid_source():
    source = Source(id=1, ip_addr="192.168.1.100", country_code="US")
    assert source.id == 1

def test_invalid_ip():
    with pytest.raises(ValidationError):
        Source(id=1, ip_addr="256.168.1", country_code="US")

def test_valid_person():
    person = Person(id=1, name="John Doe", addr="123 Main St")
    assert person.name == "John Doe"

def test_empty_name():
    with pytest.raises(ValidationError):
        Person(id=1, name="", addr="123 Main St")

def test_valid_vote():
    vote = Vote(block_id="0x1a2b3c4d", voter_id=1, timestamp="2024-03-31 14:30:00", source_id=1)
    assert vote.block_id == "0x1a2b3c4d"

def test_invalid_timestamp():
    with pytest.raises(ValidationError):
        Vote(block_id="0x1a2b3c4d", voter_id=1, timestamp="2024/03/31 14:30:00", source_id=1)
