
# de-oldify repo
git clone https://github.com/jantic/DeOldify.git deoldify_repo
ln -s deoldify_repo/deoldify deoldify

# de-oldify models
mkdir models
wget https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth -O ./models/ColorizeArtistic_gen.pth
wget https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth -O ./models/ColorizeStable_gen.pth

# super-resolution repo
git clone https://github.com/krasserm/super-resolution.git
ln -s super-resolution/model model
ln -s super-resolution/data.py data.py
ln -s super-resolution/utils.py utils.py

# temp
ln -s super-resolution/demo demo

# super-resolution weights
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xjyW_0dDS4jSTxKVZwtlkyfS4Oso-GUF' -O weights-edsr-16-x4.tar.gz
tar -xzf weights-edsr-16-x4.tar.gz
rm weights-edsr-16-x4.tar.gz
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1JfQNGQZ9cG-lyC5EB0W3MpySjPlDJXpU' -O weights-wdsr-b-32-x4.tar.gz
tar -xzf weights-wdsr-b-32-x4.tar.gz
rm weights-wdsr-b-32-x4.tar.gz
# TODO: srgan file is too large to download this way
#wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1u9ituA3ScttN9Vi-UkALmpO0dWQLm8Rv' -O weights-srgan.tar.gz
#tar -xzf weights-srgan.tar.gz
#rm weights-srgan.tar.gz

https://drive.google.com/open?id=1u9ituA3ScttN9Vi-UkALmpO0dWQLm8Rv

# python venv
rm -fr venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt