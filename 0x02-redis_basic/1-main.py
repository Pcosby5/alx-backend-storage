#!/usr/bin/env python3
"""
Main file
"""
from exercise import Cache

def main():
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        retrieved_value = cache.get(key, fn=fn)
        assert retrieved_value == value, f"Expected {value} but got {retrieved_value}"
        print(f"Stored and retrieved {value} successfully with key {key}")

if __name__ == "__main__":
    main()
