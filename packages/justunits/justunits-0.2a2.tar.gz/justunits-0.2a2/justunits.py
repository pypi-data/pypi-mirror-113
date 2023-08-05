__author__ = "David Scheliga"
__email__ = "david.scheliga@gmx.de"
__version__ = "0.2a2"
__all__ = [
    "DerivedUnit",
    "AttributeUnitSeparators",
    "AUnit",
    "BaseSiUnits",
    "BareUnit",
    "create_unit",
    "DEFAULT_ALLOWED_SEPARATORS",
    "DEFAULT_ATTRIBUTE_UNIT_SEPARATOR",
    "DEFAULT_DIVIDING_STYLE",
    "DEFAULT_POWER_STYLE",
    "DEFAULT_SEPARATION_STYLE",
    "DEFAULT_UNIT_STYLE",
    "from_string",
    "join_unit",
    "Prefix",
    "prefix_base_unit",
    "PREFIX_FOR_ONE",
    "reformat_unit",
    "register_unit",
    "reset_unit_library",
    "set_default_attribute_unit_separator",
    "set_default_unit_style",
    "SiPrefixes",
    "SiUnits",
    "split_attribute_unit",
    "split_number_and_unit",
    "split_unit",
    "split_unit_text",
    "to_string",
    "UnitDividingStyle",
    "UnitPowerStyle",
    "UnitSeparationStyle",
    "UnitStyle",
    "UnknownUnit",
]

import copy
import csv
import io
import re
import warnings
from collections.abc import Sequence
from collections import namedtuple, OrderedDict
from enum import auto, IntFlag
from functools import lru_cache
from itertools import chain
from string import Template
from typing import (
    Optional,
    List,
    Pattern,
    Tuple,
    Union,
    Iterable,
    Dict,
    Iterator,
    Generator,
    Callable,
    Any,
)


_unit_table_title_line = "symbol, name, quantity, prefixes"

_default_raw_unit_table = (
    _unit_table_title_line
    + """
s, second, time, m 
m, meter, length, m k
g, gram, mass, µ m k
A, ampere, electric current, G M m k
K, kelvin, thermodynamic temperature,
mol, mole, amount of substance,
cd, candela, luminous intensity,
rad, radian, plane angle,
sr, steradian, solid angle, 
min, minute, time,
h, hour, time
d, day, time
°, degree, angle
´, minute, angle
´´, second, angle
L, liter, volume, h da d,c,m
t, tonne, mass, M k
Np, neper, ,
B, bel, , d
eV, electronvolt,
u, unified atomic mass unit, ,
au, astonomical unit, ,
Hz, hertz, frequency, T G M k
N, newton, "force, weight", G M k m µ
Pa, pascal, "pressure, stress", G M k h da d c m µ
J, joule, "energy, work, heat", G M k m μ n
W, watt, "power, radiant flux", T G M k m μ
C, coulomb, electric charge,
V, volt, "electrical potential difference (voltage emf)", T G M k m µ
F, farad, capacitance,
Ω, ohm, "resistance, impedance, reactance", G M k m µ
S, siemens , electrical conductance, G M k m μ
Wb, weber, magnetic flux, 
T, tesla, magnetic flux density, G M k m μ
H, henry, inductance, G M k m μ
°C, degree Celsius, temperature relative to 273.15 K,
lm, lumen, luminous flux,
lx, lux, illuminance,
Bq, becquerel, radioactivity (decays per unit time),
Gy, gray, absorbed dose (of ionising radiation),
Sv, sievert, equivalent dose (of ionising radiation), m μ
kat, katal, catalytic activity,
"""
)

_source_repository_url = "https://gitlab.com/david.scheliga/justunits"
_UNIT_SEPARATOR_DOT_OPERATOR = "⋅"
_UNIT_SEPARATOR_ASTERISK = "*"
_UNIT_DIVIDER_CHAR = "/"
_SPLITS_UNITS_PATTERN = re.compile(r"[\*⋅]")
_BASE_UNIT_PATTERN = (
    r"^(?P<symbol>{})(?P<power>(\^[\+-]?[1-9/]{{0,2}}[1-9])|([⁺⁻]?[¹²³⁴½⅔⅓]))?"
)
_enclosed_unit_pattern = re.compile(r"\((.*?)\)")

Prefix = namedtuple("Prefix", "symbol name decimal")

BaseUnit = namedtuple("BareUnit", "symbol name quantity")
"""
The **immutable**, minimum unit definition consisting of the unit's symbol, its name and
the quantity this units stands for.
"""

PREFIX_FOR_ONE = Prefix("", "", 1)
"""
This is the (non existing prefix) placeholder for 1.
"""

_base_si_prefixes = {
    "Y": Prefix("y", "yotta", 10 ** 24),
    "Z": Prefix("Z", "zetta", 10 ** 21),
    "E": Prefix("E", "exa", 10 ** 18),
    "P": Prefix("P", "peta", 10 ** 15),
    "T": Prefix("T", "tera", 10 ** 12),
    "G": Prefix("G", "giga", 10 ** 9),
    "M": Prefix("M", "mega", 10 ** 6),
    "k": Prefix("k", "kilo", 10 ** 3),
    "h": Prefix("h", "hecto", 10 ** 2),
    "da": Prefix("da", "deka", 10),
    "": PREFIX_FOR_ONE,
    "d": Prefix("d", "deci", 10 ** -1),
    "c": Prefix("c", "centi", 10 ** -2),
    "m": Prefix("m", "milli", 10 ** -3),
    "µ": Prefix("μ", "micro", 10 ** -6),
    "μ": Prefix("µ", "micro", 10 ** -6),
    "n": Prefix("n", "nano", 10 ** -9),
    "p": Prefix("p", "pico", 10 ** -12),
    "f": Prefix("f", "femto", 10 ** -15),
    "a": Prefix("a", "atto", 10 ** -18),
    "z": Prefix("z", "zepto", 10 ** -21),
    "y": Prefix("y", "yocto", 10 ** -24),
}


class BareUnit:
    def __init__(self, symbol: str, name: str, quantity: str):
        """

        Args:
            symbol:
            name:
            quantity:

        Examples:

            >>> from justunits import BareUnit
            >>> pressure = BareUnit("Pa", "pascal", "pressure")
            >>> stress = BareUnit("Pa", "pascal", "stress")
            >>> pascal = BareUnit("Pa", "pascal", "pressure, stress")
            >>> meter = BareUnit("m", "meter", "length")

            >>> pressure == stress == pascal
            True

            >>> pascal != meter
            True

            >>> hash(pressure) == hash(stress) == hash(pascal)
            True

            >>> hash(pascal) != hash(meter)
            True

            >>> unit_map = {"m": meter, "Pa": pascal}
            >>> unit_map[pascal]
            BareUnit('Pa', 'pascal', 'pressure, stress')

        .. doctest::
           :hide:

           >>> from justunits import BareUnit
           >>> from doctestprinter import doctest_iter_print
           >>> b = BareUnit("b", "", "")
           >>> B = BareUnit("B", "", "")
           >>> E = BareUnit("E", "", "")
           >>> d = BareUnit("d", "", "")
           >>> unsorted_units = [b, E, B, d]
           >>> list(sorted(iter("bEBd")))
           ['B', 'E', 'b', 'd']
           >>> str(B)
           'B'
           >>> sorted_units = list(sorted(unsorted_units, key=lambda x:str(x)))
           >>> [str(x) for x in sorted_units]
           ['B', 'E', 'b', 'd']
        """
        self._items = (str(symbol), str(name), str(quantity))

    def __hash__(self):
        return hash(self.symbol)

    def __eq__(self, other):
        return other == self.symbol

    def __ne__(self, other):
        return other != self.symbol

    def __lt__(self, other):
        return self.symbol < other

    def __gt__(self, other):
        return self.symbol > other

    def __repr__(self):
        return "{}{}".format(self.__class__.__name__, self._items)

    def __str__(self):
        return self.symbol

    @property
    def symbol(self):
        return self._items[0]

    @property
    def name(self):
        return self._items[1]

    @property
    def quantity(self):
        return self._items[2]


class _GetsFirstIntFlag(IntFlag):
    @classmethod
    def get_first_hit(cls, other: int, default: Optional[IntFlag] = None) -> int:
        """
        Returns the first hit within the enumeration. A custom *default* is returned,
        if no item fitted.

        Args:
            other:
                The flags which first hit will be returned.

            default:
                The default value, if *other* did not hit anything. Default is *None*.

        Returns:
            int
        """
        for item in reversed(cls):
            if (other & item) == item:
                return item
        return default


class AttributeUnitSeparators(_GetsFirstIntFlag):
    WHITESPACE_BOXED = auto()
    """
    Leads to 'attribute [unit]'
    """

    UNDERLINE_BOXED = auto()
    """
    Leads to 'attribute_[unit]'
    """

    WHITESPACE_IN = auto()
    """
    Leads to 'attribute in unit'
    """

    UNDERLINED_IN = auto()
    """
    Leads to 'attribute_in_unit'
    """

    HASH_SIGN = auto()
    """
    Leads to 'attribute#unit'
    """

    SINGLE_UNDERLINE = auto()
    """
    Leads to 'attribute_unit'
    """

    SINGLE_WHITESPACE = auto()
    """
    Leads to 'attribute unit'
    """


class UnitPowerStyle(_GetsFirstIntFlag):
    SUPERSCRIPT = 256
    """
    Leads to superscripting powers like *a⁻¹*
    """
    CARET = 512
    """
    Powers are represented in ascii compatible like *a^-1*
    """


class UnitDividingStyle(_GetsFirstIntFlag):
    SLASHED = 1024
    """
    Units are divided by a forward slash like *a/b*.
    """
    BY_POWER = 2048
    """
    Divisions of units is represented using powers like *a/b* being *a⋅b⁻¹*.
    """


class UnitSeparationStyle(_GetsFirstIntFlag):
    DOT = 4096
    """
    Units are separated using a dot operator *⋅* like *a⋅b*
    """
    ASTERISK = 8192
    """
    Units are separated by an asterisk like *a*b* being ascii compatible.
    """


class UnitStyle(IntFlag):
    SIMPLE_ASCII = (
        UnitPowerStyle.CARET | UnitDividingStyle.SLASHED | UnitSeparationStyle.ASTERISK
    )
    """
    Results into 'kg/(s^2*K)*m^2'
    """
    TOTAL_POWER_ASCII = (
        UnitPowerStyle.CARET | UnitDividingStyle.BY_POWER | UnitSeparationStyle.ASTERISK
    )
    """
    Results into 'kg*s^-2*K^-1*m^2'
    """
    FINE_SLASHED_SUPERSCRIPT = (
        UnitPowerStyle.SUPERSCRIPT | UnitDividingStyle.SLASHED | UnitSeparationStyle.DOT
    )
    """
    Results into 'kg/(s²⋅K)⋅m²'
    """
    FINE_POWERED_SUPERSCRIPT = (
        UnitPowerStyle.SUPERSCRIPT
        | UnitDividingStyle.BY_POWER
        | UnitSeparationStyle.DOT
    )
    """
    Results into 'kg⋅s⁻²⋅K⁻¹⋅m²'
    """


DEFAULT_ATTRIBUTE_UNIT_SEPARATOR = AttributeUnitSeparators.WHITESPACE_IN
"""
The style separating attributes/values from units.
"""

DEFAULT_ALLOWED_SEPARATORS = (
    AttributeUnitSeparators.UNDERLINED_IN
    | AttributeUnitSeparators.WHITESPACE_IN
    | AttributeUnitSeparators.WHITESPACE_BOXED
    | AttributeUnitSeparators.HASH_SIGN
    | AttributeUnitSeparators.UNDERLINE_BOXED
)
"""
By default only 5 of 7 supported attribute unit separator are taken into account
as the absolute certain separation of an single underline or whitespace separated 
unit is ambiguous, without limiting the results to the content of the unit library.
Such a behaviour may be implemented in future releases, if it turns out to be
necessary.
"""

DEFAULT_POWER_STYLE = UnitPowerStyle.SUPERSCRIPT
"""
The default style how powers are represented.
"""

DEFAULT_DIVIDING_STYLE = UnitDividingStyle.SLASHED
"""
The default style how unit fractions are represented.
"""

DEFAULT_SEPARATION_STYLE = UnitSeparationStyle.DOT
"""
The default style by which character units are separated.
"""

DEFAULT_UNIT_STYLE = (
    DEFAULT_POWER_STYLE | DEFAULT_DIVIDING_STYLE | DEFAULT_SEPARATION_STYLE
)
"""
The default unit style composed of power-, dividing- and separation-style.
"""

