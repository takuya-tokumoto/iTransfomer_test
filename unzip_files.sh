#!/bin/bash

for file in ./tmp/*.zip
do
  filename=$(basename "$file")
  if [ "$filename" = "Rotary_beacon_light.zip" ]; then
    # Rotary_beacon_light.zip ファイルのみ特定のディレクトリに解凍
    UNZIP_DISABLE_ZIPBOMB_DETECTION=TRUE unzip -d ./data/input/Rotary_beacon_light/ "$file"
  else
    # その他のファイルは元のディレクトリに解凍
    UNZIP_DISABLE_ZIPBOMB_DETECTION=TRUE unzip -d ./data/input/ "$file"
  fi
done
