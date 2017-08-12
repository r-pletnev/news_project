import codecs
import re 
from urllib.parse import urlparse

def nofollow(txt):
    index = txt.find('>')
    return '{} rel="nofollow"{}'.format(txt[:index], txt[index:])


def noindex_nofollow(txt, start, end, noindex=True):
    inner_txt = txt[start:end] if noindex else nofollow(txt[start:end])
    return '{}<noindex>{}</noindex>{}'.format(txt[:start], inner_txt, txt[:end])


def process_body(value):
    """Add nofollow and noindex for arrow tags"""
    value_copy = value[:]
    import pdb;pdb.set_trace()
    
    a_tags = r'<a\s+(?P<part_one>[^>]*)>.*?<\/a>'
    for m in re.finditer(a_tags, value):
        a_start, a_end = m.span()
        value_copy = noindex_nofollow(value_copy, a_start, a_end)

    value_new_copy = value_copy[:]
    for m in re.finditer(a_tags, value_copy):
        a_start, a_end = m.span()
        value_new_copy = noindex_nofollow(value_new_copy, a_start, a_end, noindex=False)

    return value_new_copy

def get_unicode_string(txt):
    """Will decode unicode_escape after waspace script mess"""
    text, _ = codecs.getdecoder('unicode_escape')(txt)
    return text.replace('"', "")

def get_url_params(value):
    return urlparse(value)._asdict()