_DEFAULT_HASHING_STYLE = UnitStyle.TOTAL_POWER_ASCII
"""
The style which is used for hashing units.
"""


class _Defaults:
    def __init__(self):
        self.ATTRIBUTE_UNIT_SEPARATOR = DEFAULT_ATTRIBUTE_UNIT_SEPARATOR
        self.ALLOWED_SEPARATORS = DEFAULT_ALLOWED_SEPARATORS
        self.POWER_STYLE = DEFAULT_POWER_STYLE
        self.DIVIDING_STYLE = DEFAULT_DIVIDING_STYLE
        self.SEPARATION_STYLE = DEFAULT_SEPARATION_STYLE
        self.UNIT_STYLE = DEFAULT_UNIT_STYLE
        self._HASHING_STYLE = _DEFAULT_HASHING_STYLE


_defaults = _Defaults()
"""
The runtime styling defaults.
"""


class SiPrefixes:
    yotta = _base_si_prefixes["Y"]
    zetta = _base_si_prefixes["Z"]
    exa = _base_si_prefixes["E"]
    peta = _base_si_prefixes["P"]
    tera = _base_si_prefixes["T"]
    giga = _base_si_prefixes["G"]
    mega = _base_si_prefixes["M"]
    kilo = _base_si_prefixes["k"]
    hecto = _base_si_prefixes["h"]
    deca = _base_si_prefixes["da"]
    deci = _base_si_prefixes["d"]
    ONE = _base_si_prefixes[""]
    centi = _base_si_prefixes["c"]
    milli = _base_si_prefixes["m"]
    micro = _base_si_prefixes["µ"]
    nano = _base_si_prefixes["n"]
    pico = _base_si_prefixes["p"]
    femto = _base_si_prefixes["f"]
    atto = _base_si_prefixes["a"]
    zepto = _base_si_prefixes["z"]
    yocto = _base_si_prefixes["y"]

    @staticmethod
    def get_prefix(symbol: str) -> Prefix:
        """
        Returns the requested symbol's Prefix-Object.
        Args:
            symbol(str):
                Symbol of an SI-prefix.

        Returns:
            Prefix

        Raises:
            KeyError

        Examples:

            >>> import justunits
            >>> justunits.SiPrefixes.get_prefix("Z")
            Prefix(symbol='Z', name='zetta', decimal=1000000000000000000000)

            An empty string is an additional placeholder for the power of Zero
            related to the base unit.

            >>> justunits.SiPrefixes.get_prefix("")
            Prefix(symbol='', name='', decimal=1)

            Not existing symbols raises KeyErrors instead returning 1.

            >>> justunits.SiPrefixes.get_prefix("i")
            Traceback (most recent call last):
            ...
            KeyError: 'The supplied key is not a SI-prefix and does not exist.'
            >>> justunits.SiPrefixes.get_prefix(None)
            Traceback (most recent call last):
            ...
            KeyError: 'The supplied key is not a SI-prefix and does not exist.'
        """
        try:
            return _base_si_prefixes[symbol]
        except KeyError:
            raise KeyError("The supplied key is not a SI-prefix and does not exist.")


_detects_raw_powers_pattern = re.compile(
    r"\^(?P<dividend>[\-+]?[0-9\.]+)/?(?P<divisor>[2-9]?)?"
)
_UNIT_TABLE_PREFIX_DELIMITER = " "


_ignoring_boxing_whitespaces_pattern = re.compile(r"^\s*(.*?)\s*(\r?\n?)$")


def _strips_enclosing_whitespaces(text: str) -> str:
    """

    Args:
        text:

    Returns:

    .. doctest::

        >>> # Access to private member for testing
        >>> # noinspection PyProtectedMember
        >>> from justunits import _strips_enclosing_whitespaces
        >>> _strips_enclosing_whitespaces("A name         ")
        'A name'
        >>> _strips_enclosing_whitespaces("     A name")
        'A name'
        >>> _strips_enclosing_whitespaces("    A name     ")
        'A name'

    """
    matched_content = _ignoring_boxing_whitespaces_pattern.match(text)
    if matched_content is None:
        return text
    inner_content_without_boxing_whitespaces = matched_content.group(1)
    return inner_content_without_boxing_whitespaces


def _read_raw_unit_table(text_buffer) -> List["AUnit"]:
    csv_reader = csv.reader(text_buffer, skipinitialspace=True)
    all_read_units = []
    next(csv_reader)  #  skip the title line
    for raw_table_unit_definition in csv_reader:
        hit_an_empty_line = not raw_table_unit_definition
        if hit_an_empty_line:
            continue
        hit_a_comment = raw_table_unit_definition[0] == "#"
        if hit_a_comment:
            continue
        symbol, name, quantity, *potential_prefixes = raw_table_unit_definition
        current_base_unit = BareUnit(symbol=symbol, name=name, quantity=quantity)

        only_a_base_unit_defined = (
            len(potential_prefixes) == 0 or potential_prefixes[0] == ""
        )
        if only_a_base_unit_defined:
            all_read_units.append(AUnit(current_base_unit))
            continue
        supported_prefixes = potential_prefixes[0]

        clean_supported_prefixes = _strips_enclosing_whitespaces(supported_prefixes)
        prefix_symbols = clean_supported_prefixes.split(_UNIT_TABLE_PREFIX_DELIMITER)
        all_supported_variants_of_current = prefix_base_unit(
            base_unit=current_base_unit, supported_prefixes=prefix_symbols
        )
        all_read_units.extend(all_supported_variants_of_current)
    return all_read_units


def _extract_raw_power(power_text: str) -> Optional[dict]:
    """

    Args:
        power_text:

    Returns:

    .. doctest::
        >>> _extract_raw_power("^1")
        {'dividend': '1', 'divisor': ''}
        >>> _extract_raw_power("^+1")
        {'dividend': '+1', 'divisor': ''}
        >>> _extract_raw_power("^-3")
        {'dividend': '-3', 'divisor': ''}
        >>> _extract_raw_power("^1/3")
        {'dividend': '1', 'divisor': '3'}
        >>> _extract_raw_power("^+1/3")
        {'dividend': '+1', 'divisor': '3'}
        >>> _extract_raw_power("^-1/3")
        {'dividend': '-1', 'divisor': '3'}
        >>> _extract_raw_power("^-0.5")
        {'dividend': '-0.5', 'divisor': ''}
        >>> _extract_raw_power("↉")

    """
    matched_power = _detects_raw_powers_pattern.match(power_text)
    if matched_power is None:
        return None
    return matched_power.groupdict()


def _convert_to_int_or_float(
    number_text: str, default: Optional[Union[int, float]] = None
) -> Union[int, float]:
    """

    Args:
        number_text:
        default:

    Returns:

    .. doctest::

        >>> _convert_to_int_or_float("1")
        1
        >>> _convert_to_int_or_float("1.0")
        1.0
        >>> _convert_to_int_or_float("", 1)
        1
        >>> _convert_to_int_or_float(".a", 1.0)
        1.0
    """
    potentially_a_float = "." in number_text
    try:
        if potentially_a_float:
            return float(number_text)
        return int(number_text)
    except ValueError:
        return default


def _convert_raw_power(power_text: str) -> Union[int, float]:
    """
    Converts the raw power priotary preserving integers.

    Args:
        power_text:
            The extracted power of an unit text.

    Returns:
        Union[int, float]

    .. doctest ::

        >>> _convert_raw_power("^0.5")
        0.5
        >>> _convert_raw_power("^2")
        2
        >>> _convert_raw_power("^+2")
        2
        >>> _convert_raw_power("^-2")
        -2
        >>> _convert_raw_power("^2/3")
        0.6666666666666666
        >>> _convert_raw_power("^+2/3")
        0.6666666666666666
        >>> _convert_raw_power("^-2/3")
        -0.6666666666666666
        >>> _convert_raw_power("↉")

    """
    power_parts = _extract_raw_power(power_text=power_text)
    if power_parts is None:
        return None

    divisor = _convert_to_int_or_float(power_parts["divisor"], 1)
    dividend = _convert_to_int_or_float(power_parts["dividend"], 1)

    if divisor == 1:
        return dividend
    return dividend / divisor


# "½⅓⅕⅙⅛⅔⅖⅚⅜¾⅗⅝⅞⅘¼⅐⅑⅒"

_neutral_superscripts_fractions = {}

_almost_all_the_powers = {
    "¹": 1,
    "⁺¹": 1,
    "⁻¹": -1,
    "²": 2,
    "⁺²": 2,
    "⁻²": -2,
    "³": 3,
    "⁺³": 3,
    "⁻³": -3,
    "⁴": 4,
    "⁺⁴": 4,
    "⁻⁴": -4,
    "½": 1 / 2,
    "⁺½": 1 / 2,
    "⁻½": -1 / 2,
    "⅔": 2 / 3,
    "⁺⅔": 2 / 3,
    "⁻⅔": -2 / 3,
    "⅓": 1 / 3,
    "⁺⅓": 1 / 3,
    "⁻⅓": -1 / 3,
}

_neutral_superscripts_fractions = {
    "½": (1 / 2),
    "⅓": (1 / 3),
    "¼": (1 / 4),
    "⅕": (1 / 5),
    "⅙": (1 / 6),
    "⅐": (1 / 7),
    "⅛": (1 / 8),
    "⅑": (1 / 9),
    "⅒": (1 / 10),
    "⅔": (2 / 3),
    "⅖": (2 / 5),
    "¾": (3 / 4),
    "⅗": (3 / 5),
    "⅜": (3 / 8),
    "⅘": (4 / 5),
    "⅚": (5 / 6),
    "⅝": (5 / 8),
    "⅞": (7 / 8),
}

_negative_superscript_fractions = {
    "⁻" + power: fraction for power, fraction in _neutral_superscripts_fractions.items()
}

_positive_superscript_fractions = {
    "⁺" + power: fraction for power, fraction in _neutral_superscripts_fractions.items()
}

_superscript_fractions = copy.copy(_neutral_superscripts_fractions)
_superscript_fractions.update(_negative_superscript_fractions)
_superscript_fractions.update(_positive_superscript_fractions)


class UnknownUnit(object):
    UNIT_TYPE = -2

    def __init__(
        self, unit_text: str, switch_power: bool = False, was_enclosed: bool = False
    ):
        """
        The unknown unit appears for cases in which text could not be resolved to
        units known by the current runtime library.

        Args:
            unit_text:
                Text for which no 'known' unit could be found.

            switch_power:
                States whether the unit would need to switch power due to division.

            was_enclosed:
                States if the unit text was enclosed by round brackets.

        Examples:

            Fruits are definitivelly unknown to the unit library.

            >>> import justunits
            >>> justunits.from_string("pear/apple")
            (UnknownUnit('pear'), UnknownUnit('apple' *^-1))

            Any unknown occurance can be registered.

            >>> justunits.register_unit(justunits.create_unit("pear", "pear", "fruit"))
            >>> justunits.from_string("pear/apple")
            (AUnit(pear 'pear' fruit), UnknownUnit('apple' *^-1))

        .. doctest::
           :hide:

            >>> import justunits
            >>> justunits.reset_unit_library()
            >>> justunits.from_string("pear/apple")
            (UnknownUnit('pear'), UnknownUnit('apple' *^-1))
        """
        assert unit_text != "", "An empty unit text should not be supported."
        self._unit_text = unit_text
        self._switching_power_needed = switch_power
        self._was_enclosed = was_enclosed

    @property
    def first_letter(self):
        """
        The first letter of the unit's text.

        Returns:
            int

        Examples:

            >>> from justunits import UnknownUnit
            >>> UnknownUnit("apple").first_letter
            'a'
        """
        assert len(self._unit_text) > 0, "An empty unknown unit is not supported."
        return self._unit_text[0]

    @property
    def power(self):
        if self._switching_power_needed:
            return -1
        return 1

    @property
    def symbol(self) -> str:
        return self._unit_text

    @property
    def width(self) -> int:
        """
        Returns the width (length) of the unit's text.

        Returns:
            int

        Examples:

            >>> from justunits import UnknownUnit
            >>> UnknownUnit("apple").width
            5
        """
        return len(self._unit_text)

    @property
    def text(self) -> str:
        """
        The text which contains unknown unit definitions. They might be not
        detected yet.

        Returns:
            str
        """
        return self._unit_text

    @property
    def switching_power_needed(self) -> bool:
        """
        States whether the power of an unit must be switched after detection or not.

        Returns:
            bool
        """
        return self._switching_power_needed

    def split(self, splitting_pattern: Optional[Pattern] = None) -> List["UnknownUnit"]:
        """

        Args:
            splitting_pattern:
                Regex pattern splitting the unit. If not provided, than the default
                splitting pattern is used.

        Returns:
            List[UnknownUnit]

        Examples:
            >>> from justunits import UnknownUnit
            >>> UnknownUnit("N*m").split()
            [UnknownUnit('N'), UnknownUnit('m')]
            >>> UnknownUnit("s", switch_power=True).split()
            [UnknownUnit('s' *^-1)]
            >>> UnknownUnit("axb_c").split(re.compile("[x_]"))
            [UnknownUnit('a'), UnknownUnit('b'), UnknownUnit('c')]

        """
        if splitting_pattern is None:
            splitting_pattern = _SPLITS_UNITS_PATTERN
        split_text_parts = splitting_pattern.split(self._unit_text)
        split_unknown_units = [
            UnknownUnit(unit_text=split_text, switch_power=self._switching_power_needed)
            for split_text in split_text_parts
        ]
        return split_unknown_units

    def __repr__(self):
        power_switching = ""
        if self._switching_power_needed:
            power_switching = " *^-1"
        return "{}('{}'{})".format(
            self.__class__.__name__, self._unit_text, power_switching
        )


