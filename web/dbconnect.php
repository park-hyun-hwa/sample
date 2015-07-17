<?php

$mysql_hostname = "10.255.252.132";

$mysql_user = "root";

$mysql_password = "tinyos";

$mysql_database = "keti";

$bd = mysql_connect($mysql_hostname, $mysql_user, $mysql_password) or die("db connect error");

mysql_select_db($mysql_database, $bd) or die("db connect error");


?>
