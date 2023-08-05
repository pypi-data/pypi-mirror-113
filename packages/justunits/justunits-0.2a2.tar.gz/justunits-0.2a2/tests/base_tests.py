import re

import justunits
from justunits import (
    _ChainedUnitItem,
    SiUnits,
    SiPrefixes,
    DerivedUnit,
    join_unit,
    UnitPowerStyle,
    UnitDividingStyle,
    UnitSeparationStyle,
    _defaults,
    AttributeUnitSeparators,
    _get_target_unit_style,
    create_unit,
    UnitStyle,
    _get_separators,
    _make_separation_pattern,
)


def test_chained_item__the_ms_m_mm_problem():
    millisecond_item = _ChainedUnitItem(SiUnits.second.with_prefix(SiPrefixes.milli))
    meter_item = _ChainedUnitItem(SiUnits.meter)
    millimeter_item = _ChainedUnitItem(SiUnits.millimeter)
    millisecond_item.sort_in(meter_item)
    millisecond_item.sort_in(millimeter_item)
    assert str(millisecond_item) == "ms -> mm -> m"


def test_join_unit_pressure():
    pressure = DerivedUnit(
        SiUnits.kilogram, SiUnits.meter.with_power(-1), SiUnits.second.with_power(-2)
    )
    input_format_output_string_pairs = [
        (UnitDividingStyle.BY_POWER, "a [kg⋅m⁻¹⋅s⁻²]"),
        (UnitDividingStyle.SLASHED, "a [kg/(m⋅s²)]"),
        (UnitPowerStyle.SUPERSCRIPT, "a [kg/(m⋅s²)]"),
        (UnitPowerStyle.CARET, "a [kg/(m⋅s^2)]"),
        (UnitSeparationStyle.ASTERISK, "a [kg/(m*s²)]"),
        (UnitSeparationStyle.DOT, "a [kg/(m⋅s²)]"),
    ]
    assert _defaults.ATTRIBUTE_UNIT_SEPARATOR == AttributeUnitSeparators.WHITESPACE_BOXED
    for input_format, expected_output in input_format_output_string_pairs:
        assert expected_output == join_unit("a", pressure, target_format=input_format)


def test__get_target_unit_style():
    uds = UnitDividingStyle
    ups = UnitPowerStyle
    uss = UnitSeparationStyle

    test_target_pairs = [
        (
            None,
            _defaults.POWER_STYLE | _defaults.DIVIDING_STYLE | _defaults.SEPARATION_STYLE,
        ),
        (ups.CARET, ups.CARET | _defaults.DIVIDING_STYLE | _defaults.SEPARATION_STYLE),
        (
            ups.SUPERSCRIPT,
            ups.SUPERSCRIPT | _defaults.DIVIDING_STYLE | _defaults.SEPARATION_STYLE,
        ),
        (uds.BY_POWER, _defaults.POWER_STYLE | uds.BY_POWER | _defaults.SEPARATION_STYLE),
        (uds.SLASHED, _defaults.POWER_STYLE | uds.SLASHED | _defaults.SEPARATION_STYLE),
        (uss.DOT, _defaults.POWER_STYLE | _defaults.DIVIDING_STYLE | uss.DOT),
        (uss.ASTERISK, _defaults.POWER_STYLE | _defaults.DIVIDING_STYLE | uss.ASTERISK),
    ]
    for input_style, expected_style in test_target_pairs:
        received_style = _get_target_unit_style(input_style)
        assert received_style == expected_style


def test_stress():
    """

    >>> from justunits import from_string, to_string
    >>> stress = from_string("N/mm")
    >>> to_string(stress)
    'N/mm'
    """
    stress = DerivedUnit(
        create_unit("N", "newton", "force"),
        SiUnits.meter.with_prefix(SiPrefixes.milli).with_power(-1),
    )
    stress.style = UnitStyle.TOTAL_POWER_ASCII
    assert str(stress) == "N*mm^-1"

    stress.style = UnitStyle.SIMPLE_ASCII
    assert str(stress) == "N/mm"

    stress.style = UnitStyle.FINE_POWERED_SUPERSCRIPT
    assert str(stress) == "N⋅mm⁻¹"

    stress.style = UnitStyle.FINE_SLASHED_SUPERSCRIPT
    assert str(stress) == "N/mm"


def test_allowed_separators():
    separators = _get_separators(AttributeUnitSeparators(127))
    tester = re.compile(_make_separation_pattern(separators))

    supported_separators = ["_in_", " in ", "#", " [", "_[", "_", " "]

    for valid_sep in supported_separators:
        matched = tester.match(valid_sep)
        assert matched is not None, "'{}' should be matched.".format(valid_sep)
        matched_result = matched.groupdict()
        assert matched_result["separator"] == valid_sep