def _match_unit(unit_text: str, unit_pattern: Pattern) -> Optional[Tuple[dict, str]]:
    """

    Args:
        unit_text:
        unit_pattern:

    Returns:


    .. doctest::

        >>> millisecond_pattern = re.compile(_BASE_UNIT_PATTERN.format("ms"))
        >>> _match_unit("ms^-1", millisecond_pattern)
        ({'symbol': 'ms', 'power': '^-1'}, '')
        >>> _match_unit("ms⁻¹", millisecond_pattern)
        ({'symbol': 'ms', 'power': '⁻¹'}, '')
        >>> meter_pattern = re.compile(_BASE_UNIT_PATTERN.format("m"))
        >>> _match_unit("m²", meter_pattern)
        ({'symbol': 'm', 'power': '²'}, '')
        >>> _match_unit("m⁺²", meter_pattern)
        ({'symbol': 'm', 'power': '⁺²'}, '')
        >>> _match_unit("mm²", meter_pattern)
        ({'symbol': 'm', 'power': '1'}, 'm²')
        >>> found_nothing = _match_unit("µm²", meter_pattern)
        >>> print(found_nothing)
        None
    """
    matched_unit = unit_pattern.search(unit_text)
    if matched_unit is None:
        return None

    matched_parts = matched_unit.groupdict()
    symbol = matched_unit["symbol"]
    power_of_unit = matched_parts["power"]

    if power_of_unit is None or not power_of_unit:
        power_of_unit = "1"

    remains = unit_text[matched_unit.end() :]

    return {"symbol": symbol, "power": power_of_unit}, remains


def _convert_power_representation(power_repr) -> float:
    """

    Args:
        power_repr:

    Returns:


    .. doctest::
        >>> _convert_power_representation("1")
        1
        >>> _convert_power_representation("²")
        2
        >>> _convert_power_representation("⁻½")
        -0.5
    """
    try:
        return _almost_all_the_powers[power_repr]
    except KeyError:
        pass

    if power_repr == "1":
        return 1

    potential_power = _convert_raw_power(power_text=power_repr)

    if potential_power is None:
        raise NotImplementedError(
            "The representation of the power '{}' is not implemented/supported"
            " within this version. Please create an issue at {}.".format(
                power_repr, _source_repository_url
            )
        )

    return potential_power


_beneath_divider = re.compile(r"(/\(.*?\)|/.*)[\*⋅]?")


def _extract_enclosed(unit_text: str) -> str:
    """

    Args:
        unit_text:

    Returns:

    >>> _extract_enclosed("(a)")
    'a'
    >>> _extract_enclosed("/(a*b)*")
    'a*b'
    >>> _extract_enclosed("")
    ''
    """
    if not unit_text:
        return ""
    matched_enclosing = _enclosed_unit_pattern.search(unit_text)
    if matched_enclosing is None:
        return unit_text
    return matched_enclosing.group(1)


def _split_divisions_of_units(unit_text: str) -> List[UnknownUnit]:
    """

    Args:
        unit_text:

    Returns:

    .. doctest::

        >>> from doctestprinter import doctest_iter_print
        >>> _split_divisions_of_units("")
        []
        >>> doctest_iter_print(_split_divisions_of_units("a*b/(c*d)*e*f/g"))
        UnknownUnit('a*b')
        UnknownUnit('c*d' *^-1)
        UnknownUnit('e*f')
        UnknownUnit('g' *^-1)
        >>> _split_divisions_of_units("a")
        [UnknownUnit('a')]
        >>> _split_divisions_of_units("a/b")
        [UnknownUnit('a'), UnknownUnit('b' *^-1)]
        >>> _split_divisions_of_units("ab/(c*d²)")
        [UnknownUnit('ab'), UnknownUnit('c*d²' *^-1)]
        >>> _split_divisions_of_units("ab/(c*d²)*e²")
        [UnknownUnit('ab'), UnknownUnit('c*d²' *^-1), UnknownUnit('e²')]
        >>> _split_divisions_of_units("ab/(c*d²)*e")
        [UnknownUnit('ab'), UnknownUnit('c*d²' *^-1), UnknownUnit('e')]
    """
    got_an_empty_unit_so_return_empty_list = not unit_text
    if got_an_empty_unit_so_return_empty_list:
        return []

    nothing_to_split_so_leave_early = _UNIT_DIVIDER_CHAR not in unit_text
    if nothing_to_split_so_leave_early:
        return [UnknownUnit(unit_text)]

    separated_units_by_divider = []
    last_end = 0
    for dividing_item in _beneath_divider.finditer(unit_text):
        start, end = dividing_item.span()
        if start > 0:
            leading_item = unit_text[last_end:start]
            if leading_item:
                separated_units_by_divider.append(UnknownUnit(leading_item))
        sub_unit_text = dividing_item.group(0)[1:]
        sub_unit_text = _extract_enclosed(sub_unit_text)
        sub_unit = UnknownUnit(sub_unit_text, switch_power=True)
        separated_units_by_divider.append(sub_unit)
        last_end = end

    a_trailing_part_exists = last_end < len(unit_text)
    if a_trailing_part_exists:
        trailing_unit_text = unit_text[last_end:]
        trailing_item = UnknownUnit(trailing_unit_text)
        separated_units_by_divider.append(trailing_item)

    return separated_units_by_divider

    had_enclosed_units, unit_text = _substitute_enclosed_separator(unit_text)
    top_unit_text, *bottom_unit_text = unit_text.split(_UNIT_DIVIDER_CHAR, 1)
    if bottom_unit_text:
        return [
            UnknownUnit(top_unit_text),
            UnknownUnit(bottom_unit_text[0], switch_power=True),
        ]
    return [UnknownUnit(top_unit_text)]


def _pre_split_units_by_delimiter(
    *unknown_units,
) -> List[UnknownUnit]:
    """

    Args:
        unit_text:

    Returns:


    .. doctest::

        >>> _pre_split_units_by_delimiter(UnknownUnit("m*s^-1"))
        [UnknownUnit('m'), UnknownUnit('s^-1')]
        >>> _pre_split_units_by_delimiter(UnknownUnit("m⋅s⁻¹"))
        [UnknownUnit('m'), UnknownUnit('s⁻¹')]
        >>> _pre_split_units_by_delimiter(UnknownUnit("m*s²", switch_power=True))
        [UnknownUnit('m' *^-1), UnknownUnit('s²' *^-1)]

    """
    if not unknown_units:
        return []

    assert isinstance(
        unknown_units[0], UnknownUnit
    ), "unknown_units must contain UnknownUnit-types."

    split_unknown_units = []
    for unknown_unit in unknown_units:
        split_units = unknown_unit.split()
        split_unknown_units.extend(split_units)
    return split_unknown_units


def _split_text_into_unknown_units(unit_text: str) -> List[UnknownUnit]:
    """

    Args:
        unit_text:

    Returns:


    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> # Access to private member for testing
        >>> # noinspection PyProtectedMember
        >>> from justunits import _split_text_into_unknown_units
        >>> _split_text_into_unknown_units("m/s")
        [UnknownUnit('m'), UnknownUnit('s' *^-1)]
        >>> doctest_iter_print(_split_text_into_unknown_units("a*b/(c⋅d)"))
        UnknownUnit('a')
        UnknownUnit('b')
        UnknownUnit('c' *^-1)
        UnknownUnit('d' *^-1)
        >>> doctest_iter_print(_split_text_into_unknown_units("ab/(c*d^2)*e"))
        UnknownUnit('ab')
        UnknownUnit('c' *^-1)
        UnknownUnit('d^2' *^-1)
        UnknownUnit('e')
    """
    split_by_divider = _split_divisions_of_units(unit_text=unit_text)
    final_split_units = _pre_split_units_by_delimiter(*split_by_divider)
    return final_split_units


