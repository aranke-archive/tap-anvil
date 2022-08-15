"""Tests standard tap features using the built-in SDK tests library."""
from dotenv import load_dotenv
from singer_sdk.testing import get_standard_tap_tests

from tap_anvil.tap import TapAnvil


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    load_dotenv()
    tests = get_standard_tap_tests(TapAnvil)
    for test in tests:
        test()
