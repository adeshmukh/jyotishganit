"""
Tests for divisional chart calculations.

Uses mock D1 charts to avoid ephemeris loading for fast unit tests.
"""

import pytest

from jyotishganit.components import divisional_charts
from jyotishganit.core.models import (
    House,
    PlanetDignities,
    PlanetPosition,
    RasiChart,
)


def _make_d1_chart(asc_sign: str = "Aries", asc_degrees: float = 10.0):
    """Create a minimal D1 chart for testing divisional charts."""
    houses = [
        House(1, asc_sign, "Mars", 0.0, [], [], [], sign_degrees=asc_degrees),
        House(2, "Taurus", "Venus", 0.0, [], [], []),
        House(3, "Gemini", "Mercury", 0.0, [], [], []),
        House(4, "Cancer", "Moon", 0.0, [], [], []),
        House(5, "Leo", "Sun", 0.0, [], [], []),
        House(6, "Virgo", "Mercury", 0.0, [], [], []),
        House(7, "Libra", "Venus", 0.0, [], [], []),
        House(8, "Scorpio", "Mars", 0.0, [], [], []),
        House(9, "Sagittarius", "Jupiter", 0.0, [], [], []),
        House(10, "Capricorn", "Saturn", 0.0, [], [], []),
        House(11, "Aquarius", "Saturn", 0.0, [], [], []),
        House(12, "Pisces", "Jupiter", 0.0, [], [], []),
    ]
    planets = [
        PlanetPosition(
            "Sun", "Taurus", 15.5, "Rohini", 2, "Rohini", 2, "direct",
            {}, PlanetDignities(), [], {}, []
        ),
        PlanetPosition(
            "Moon", "Gemini", 8.2, "Ardra", 1, "Ardra", 3, "direct",
            {}, PlanetDignities(), [], {}, []
        ),
    ]
    return RasiChart(planets, houses)


class TestDivisionalChartDegrees:
    """Test that divisional charts expose sign degrees for planets and ascendant."""

    def test_divisional_ascendant_has_sign_degrees(self):
        """Divisional ascendant should include degrees within the divisional sign."""
        d1 = _make_d1_chart("Aries", 10.0)
        d9 = divisional_charts.compute_divisional_chart(d1, "D9")

        assert hasattr(d9.ascendant, "sign_degrees")
        assert isinstance(d9.ascendant.sign_degrees, (int, float))
        assert 0.0 <= d9.ascendant.sign_degrees < 30.0

    def test_divisional_planet_positions_have_sign_degrees(self):
        """Divisional planet positions should include degrees within the divisional sign."""
        d1 = _make_d1_chart("Aries", 10.0)
        d9 = divisional_charts.compute_divisional_chart(d1, "D9")

        for house in d9.houses:
            for occupant in house.occupants:
                assert hasattr(occupant, "sign_degrees")
                assert isinstance(occupant.sign_degrees, (int, float))
                assert 0.0 <= occupant.sign_degrees < 30.0

    def test_divisional_chart_to_dict_includes_sign_degrees(self):
        """Serialized divisional chart should include signDegrees in JSON output."""
        d1 = _make_d1_chart("Aries", 10.0)
        d9 = divisional_charts.compute_divisional_chart(d1, "D9")

        asc_dict = d9.ascendant.to_dict()
        assert "signDegrees" in asc_dict

        for house in d9.houses:
            for occupant in house.occupants:
                occ_dict = occupant.to_dict()
                assert "signDegrees" in occ_dict

    @pytest.mark.parametrize("chart_type", ["D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"])
    def test_all_divisional_charts_expose_degrees(self, chart_type):
        """All divisional chart types (D2-D60) should expose sign degrees."""
        d1 = _make_d1_chart("Aries", 10.0)
        div_chart = divisional_charts.compute_divisional_chart(d1, chart_type)

        assert hasattr(div_chart.ascendant, "sign_degrees")
        assert div_chart.ascendant.to_dict().get("signDegrees") is not None

        for house in div_chart.houses:
            for occupant in house.occupants:
                assert occupant.sign_degrees is not None
                assert "signDegrees" in occupant.to_dict()
