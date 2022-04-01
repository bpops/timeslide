
# timeslide macOS bundler

# build using pyinstaller
source ./venv/bin/activate
rm -fr dist build
pyinstaller timeslide.spec -n TimeSlide
# --paths="venv/lib/python3.7/site-packages/cv2/"

# convert icons, and bundle
iconutil -c icns -o imgs/icon-windowed.icns imgs/icon.iconset
mv imgs/icon-windowed.icns dist/timeslide.app/Contents/Resources/.

# rename app
mv dist/timeslide.app dist/TimeSlide.app
