"""Tests pour les utilitaires de profiling."""

import pstats

from pipeline.profiling import print_top_functions, profile_with_cprofile


def _dummy_work() -> int:
    return sum(i * i for i in range(10_000))


class TestProfiling:
    def test_profile_returns_stats(self) -> None:
        stats = profile_with_cprofile(_dummy_work)
        assert isinstance(stats, pstats.Stats)

    def test_print_top_functions_no_error(self) -> None:
        stats = profile_with_cprofile(_dummy_work)
        print_top_functions(stats, n=5)
