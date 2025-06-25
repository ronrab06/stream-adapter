import pytest
from stream_adapter import StreamAdapter, MESSAGE_SIZE, PAD_VALUE_MAX

@pytest.fixture
def adapter():
    return StreamAdapter()

def test_empty_chunk_input(adapter):
    result = adapter.get_stream_chunks([])

    assert result == []
    assert adapter.next_pad_value == 1

def test_exact_msg_size(adapter):
    input_chunk = list(range(MESSAGE_SIZE))
    result = adapter.get_stream_chunks(input_chunk)

    assert result == [input_chunk]
    assert adapter.next_pad_value == 1

def test_multiple_full_messages(adapter):
    chunk = list(range(1, 25))
    expected_output = [list(range(1, 13)), list(range(13, 25))]
    result = adapter.get_stream_chunks(chunk)

    assert result == expected_output
    assert adapter.next_pad_value == 1

def test_smaller_than_msg(adapter):
    chunk = [10, 20, 30, 40, 50]
    expected_output = [[10, 20, 30, 40, 50, 1, 2, 1, 2, 1, 2, 1]]
    result = adapter.get_stream_chunks(chunk)

    assert result == expected_output
    assert adapter.next_pad_value == 2

def test_larger_than_msg(adapter):
    chunk = list(range(1, 15))
    expected_output = [
        list(range(1, 13)),
        [13, 14, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    ]
    result = adapter.get_stream_chunks(chunk)

    assert result == expected_output
    assert adapter.next_pad_value == 1

def test_continuous_filling_between_calls(adapter):
    adapter.get_stream_chunks(list(range(11)))
    assert adapter.next_pad_value == 2

    chunk = list(range(15))
    result = adapter.get_stream_chunks(chunk)

    expected_messages = [[2] + list(range(11)), 
                         list(range(11, 15)) + [1, 2, 1, 2, 1, 2, 1, 2]]

    assert result == expected_messages
    assert adapter.next_pad_value == 1

def test_replace_555_with_666_start(adapter):
    chunk = [5, 5, 5, 1, 2]
    result = adapter.get_stream_chunks(chunk)
    expected = [[6, 6, 6, 1, 2, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666_end(adapter):
    chunk = [1, 2, 5, 5, 5]
    result = adapter.get_stream_chunks(chunk)
    expected = [[1, 2, 6, 6, 6, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666_middle(adapter):
    chunk = [1, 5, 5, 5, 2]
    result = adapter.get_stream_chunks(chunk)
    expected = [[1, 6, 6, 6, 2, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666(adapter):
    chunk = [5, 5, 5]
    result = adapter.get_stream_chunks(chunk)
    expected = [[6, 6, 6, 1, 2, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666_multiple(adapter):
    chunk = [5, 5, 5, 7, 5, 5, 5, 8]
    result = adapter.get_stream_chunks(chunk)
    expected = [[6, 6, 6, 7, 6, 6, 6, 8, 1, 2, 1, 2]]

    assert result == expected

def test_replace_555_with_666_overlapping(adapter):
    chunk = [5, 5, 5, 5]
    result = adapter.get_stream_chunks(chunk)
    expected = [[6, 6, 6, 5, 1, 2, 1, 2, 1, 2, 1, 2]]

    assert result == expected

def test_replace_555_with_666_twice_in_a_row(adapter):
    chunk = [5, 5, 5, 5, 5, 5, 5]
    result = adapter.get_stream_chunks(chunk)
    expected = [[6, 6, 6, 6, 6, 6, 5, 1, 2, 1, 2, 1]]

    assert result == expected