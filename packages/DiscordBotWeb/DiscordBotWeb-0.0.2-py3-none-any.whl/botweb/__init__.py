import os, shutil

def web(name, description, link, filename):
	if not os.path.exists("./templates"):
		os.mkdir("./templates")
	else:
		pass
	if not os.path.exists("./static"):
		os.mkdir("./static")
	else:
		pass
	try:
		shutil.move("./logo.png", "./static")
	except:
		pass
	with open(f"./templates/{filename}.html", "w") as file:
		head = f'''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width" />
	<title> {name} </title>
	<link href="https://fonts.googleapis.com/css?family=B612" rel="stylesheet" />
</head>'''

		style =	'''
	<style>
		* {
			font-family: "B612";
			color: white;
		}

		body {
			background: #0B1727;
		}

		.name {
			position: relative;
			color: #fff;
			font-family: "B612";
			font-size: 20px;
		}

		.line {
			width: 50px;
			height: 5px;
			background: white;
			position: relative;
			animation: line 5s;
			animation-direction: alternate;
			animation-iteration-count: infinite;
		}

		@keyframes line {
			0% {
				left: 0px;
				top: 0px;
				width: 50px;
			}
			50% {
				left: 150px;
				top: 0px;
				width: 5px;
			}
			100% {
				left: 0px;
				top: 0px;
				width: 50px;
			}
		}

		.logo {
			background-image: url("./static/logo.png");
			background-size: 200px;
			background-repeat: no-repeat;
			width: 200px;
			height: 200px;
		}

		.invite {
			position: absolute;
			transform: translate(-50%, -50%);
			width: 200px;
			height: 50px;
			text-align: center;
			line-height: 50px;
			color: #000;
			font-size: 25px;
			font-family: "B612";
			text-transform: uppercase;
			text-decoration: none;
			box-sizing: border-box;
			background: white;
			background-size: 400%;
			border-radius: 5px;
		}
	</style>'''

		body = f'''
	<body>
		<div class="name">
			<b>{name}</b>
		</div>
		<div class="line"></div>
		<center>
			<div class="logo"></div>
			<h1>{name}</h1>
			<br />
			{description}
			<br />
			<br />
			<br />
			<br />
			<a href={link} class="invite">Invite</a>
		</center>
	</body>
</html>'''
		file.write(head)
		file.write(style)
		file.write(body)
		file.close()