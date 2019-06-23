<?php
	$commandKill = 'sudo reboot';
	$last_lineKill = system($commandKill, $retvalKill);
	echo $retvalKill . "\n";
?>