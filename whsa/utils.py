import re


NAME_RX = r'(?P<last_name>.+?), (?:(?P<suffix>[^,]+),)? *(?P<first_name>.+?) *(?P<middle_name>[A-Z]\.)?$'


def cleanspaces(txt):
    return re.sub(r'\s{2,}', ' ', txt).strip()

def parse_name(name):
    """
    name is a string

    returns dict: {'last_name': 'x', 'first_name': , 'middle_name', 'suffix'}

    Examples:
        Trump, Ivanka M.
        Hsu, Irene
        Johnston, Jr., Robert O.
    """
    mx = re.match(NAME_RX, name)
    if mx:
        return mx.groupdict()
    else:
        # import code; code.interact(local=locals())
        return {}
