
# timeslide macOS bundler

# build using pyinstaller
source ./venv/bin/activate
rm -fr dist build
pyinstaller timeslide.spec

# convert icons, and bundle
iconutil -c icns -o imgs/icon-windowed.icns imgs/icon.iconset
mv imgs/icon-windowed.icns dist/timeslide.app/Contents/Resources/.