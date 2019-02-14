def md_heading(level, heading):
    """ Returns the markdown heading at the level specified
    """
    return "{} {}\n".format("#"*int(level), heading)

def is_indented(text):
    """ Simple check to see if a line is indented
    For now, a line that starts with ANY whitespace is indented
    """

    return bool(len(text) - len(text.lstrip()))