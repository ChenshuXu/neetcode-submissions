"""Regression check for the retry follow-up; solution.py contains print examples."""
from solution import Fetcher, MockClient


if __name__ == "__main__":
    client = MockClient({0: ([1, 2], 7), 7: ([3, 4], None)}, failures={7: 2})
    reader = Fetcher(client.fetch, max_attempts=2)
    try:
        reader.fetch_n(3)
    except TimeoutError:
        pass
    else:
        raise AssertionError("Expected exhausted retries")

    assert client.calls == [0, 7, 7]
    assert reader.fetch_n(0) == []
    assert client.calls == [0, 7, 7]
    assert reader.fetch_n(1) == [1]
    assert client.calls == [0, 7, 7]
    assert reader.fetch_n(3) == [2, 3, 4]
    assert client.calls == [0, 7, 7, 7]
    assert reader.fetch_n(1) == []
    assert client.calls == [0, 7, 7, 7]
    print("Retry exhaustion and continuation passed.")