class AUnit(object):
    UNIT_TYPE = 1

    def __init__(
        self,
        raw_unit: BareUnit,
        prefix: Optional[Prefix] = None,
        power: Union[int, float] = 1,
    ):
        """
        A unit represents just a single unit like meter 'm' and second 's'. In this
        context a unit is defined a distingtiv symbol (mostly a single letter).

        Args:
            raw_unit:
                The raw unit this unit is based on.

            prefix:
                The SI-Prefix of this unit.

            power:
                Power of this unit. Default is 1.

        Examples:

            .. currentmodule:: justunits

            A unit is composed of an immutable :data:`RawUnit`, :class:`SiPrefix` and
            the power the *RawUnit* comes with.

            >>> from justunits import SiPrefixes
            >>> raw_apple = BareUnit("apple", "apple", "fruit")
            >>> apple = AUnit(raw_apple)
            >>> apple
            AUnit(apple 'apple' fruit)
            >>> print(apple)
            apple
            >>> kiloapple = AUnit(raw_apple, prefix=SiPrefixes.kilo)
            >>> kiloapple
            AUnit(kapple 'kiloapple' fruit, 1e+03apple)


            :class:`AUnit` are comparable and hashable to support usage as key
            within within mappings.

            >>> another_apple = create_unit("apple", "apple", "fruit")
            >>> apple == another_apple
            True

            >>> apple != kiloapple
            True

            >>> hash(apple) == hash(another_apple)
            True

            >>> hash(apple) == hash(kiloapple)
            False

            >>> map = {apple: "an apple", kiloapple: "many apples"}
            >>> map[kiloapple]
            'many apples'

        .. doctest::
           :hide:

            >>> import justunits
            >>> meter = justunits.SiUnits.meter.with_prefix(justunits.SiPrefixes.milli)
            >>> meter.symbol
            'mm'
            >>> meter.name
            'millimeter'
            >>> meter.quantity
            'length'


        """
        warnings.warn(
            "AUnit might be renamed within the next release for a better distinction.",
            PendingDeprecationWarning
        )

        self._unit = raw_unit

        try:
            self._power = float(power)
        except TypeError:
            raise TypeError("The power of an unit must be a float.")

        if prefix is not None:
            self._prefix = prefix
        else:
            self._prefix = PREFIX_FOR_ONE
        self._complete_name = self._prefix.name + self._unit.name
        self._complete_symbol = self._prefix.symbol + self._unit.symbol

    def __repr__(self):
        if self._power == 1:
            power_repr = ""
        else:
            power_repr = "; power={:.1g}".format(self._power)

        if self._prefix.decimal == 1:
            decimal_repr = ""
        else:
            decimal_repr = ", {:.1g}{}".format(self._prefix.decimal, self._unit.symbol)

        return "AUnit({symbol} '{name}' {quantity}{decimal_unit}{power})".format(
            symbol=self._complete_symbol,
            name=self._complete_name,
            quantity=self._unit.quantity,
            decimal_unit=decimal_repr,
            power=power_repr,
        )

    def __str__(self):
        if self._power == 1:
            return "{}".format(self._complete_symbol)
        else:
            return "{}^{}".format(self._complete_symbol, self._power)

    def __copy__(self) -> "AUnit":
        return self.__class__(self._unit, self._prefix, self._power)

    def __eq__(self, other):
        return other and self.symbol == other.symbol and self.power == other.power

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.symbol, self.power))

    def __iter__(self) -> Iterator["AUnit"]:
        yield self

    def __len__(self):
        return 1

    def __getitem__(self, index: int) -> "AUnit":
        if index != 0:
            raise IndexError("Index out of bound. AUnit just has itself.")
        return self

    def switch_power(self):
        """
        The unit's power is multiplied by -1.

        Examples:

            >>> raw_apple = BareUnit("apple", "apple", "fruit")
            >>> sample_unit = AUnit(raw_apple)
            >>> str(sample_unit)
            'apple'
            >>> sample_unit.switch_power()
            >>> str(sample_unit)
            'apple^-1.0'
        """
        self._power *= -1

    @property
    def power(self) -> Union[int, float]:
        """
        The units power. Default is ^1.

        Returns:
            Union[int, float]
        """
        return self._power

    @property
    def width(self) -> int:
        """
        Width (length) of the unit's symbol (including any prefix).

        Returns:
            int
        """
        return len(self._complete_symbol)

    @property
    def first_letter(self) -> str:
        """
        The symbols first letter.

        Returns:
            str
        """
        return self._complete_symbol[0]

    @property
    def symbol(self) -> str:
        """
        The unit's symbol including any prefix.

        Returns:
            str
        """
        return self._complete_symbol

    @property
    def name(self) -> str:
        """
        The units name.

        Returns:
            str
        """
        return self._complete_name

    @property
    def quantity(self) -> str:
        """
        The quantity the unit stands for.

        Returns:
            str
        """
        return self._unit.quantity

    @property
    def base_symbol(self) -> str:
        """
        The unit's symbol without any prefix.

        Returns:
            str
        """
        return self._unit.symbol

    @property
    def prefix_symbol(self) -> str:
        """
        The symbol of the unit's prefix, if carrying one.

        Notes:
            The base unit carries a prefix representing 1 with an empty str as prefix.

        Returns:
            str
        """
        return self._prefix.symbol

    def with_power(self, power: Union[int, float]) -> "AUnit":
        """
        Returns a unit based on this unit's base unit with the requested power.

        Args:
            power:
                Power the new unit should carry.

        Returns:
            AUnit

        Examples:
            >>> import justunits
            >>> from justunits import SiUnits, SiPrefixes
            >>> capture_time = SiUnits.second.with_prefix(SiPrefixes.nano)
            >>> capture_time
            AUnit(ns 'nanosecond' time, 1e-09s)
            >>> frames_per_second = capture_time.with_power(-1)
            >>> frames_per_second
            AUnit(ns 'nanosecond' time, 1e-09s; power=-1)
            >>> justunits.to_string(frames_per_second)
            'ns'
        """
        return self.__class__(self._unit, power=power, prefix=self._prefix)

    def with_prefix(self, prefix: Prefix) -> "AUnit":
        """
        Returns a unit based on this unit's base unit with the requested prefix.

        Args:
            prefix:
                The prefix of the requested unit.

        Returns:
            AUnit

        Examples:
            >>> from justunits import SiUnits, SiPrefixes
            >>> capture_time = SiUnits.second.with_prefix(SiPrefixes.nano)
            >>> capture_time
            AUnit(ns 'nanosecond' time, 1e-09s)
        """
        return self.__class__(self._unit, power=self._power, prefix=prefix)

    def without_prefix(self) -> "AUnit":
        """
        The base unit with the current power.

        Returns:
            AUnit

        Examples:
            >>> from justunits import SiUnits, SiPrefixes
            >>> capture_time = SiUnits.second.with_prefix(SiPrefixes.nano)
            >>> frames_per_second = capture_time.with_power(-1)
            >>> frames_per_second
            AUnit(ns 'nanosecond' time, 1e-09s; power=-1)
            >>> frames_per_second.without_prefix()
            AUnit(s 'second' time; power=-1)

        """
        return self.__class__(self._unit, power=self._power)

    def bare(self) -> "AUnit":
        """
        A unit based on this unit's base unit solely.

        Returns:
            AUnit

        Examples:
            >>> from justunits import SiUnits, SiPrefixes
            >>> capture_time = SiUnits.second.with_prefix(SiPrefixes.nano)
            >>> frames_per_second = capture_time.with_power(-1)
            >>> frames_per_second
            AUnit(ns 'nanosecond' time, 1e-09s; power=-1)
            >>> frames_per_second.bare()
            AUnit(s 'second' time)
        """
        return self.__class__(self._unit)

    def to_raw_parts(self) -> List:
        """


        Returns:

        Examples:

            >>> from justunits import SiUnits
            >>> from doctestprinter import doctest_print
            >>> doctest_print(SiUnits.millimeter.to_raw_parts(), max_line_width=50)
            [BareUnit('m', 'meter', 'length'), Prefix(symbol='m',
            name='milli', decimal=0.001), 1.0]

            >>> doctest_print(SiUnits.meter.to_raw_parts(), max_line_width=50)
            [BareUnit('m', 'meter', 'length'), Prefix(symbol='',
            name='', decimal=1), 1.0]

        """
        return [self._unit, self._prefix, self._power]


def create_unit(symbol: str, name: str, quantity: str, prefix: Optional[Prefix] = None) -> AUnit:
    """
    Creates a basic unit of your liking.

    Args:
        symbol:
            Symbol the carries.

        name:
            The unit's name.

        quantity:
            What the unit stands for.

        prefix:
            An optional, additional prefix.

    Returns:
        AUnit

    Examples:
        >>> from justunits import create_unit
        >>> create_unit("ba", "banana", "fruit", prefix=SiPrefixes.atto)
        AUnit(aba 'attobanana' fruit, 1e-18ba)

    """
    return AUnit(BareUnit(symbol=symbol, name=name, quantity=quantity), prefix=prefix)


_base_si_unit_map = {
    "s": AUnit(BareUnit("s", "second", "time")),
    "m": AUnit(BareUnit("m", "meter", "length")),
    "kg": AUnit(BareUnit("g", "gram", "mass"), prefix=SiPrefixes.kilo),
    "A": AUnit(BareUnit("A", "ampere", "electric current")),
    "K": AUnit(BareUnit("K", "kelvin", "thermodynamic temperature")),
    "mol": AUnit(BareUnit("mol", "mole", "amount of substance")),
    "cd": AUnit(BareUnit("cd", "candela", "luminous intensity")),
}

_si_unit_map = {
    "rad": AUnit(BareUnit("rad", "radian", "plane angle")),
    "sr": AUnit(BareUnit("sr", "steradian", "solid angle")),
    "Hz": AUnit(BareUnit("Hz", "hertz", "frequency")),
    "N": AUnit(BareUnit("N", "newton", "force, weight")),
    "Pa": AUnit(BareUnit("Pa", "pascal", "pressure, stress")),
    "J": AUnit(BareUnit("J", "joule", "energy, work, heat")),
    "W": AUnit(BareUnit("W", "watt", "power, radiant flux")),
    "C": AUnit(BareUnit("C", "coulomb ", "electric charge")),
    "V": AUnit(
        BareUnit("V", "volt", "electrical potential difference (voltage)), emf")
    ),
    "F": AUnit(BareUnit("F", "farad", "capacitance ")),
    "Ω": AUnit(BareUnit("Ω", "ohm", "resistance, impedance, reactance")),
    "S": AUnit(BareUnit("S", "siemens ", "electrical conductance")),
    "Wb": AUnit(BareUnit("Wb", "weber", "magnetic flux ")),
    "T": AUnit(BareUnit("T", "tesla", "magnetic flux density ")),
    "H": AUnit(BareUnit("H", "henry", "inductance")),
    "°C": AUnit(BareUnit("°C", "degree Celsius", "temperature relative to 273.15 K")),
    "lm": AUnit(BareUnit("lm", "lumen", "luminous flux ")),
    "lx": AUnit(BareUnit("lx", "lux", "illuminance ")),
    "Bq": AUnit(BareUnit("Bq", "becquerel", "radioactivity (decays per unit time) ")),
    "Gy": AUnit(BareUnit("Gy", "gray", "absorbed dose (of ionising radiation) ")),
    "Sv": AUnit(BareUnit("Sv", "sievert", "equivalent dose (of ionising radiation)")),
    "kat": AUnit(BareUnit("kat", "katal", "catalytic activity")),
}


class BaseSiUnits:
    second = _base_si_unit_map["s"]
    meter = _base_si_unit_map["m"]
    kilogram = _base_si_unit_map["kg"]
    ampere = _base_si_unit_map["A"]
    kelvin = _base_si_unit_map["K"]
    mol = _base_si_unit_map["mol"]
    candela = _base_si_unit_map["cd"]

    @staticmethod
    def get_unit(symbol: str) -> AUnit:
        """
        Returns a SI-Unit for the requested symbol.

        Args:
            symbol(str):
                Symbol of an SI-Unit.

        Returns:
            AUnit

        Raises:
            KeyError

        Examples:

            >>> import justunits
            >>> justunits.BaseSiUnits.get_unit("m")
            AUnit(m 'meter' length)

            AttributeError: type object 'BaseSiUnits' has no attribute 'get_prefix'

            >>> justunits.SiUnits.get_unit("i")
            Traceback (most recent call last):
            ...
            KeyError: 'The supplied key is not a SI-AUnit and does not exist.'
            >>> justunits.SiUnits.get_unit(None)
            Traceback (most recent call last):
            ...
            KeyError: 'The supplied key is not a SI-AUnit and does not exist.'
        """
        try:
            return AUnit(_base_si_unit_map[symbol])
        except KeyError:
            raise KeyError("The supplied key is not a SI-AUnit and does not exist.")




_additional_units = {
    "g": AUnit(BareUnit("g", "gram", "mass")),
    "t": AUnit(BareUnit("t", "tonne", "mass")),
}


class SiUnits(BaseSiUnits):
    millimeter = BaseSiUnits.meter.with_prefix(prefix=SiPrefixes.milli)
    kilometer = BaseSiUnits.meter.with_prefix(prefix=SiPrefixes.kilo)
    gram = _additional_units["g"]
    tonne = _additional_units["t"]
    radian = _si_unit_map["rad"]
    steradian = _si_unit_map["sr"]
    hertz = _si_unit_map["Hz"]
    newton = _si_unit_map["N"]
    pascal = _si_unit_map["Pa"]
    joule = _si_unit_map["J"]
    watt = _si_unit_map["W"]
    coulomb = _si_unit_map["C"]
    volt = _si_unit_map["V"]
    farad = _si_unit_map["F"]
    ohm = _si_unit_map["Ω"]
    siemens = _si_unit_map["S"]
    weber = _si_unit_map["Wb"]
    tesla = _si_unit_map["T"]
    henry = _si_unit_map["H"]
    degree_celsius = _si_unit_map["°C"]
    lumen = _si_unit_map["lm"]
    lux = _si_unit_map["lx"]
    becquerel = _si_unit_map["Bq"]
    gray = _si_unit_map["Gy"]
    sievert = _si_unit_map["Sv"]
    katal = _si_unit_map["kat"]


def prefix_base_unit(
    base_unit: BareUnit, supported_prefixes: Iterable[str]
) -> List[AUnit]:
    """

    Args:
        base_unit:
        supported_prefixes:

    Returns:

    Examples:

        >>> from doctestprinter import doctest_iter_print
        >>> base_unit = BareUnit("m", "meter", "length")
        >>> units = prefix_base_unit(base_unit, ["m", "k", "µ"])
        >>> doctest_iter_print(units, edits_item=lambda x: repr(x))
        AUnit(m 'meter' length)
        AUnit(mm 'millimeter' length, 0.001m)
        AUnit(km 'kilometer' length, 1e+03m)
        AUnit(μm 'micrometer' length, 1e-06m)

        >>> units = prefix_base_unit(base_unit, "")
        >>> doctest_iter_print(units, edits_item=lambda x: repr(x))
        AUnit(m 'meter' length)
    """
    requested_units = [AUnit(base_unit)]

    if supported_prefixes is None or not supported_prefixes:
        return requested_units

    for prefix_symbol in supported_prefixes:
        try:
            prefix = _base_si_prefixes[prefix_symbol]
        except KeyError:
            raise KeyError(
                "Prefix with the symbol '{}' could not be obtained for"
                " the unit {}".format(prefix_symbol, base_unit.name)
            )
        new_unit = AUnit(base_unit, prefix=prefix)
        requested_units.append(new_unit)
    return requested_units


_KeyChainIndex = namedtuple("_KeyChainIndex", "letter_index length")


