HATMAP = {
    'Cx': 'Ĉ', 'cx': 'ĉ',
    'Gx': 'Ĝ', 'gx': 'ĝ',
    'Hx': 'Ĥ', 'hx': 'ĥ',
    'Jx': 'Ĵ', 'jx': 'ĵ',
    'Sx': 'Ŝ', 'sx': 'ŝ',
    'Ux': 'Ŭ', 'ux': 'ŭ'}


def apply_hatmap(text):
    """Convert alphabet + x to hatted alphabet

    Args:
        text (str): text which may include alphabet + x

    Returns:
        str: text without alphabet + x
    """
    for k, v in HATMAP.items():
        text = text.replace(k, v)
    return text
