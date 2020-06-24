
# timeslide macOS bundler

source ./venv/bin/activate
rm -fr dist build
#pyinstaller -F timeslide.spec
pyinstaller timeslide.spec