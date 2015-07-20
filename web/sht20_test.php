<?php
$re=exec("sudo cat /home/pi/hyunhwa/workspace/test/sht20_data.txt");
$div=explode("temp:",$re);
$value=explode("humi:",$div[1]);
echo ("Time=".date("Y-m-d H:i:s").);
echo ("Temperature=".$value[0].);
echo("Humidity=".$value[1].);
?>
