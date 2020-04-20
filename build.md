# Denpendence
1. Install **Kismet**

    [Kismet install documentation, which includes all systems](https://www.kismetwireless.net/docs/readme/packages/)

2. Install **Python3**
    
    If you have python, please check the verison
    ```
    $ python --version
    ```
    Install all the following python dependence
    ```python
    pip install certifi cffi chardet Click cryptography Flask idna Jinja2 MarkupSafe numpy pycparser pycryptodome PyMySQL requests six urllib3 virtualenv virtualenvwrapper-win Werkzeug
    ```
    If you have install some of them, just check the dependece version as

# Kismet setup
1. Making sure you have wifi card on your machine that supports monitor mode

    [You can check your wifi card here](https://techwiser.com/check-if-wireless-adapter-supports-monitor-mode/)

2. Download the Seeet folder
3. In one command prompt, enter Seeet folder that just created
    ```
    $ kismet
    ```
    In a new Web browser page, enter http://localhost:2501/. Enable the wifi monitor in this web.

    To enable wifi monitor for kismet, you can select the left right corner menu, and select Data Sources.

    In Data Sources, you are able to see the wifi card that support monitor mode, enable it.

    **note**: if you only have one wifi card, open monitor mode will let you offline.
# Running
## server
1. Open the server in the Seeet folder
2. run server script
    ```
    python app.py
    ```
3. Open other command, enter the folder Seeet, run the kismet_init.py
    ```
    $ python kismet_init.py "Kismet_data.kismet" "Your wifi name"
    ```
    **note**: "Kismet_data.kismet" is in this folder while running kismet, the name should be like something "Kismet-20200419-02-00-10-1.kismet". Replace the name within your folder

## client
1. Open the web browser, and open localhost:"your server port" 