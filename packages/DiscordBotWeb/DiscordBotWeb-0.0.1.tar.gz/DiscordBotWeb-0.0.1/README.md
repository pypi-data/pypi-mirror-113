# DiscordBotWeb

## New Release Notes
 - Published 7/15/2021 (v0.0.1)

## Features
 - Made With The Powerful Module, OS
 - No HTML Prior Knowledge Required
 - Made To Be Used With Flask

## How It Works
 - ```import botweb```
   - You Guys Should Know What This Does, It Imports The Module
 - ```botweb.web(name, description, link, filename)```
   - This Is Where It Gets Tricky, Lets Break It Down, ```botweb.web()``` is the function itself, ```name, description, link, filename``` Are The Attributes For The Function. 
     - The ```name``` Attribute Is For The Name Of Your Bot. Secondly, The ```description``` Attribute Is A Small Description Of Your Bot, Make Sure It Is Under 10 Words For A Clean Looking Website. Thirdly, The ```link``` Attribute Is For The Link Of Your Bot, The Link Will Be Used For The Invite Button. Lastly, The ```filename``` Attribute Is The Name That You Want Your HTML File To Be Named.

## Example With Flask 
 - Please Note That You Must Use Flask
 ```py
 from flask import Flask, render_template
 import botweb

 app = Flask(__name__)

 @app.route("/")
 def main():
	# Make Sure To Keep An Logo Of Your Bot In The Same Directory Of This Python File
	botweb.web("Bot Name", "Description Of Bot", "Invite Link", "index") # The Last Attribute Is The Name That You Want The HTML File To Be
	return render_template("index.html") # Make Sure It Is The Same Name As You Put In The Last Attribute When Calling botweb.web(), And Just Add The .html Extension.

 ```