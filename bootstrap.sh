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

# brew install libpng, cmake
brew install libpng cmake

# python venv
rm -fr venv
python3 -m venv --copies venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt