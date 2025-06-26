import pytest
from stream_adapter import StreamAdapter, PAD_VALUE_MAX

@pytest.fixture
def adapter():
    return StreamAdapter(12)

def test_empty_chunk_input(adapter):
    result = adapter.get_stream_chunks([])

    assert result == []
    assert adapter.next_pad_value == 1

def test_exact_msg_size(adapter):
    message = list(range(adapter.chunk_size))
    result = adapter.get_stream_chunks(message)

    assert result == [message]
    assert adapter.next_pad_value == 1

def test_multiple_full_messages(adapter):
    message = list(range(1, 25))
    expected_output = [list(range(1, 13)), list(range(13, 25))]
    result = adapter.get_stream_chunks(message)

    assert result == expected_output
    assert adapter.next_pad_value == 1

def test_smaller_than_msg(adapter):
    message = [10, 20, 30, 40, 50]
    expected_output = [[10, 20, 30, 40, 50, 1, 2, 1, 2, 1, 2, 1]]
    result = adapter.get_stream_chunks(message)

    assert result == expected_output
    assert adapter.next_pad_value == 2

def test_larger_than_msg(adapter):
    message = list(range(1, 15))
    expected_output = [
        list(range(1, 13)),
        [13, 14, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    ]
    result = adapter.get_stream_chunks(message)

    assert result == expected_output
    assert adapter.next_pad_value == 1

def test_continuous_filling_between_calls(adapter):
    adapter.get_stream_chunks(list(range(11)))
    assert adapter.next_pad_value == 2

    chunk = list(range(15))
    result = adapter.get_stream_chunks(chunk)

    expected_chunks = [[2] + list(range(11)), 
                         list(range(11, 15)) + [1, 2, 1, 2, 1, 2, 1, 2]]

    assert result == expected_chunks
    assert adapter.next_pad_value == 1

def test_replace_555_with_666_start(adapter):
    message = [5, 5, 5, 1, 2]
    result = adapter.get_stream_chunks(message)
    expected = [[6, 6, 6, 1, 2, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666_end(adapter):
    message = [1, 2, 5, 5, 5]
    result = adapter.get_stream_chunks(message)
    expected = [[1, 2, 6, 6, 6, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666_middle(adapter):
    message = [1, 5, 5, 5, 2]
    result = adapter.get_stream_chunks(message)
    expected = [[1, 6, 6, 6, 2, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666(adapter):
    message = [5, 5, 5]
    result = adapter.get_stream_chunks(message)
    expected = [[6, 6, 6, 1, 2, 1, 2, 1, 2, 1, 2, 1]]

    assert result == expected

def test_replace_555_with_666_multiple(adapter):
    message = [5, 5, 5, 7, 5, 5, 5, 8]
    result = adapter.get_stream_chunks(message)
    expected = [[6, 6, 6, 7, 6, 6, 6, 8, 1, 2, 1, 2]]

    assert result == expected

def test_replace_555_with_666_overlapping(adapter):
    message = [5, 5, 5, 5]
    result = adapter.get_stream_chunks(message)
    expected = [[6, 6, 6, 5, 1, 2, 1, 2, 1, 2, 1, 2]]

    assert result == expected

def test_replace_555_with_666_twice_in_a_row(adapter):
    message = [5, 5, 5, 5, 5, 5, 5]
    result = adapter.get_stream_chunks(message)
    expected = [[6, 6, 6, 6, 6, 6, 5, 1, 2, 1, 2, 1]]

    assert result == expected

def test_message_size_6():
    adapter = StreamAdapter(6)
    message = list(range(1, 8))
    result = adapter.get_stream_chunks(message)
    expected = [
        list(range(1, 7)),
        [7, 1, 2, 1, 2, 1]
    ]

    assert result == expected
    assert adapter.next_pad_value == 2

    second_message = list(range(8, 11))
    result = adapter.get_stream_chunks(second_message)
    expected = [[2, 8, 9, 10, 1, 2]]

    assert adapter.next_pad_value == 1
    assert result == expected