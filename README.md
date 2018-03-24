Poll-n
======

All the code is under the Mozilla Public License Version 2.0.

Fonts are under there own license.

The image named "draw.png" is the property of "Krystalia" : https://krysthalia.deviantart.com/, all right reserved.

Other images are also under the Mozilla Public License Version 2.0.

install
-------

Fedora / Arch-linux:
```
pip install -r requirements.txt
```

Debian / Open-suse leap
```
pip3 install -r requirements.txt
```

It should work on windows, you need to install python 3 and pip for windows and do the same as fedora command.

start
-----

Fedora / Arch-linux:
```
cd polln
python manage.py runserver
```

Debian / Open-suse leap
```
cd polln
python3 manage.py runserver
```

Update css
----------
```
sudo npm install stylus -g
stylus -w themes/main.styl -o polln/webApp/static/webApp/style.css
```

