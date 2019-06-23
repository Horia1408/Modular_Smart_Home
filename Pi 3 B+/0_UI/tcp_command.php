 <?php
 	$newURL = '/relays.php';
    $message = $_GET["name"] . ":" . $_GET["value"];
 	//echo $message;

 	$command = 'python /var/fpwork/hcostina/Licenta/client.py ' . $_GET["ip"] . ' ' . $message;
	$last_line = system($command, $retval);
	echo $retval;

	header('Location: ' . $newURL);
 ?>