class _ChainedUnitItem(object):
    """
    Examples:
        >>> from justunits import SiUnits
        >>> meter_item = _ChainedUnitItem(SiUnits.meter)
        >>> mol_item = _ChainedUnitItem(SiUnits.mol)
        >>> mol_item.sort_in(meter_item)
        >>> mol_item
        mol -> m


        >>> meter_item = _ChainedUnitItem(SiUnits.meter)
        >>> mol_item = _ChainedUnitItem(SiUnits.mol)
        >>> meter_item.sort_in(mol_item)
        >>> meter_item
        m
        >>> meter_item.left_end
        mol -> m

    """

    def __init__(self, unit):
        self._unit = unit
        self._pattern = re.compile(_BASE_UNIT_PATTERN.format(self._unit.symbol))
        self.next_item = None
        self.previous_item = None

    def __repr__(self):
        if self.next_item is not None:
            return "{} -> {}".format(self._unit.symbol, repr(self.next_item))
        return self._unit.symbol

    @property
    def left_end(self) -> "_ChainedUnitItem":
        if self.previous_item is None:
            return self
        return self.previous_item.left_end

    @property
    def unit(self) -> AUnit:
        return self._unit

    @property
    def first_letter(self) -> str:
        return self._unit.first_letter

    @property
    def symbol_width(self) -> int:
        return self._unit.width

    def sort_in(self, unit_item: "_ChainedUnitItem"):
        """

        Args:
            unit_item:

        Returns:

        """
        i_and_other_share_same_category = unit_item.first_letter == self.first_letter
        if not i_and_other_share_same_category:
            raise ValueError("The unit must be of an equal category.")

        other_is_equal_or_thinner = unit_item.symbol_width <= self.symbol_width
        if other_is_equal_or_thinner:
            if self.next_item is not None:
                self.next_item.sort_in(unit_item)
                return
            self.link_right(unit_item)

        other_is_wider_switch_place = self.symbol_width < unit_item.symbol_width
        if other_is_wider_switch_place:
            self.link_left(unit_item)

    def link_right(self, new_chain_item: "_ChainedUnitItem"):
        """

        Args:
            new_chain_item:

        Returns:

        .. doctest::

            >>> # Access to private member for testing
            >>> # noinspection PyProtectedMember
            >>> from justunits import _ChainedUnitItem, create_unit
            >>> first_item = _ChainedUnitItem(create_unit("a", "", ""))
            >>> second_item = _ChainedUnitItem(create_unit("b", "", ""))
            >>> third_item = _ChainedUnitItem(create_unit("c", "", ""))
            >>> first_item.link_right(second_item)
            >>> first_item
            a -> b
            >>> second_item.previous_item
            a -> b
            >>> second_item
            b
            >>> first_item.link_right(third_item)
            Traceback (most recent call last):
            ...
            ValueError: A right chaining can only be performed, if not already chained.

        """
        if new_chain_item is self:
            raise ValueError("A item cannot be linked to itself.")
        if self.next_item is not None:
            raise ValueError(
                "A right chaining can only be performed, if not already chained."
            )
        self.next_item = new_chain_item
        self.next_item.previous_item = self

    def link_left(self, new_chain_item: "_ChainedUnitItem"):
        """

        Args:
        new_chain_item:

        Returns:

        .. doctest::

            >>> # Access to private member for testing
            >>> # noinspection PyProtectedMember
            >>> from justunits import _ChainedUnitItem, create_unit
            >>> first_item = _ChainedUnitItem(create_unit("a", "", ""))
            >>> second_item = _ChainedUnitItem(create_unit("b", "", ""))
            >>> third_item = _ChainedUnitItem(create_unit("c", "", ""))
            >>> second_item.link_left(first_item)
            >>> first_item
            a -> b
            >>> second_item.previous_item
            a -> b
            >>> second_item
            b
            >>> second_item.link_left(third_item)
            >>> third_item
            c -> b
            >>> first_item
            a -> c -> b

        """
        if new_chain_item is self:
            raise ValueError("A item cannot be linked to itself.")
        # the previous_item item get the new item as the next in the chain
        an_existing_previous_item_gets_the_new_item = self.previous_item is not None
        if an_existing_previous_item_gets_the_new_item:
            self.previous_item.next_item = new_chain_item
        # switch places between self and new item
        new_chain_item.previous_item = self.previous_item
        new_chain_item.next_item = self
        self.previous_item = new_chain_item

    def detect(self, unknown_unit: UnknownUnit) -> List[AUnit]:
        """
        Detects the leading unit within an equal category (first letter)
        of this chain.

        Args:
            unknown_unit:

        Returns:
            List[AUnit]:
                The detected units and/or undetected *unknown unit*.

        Examples:

            >>> # Access to private member for testing
            >>> # noinspection PyProtectedMember
            >>> from justunits import SiUnits, SiPrefixes, _ChainedUnitItem
            >>> from doctestprinter import doctest_iter_print
            >>> mole_item = _ChainedUnitItem(SiUnits.mol)
            >>> found_units = mole_item.detect(UnknownUnit("mmolm"))
            >>> print(found_units)
            [UnknownUnit('mmolm')]
            >>> found_units = mole_item.detect(UnknownUnit("molmm"))
            >>> doctest_iter_print(found_units, edits_item=repr)
            AUnit(mol 'mole' amount of substance)
            UnknownUnit('mm')

            >>> mole_item.sort_in(_ChainedUnitItem(SiUnits.millimeter))
            >>> mole_item
            mol -> mm
            >>> found_units = mole_item.detect(UnknownUnit("mmmol"))
            >>> doctest_iter_print(found_units, edits_item=repr)
            AUnit(mm 'millimeter' length, 0.001m)
            UnknownUnit('mol')

        """
        cannot_fit_in = unknown_unit.width < self.symbol_width
        if cannot_fit_in:
            if self.next_item is None:
                return [unknown_unit]
            return self.next_item.detect(unknown_unit=unknown_unit)

        matching_result = _match_unit(unknown_unit.text, unit_pattern=self._pattern)
        was_not_within_unknown_unit = matching_result is None
        if was_not_within_unknown_unit:
            if self.next_item is None:
                return [unknown_unit]
            return self.next_item.detect(unknown_unit=unknown_unit)

        symbol_power, remaining_unit_text = matching_result
        power_of_unit = _convert_power_representation(symbol_power["power"])
        found_unit = self._unit.with_power(power_of_unit)
        if unknown_unit.switching_power_needed:
            found_unit.switch_power()

        units_are_still_undetected = len(remaining_unit_text) > 0
        if units_are_still_undetected:
            undetected_units = UnknownUnit(
                remaining_unit_text,
                switch_power=unknown_unit.switching_power_needed,
            )
            return [found_unit, undetected_units]
        return [found_unit]


class _UnitLibrary:
    """
    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> from justunits import SiUnits

        2 units with same first char but different length.

        >>> mole = SiUnits.mol
        >>> meter = SiUnits.meter

        A made up unit with same leading letter and equal length to 'mole'.

        >>> mate = AUnit(BareUnit("mat", "mate", "a tea"))

        A made up unit with same but uppercase leading letter and equal length
        to 'meter'.

        >>> big_m = AUnit(BareUnit("M", "Big M", "Makes m big"))

        Other units which should be sort in.

        >>> second = SiUnits.second
        >>> ampere = SiUnits.ampere

        >>> sample_map = _UnitLibrary()
        >>> sample_map.register_many(mate, mole, meter, big_m, second, ampere)
        >>> doctest_iter_print(sample_map.short_cuts)
        _KeyChainIndex(letter_index='m', length=3):
          mat -> mol -> m
        _KeyChainIndex(letter_index='m', length=1):
          m
        _KeyChainIndex(letter_index='M', length=1):
          M
        _KeyChainIndex(letter_index='s', length=1):
          s
        _KeyChainIndex(letter_index='A', length=1):
          A

    """

    def __init__(self):
        self._units = OrderedDict()
        self._short_cuts = {}
        self._categories = {}

    @property
    def short_cuts(self):
        return self._short_cuts

    @property
    def categories(self):
        return self._categories

    @staticmethod
    def create_chain_index(unit: AUnit) -> _KeyChainIndex:
        """

        Args:
            unit:

        Returns:


        Examples:
            >>> from justunits import SiUnits, SiPrefixes
            >>> _UnitLibrary.create_chain_index(SiUnits.meter)
            _KeyChainIndex(letter_index='m', length=1)

            >>> _UnitLibrary.create_chain_index(SiUnits.millimeter)
            _KeyChainIndex(letter_index='m', length=2)

            >>> _UnitLibrary.create_chain_index(SiUnits.kilogram)
            _KeyChainIndex(letter_index='k', length=2)
        """
        key = unit.first_letter
        symbol_length = unit.width
        return _KeyChainIndex(key, symbol_length)

    def register_many(self, *units):
        """

        Args:
            *units:

        Returns:


        Examples:

            >>> from doctestprinter import doctest_iter_print
            >>> # Access to private member for testing
            >>> # noinspection PyProtectedMember
            >>> from justunits import _UnitLibrary, SiUnits
            >>> sample_library = _UnitLibrary()
            >>> sample_library.register_many(
            ...     SiUnits.meter,
            ...     SiUnits.meter.with_prefix(SiPrefixes.milli),
            ...     SiUnits.mol,
            ...     SiUnits.second,
            ...     SiUnits.kilogram
            ... )

            >>> doctest_iter_print(sample_library.short_cuts)
            _KeyChainIndex(letter_index='m', length=1):
              m
            _KeyChainIndex(letter_index='m', length=2):
              mm -> m
            _KeyChainIndex(letter_index='m', length=3):
              mol -> mm -> m
            _KeyChainIndex(letter_index='s', length=1):
              s
            _KeyChainIndex(letter_index='k', length=2):
              kg


            >>> doctest_iter_print(sample_library.categories)
            m:
              mol -> mm -> m
            s:
              s
            k:
              kg

        """
        for unit in units:
            self.register_unit(unit)

    def register_unit(self, unit: AUnit):
        """

        Args:
            unit:

        Returns:

        Examples:

            >>> from doctestprinter import doctest_iter_print
            >>> # Access to private member for testing
            >>> # noinspection PyProtectedMember
            >>> from justunits import _UnitLibrary, SiUnits
            >>> millisecond = SiUnits.second.with_prefix(SiPrefixes.milli)
            >>> millimeter = SiUnits.meter.with_prefix(SiPrefixes.milli)
            >>> sample_library = _UnitLibrary()
            >>> sample_library.register_unit(millimeter)
            >>> sample_library.register_unit(millisecond)
            >>> doctest_iter_print(sample_library.short_cuts)
            _KeyChainIndex(letter_index='m', length=2):
              mm -> ms

        """
        if unit.symbol in self._units:
            overridden_unit = self._units[unit.symbol]
            overridden_unit_repr = "'{} {}'".format(
                overridden_unit.symbol, overridden_unit.name
            )
            overriding_repr = "'{} {}'".format(unit.symbol, unit.name)
            warnings.warn(
                "The current unit {overriding} will override the existing unit"
                " {overridden} within the current library's register."
                " At this point '{overriding}' might still be overruled by an remaining"
                " reference of {overridden}. This behavior will be changed in future"
                " releases.".format(
                    overriding=overriding_repr, overridden=overridden_unit_repr
                )
            )
        self._units[unit.symbol] = unit

        new_item = _ChainedUnitItem(unit)

        chain_index = self.create_chain_index(unit=unit)
        category_index = chain_index.letter_index

        non_existing_shortcut_should_be_created = chain_index not in self._short_cuts
        if non_existing_shortcut_should_be_created:
            self._short_cuts[chain_index] = new_item

        try:
            category_item = self._categories[category_index]
            category_item.sort_in(new_item)
            self._categories[category_index] = category_item.left_end
        except KeyError:
            self._categories[category_index] = new_item

    def _get_entry_point_item(self, chain_index: _KeyChainIndex) -> _ChainedUnitItem:
        try:
            entry_point_item = self._short_cuts[chain_index]
            return entry_point_item
        except KeyError:
            pass

        try:
            entry_point_item = self._categories[chain_index.letter_index]
            return entry_point_item
        except KeyError:
            warnings.warn(
                "No fitting unit for anything starting with '{}' is registered."
                " Please extend your library.".format(chain_index.letter_index)
            )

    def _quick_iter_detection(
        self, unknown_units: Iterable[UnknownUnit]
    ) -> Generator[Union[AUnit, UnknownUnit], None, None]:
        """
        Tries a direct hit within the major library's register. Either returning AUnit
        on success or the UnknownUnit for futher detection.

        Args:
            unknown_units:
                Units to probe for known units of this library.

        Yield:
            Union[AUnit, UnknownUnit]

        .. doctest::

            >>> # Access to private member for testing
            >>> # noinspection PyProtectedMember
            >>> from justunits import _UnitLibrary
            >>> sample_lib = _UnitLibrary()
            >>> sample_lib.register_unit(create_unit("apple", "apple", "fruit"))

            Is going to be detected by the quick find.

            >>> sample_lib.detect("apple")
            [AUnit(apple 'apple' fruit)]

            Needs to be detected the conversvative way.
            >>> sample_lib.detect("apple⁻¹")
            [AUnit(apple 'apple' fruit; power=-1)]

            Strawberries are still unknown.
            >>> sample_lib.detect("strawberry")
            [UnknownUnit('strawberry')]
        """
        for unit_to_probe in unknown_units:
            if unit_to_probe.UNIT_TYPE != UnknownUnit.UNIT_TYPE:
                yield unit_to_probe
                continue
            searched_symbol = unit_to_probe.text
            unit_consist_of_known_single_unit = searched_symbol in self._units
            if unit_consist_of_known_single_unit:
                found_unit = copy.copy(self._units[searched_symbol])
                if unit_to_probe.switching_power_needed:
                    found_unit.switch_power()
                yield found_unit
            else:
                yield unit_to_probe

    @lru_cache(maxsize=1)
    def unique_letters(self) -> str:
        """

        Returns:

        .. doctest::

            >>> from doctestprinter import doctest_print
            >>> # Access to private member for testing
            >>> # noinspection PyProtectedMember
            >>> from justunits import _unit_library
            >>> all_letters = _unit_library.unique_letters()
            >>> doctest_print(all_letters, max_line_width=70)
            ABCFGHJKLMNPSTVWabcdeghiklmnopqrstuvxyz°´µΩμ

        """
        all_symbols = "".join(self._units)
        unique_symbols = list(sorted(set(all_symbols)))
        all_together = "".join(unique_symbols)
        return all_together

    def _detect_along_chain(self, unknown_unit):
        if unknown_unit.UNIT_TYPE != UnknownUnit.UNIT_TYPE:
            return (unknown_unit,)

        searched_index = self.create_chain_index(unknown_unit)
        detecting_item = self._get_entry_point_item(chain_index=searched_index)
        no_unit_starting_like_this_is_registered = detecting_item is None
        if no_unit_starting_like_this_is_registered:
            return (unknown_unit,)
        probed_units = detecting_item.detect(unknown_unit=unknown_unit)

        one_unknown_remains_break_cycle_its_not_registered = len(probed_units) == 1
        if one_unknown_remains_break_cycle_its_not_registered:
            return probed_units
        return self._detect(*probed_units)

    def _detect(self, *unknown_units):
        if len(unknown_units) == 1:
            if unknown_units[0].UNIT_TYPE != UnknownUnit.UNIT_TYPE:
                return unknown_units

        detected_units = []
        for unit_to_probe in self._quick_iter_detection(unknown_units):
            if unit_to_probe.UNIT_TYPE != UnknownUnit.UNIT_TYPE:
                detected_units.append(unit_to_probe)
                continue

            finished_probed_units = self._detect_along_chain(unit_to_probe)

            detected_units.extend(finished_probed_units)

        return detected_units

    def detect(self, unit_text: str) -> List[Union[AUnit, UnknownUnit]]:
        """

        Args:
            unit_text:

        Returns:
            List[Union[AUnit, UnknownUnit]]

        Examples:

            >>> from doctestprinter import doctest_iter_print
            >>> detected_sample_units = _unit_library.detect("mmmol")
            >>> doctest_iter_print(detected_sample_units, edits_item=repr)
            AUnit(mm 'millimeter' length, 0.001m)
            AUnit(mol 'mole' amount of substance)

            >>> detected_sample_units = _unit_library.detect("mm/s")
            >>> doctest_iter_print(detected_sample_units, edits_item=repr)
            AUnit(mm 'millimeter' length, 0.001m)
            AUnit(s 'second' time; power=-1)

            >>> detected_sample_units = _unit_library.detect("m*s^-1")
            >>> doctest_iter_print(detected_sample_units, edits_item=repr)
            AUnit(m 'meter' length)
            AUnit(s 'second' time; power=-1)

            >>> detected_sample_units = _unit_library.detect("kg/(m*s^2)*m")
            >>> doctest_iter_print(detected_sample_units, edits_item=repr)
            AUnit(kg 'kilogram' mass, 1e+03g)
            AUnit(m 'meter' length; power=-1)
            AUnit(s 'second' time; power=-2)
            AUnit(m 'meter' length)
        """
        prepared_units = _split_text_into_unknown_units(unit_text=unit_text)
        detected_units = self._detect(*prepared_units)
        return detected_units

    def clear(self):
        self._units.clear()
        self._short_cuts.clear()
        self._categories.clear()

    def from_buffer(self, text_buffer):
        self.clear()
        units = _read_raw_unit_table(text_buffer=text_buffer)
        self.register_many(*units)

    def to_unit_map(self) -> Dict[str, Dict[str, AUnit]]:
        unit_map = {}
        for symbol, unit in self._units.items():
            symbol = unit.base_symbol
            if symbol not in unit_map:
                unit_map[symbol] = {}
            unit_map[symbol][unit.prefix_symbol] = unit
        return unit_map


