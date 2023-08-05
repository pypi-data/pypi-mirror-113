import justunits
from justunits import _default_raw_unit_table, _read_raw_unit_table, _unit_library



def test_default_unit_table():
    """

    >>> from doctestprinter import doctest_print, doctest_iter_print
    >>> units = test_default_unit_table()
    >>> doctest_print([str(unit) for unit in units], max_line_width=70)
    ['s', 'ms', 'm', 'mm', 'km', 'g', 'μg', 'mg', 'kg', 'A', 'GA', 'MA', 'mA',
    'kA', 'K', 'mol', 'cd', 'rad', 'sr', 'min', 'h', 'd', '°', '´', '´´', 'L',
    'hL', 'daL', 'dL', 't', 'Mt', 'kt', 'Np', 'B', 'dB', 'eV', 'u', 'au', 'Hz',
    'THz', 'GHz', 'MHz', 'kHz', 'N', 'GN', 'MN', 'kN', 'mN', 'μN', 'Pa', 'GPa',
    'MPa', 'kPa', 'hPa', 'daPa', 'dPa', 'cPa', 'mPa', 'μPa', 'J', 'GJ', 'MJ',
    'kJ', 'mJ', 'µJ', 'nJ', 'W', 'TW', 'GW', 'MW', 'kW', 'mW', 'µW', 'C', 'V',
    'TV', 'GV', 'MV', 'kV', 'mV', 'μV', 'F', 'Ω', 'GΩ', 'MΩ', 'kΩ', 'mΩ', 'μΩ',
    'S', 'GS', 'MS', 'kS', 'mS', 'µS', 'Wb', 'T', 'GT', 'MT', 'kT', 'mT', 'µT',
    'H', 'GH', 'MH', 'kH', 'mH', 'µH', '°C', 'lm', 'lx', 'Bq', 'Gy', 'Sv',
    'mSv', 'µSv', 'kat']


    >>> doctest_iter_print(units, edits_item=repr)
    AUnit(s 'second' time)
    AUnit(ms 'millisecond' time, 0.001s)
    AUnit(m 'meter' length)
    AUnit(mm 'millimeter' length, 0.001m)
    AUnit(km 'kilometer' length, 1e+03m)
    AUnit(g 'gram' mass)
    AUnit(μg 'microgram' mass, 1e-06g)
    AUnit(mg 'milligram' mass, 0.001g)
    AUnit(kg 'kilogram' mass, 1e+03g)
    AUnit(A 'ampere' electric current)
    AUnit(GA 'gigaampere' electric current, 1e+09A)
    AUnit(MA 'megaampere' electric current, 1e+06A)
    AUnit(mA 'milliampere' electric current, 0.001A)
    AUnit(kA 'kiloampere' electric current, 1e+03A)
    AUnit(K 'kelvin' thermodynamic temperature)
    AUnit(mol 'mole' amount of substance)
    AUnit(cd 'candela' luminous intensity)
    AUnit(rad 'radian' plane angle)
    AUnit(sr 'steradian' solid angle)
    AUnit(min 'minute' time)
    AUnit(h 'hour' time)
    AUnit(d 'day' time)
    AUnit(° 'degree' angle)
    AUnit(´ 'minute' angle)
    AUnit(´´ 'second' angle)
    AUnit(L 'liter' volume)
    AUnit(hL 'hectoliter' volume, 1e+02L)
    AUnit(daL 'dekaliter' volume, 1e+01L)
    AUnit(dL 'deciliter' volume, 0.1L)
    AUnit(t 'tonne' mass)
    AUnit(Mt 'megatonne' mass, 1e+06t)
    AUnit(kt 'kilotonne' mass, 1e+03t)
    AUnit(Np 'neper' )
    AUnit(B 'bel' )
    AUnit(dB 'decibel' , 0.1B)
    AUnit(eV 'electronvolt' )
    AUnit(u 'unified atomic mass unit' )
    AUnit(au 'astonomical unit' )
    AUnit(Hz 'hertz' frequency)
    AUnit(THz 'terahertz' frequency, 1e+12Hz)
    AUnit(GHz 'gigahertz' frequency, 1e+09Hz)
    AUnit(MHz 'megahertz' frequency, 1e+06Hz)
    AUnit(kHz 'kilohertz' frequency, 1e+03Hz)
    AUnit(N 'newton' force, weight)
    AUnit(GN 'giganewton' force, weight, 1e+09N)
    AUnit(MN 'meganewton' force, weight, 1e+06N)
    AUnit(kN 'kilonewton' force, weight, 1e+03N)
    AUnit(mN 'millinewton' force, weight, 0.001N)
    AUnit(μN 'micronewton' force, weight, 1e-06N)
    AUnit(Pa 'pascal' pressure, stress)
    AUnit(GPa 'gigapascal' pressure, stress, 1e+09Pa)
    AUnit(MPa 'megapascal' pressure, stress, 1e+06Pa)
    AUnit(kPa 'kilopascal' pressure, stress, 1e+03Pa)
    AUnit(hPa 'hectopascal' pressure, stress, 1e+02Pa)
    AUnit(daPa 'dekapascal' pressure, stress, 1e+01Pa)
    AUnit(dPa 'decipascal' pressure, stress, 0.1Pa)
    AUnit(cPa 'centipascal' pressure, stress, 0.01Pa)
    AUnit(mPa 'millipascal' pressure, stress, 0.001Pa)
    AUnit(μPa 'micropascal' pressure, stress, 1e-06Pa)
    AUnit(J 'joule' energy, work, heat)
    AUnit(GJ 'gigajoule' energy, work, heat, 1e+09J)
    AUnit(MJ 'megajoule' energy, work, heat, 1e+06J)
    AUnit(kJ 'kilojoule' energy, work, heat, 1e+03J)
    AUnit(mJ 'millijoule' energy, work, heat, 0.001J)
    AUnit(µJ 'microjoule' energy, work, heat, 1e-06J)
    AUnit(nJ 'nanojoule' energy, work, heat, 1e-09J)
    AUnit(W 'watt' power, radiant flux)
    AUnit(TW 'terawatt' power, radiant flux, 1e+12W)
    AUnit(GW 'gigawatt' power, radiant flux, 1e+09W)
    AUnit(MW 'megawatt' power, radiant flux, 1e+06W)
    AUnit(kW 'kilowatt' power, radiant flux, 1e+03W)
    AUnit(mW 'milliwatt' power, radiant flux, 0.001W)
    AUnit(µW 'microwatt' power, radiant flux, 1e-06W)
    AUnit(C 'coulomb' electric charge)
    AUnit(V 'volt' electrical potential difference (voltage emf))
    AUnit(TV 'teravolt' electrical potential difference (voltage emf), 1e+12V)
    AUnit(GV 'gigavolt' electrical potential difference (voltage emf), 1e+09V)
    AUnit(MV 'megavolt' electrical potential difference (voltage emf), 1e+06V)
    AUnit(kV 'kilovolt' electrical potential difference (voltage emf), 1e+03V)
    AUnit(mV 'millivolt' electrical potential difference (voltage emf), 0.001V)
    AUnit(μV 'microvolt' electrical potential difference (voltage emf), 1e-06V)
    AUnit(F 'farad' capacitance)
    AUnit(Ω 'ohm' resistance, impedance, reactance)
    AUnit(GΩ 'gigaohm' resistance, impedance, reactance, 1e+09Ω)
    AUnit(MΩ 'megaohm' resistance, impedance, reactance, 1e+06Ω)
    AUnit(kΩ 'kiloohm' resistance, impedance, reactance, 1e+03Ω)
    AUnit(mΩ 'milliohm' resistance, impedance, reactance, 0.001Ω)
    AUnit(μΩ 'microohm' resistance, impedance, reactance, 1e-06Ω)
    AUnit(S 'siemens ' electrical conductance)
    AUnit(GS 'gigasiemens ' electrical conductance, 1e+09S)
    AUnit(MS 'megasiemens ' electrical conductance, 1e+06S)
    AUnit(kS 'kilosiemens ' electrical conductance, 1e+03S)
    AUnit(mS 'millisiemens ' electrical conductance, 0.001S)
    AUnit(µS 'microsiemens ' electrical conductance, 1e-06S)
    AUnit(Wb 'weber' magnetic flux)
    AUnit(T 'tesla' magnetic flux density)
    AUnit(GT 'gigatesla' magnetic flux density, 1e+09T)
    AUnit(MT 'megatesla' magnetic flux density, 1e+06T)
    AUnit(kT 'kilotesla' magnetic flux density, 1e+03T)
    AUnit(mT 'millitesla' magnetic flux density, 0.001T)
    AUnit(µT 'microtesla' magnetic flux density, 1e-06T)
    AUnit(H 'henry' inductance)
    AUnit(GH 'gigahenry' inductance, 1e+09H)
    AUnit(MH 'megahenry' inductance, 1e+06H)
    AUnit(kH 'kilohenry' inductance, 1e+03H)
    AUnit(mH 'millihenry' inductance, 0.001H)
    AUnit(µH 'microhenry' inductance, 1e-06H)
    AUnit(°C 'degree Celsius' temperature relative to 273.15 K)
    AUnit(lm 'lumen' luminous flux)
    AUnit(lx 'lux' illuminance)
    AUnit(Bq 'becquerel' radioactivity (decays per unit time))
    AUnit(Gy 'gray' absorbed dose (of ionising radiation))
    AUnit(Sv 'sievert' equivalent dose (of ionising radiation))
    AUnit(mSv 'millisievert' equivalent dose (of ionising radiation), 0.001Sv)
    AUnit(µSv 'microsievert' equivalent dose (of ionising radiation), 1e-06Sv)
    AUnit(kat 'katal' catalytic activity)
    """
    import io
    stext = io.StringIO(_default_raw_unit_table)
    return _read_raw_unit_table(stext)


