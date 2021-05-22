import click
import dotenv
import os, subprocess, pathlib, time, string, random, requests, signal
from webbrowser import open_new
from auth.auth import renewAccessToken, getScope, app
from data import api, view, chart
from subprocess import Popen, PIPE

#Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

@click.group()
def cli():
  pass

@cli.command(name = 'init')
def start():
	output("Greetings ✨", "bright_white")
	init()

@cli.command(name = 'wallet')
def wallet():
	view.selectCoin(api.getCoin())

@cli.command(name = 'graph')
def graph():
	coin = api.getCoin()
	chart.getChartData(api.getCoin())

@cli.command(name = 'switch')
def switch():
	output("I'll need you to authorize me to switch wallets 😁", 'yellow')
	time.sleep(2)
	login()

@cli.command(name = 'address')
def switch():
	output("Use this address to receive new payments 🧧", 'yellow')
	try:
		click.echo(api.createAddress(api.getCoin()))
	except Exception as err:
		output("Unable to fetch an address 😔", 'red')

@cli.command(name = 'refresh')
def refresh():
	try:
		refresh()
		output("Successfully renewed access token 👏",'green')
	except Exception as err:
		output("Failed to renewed access token, please login again", 'red')
		login()

@cli.command(name = 'reset')
def reset():
	output("Good Bye 🥲", 'bright_white')
	subprocess.call("rm -rf .env",shell = True)
	subprocess.call("touch .env",shell = True)

@cli.command(name = 'switch')
def switch():
	output("I'll need you to authorize me to switch wallets 😁", 'yellow')
	time.sleep(2)
	login()

def genState():
	return ''.join(random.choice(string.ascii_uppercase 
		+ string.ascii_lowercase + string.digits) for _ in range(16))
	

def init():
	if os.getenv('LOGIN_STATE') == None:
		if os.getenv('CLIENTID') == None and os.getenv('CLIENT_SECRET') == None:
			output("Let's get you setup 🪄", 'bright_white')
			output("Head over to your Coinbase account and under the API tab create a new OAuth Application 👩‍💻", 'bright_white')
			output("Make a note of the CLIENTID and the CLIENT_SECRET, I'll need it 😉", 'bright_white')
			output("✍️  Enter your Client ID : ", 'blue')
			clientid = input()
			dotenv.set_key(dotenv_file, 'CLIENTID', clientid)
			output("✍️  Enter your Client Secret : ", 'blue')
			clientSecret = input()
			dotenv.set_key(dotenv_file, 'CLIENT_SECRET', clientSecret)
			output("✍️  Enter a redirect URL : ", 'blue')
			redirectUrl = input()
			dotenv.set_key(dotenv_file, 'REDIRECT_URL', redirectUrl)

		if os.getenv('NOOMICS_API_KEY') == None and os.getenv('BINANCE_API_KEY') == None and os.getenv('BINANCE_SECRET_KEY') == None:
			output("I also use data from Noomics and Binance to function, I'll need their API keys to proceed 😊", 'bright_white')
			output("Enter your Noomics API key : ", 'blue')
			noomics = input()
			dotenv.set_key(dotenv_file, 'NOOMICS_API_KEY', noomics)
			output("Enter your Binance API key : ", 'blue')
			binance_api = input()
			dotenv.set_key(dotenv_file, 'BINANCE_API_KEY', binance_api)
			output("Enter your Binance Secret key : ", 'blue')
			binance_secret = input()
			dotenv.set_key(dotenv_file, 'BINANCE_SECRET_KEY', binance_secret)
			output("That's all the info I need, thanks ! 😊", "yellow")
			login()

		else:
			if os.getenv('TIME') == None:
				login()
			elif time.time() - float(os.getenv('TIME')) > 7200: 
				output("⚠️ Access token expired", "yellow")
				output("Redirecting you to login page to renew it", "yellow")
				time.sleep(2)
				login()
			else:
				refresh()

def output(inp, color):
	click.echo()
	click.echo(
				click.style(inp, fg=color, bold=True)
			)
	click.echo()

def login():
	path = pathlib.Path().absolute()
	dotenv.load_dotenv()

	#Kill any process running at PORT 6660
	removeProcess()

	output("In order to continue, you must login to your Coinbase account 💳", 'bright_white')
	output("I'm taking you to the login page right now", 'bright_white')
	time.sleep(2)

	AUTH_URI = ('https://www.coinbase.com/oauth/' 
		+ 'authorize?response_type=code&client_id=' + os.getenv('CLIENTID') + '&redirect_uri=' 
		+ os.getenv('REDIRECT_URL') + '&scope=' + getScope() + '&meta[send_limit_amount]=1'+
		'&meta[send_limit_currency]=USD'+'&code=' + '302')
	
	open_new(AUTH_URI)
	
	#start the flask server for OAuth
	app.run(port=6660)

def refresh():

	#Fetch new access token using refresh token 
	if time.time() - float(os.getenv('TIME')) <= 7200:
		renewAccessToken()

def removeProcess():
	port = 6660
	process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	for process in str(stdout.decode("utf-8")).split("\n")[1:]:       
		data = [x for x in process.split(" ") if x != '']
		if (len(data) <= 1):
			continue

		os.kill(int(data[1]), signal.SIGKILL)

if __name__ == "__main__":
   cli()