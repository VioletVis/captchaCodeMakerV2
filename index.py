from flask import Flask, render_template
import requests
app = Flask(__name__)
#app.config['TEMPLATES_AUTO_RELOAD'] = True # Debug

#region Roblox shit

def funCaptchaPublicKeys(key = "ACTION_TYPE_WEB_LOGIN"):
    """
    Gets current funcaptcha key
    so if they update so does this

    Args:
        key (str, optional): Key name. Defaults to "ACTION_TYPE_WEB_LOGIN".

    Returns:
        str: Current Funcaptcha public key
    """
    return requests.get("https://apis.rbxcdn.com/captcha/v1/metadata").json()["funCaptchaPublicKeys"][key]

def getXsrf():
    """
    Fuck Roblox's Cross-site request forgery shit

    Returns:
        str: X-Csrf-Token
    """
    xsrHeader = requests.post("https://auth.roblox.com/v2/login", headers={
        "X-CSRF-TOKEN": ""
    }).headers['x-csrf-token']
    return xsrHeader


def getFieldData():
    """
    Get the field data code thingy That Roblox uses for captchas now

    Returns:
        str: Field data for captcha
    
    To read the codes do this::

        data = getFieldData()
        captchaId = data.split(",")[0]
        captchaData = data.split(",")[1] #(not used for creating/logging into accounts
    """
    headers = {
        'authority': 'auth.roblox.com',
        'x-csrf-token': getXsrf(),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
    }
    data = {
    "ctype": "Username",
    "username":"CleanedByBy",
    "password":"Red284go!",
    "captchaId":"a",
    "captchaToken":"token",
    "captchaProvider":"PROVIDER_ARKOSE_LABS"
}
    return requests.post('https://auth.roblox.com/v2/login', headers=headers, json=data).json()

#endregion

@app.route('/', methods=['GET'])
def hello_world():
    """
    Renders out the captcha page when user goes to main page.
    """
    return getFieldData()
    #data = getFieldData().split(',')

    # Give the user the captcha page
    return render_template('getcode.html',
                            funCaptchaPublicKeys = funCaptchaPublicKeys("ACTION_TYPE_WEB_LOGIN"),
                            message = "Solve captcha to get the code!",
                            data = str( data[1]),
                            id = data[0]
                        )

# run flask i guess
if __name__ == '__main__':
    
    app.run(port=80)
