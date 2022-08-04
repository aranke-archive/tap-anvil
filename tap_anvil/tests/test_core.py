"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_standard_tap_tests

from tap_anvil.tap import TapAnvil

SAMPLE_CONFIG: dict = {}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapAnvil, config=SAMPLE_CONFIG)
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.
