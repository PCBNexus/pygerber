import re
from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.meta import Meta
from pygerber.validators import Dispatcher
from pygerber.validators.validator import Validator, load_validators


class CoordinateTest(TestCase):
    def get_dummy_token(self):
        return SimpleNamespace(meta=Meta())

    def test_coordinate(self):
        token = self.get_dummy_token()
        test_value = "30100"

        @load_validators
        class ARGS_dispatcher(Dispatcher):
            VALUE = Validator()

        validator1 = ARGS_dispatcher(r"(?P<VALUE>[a-z]+)")

        cleaned1 = validator1(token, "foo")
        cleaned2 = validator1(token, "bar")
        self.assertEqual(cleaned1.VALUE, 'foo')
        self.assertEqual(cleaned2.VALUE, 'bar')


if __name__ == "__main__":
    main()