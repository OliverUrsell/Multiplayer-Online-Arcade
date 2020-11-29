
<!-- 
	|| ||
	|| ||
	\\_//
Oliver Ursell
-->

<!DOCTYPE HTML>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta content="width=device-width, initial-scale=1" name="viewport" />
		<title>Frogger</title>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
		<script src="https://code.jquery.com/jquery-3.2.1.min.js" crossorigin="anonymous"></script>
		<link rel="stylesheet" href="boss.css">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.min.js" type="text/javascript"></script>
	</head>
	<body>

		<?php
			$name = htmlspecialchars($_POST["name"]);
			$host = htmlspecialchars($_POST["host"]);
			echo '<script type="text/javascript">
					var name = "'. $name .'";
					var host = "'. $host .'";
				  </script>'
		?>
		<script type="text/javascript" src="boss.js"></script>

		<h1 id="lives">Lives: 3/3</h1>

		<button id="lane1" class="moveButton" zone="1">Zone 1</button>
		<button id="lane2" class="moveButton" zone="2">Zone 2</button>
		<button id="lane3" class="moveButton" zone="3">Zone 3</button>
		<button id="lane4" class="moveButton" zone="4">Zone 4</button>
		<button id="lane5" class="moveButton" zone="5">Zone 5</button>

		</form>

	</body>
</html>