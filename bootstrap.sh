# timeslide bootstrap

# de-oldify repo
git clone https://github.com/jantic/DeOldify.git deoldify_repo
ln -s deoldify_repo/deoldify deoldify

# de-oldify models
mkdir models
wget https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth -O ./models/ColorizeArtistic_gen.pth
wget https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth -O ./models/ColorizeStable_gen.pth

# opencv2 models
wget https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x2.pb -O ./models/EDSR_x2.pb
wget https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x3.pb -O ./models/EDSR_x3.pb
wget https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x4.pb -O ./models/EDSR_x4.pb
wget https://github.com/fannymonori/TF-ESPCN/raw/master/export/ESPCN_x2.pb -O ./models/ESPCN_x2.pb
wget https://github.com/fannymonori/TF-ESPCN/raw/master/export/ESPCN_x3.pb -O ./models/ESPCN_x3.pb
wget https://github.com/fannymonori/TF-ESPCN/raw/master/export/ESPCN_x4.pb -O ./models/ESPCN_x4.pb
wget https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x2.pb -O ./models/FSRCNN_x2.pb
wget https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x3.pb -O ./models/FSRCNN_x3.pb
wget https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x4.pb -O ./models/FSRCNN_x4.pb
wget https://github.com/fannymonori/TF-LapSRN/raw/master/export/LapSRN_x2.pb -O ./models/LapSRN_x2.pb
wget https://github.com/fannymonori/TF-LapSRN/raw/master/export/LapSRN_x4.pb -O ./models/LapSRN_x4.pb
wget https://github.com/fannymonori/TF-LapSRN/raw/master/export/LapSRN_x8.pb -O ./models/LapSRN_x8.pb

# dped
# wget https://polybox.ethz.ch/index.php/s/7z5bHNg5r5a0g7k/download -O vgg_pretrained/imagenet-vgg-verydeep-19.mat

# super-resolution repo
#git clone https://github.com/krasserm/super-resolution.git
#ln -s super-resolution/model model
#ln -s super-resolution/data.py data.py
#ln -s super-resolution/utils.py utils.py

# super-resolution weights
#wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xjyW_0dDS4jSTxKVZwtlkyfS4Oso-GUF' -O weights-edsr-16-x4.tar.gz
#tar -xzf weights-edsr-16-x4.tar.gz
#rm weights-edsr-16-x4.tar.gz
#wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1JfQNGQZ9cG-lyC5EB0W3MpySjPlDJXpU' -O weights-wdsr-b-32-x4.tar.gz
#tar -xzf weights-wdsr-b-32-x4.tar.gz
#rm weights-wdsr-b-32-x4.tar.gz

# python venv
rm -fr venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt