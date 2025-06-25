PLUGIN_NAME = 'Feat. Artists in Titles'
PLUGIN_AUTHOR = 'Lukas Lalinsky, Michael Wiencek, Bryan Toth, JeromyNix (NobahdiAtoll)'
PLUGIN_DESCRIPTION = 'Move "feat." from artist names to album and track titles. Match is case insensitive.'
PLUGIN_VERSION = "0.5"
PLUGIN_API_VERSIONS = ["0.9.0", "0.10", "0.15", "0.16", "2.0"]

from picard.metadata import register_album_metadata_processor, register_track_metadata_processor
from picard import log
import re

_feat_re = re.compile(r"([\s\S]+) feat\.([\s\S]+)", re.IGNORECASE)


def _fixed_title(s):
    """
    Title-cases a string, but corrects for apostrophes, e.g., "Don't"
    instead of "Don'T", "Let's" instead of "Let'S", and "I'm" instead of "I'M".
    """
    log.debug("FEATARTISTS: === _fixed_title DEBUG ===")
    log.debug(f"FEATARTISTS: INPUT: '{s}'")
    log.debug(f"FEATARTISTS: INPUT repr: {repr(s)}")

    titled_s = s.title()
    log.debug(f"FEATARTISTS: AFTER s.title(): '{titled_s}'")
    log.debug(f"FEATARTISTS: AFTER s.title() repr: {repr(titled_s)}")

    # Debug apostrophe characters - check for both ASCII and Unicode apostrophes
    apostrophe_chars = ["'", "'", "'", "`"]  # ASCII 39, Unicode 8217, Unicode 8216, grave accent
    for i, char in enumerate(titled_s):
        if char in apostrophe_chars:
            context_start = max(0, i-2)
            context_end = min(len(titled_s), i+3)
            context = titled_s[context_start:context_end]
            log.debug(f"FEATARTISTS: APOSTROPHE found at pos {i}: '{char}' (ord={ord(char)}) in context: '{context}'")

    # Apply the regex fix for Unicode 8217 (right single quotation mark)
    # This is the actual character used in MusicBrainz data after .title()
    pattern = r"(\w)’([A-Za-z])"  # Unicode 8217 right single quotation mark
    matches = re.findall(pattern, titled_s)
    log.debug(f"FEATARTISTS: REGEX PATTERN: {pattern}")
    log.debug(f"FEATARTISTS: REGEX MATCHES found: {matches}")

    # Replace Unicode 8217 apostrophes with proper lowercase after word characters
    result = re.sub(pattern, lambda m: m.group(1) + "'" + m.group(2).lower(), titled_s)

    log.debug(f"FEATARTISTS: FINAL RESULT: '{result}'")
    log.debug(f"FEATARTISTS: FINAL RESULT repr: {repr(result)}")
    log.debug("FEATARTISTS: === END DEBUG ===")

    return result


def move_album_featartists(tagger, metadata, release):
    match = _feat_re.match(metadata["albumartist"])
    if match:
        metadata["albumartist"] = match.group(1)
        metadata["album"] += " (feat.%s)" % match.group(2)
    match = _feat_re.match(metadata["albumartistsort"])
    if match:
        metadata["albumartistsort"] = match.group(1)


def move_track_featartists(tagger, metadata, track, release):
    log.debug("FEATARTISTS: === TRACK PROCESSOR CALLED ===")
    log.debug(f"FEATARTISTS: Track title: '{metadata['title']}'")
    log.debug(f"FEATARTISTS: Track artist: '{metadata['artist']}'")

    # Always process the title with _fixed_title
    title = _fixed_title(metadata["title"])

    # Check for featured artists
    match = _feat_re.match(metadata["artist"])
    if match:
        log.debug(f"FEATARTISTS: FEATURED ARTIST FOUND: {match.group(2)}")
        metadata["artist"] = match.group(1)
        featured_artist = match.group(2).strip()
        title += " (feat. " + _fixed_title(featured_artist) + ")"
    else:
        log.debug(f"FEATARTISTS: NO FEATURED ARTIST FOUND in artist: '{metadata['artist']}'")

    metadata["title"] = title
    log.debug(f"FEATARTISTS: FINAL TITLE SET TO: '{metadata['title']}'")
    log.debug("FEATARTISTS: === END TRACK PROCESSOR ===")

    match = _feat_re.match(metadata["artistsort"])
    if match:
        metadata["artistsort"] = match.group(1)

register_album_metadata_processor(move_album_featartists)
register_track_metadata_processor(move_track_featartists)
