# Feat. Artists in Titles - Personal Modification

This repository contains a modified version of the "Feat. Artists in Titles" plugin for [MusicBrainz Picard](https://picard.musicbrainz.org/).

## Original Plugin

The original script was created by **Lukas Lalinsky, Michael Wiencek, Bryan Toth, and JeromyNix (NobahdiAtoll)**. Its purpose is to move "feat." from artist names to album and track titles.

## Modification

This version introduces a small change to the `move_track_featartists` function. In addition to its original behavior, the script now also:

1.  Title-cases the main song title.
2.  Title-cases the featured artist's name.
3.  Ensures `(feat. ...)` remains in lowercase within the title.

## Purpose of this Fork

This modification was created to solve a specific formatting problem. Using the standard Picard tagger script function `$title(%title%)` also capitalizes "feat." to "Feat.", which is undesirable.

This modified plugin provides a way to correctly title-case the song and featured artist while preserving the lowercase "feat." convention. This change makes the following part of a tagger script unnecessary:

```
$noop(
For track title
    $set(title,$title(%title%))
Not needed with custom python script
)

$set(album,$title(%album%))
$set(artist,$title(%artist%))
$set(artists,$title(%artists%))
$set(albumartist,$title(%albumartist%))
$set(albumartistsort,$title(%albumartistsort%))
$set(artistsort,$title(%artistsort%))
$set(albumartistsortorder,$title(%albumartistsortorder%))
```
