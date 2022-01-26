from glue_job import for_test


def test_for_test():
    result = for_test()
    assert result == 1
