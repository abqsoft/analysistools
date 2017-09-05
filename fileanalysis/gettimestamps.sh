#!/bin/bash
echo path,type,created,created_utc,accessed,accessed_utc,modified,modified_utc
find $1 -name "*" -print0 | xargs -n1 -I_filename -0 stat -c %n,%F,%Z,%z,%X,%x,%Y,%y _filename
