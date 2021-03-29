<?php

	header("Content-Type: application/json");

	$output = file_get_contents("../data/vehicles.json");

	if(!$output) {
		$output = [
			"error" => "invalid or missing input"
		];
	}

	echo $output;

?>