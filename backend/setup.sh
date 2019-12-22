# init venv
python3 -m venv tara
source tara/bin/activate

# install selenium
pip3 install selenium -t seleniumLayer/selenium/python/lib/python3.6/site-packages
cd seleniumLayer
mkdir chromedriver
cd chromedriver
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
unzip chromedriver.zip
rm chromedriver.zip

# download chrome binary
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip headless-chromium.zip
rm headless-chromium.zip

