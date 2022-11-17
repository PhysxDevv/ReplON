import requests
import os

class ReplON:
  def __init__(self, KEY):
    self.KEY = KEY
    self.payload = "api_key=" + KEY + "&format=json&logs=1"
    self.headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
        }
    self.replowner = os.environ['REPL_OWNER']
    self.replname = os.environ['REPL_SLUG']

  def getMonitors(self):
    response = requests.request("POST", "https://api.uptimerobot.com/v2/getMonitors", data=self.payload, headers=self.headers)
    return response.text

  def activate(self):
    with open("server.py", "w") as server:
      server.write("""from flask import Flask
app = Flask('app')
@app.route('/')
def index():
  return 'ReplON Server Activated!'
app.run(host='0.0.0.0', port=8080)""")
      server.close()
    
    monitorPayload = self.payload + "&type=1&url=http%3A%2F%2F" + self.replname + "." + self.replowner + ".repl.co" + "&friendly_name=" + self.replname
    response = requests.request("POST", "https://api.uptimerobot.com/v2/newMonitor", data=monitorPayload, headers=self.headers)
    os.system("python3 server.py")
    return response.text