def test_to_unit_map():
    """

    >>> from doctestprinter import doctest_iter_print
    >>> default_unit_map = test_to_unit_map()
    >>> def show_prefix_symbols(unit_map):
    ...     prefixes = list(unit_map)
    ...     all_used_prefixes = "', '".join(prefixes)
    ...     return "'{}'".format(all_used_prefixes)
    >>> doctest_iter_print(default_unit_map, edits_item=show_prefix_symbols)
    s:
      '', 'm'
    m:
      '', 'm', 'k'
    g:
      '', 'μ', 'm', 'k'
    A:
      '', 'G', 'M', 'm', 'k'
    K:
      ''
    mol:
      ''
    cd:
      ''
    rad:
      ''
    sr:
      ''
    min:
      ''
    h:
      ''
    d:
      ''
    °:
      ''
    ´:
      ''
    ´´:
      ''
    L:
      '', 'h', 'da', 'd'
    t:
      '', 'M', 'k'
    Np:
      ''
    B:
      '', 'd'
    eV:
      ''
    u:
      ''
    au:
      ''
    Hz:
      '', 'T', 'G', 'M', 'k'
    N:
      '', 'G', 'M', 'k', 'm', 'μ'
    Pa:
      '', 'G', 'M', 'k', 'h', 'da', 'd', 'c', 'm', 'μ'
    J:
      '', 'G', 'M', 'k', 'm', 'µ', 'n'
    W:
      '', 'T', 'G', 'M', 'k', 'm', 'µ'
    C:
      ''
    V:
      '', 'T', 'G', 'M', 'k', 'm', 'μ'
    F:
      ''
    Ω:
      '', 'G', 'M', 'k', 'm', 'μ'
    S:
      '', 'G', 'M', 'k', 'm', 'µ'
    Wb:
      ''
    T:
      '', 'G', 'M', 'k', 'm', 'µ'
    H:
      '', 'G', 'M', 'k', 'm', 'µ'
    °C:
      ''
    lm:
      ''
    lx:
      ''
    Bq:
      ''
    Gy:
      ''
    Sv:
      '', 'm', 'µ'
    kat:
      ''



    """
    justunits.reset_unit_library()
    return _unit_library.to_unit_map()


