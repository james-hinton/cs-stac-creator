ISO = {
    'fiji' : 'FJI',
    'solomon islands' : 'SLB',
    'vanuatu' : 'VUT',
}

def get_iso(country: str) -> str:
    """
    Return ISO code based on country

    :param country: Country name (str)

    :return: ISO Code (str)
    """
    return ISO.get(country.strip().lower())
