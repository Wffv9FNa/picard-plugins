PLUGIN_NAME = 'Feat. Artists in Titles'
PLUGIN_AUTHOR = 'Lukas Lalinsky, Michael Wiencek, Bryan Toth, JeromyNix (NobahdiAtoll)'
PLUGIN_DESCRIPTION = 'Move "feat." from artist names to album and track titles. Match is case insensitive.'
PLUGIN_VERSION = "0.5"
PLUGIN_API_VERSIONS = ["0.9.0", "0.10", "0.15", "0.16", "2.0"]

from picard.metadata import register_album_metadata_processor, register_track_metadata_processor
import re

_feat_re = re.compile(r"([\s\S]+) feat\.([\s\S]+)", re.IGNORECASE)


def _fixed_title(s):
    """
    Title-cases a string, but corrects for apostrophes, e.g., "Don't"
    instead of "Don'T".
    """
    titled_s = s.title()
    return re.sub(r"(\w)'(\w)", lambda m: m.group(1) + "'" + m.group(2).lower(), titled_s)


def move_album_featartists(tagger, metadata, release):
    match = _feat_re.match(metadata["albumartist"])
    if match:
        metadata["albumartist"] = match.group(1)
        metadata["album"] += " (feat.%s)" % match.group(2)
    match = _feat_re.match(metadata["albumartistsort"])
    if match:
        metadata["albumartistsort"] = match.group(1)


def move_track_featartists(tagger, metadata, track, release):
    title = _fixed_title(metadata["title"])
    match = _feat_re.match(metadata["artist"])
    if match:
        metadata["artist"] = match.group(1)
        featured_artist = match.group(2).strip()
        title += " (feat. " + _fixed_title(featured_artist) + ")"
    metadata["title"] = title
    match = _feat_re.match(metadata["artistsort"])
    if match:
        metadata["artistsort"] = match.group(1)

register_album_metadata_processor(move_album_featartists)
register_track_metadata_processor(move_track_featartists)