def test_short_cuts():
    """

    >>> from doctestprinter import doctest_iter_print
    >>> default_library_shortcuts = test_short_cuts()
    >>> doctest_iter_print(default_library_shortcuts)
    _KeyChainIndex(letter_index='s', length=1):
      s
    _KeyChainIndex(letter_index='m', length=2):
      ms -> mm -> mg -> mA -> mN -> mJ -> mW -> mV -> mΩ -> mS -> mT -> mH -> m
    _KeyChainIndex(letter_index='m', length=1):
      m
    _KeyChainIndex(letter_index='k', length=2):
      km -> kg -> kA -> kt -> kN -> kJ -> kW -> kV -> kΩ -> kS -> kT -> kH
    _KeyChainIndex(letter_index='g', length=1):
      g
    _KeyChainIndex(letter_index='μ', length=2):
      μg -> μN -> μV -> μΩ
    _KeyChainIndex(letter_index='A', length=1):
      A
    _KeyChainIndex(letter_index='G', length=2):
      GA -> GN -> GJ -> GW -> GV -> GΩ -> GS -> GT -> GH -> Gy
    _KeyChainIndex(letter_index='M', length=2):
      MA -> Mt -> MN -> MJ -> MW -> MV -> MΩ -> MS -> MT -> MH
    _KeyChainIndex(letter_index='K', length=1):
      K
    _KeyChainIndex(letter_index='m', length=3):
      mol -> min -> mPa -> mSv -> ms -> mm -> mg -> mA -> mN -> mJ -> mW -> mV -> mΩ -> mS -> mT -> mH -> m
    _KeyChainIndex(letter_index='c', length=2):
      cd
    _KeyChainIndex(letter_index='r', length=3):
      rad
    _KeyChainIndex(letter_index='s', length=2):
      sr -> s
    _KeyChainIndex(letter_index='h', length=1):
      h
    _KeyChainIndex(letter_index='d', length=1):
      d
    _KeyChainIndex(letter_index='°', length=1):
      °
    _KeyChainIndex(letter_index='´', length=1):
      ´
    _KeyChainIndex(letter_index='´', length=2):
      ´´ -> ´
    _KeyChainIndex(letter_index='L', length=1):
      L
    _KeyChainIndex(letter_index='h', length=2):
      hL -> h
    _KeyChainIndex(letter_index='d', length=3):
      daL -> dPa -> dL -> dB -> d
    _KeyChainIndex(letter_index='d', length=2):
      dL -> dB -> d
    _KeyChainIndex(letter_index='t', length=1):
      t
    _KeyChainIndex(letter_index='N', length=2):
      Np -> N
    _KeyChainIndex(letter_index='B', length=1):
      B
    _KeyChainIndex(letter_index='e', length=2):
      eV
    _KeyChainIndex(letter_index='u', length=1):
      u
    _KeyChainIndex(letter_index='a', length=2):
      au
    _KeyChainIndex(letter_index='H', length=2):
      Hz -> H
    _KeyChainIndex(letter_index='T', length=3):
      THz -> TW -> TV -> T
    _KeyChainIndex(letter_index='G', length=3):
      GHz -> GPa -> GA -> GN -> GJ -> GW -> GV -> GΩ -> GS -> GT -> GH -> Gy
    _KeyChainIndex(letter_index='M', length=3):
      MHz -> MPa -> MA -> Mt -> MN -> MJ -> MW -> MV -> MΩ -> MS -> MT -> MH
    _KeyChainIndex(letter_index='k', length=3):
      kHz -> kPa -> kat -> km -> kg -> kA -> kt -> kN -> kJ -> kW -> kV -> kΩ -> kS -> kT -> kH
    _KeyChainIndex(letter_index='N', length=1):
      N
    _KeyChainIndex(letter_index='P', length=2):
      Pa
    _KeyChainIndex(letter_index='h', length=3):
      hPa -> hL -> h
    _KeyChainIndex(letter_index='d', length=4):
      daPa -> daL -> dPa -> dL -> dB -> d
    _KeyChainIndex(letter_index='c', length=3):
      cPa -> cd
    _KeyChainIndex(letter_index='μ', length=3):
      μPa -> μg -> μN -> μV -> μΩ
    _KeyChainIndex(letter_index='J', length=1):
      J
    _KeyChainIndex(letter_index='µ', length=2):
      µJ -> µW -> µS -> µT -> µH
    _KeyChainIndex(letter_index='n', length=2):
      nJ
    _KeyChainIndex(letter_index='W', length=1):
      W
    _KeyChainIndex(letter_index='T', length=2):
      TW -> TV -> T
    _KeyChainIndex(letter_index='C', length=1):
      C
    _KeyChainIndex(letter_index='V', length=1):
      V
    _KeyChainIndex(letter_index='F', length=1):
      F
    _KeyChainIndex(letter_index='Ω', length=1):
      Ω
    _KeyChainIndex(letter_index='S', length=1):
      S
    _KeyChainIndex(letter_index='W', length=2):
      Wb -> W
    _KeyChainIndex(letter_index='T', length=1):
      T
    _KeyChainIndex(letter_index='H', length=1):
      H
    _KeyChainIndex(letter_index='°', length=2):
      °C -> °
    _KeyChainIndex(letter_index='l', length=2):
      lm -> lx
    _KeyChainIndex(letter_index='B', length=2):
      Bq -> B
    _KeyChainIndex(letter_index='S', length=2):
      Sv -> S
    _KeyChainIndex(letter_index='µ', length=3):
      µSv -> µJ -> µW -> µS -> µT -> µH

    """
    justunits.reset_unit_library()
    return _unit_library.short_cuts