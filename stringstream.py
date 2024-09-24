from typing import Callable
from debug import *

class StringStream:
    def __init__(self, src: str):
        # debug("StringStream", "__init__", "Initializing from {}", src)
        self._i = 0
        self._src = src

    def is_valid(self, n: int = 1) -> bool:
        test_position = self._i + n
        length = len(self._src)
        result = test_position <= length
        # debug("StringStream", "is_valid", "Total stream size: {}. Are {} upcoming ({} total) elements valid? {}", length, n, test_position, result)
        return result

    def peek(self, n: int = 1) -> str | None:
        if debug_surround(lambda: self.is_valid(n)):
            result = self._src[self._i:self._i + n]
            # debug("StringStream", "peek", "Next {} elements are {}", n, result)
            return result
        # debug("StringStream", "peek", "Fewer than {} elements are upcoming, cannot peek", n)

    def is_eq(self, test: str) -> bool:
        peeked = self.peek(len(test))
        result = peeked == test
        debug("StringStream", "is_eq", "Is {} == {}? {}", peeked, test, result)
        return result

    # def is_in(self, test: str | list[str]) -> bool:
    #     # debug("StringStream", "is_in", "Does the upcoming stream contain any of {}? {}", [x for x in test])
    #     result = debug_surround(lambda: any([self.is_eq(x) for x in test]))
    #     return result

    def skip(self, n: int = 1):
        i = self._i
        self._i += n
        debug("StringStream", "skip", "Skipping {} forward from {} to {}. Remaining stream is now {}", n, i, self._i, self.remaining())

    def skip_if_eq(self, test: str) -> bool:
        if self.is_eq(test):
            n = len(test)
            # debug("StringStream", "skip_if_eq", "Upcoming stream matches {}, skipping {} elements", test, n)
            self.skip(n)
            return True
        else:
            return False

    def take(self, n = 1) -> str:
        result = self.peek(n)
        self._i += n
        debug("StringStream", "take", "Took {} elements ({}) from stream. Remaining stream is now {}", n, result, self.remaining())
        return result

    def take_while(self, pred: Callable[[str], bool]) -> str:
        i = self._i
        debug("StringStream", "take_while", "Starting at {} with predicate {}", i, pred)
        debug_stack_push()
        while True:
            if not self.is_valid():
                debug("StringStream", "take_while", "Stream is out of elements")
                break
            next = self.peek()
            # debug("StringStream", "take_while", "Next element ({}) is valid, continuing", next)
            if not pred(next):
                debug("StringStream", "take_while", "{} fails predicate", next)
                break
            debug("StringStream", "take_while", "({}) passes predicate, continuing", next)
            self.skip()
        result = self._src[i:self._i]
        debug("StringStream", "take_while", "Finishing with range [{}:{}] => {}. Remaining stream is now {}", i, self._i, result, self.remaining())
        debug_stack_pop()
        return result

    def remaining(self) -> str:
        return self._src[self._i:]