_unit_library = _UnitLibrary()
_unit_library.from_buffer(text_buffer=io.StringIO(_default_raw_unit_table))


def reset_unit_library():
    """
    Resets the unit library to the default definition.
    """
    global _unit_library
    _unit_library.from_buffer(text_buffer=io.StringIO(_default_raw_unit_table))


def set_default_unit_style(unit_style: int):
    """
    Sets the default unit style. The change is limited for the current runtime.

    Args:
        unit_style:
            Combination of UnitPowerStyle, UnitDividingStyle and UnitSeparationStyle.

    Raises:
        ValueError:
            If not within :class:`justunits.UnitStyle`.
    """
    global _defaults
    _defaults.UNIT_STYLE = _get_target_unit_style(unit_style)


_integer_superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
_super_script_integer_powers = {i: _integer_superscripts[i] for i in range(10)}
_superscript_fractional_powers = {
    (1 / 2): "½",
    (1 / 3): "⅓",
    (1 / 4): "¼",
    (1 / 5): "⅕",
    (1 / 6): "⅙",
    (1 / 7): "⅐",
    (1 / 8): "⅛",
    (1 / 9): "⅑",
    (1 / 10): "⅒",
    (2 / 3): "⅔",
    (2 / 5): "⅖",
    (3 / 4): "¾",
    (3 / 5): "⅗",
    (3 / 8): "⅜",
    (4 / 5): "⅘",
    (5 / 6): "⅚",
    (5 / 8): "⅝",
    (7 / 8): "⅞",
}
_superscript_powers = _super_script_integer_powers.copy()
_superscript_powers.update(_superscript_fractional_powers)


def _get_superscript_power(power: Union[int, float]) -> str:
    """

    Args:
        power:

    Returns:

    .. doctest::

        >>> _get_superscript_power(1)
        '¹'
        >>> _get_superscript_power(-1)
        '⁻¹'
        >>> _get_superscript_power(1/2)
        '½'
        >>> _get_superscript_power(3/8)
        '⅜'
        >>> _get_superscript_power(0.1234567)
        Traceback (most recent call last):
        ...
        KeyError: 'Decimal powers are not supported.'
    """
    if power < 0:
        power = abs(power)
        sign = "⁻"
    else:
        sign = ""

    try:
        return sign + _superscript_powers[power]
    except KeyError:
        raise KeyError("Decimal powers are not supported.")


def _get_superscript_power_representation(power: Union[int, float]) -> str:
    if power == 1:
        return ""
    return _get_superscript_power(power)


_default_caret_power_decimal_format = "{:.3g}"


def _get_caret_power(power: Union[int, float]) -> str:
    """

    Args:
        power:

    Returns:

    .. doctest::

        >>> _get_caret_power(1)
        '^1'
        >>> _get_caret_power(-1)
        '^-1'
        >>> _get_caret_power(-2.0)
        '^-2'
        >>> _get_caret_power(1/2)
        '^(1/2)'
        >>> _get_caret_power(3/8)
        '^(3/8)'
    """
    if power < 0:
        power = abs(power)
        sign = "-"
    else:
        sign = ""

    if isinstance(power, int):
        return "^{}{}".format(sign, _default_caret_power_decimal_format.format(power))

    dividend, divisor = power.as_integer_ratio()
    is_still_an_integer = divisor == 1
    if is_still_an_integer:
        return "^{}{}".format(sign, _default_caret_power_decimal_format.format(power))
    return sign + "^({}{}/{})".format(sign, dividend, divisor)


def _get_caret_power_representation(power: Union[int, float]) -> str:
    if power == 1:
        return ""
    return _get_caret_power(power)


def _make_single_unit(unit: AUnit, unit_style: UnitStyle) -> str:
    """

    Args:
        unit:
        unit_style:

    Returns:

    >>> _make_single_unit(SiUnits.millimeter, UnitStyle.FINE_POWERED_SUPERSCRIPT)
    'mm'
    >>> _make_single_unit(SiUnits.millimeter.with_power(-1), UnitStyle.FINE_POWERED_SUPERSCRIPT)
    'mm⁻¹'
    >>> _make_single_unit(SiUnits.millimeter.with_power(-1), UnitStyle.TOTAL_POWER_ASCII)
    'mm^-1'
    >>> _make_single_unit(SiUnits.millimeter, UnitStyle.TOTAL_POWER_ASCII)
    'mm'
    >>> _make_single_unit(SiUnits.millimeter.with_power(-2), UnitStyle.FINE_POWERED_SUPERSCRIPT)
    'mm⁻²'
    >>> _make_single_unit(SiUnits.millimeter.with_power(-2), UnitStyle.FINE_SLASHED_SUPERSCRIPT)
    'mm²'
    >>> _make_single_unit(SiUnits.millimeter.with_power(-2), UnitStyle.SIMPLE_ASCII)
    'mm^2'
    >>> _make_single_unit(SiUnits.millimeter.with_power(-2), UnitStyle.TOTAL_POWER_ASCII)
    'mm^-2'
    """
    number_is_flat = float(unit.power).as_integer_ratio()[1] == 1
    if not number_is_flat:
        raise NotImplementedError("not implemented yet")

    fine_powered_style = UnitPowerStyle.SUPERSCRIPT | UnitDividingStyle.BY_POWER
    if (unit_style & fine_powered_style) == fine_powered_style:
        power_repr = _get_superscript_power_representation(unit.power)
        return "{}{}".format(unit.symbol, power_repr)

    fine_slashed_style = UnitPowerStyle.SUPERSCRIPT | UnitDividingStyle.SLASHED
    if (unit_style & fine_slashed_style) == fine_slashed_style:
        power_repr = _get_superscript_power_representation(abs(unit.power))
        return "{}{}".format(unit.symbol, power_repr)

    rough_powered_style = UnitPowerStyle.CARET | UnitDividingStyle.BY_POWER
    if (unit_style & rough_powered_style) == rough_powered_style:
        power_repr = _get_caret_power_representation(unit.power)
        return "{}{}".format(unit.symbol, power_repr)

    rough_slashed_style = UnitPowerStyle.CARET | UnitDividingStyle.SLASHED
    if (unit_style & rough_slashed_style) == rough_slashed_style:
        power_repr = _get_caret_power_representation(abs(unit.power))
        return "{}{}".format(unit.symbol, power_repr)


class _UnitReprGroup:
    def __init__(self):
        self.negative_power = False
        self.unit_representations = []

    def __repr__(self):
        return str(self.unit_representations)

    def append(self, unit_repr):
        self.unit_representations.append(unit_repr)

    def __bool__(self):
        return len(self.unit_representations) > 0


def _group_for_enclosing(
    unit_repr_pairs: List[Tuple[AUnit, str]]
) -> List[_UnitReprGroup]:
    """

    Args:
        unit_repr_pairs:

    Returns:

    .. doctest::

        >>> newton_meter_pairs = [
        ...     (SiUnits.kilogram, "kg"),
        ...     (SiUnits.meter.with_power(-1), "m"),
        ...     (SiUnits.second.with_power(-2), "s²"),
        ...     (SiUnits.meter, "m")
        ... ]
        >>> _group_for_enclosing(newton_meter_pairs)
        [['kg'], ['m', 's²'], ['m']]
    """

    unit_groups = []
    last_power_was_negative = False
    subgroup = _UnitReprGroup()
    unit_groups.append(subgroup)
    for unit, unit_repr in unit_repr_pairs:
        this_power_is_negative = unit.power < 0
        if not subgroup:
            subgroup.negative_power = this_power_is_negative
            subgroup.append(unit_repr)
            last_power_was_negative = this_power_is_negative
            continue

        if this_power_is_negative and last_power_was_negative:
            subgroup.append(unit_repr)
        else:
            subgroup = _UnitReprGroup()
            unit_groups.append(subgroup)
            subgroup.negative_power = this_power_is_negative
            subgroup.append(unit_repr)
        last_power_was_negative = this_power_is_negative
    return unit_groups


