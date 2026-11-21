"""Resolve former project URLs without altering retained source documents."""
import re
from urllib.parse import urlsplit, urlunsplit

REPOSITORY = 'KomorebiP/The-Komorebi-Program'
BASE_URL = 'https://komorebip.github.io/The-Komorebi-Program/'
LEGACY_REPOSITORY = 'KomorebiP/Operation-KOMOREBI'


def canonical_project_url(url):
    parts = urlsplit(url)
    if parts.scheme not in {'http', 'https'}:
        return url
    host = parts.netloc.casefold()
    if host == 'komorebip.github.io':
        previous, current = '/Operation-KOMOREBI', '/The-Komorebi-Program'
    elif host in {'github.com', 'raw.githubusercontent.com'}:
        previous, current = '/' + LEGACY_REPOSITORY, '/' + REPOSITORY
    elif host == 'api.github.com':
        previous, current = '/repos/' + LEGACY_REPOSITORY, '/repos/' + REPOSITORY
    else:
        return url
    path = parts.path
    if path.casefold() == previous.casefold() or path.casefold().startswith(previous.casefold() + '/'):
        return urlunsplit(parts._replace(path=current + path[len(previous):]))
    return url


def canonical_project_links(text):
    """Use current addresses in generated navigation, retaining its source records."""
    return re.sub(r"https?://[^\s<>\"']+", lambda match: canonical_project_url(match[0]), text)
