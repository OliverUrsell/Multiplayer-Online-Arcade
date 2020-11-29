
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
		<link rel="stylesheet" href="frogger.css">
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
		<script type="text/javascript" src="frogger.js"></script>

		<button id="move" class="moveButton">Move Up</button>
		<button id="moveBack" class="moveButton">Move Down</button>

		</form>

	</body>
</html>