def _construct_unit(units: List[AUnit], unit_style: UnitStyle) -> str:
    """

    Args:
        units:
        unit_style:

    Returns:

    .. doctest::

        >>> newton_meter = [
        ...     SiUnits.kilogram,
        ...     SiUnits.meter.with_power(-1),
        ...     SiUnits.second.with_power(-2),
        ...     SiUnits.meter
        ... ]
        >>> _construct_unit(newton_meter, unit_style=UnitStyle.FINE_SLASHED_SUPERSCRIPT)
        'kg/(m⋅s²)⋅m'
        >>> _construct_unit(newton_meter, unit_style=UnitStyle.FINE_POWERED_SUPERSCRIPT)
        'kg⋅m⁻¹⋅s⁻²⋅m'

    """

    separator = None
    if unit_style & UnitSeparationStyle.DOT:
        separator = _UNIT_SEPARATOR_DOT_OPERATOR
    elif unit_style & UnitSeparationStyle.ASTERISK:
        separator = _UNIT_SEPARATOR_ASTERISK

    assert separator in [_UNIT_SEPARATOR_DOT_OPERATOR, _UNIT_SEPARATOR_ASTERISK]

    divide_by_slash = unit_style & UnitDividingStyle.SLASHED
    represent_by_negative_powers = unit_style & UnitDividingStyle.BY_POWER
    if divide_by_slash:
        unit_repr_pairs = []
        for unit in units:
            unit_repr = _make_single_unit(unit=unit, unit_style=unit_style)
            unit_repr_pairs.append((unit, unit_repr))
        unit_groups = _group_for_enclosing(unit_repr_pairs)

        final_unit_representation = ""
        for unit_group in unit_groups:
            if unit_group.negative_power:
                assert (
                    len(unit_group.unit_representations) > 0
                ), "A unit group without units should not exist."
                if len(unit_group.unit_representations) > 1:
                    unit_repr = separator.join(unit_group.unit_representations)
                    final_unit_representation += "/({})".format(unit_repr)
                else:
                    unit_repr = str(unit_group.unit_representations[0])
                    final_unit_representation += "/{}".format(unit_repr)
            else:
                if len(unit_group.unit_representations) > 1:
                    unit_repr = separator.join(unit_group.unit_representations)
                else:
                    unit_repr = unit_group.unit_representations[0]
                final_unit_representation += "{}{}".format(separator, unit_repr)

        return final_unit_representation[1:]

    elif represent_by_negative_powers:
        single_unit_representations = [
            _make_single_unit(unit=unit, unit_style=unit_style) for unit in units
        ]
        final_unit_representation = separator.join(single_unit_representations)
        return final_unit_representation


def from_string(unit_text: str) -> "DerivedUnit":
    """

    Args:
        unit_text:

    Returns:

    Examples:

        >>> import justunits
        >>> torque = justunits.from_string("Nm")
        >>> torque
        (AUnit(N 'newton' force, weight), AUnit(m 'meter' length))

        >>> str(torque)
        'N⋅m'

        >>> millisecond = justunits.from_string("ms")
        >>> millisecond
        (AUnit(ms 'millisecond' time, 0.001s),)

        >>> millisecond.with_prefix(SiPrefixes.nano)
        (AUnit(ns 'nanosecond' time, 1e-09s),)

        >>> apple = justunits.from_string("apple")
        >>> apple
        (UnknownUnit('apple'),)

        >>> justunits.register_unit(create_unit("apple", "apple", "fruit"))
        >>> apple = justunits.from_string("apple")
        >>> apple
        (AUnit(apple 'apple' fruit),)
    """
    base_units = _unit_library.detect(unit_text)
    return DerivedUnit(*base_units)


def register_unit(unit: AUnit):
    global _unit_library
    _unit_library.register_unit(unit)


def to_string(unit: Iterable[AUnit], unit_style: Optional[UnitStyle] = None) -> str:
    """
    Creates a string represenation of units.

    Args:
        unit(Iterable[AUnit]):
            A sequence of units representing a single unit or a composition of units.

        unit_style(UnitStyle):
            The targeted formatting style to be applied.

    Returns:
        str

    Examples:
        >>> from justunits import UnitStyle
        >>> import justunits
        >>> heat_capacity = justunits.from_string("kg/(s^2*K)*m^2")
        >>> justunits.to_string(heat_capacity, UnitStyle.FINE_SLASHED_SUPERSCRIPT)
        'kg/(s²⋅K)⋅m²'
        >>> justunits.to_string(heat_capacity, UnitStyle.FINE_POWERED_SUPERSCRIPT)
        'kg⋅s⁻²⋅K⁻¹⋅m²'
        >>> justunits.to_string(heat_capacity, UnitStyle.TOTAL_POWER_ASCII)
        'kg*s^-2*K^-1*m^2'
        >>> justunits.to_string(heat_capacity, UnitStyle.SIMPLE_ASCII)
        'kg/(s^2*K)*m^2'

    """
    if unit_style is None:
        unit_style = _defaults.UNIT_STYLE
    return _construct_unit(unit, unit_style=unit_style)


class DerivedUnit(Sequence):
    def __init__(self, *sub_units):
        """

        Args:
            *sub_units:
            target_style:

        Examples:

            **DerivedUnit** are comparable and hashable. The order of units is neglected
            for the comparison resulting into `a⋅b == b⋅a`.

            >>> import justunits
            >>> energy = justunits.from_string("N*m")
            >>> ygrene = justunits.from_string("m*N")
            >>> energy == ygrene
            True

            :class:`DerivedUnit` is hashable like :class:`AUnit` to support usage as key
            within within mappings. In the current implementation the order of internal
            units is neglected. Meaning  *a⋅b* and *b⋅a* are considered being the same.

            >>> hash(energy) == hash(ygrene)
            True

            >>> map = {energy: "energy"}
            >>> map[ygrene]
            'energy'

            >>> pressure = justunits.from_string("N/m")
            >>> pressure != energy
            True

            >>> hash(pressure) == hash(energy)
            False


        .. doctest::
           :hide:

           >>> import justunits
           >>> stress = justunits.from_string("N/mm")
           >>> len(stress)
           2
           >>> stress[0]
           AUnit(N 'newton' force, weight)
        """
        self._units = sub_units
        self._hash_values = self.make_hash_values(self._units)

    @property
    def identity(self):
        return self._hash_values

    @staticmethod
    def make_hash_values(units: Iterable[AUnit]) -> List[Union[str, int, float]]:
        """

        Returns:

        .. doctest::

            >>> from justunits import DerivedUnit, SiUnits
            >>> DerivedUnit.make_hash_values((SiUnits.newton, SiUnits.meter))
            ('N', 1.0, 'm', 1.0)
        """
        symbol_power_pairs = [(unit.symbol, unit.power) for unit in units]
        sorted_pairs = sorted(symbol_power_pairs, key=lambda x: x[0])
        hash_values = tuple(chain.from_iterable(sorted_pairs))
        return hash_values

    def __hash__(self):
        return hash(self._hash_values)

    def __eq__(self, other: "DerivedUnit"):
        assert isinstance(other, DerivedUnit)
        return self.identity == other.identity

    def __ne__(self, other):
        assert isinstance(other, DerivedUnit)
        return self.identity != other.identity

    def with_prefix(self, prefix: SiPrefixes) -> "DerivedUnit":
        first_unit_with_prefix = self._units[0].with_prefix(prefix)
        return self.__class__(first_unit_with_prefix, *self._units[1:])

    def __iter__(self) -> Iterator[AUnit]:
        return iter(self._units)

    def __len__(self):
        return len(self._units)

    def __getitem__(self, index: int) -> AUnit:
        return self._units[index]

    def __repr__(self):
        return str(self._units)

    def __str__(self):
        return to_string(self)

    def __bool__(self):
        return len(self._units) > 0


class AnyUnit(DerivedUnit):
    def __init__(self, *sub_units):
        warnings.warn(
            "AnyUnit will be renamed to DerivedUnits within the next release."
        )
        super.__init__(*sub_units)


_supported_separator_patterns = {
    AttributeUnitSeparators.WHITESPACE_BOXED: r"\s?\[",
    AttributeUnitSeparators.UNDERLINE_BOXED: r"_\[",
    AttributeUnitSeparators.WHITESPACE_IN: r"\sin\s",
    AttributeUnitSeparators.UNDERLINED_IN: r"_in_",
    AttributeUnitSeparators.HASH_SIGN: r"#",
    AttributeUnitSeparators.SINGLE_UNDERLINE: r"_",
    AttributeUnitSeparators.SINGLE_WHITESPACE: r"\s",
}


_supported_unit_templates = {
    AttributeUnitSeparators.WHITESPACE_BOXED: Template("${attribute} [${unit}]"),
    AttributeUnitSeparators.UNDERLINE_BOXED: Template("${attribute}_[${unit}]"),
    AttributeUnitSeparators.WHITESPACE_IN: Template("${attribute} in ${unit}"),
    AttributeUnitSeparators.UNDERLINED_IN: Template("${attribute}_in_${unit}"),
    AttributeUnitSeparators.HASH_SIGN: Template("${attribute}#${unit}"),
    AttributeUnitSeparators.SINGLE_UNDERLINE: Template("${attribute}_${unit}"),
    AttributeUnitSeparators.SINGLE_WHITESPACE: Template("${attribute} ${unit}"),
}


def _get_lowest_flag(int_flag_class: IntFlag, choice) -> int:
    choices = int_flag_class(choice)
    number = choices.value
    lowest_bit = number & -number
    lowest_separator = int_flag_class(lowest_bit)
    return lowest_separator


def _get_supported_unit_template(selected_separator: int) -> Template:
    """
    Returns the template for the selected separator. If multiple separators
    are selected, then the seperator of the lowest bit is returned.

    Returns:
        AttributeUnitSeparators

    Examples:
        >>> selected_separators = (
        ...     AttributeUnitSeparators.WHITESPACE_IN
        ...     | AttributeUnitSeparators.UNDERLINED_IN
        ... )
        >>> template = _get_supported_unit_template(selected_separators)
        >>> template.substitute(attribute="name", unit="unit")
        'name in unit'
    """
    try:
        return _supported_unit_templates[selected_separator]
    except KeyError:
        pass

    lowest_choice = _get_lowest_flag(AttributeUnitSeparators, selected_separator)
    return _get_supported_unit_template(lowest_choice)


def set_default_attribute_unit_separator(separator: int):
    """
    Sets the default separator in between attribute/value and unit. The change is
    limited for the current runtime.

    Args:
        separator:
            A separator from AttributeUnitSeparators as default.

    Raises:
        ValueError:
            If *separator* is not within AttributeUnitSeparators.

    Examples:
        >>> import justunits
        >>> from justunits import AttributeUnitSeparators
        >>> justunits.join_unit("length", "mm")
        'length [mm]'
        >>> set_default_attribute_unit_separator(AttributeUnitSeparators.WHITESPACE_IN)
        >>> justunits.join_unit("length", "mm")
        'length in mm'

    .. doctest::
       :hide:

        >>> import justunits
        >>> justunits.set_default_attribute_unit_separator(
        ...  DEFAULT_ATTRIBUTE_UNIT_SEPARATOR
        ... )
        >>> justunits.set_default_attribute_unit_separator(123)
        Traceback (most recent call last):
        ...
        ValueError: Please provide a valid option of AttributeUnitSeparators
    """
    requested_separator = AttributeUnitSeparators(separator)
    if requested_separator not in AttributeUnitSeparators:
        raise ValueError("Please provide a valid option of AttributeUnitSeparators")

    global _defaults
    _defaults.ATTRIBUTE_UNIT_SEPARATOR = requested_separator


@lru_cache(10)
def _get_separators(allowed_separators: int) -> List[str]:
    """

    Args:
        allowed_separators:
            A choise of SupportedSeperators.

    Returns:
        List[str]
        List[str]

    Examples:
        >>> # Access to private member for testing
        >>> # noinspection PyProtectedMember
        >>> from justunits import _get_separators, AttributeUnitSeparators
        >>> sample_separators = (
        ...     AttributeUnitSeparators.UNDERLINED_IN | AttributeUnitSeparators.WHITESPACE_IN
        ... )
        >>> _get_separators(sample_separators)
        ['\\\\sin\\\\s', '_in_']

    """
    requested_separators = []
    for separator in AttributeUnitSeparators:
        if separator & allowed_separators:
            chosen_separator = _supported_separator_patterns[separator]
            requested_separators.append(chosen_separator)
    return requested_separators


