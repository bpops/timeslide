git clone https://github.com/jantic/DeOldify.git deoldify_repo
cp -r deoldify_repo/deoldify deoldify
mkdir models
wget https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth?dl=0 -O ./models/ColorizeArtistic_gen.pth
pip install -r requirements.txt