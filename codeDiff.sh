#!/bin/bash

set -x

#Get code changed with a revision and copy into org/fix dir
#It is easy to compare code change side by side with other tools winmerge, meld, kdiff3 ...
#Usage codeDiff.sh <revision> <[dest]>
#     Example:
#         codeDiff.sh 6616 /home/lhhoang
#  Result: codeDiff_6616.tar.gz will be stored at /home/lhhoang
#Copyright by hoang.leinfonam.com

if [ "$1" == "" ]; then
  echo "Usage: codeDiff.sh <revision> <url> <[dest]>"
  exit 0
fi

if [ "$2" == "" ]; then
  echo "Usage: codeDiff.sh <revision> <url> <[dest]>"
  exit 0
fi

CURRDIR=`pwd`

if [ "x$3" != "x" ]; then
  CURRDIR=$3
fi

SVNURL=$2

REVISION=$1
OLD=`expr $REVISION - 1`

FILES=`svn log -r $REVISION --verbose | grep "^[\ +A|M|D]" | awk '{print $2}'`

`rm -rf $CURRDIR/codeDiff_$REVISION/*`

ORGDIR="$CURRDIR/codeDiff_$REVISION/org"
FIXDIR="$CURRDIR/codeDiff_$REVISION/fix"

`mkdir -p $ORGDIR`
`mkdir -p $FIXDIR`

for file in $FILES
do
  DIR=`dirname $file`
  #echo $filename
  if [ ! -d "$FIXDIR/$DIR" ]; then
    #echo "Making dir: $CURRDIR/$DIR" 
    mkdir -p "$FIXDIR/$DIR"
  fi

  if [ ! -d "$ORGDIR/$DIR" ]; then
    #echo "Making dir: $CURRDIR/$DIR" 
    mkdir -p "$ORGDIR/$DIR"
  fi
  
  `svn export $SVNURL$file$REVISION $FIXDIR/$file 1>/dev/null` 
  `svn export $SVNURL$file$OLD $ORGDIR/$file 1>/dev/null` 
done

tar czf $CURRDIR/codeDiff_$REVISION.tar.gz $CURRDIR/codeDiff_$REVISION
#rm -rf $CURRDIR/codeDiff_$REVISION


