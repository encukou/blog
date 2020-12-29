#! /bin/bash

echo PUBLISH_DATE=${PUBLISH_DATE:=$(date -Id --date='last Mon + 4 days')}
# (this'll need to be adjusted in 2022...)
echo WEEK_NO=${WEEK_NO:=$(date +'%V' --date='last Mon + 4 days')}

echo FILENAME=${FILENAME:=posts/$PUBLISH_DATE-cs-tydenni-$WEEK_NO.md}

NNBSP=' '  # U+202F NARROW NO-BREAK SPACE

echo WEEK_START=${WEEK_START:=$(date +"%-m.$NNBSP%-d." --date='last Mon')}
echo WEEK_END=${WEEK_END:=$(date +"%-m.$NNBSP%-d." --date='last Mon + 4 days')}

if [ -e $FILENAME ]; then echo File $FILENAME exists, not overwriting.; exit 1; fi

tee $FILENAME << END | sed 's/^/    /'
Title: Týdenní poznámky #$((WEEK_NO))
Tags: weekly

<!-- PELICAN_BEGIN_SUMMARY -->

Utekl další týden ($WEEK_START–$WEEK_END), a tak si sepisuju, co jsem dělal.

<!-- PELICAN_END_SUMMARY -->

END

echo go edit $FILENAME
