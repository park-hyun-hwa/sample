<?php
$re=exec("sudo python ../test/sht20.py");
$div=explode("temp:",$re);
$value=explode("humi:",$div);
echo ("Time=".date("Y-m-d H:i:s").);
echo ("Temperature=".value[0].);
echo("Humidity=".value[1].);
?>
