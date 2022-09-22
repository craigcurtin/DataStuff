#!/usr/bin/env bash
shopt -s extglob
TMP_INPUT=/tmp/tmp_$$.md
cat [0-9][0-9]_*.md >  ${TMP_INPUT}
PANDOC_OPTS="-s -V geometry:margin=1in --table-of-contents  --title-prefix=Vault_Tutorial"
pandoc  ${PANDOC_OPTS} -o doc.pdf  ${TMP_INPUT}
pandoc  ${PANDOC_OPTS} -o doc.html  ${TMP_INPUT}

# if [ 2 ] ; then rm  ; fi
exit 0