def _make_separation_pattern(separator_patterns: List[str]) -> str:
    """

    Args:
        separator_patterns:

    Returns:

    Examples:
        >>> # Access to private member for testing
        >>> # noinspection PyProtectedMember
        >>> from justunits import (
        ...     _get_separators, AttributeUnitSeparators, _make_separation_pattern
        ... )
        >>> sample_separators = (
        ...     AttributeUnitSeparators.UNDERLINED_IN | AttributeUnitSeparators.WHITESPACE_IN
        ... )
        >>> sample_patterns = _get_separators(sample_separators)
        >>> _make_separation_pattern(sample_patterns)
        '(?P<separator>(\\\\sin\\\\s|_in_))'

    """
    joined_patterns = "|".join(separator_patterns)
    return "(?P<separator>({}))".format(joined_patterns)


_BASE_SPLITTING_PATTERN = r"^(?P<attribute>.*?){}(?P<unit>.*?)]*$"


@lru_cache(10)
def _get_splitting_pattern(allowed_separators: AttributeUnitSeparators) -> Pattern:
    """

    Args:
        allowed_separators:

    Returns:

    .. doctest::

        >>> # Access to private member for testing
        >>> # noinspection PyProtectedMember
        >>> from justunits import _get_splitting_pattern, AttributeUnitSeparators
        >>> _get_splitting_pattern(
        ...     AttributeUnitSeparators.SINGLE_WHITESPACE | AttributeUnitSeparators.WHITESPACE_BOXED
        ... )
        re.compile('^(?P<attribute>.*?)(?P<separator>(\\\\s?\\\\[|\\\\s))(?P<unit>.*?)]*$')
    """
    separator_patterns = _get_separators(allowed_separators=allowed_separators)
    separation_pattern = _make_separation_pattern(separator_patterns=separator_patterns)
    full_splitting_pattern = _BASE_SPLITTING_PATTERN.format(separation_pattern)
    return re.compile(full_splitting_pattern)


def split_attribute_unit(
    text: str, allowed_separators: Optional[AttributeUnitSeparators] = None
) -> Tuple[str, str]:
    """

    Args:
        text:
        allowed_separators:

    Returns:

    Examples:

        >>> from justunits import AttributeUnitSeparators
        >>> import justunits
        >>> justunits.split_attribute_unit("length in mm")
        ('length', 'mm')
        >>> justunits.split_attribute_unit("length [mm]")
        ('length', 'mm')
        >>> justunits.split_attribute_unit("length in mm")
        ('length', 'mm')
        >>> justunits.split_attribute_unit("length#mm")
        ('length', 'mm')
        >>> justunits.split_attribute_unit("heat capacity#kg/(s^−2*K^-1)*m^2")
        ('heat capacity', 'kg/(s^−2*K^-1)*m^2')
    """
    if allowed_separators is None:
        allowed_separators = _defaults.ALLOWED_SEPARATORS

    splitting_pattern = _get_splitting_pattern(allowed_separators=allowed_separators)
    matched_text = splitting_pattern.match(text)
    if matched_text is None:
        return text, ""

    parts = matched_text.groupdict()
    return parts["attribute"], parts["unit"]


_splits_number_with_unit = re.compile(
    r"(?P<number>(([0-9+-,.][eE][0-9+-])+|([0-9+-,.]))+)[\s]*(?P<unit>[0-9\w/\^]*)$"
)


def split_number_and_unit(text: str) -> Tuple[str, str]:
    """
    Explicitly splits a numeric text followed by an unit.

    Args:
        text(str):
            The text potentially containing a nunber with an unit specification.

    Returns:
        Tuple[str, str]

    Examples:
        >>> import justunits
        >>> justunits.split_number_and_unit("1 N")
        ('1', 'N')
        >>> justunits.split_number_and_unit("1.2 mm/s")
        ('1.2', 'mm/s')
        >>> justunits.split_number_and_unit("1.2 1")
        ('1.2', '1')
        >>> justunits.split_number_and_unit("1.23e+01 apples")
        ('1.23e+01', 'apples')
        >>> justunits.split_number_and_unit("1.2E+09 1")
        ('1.2E+09', '1')
        >>> justunits.split_number_and_unit("not_a_number apples")
        ('not_a_number apples', '')
        >>> justunits.split_number_and_unit("Just a text, 123 not/a/number.")
        ('Just a text, 123 not/a/number.', '')

    .. doctest::
       :hide:

        >>> justunits.split_number_and_unit("Enter")
        ('Enter', '')
        >>> justunits.split_number_and_unit("1.2E+09")
        ('1.2E+09', '')
        >>> justunits.split_number_and_unit("-1.2E+09")
        ('-1.2E+09', '')
        >>> justunits.split_number_and_unit("-1.2E+09")
        ('-1.2E+09', '')
        >>> justunits.split_number_and_unit("-next")
        ('-next', '')
    """
    matched_number = _splits_number_with_unit.match(text)
    if matched_number is None:
        return text, ""
    parts = matched_number.groupdict()
    return parts["number"], parts["unit"]


def split_unit_text(
    text, allowed_separators: Optional[AttributeUnitSeparators] = None
) -> Tuple[str, str]:
    """
    Splits an attribute/value with a trailing unit text.

    Args:
        text:
            Text containing an attribute/value-unit pair.

        allowed_separators:
            The separators which should be taken into account for splitting.

    Returns:
        Tuple[Union[str, float], str]

    Examples:
        >>> import justunits
        >>> justunits.split_unit_text("length in mm")
        ('length', 'mm')
        >>> justunits.split_unit_text("1.23 kN")
        ('1.23', 'kN')
    """
    number, unit = split_number_and_unit(text=text)
    if unit:
        return number, unit
    return split_attribute_unit(text=text, allowed_separators=allowed_separators)


def split_unit(
    text: str,
    allowed_separators: Optional[AttributeUnitSeparators] = None,
    converter: Optional[Callable[[str], Any]] = None,
) -> Tuple[str, Union[AUnit, UnknownUnit]]:
    """
    Splits an attribute/value with a trailing unit.

    Args:
        text:
            Text containing an attribute/value-unit pair.

        allowed_separators:
            The separators which should be taken into account for splitting.

        converter:
            A callable converting a string into the desired object. A failed
            conversion must raise a ValueError. Default is str.

    Returns:
        Tuple[str, Union[AUnit, UnknownUnit]]

    Examples:
        >>> import justunits
        >>> justunits.split_unit("1 apple", converter=int)
        (1, (AUnit(apple 'apple' fruit),))
    """
    if converter is None:
        converter = str

    number_or_something, unit_text = split_unit_text(
        text=text, allowed_separators=allowed_separators
    )
    detected_unit = from_string(unit_text=unit_text)

    target_value = converter(number_or_something)
    return target_value, detected_unit


def _get_target_unit_style(target_format: int) -> int:
    if target_format is None:
        return _defaults.UNIT_STYLE

    power_style = UnitPowerStyle.get_first_hit(
        target_format, default=_defaults.POWER_STYLE
    )
    dividing_style = UnitDividingStyle.get_first_hit(
        target_format, default=_defaults.DIVIDING_STYLE
    )
    separation_style = UnitSeparationStyle.get_first_hit(
        target_format, default=_defaults.SEPARATION_STYLE
    )

    return power_style | dividing_style | separation_style


def _get_target_separator(target_format: int) -> int:
    if target_format is None:
        return _defaults.ATTRIBUTE_UNIT_SEPARATOR
    return AttributeUnitSeparators.get_first_hit(
        target_format, default=_defaults.ATTRIBUTE_UNIT_SEPARATOR
    )


def reformat_unit(
    text: str,
    target_format: Optional[IntFlag] = None,
    converter: Optional[Callable[[str], Any]] = None,
) -> str:
    """
    Reformats a attribute/value-unit pair to a targeted format. 'None' or missing
    style definitions are replaced by _defaults.

    Args:
        text:
            Text containing an attribute/value-unit pair.

        target_format:
            The format the attribute/value-unit pair gets. 'None' or not defined
            styles are set to _defaults.

        converter:
            A callable converting a string into the desired object. A failed
            conversion must raise a ValueError. Default is str.

    Returns:
        str

    Examples:

        >>> import justunits
        >>> from justunits import reformat_unit, AttributeUnitSeparators, UnitStyle
        >>> reformat_unit("1 apple")
        '1 [apple]'
        >>> hashed = AttributeUnitSeparators.HASH_SIGN
        >>> reformat_unit("1 apple", hashed)
        '1#apple'
        >>> fine_slashed_in_style = (
        ...     AttributeUnitSeparators.WHITESPACE_IN | UnitStyle.FINE_SLASHED_SUPERSCRIPT
        ... )
        >>> reformat_unit("energy#kg/(m*s^2)")
        'energy [kg/(m⋅s²)]'

        By default single whitespace or underline separated units are not taken into
        account, allowing the distingtion between any attribute and trailing unit.

        >>> reformat_unit("without unit")
        'without unit'

        Using a more distinguishable seperator enables the reformatting of *'lazy'*
        written unit compositions like newton meter being a unit for torque. This
        is intential as being a method to make clean representations of units.

        >>> reformat_unit("torque in Nm")
        'torque [N⋅m]'

        .. note::

            The detection of *'lazy'* written units like 'Nm' is being tested
            as the default behaviour of just units within the alpha state.
            You may help by feedbacks onto the github project page
            https://github.com/david.scheliga/justunits/issues in which cases
            this leads to problems.

            Be aware that this tries for breaking unknown units into known parts.
            Leading to this such a behavior.

            >>> reformat_unit("with a unit in unit*pattern")
            'with a unit [u⋅nit⋅pattern]'

            >>> justunits.from_string("unit")
            (AUnit(u 'unified atomic mass unit' ), UnknownUnit('nit'))

            >>> justunits.register_unit(justunits.create_unit("unit", "dummy", "n.a."))
            >>> reformat_unit("with a unit in unit*pattern")
            'with a unit [unit⋅pattern]'

    """
    attribute, unit = split_unit(text=text, converter=converter)
    return join_unit(attribute=attribute, unit=unit, target_format=target_format)


def join_unit(
    attribute: Union[int, float, str],
    unit: Union[str, DerivedUnit, AUnit, UnknownUnit],
    target_format: Optional[int] = None,
) -> str:
    """
    Joins attribute and unit using one of six separators.

    Args:
        attribute:
            The attribute's name which the unit is attached to.

        unit:
            The unit which is being attached.

        target_format:

    Returns:
        str

    Examples:

        >>> import justunits
        >>> from justunits import UnitStyle, AttributeUnitSeparators
        >>> join_unit(1.23, "apples")
        '1.23 [apples]'

        >>> join_unit(1.23, "")
        '1.23'

        >>> join_unit(1.23, None)
        '1.23'

        >>> join_unit("max. pressure", "MPa", AttributeUnitSeparators.WHITESPACE_IN)
        'max. pressure in MPa'

        >>> join_unit("torque", "Nm", AttributeUnitSeparators.UNDERLINED_IN)
        'torque_in_Nm'

        >>> join_unit("distance", "mm", AttributeUnitSeparators.WHITESPACE_BOXED)
        'distance [mm]'

        >>> join_unit("distance", "mm", AttributeUnitSeparators.HASH_SIGN)
        'distance#mm'

        >>> join_unit(1.23, "apples", AttributeUnitSeparators.SINGLE_WHITESPACE)
        '1.23 apples'

        >>> join_unit("width", "mm", AttributeUnitSeparators.SINGLE_UNDERLINE)
        'width_mm'

        >>> stress = justunits.from_string("N/mm")
        >>> stress
        (AUnit(N 'newton' force, weight), AUnit(mm 'millimeter' length, 0.001m; power=-1))
        >>> join_unit(1.23, stress, AttributeUnitSeparators.WHITESPACE_IN)
        '1.23 in N/mm'
    """
    no_unit_was_provided_than_return_the_attribute = unit is None or not unit
    if no_unit_was_provided_than_return_the_attribute:
        return str(attribute)

    requested_unit_style = _get_target_unit_style(target_format=target_format)
    target_separators = _get_target_separator(target_format=target_format)

    final_attribute = str(attribute)
    if isinstance(unit, (DerivedUnit, AUnit, UnknownUnit)):
        final_unit = to_string(unit=unit, unit_style=requested_unit_style)
    else:
        final_unit = str(unit)

    attribute_unit_template = _get_supported_unit_template(target_separators)
    return attribute_unit_template.substitute(
        attribute=final_attribute, unit=final_unit
    )
