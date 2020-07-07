
# de-oldify repo
git clone https://github.com/jantic/DeOldify.git deoldify_repo
ln -s deoldify_repo/deoldify deoldify

# de-oldify models
mkdir models
wget https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth -O ./models/ColorizeArtistic_gen.pth
wget https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth -O ./models/ColorizeStable_gen.pth

# image-super-resolution
#git clone https://github.com/idealo/image-super-resolution.git isr_repo
#ln -s isr_repo/ISR ISR
#wget https://public-asai-dl-models.s3.eu-central-1.amazonaws.com/ISR/rdn-C6-D20-G64-G064-x2/PSNR-driven/rdn-C6-D20-G64-G064-x2_PSNR_epoch086.hdf5 -O ./models/rdn-psnr-large.hdf5
#wget https://public-asai-dl-models.s3.eu-central-1.amazonaws.com/ISR/rdn-C3-D10-G64-G064-x2/PSNR-driven/rdn-C3-D10-G64-G064-x2_PSNR_epoch134.hdf5 -O ./models/rdn-psnr-small.hdf5
#wget https://public-asai-dl-models.s3.eu-central-1.amazonaws.com/ISR/rdn-C6-D20-G64-G064-x2/ArtefactCancelling/rdn-C6-D20-G64-G064-x2_ArtefactCancelling_epoch219.hdf5 -O ./models/rdn-noise-cancel.hdf5
#wget https://public-asai-dl-models.s3.eu-central-1.amazonaws.com/ISR/rrdn-C4-D3-G32-G032-T10-x4-GANS/rrdn-C4-D3-G32-G032-T10-x4_epoch299.hdf5 -O ./models/rrdn-gans.hdf5

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

https://drive.google.com/open?id=1xjyW_0dDS4jSTxKVZwtlkyfS4Oso-GUF

# python venv
rm -fr venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt