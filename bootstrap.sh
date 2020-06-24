
# deoldify
git clone https://github.com/jantic/DeOldify.git deoldify_repo
ln -s deoldify_repo/deoldify deoldify
mkdir models
wget https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth -O ./models/ColorizeArtistic_gen.pth
wget https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth -O ./models/ColorizeStable_gen.pth

# image-super-resolution
git clone https://github.com/idealo/image-super-resolution.git isr_repo
wget https://github.com/idealo/image-super-resolution/raw/master/weights/sample_weights/rdn-C6-D20-G64-G064-x2/PSNR-driven/rdn-C6-D20-G64-G064-x2_PSNR_epoch086.hdf5 -O ./models/

# python venv
rm -fr venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

