<?php
if($_POST['action']=='run_python'){
  $f = $_POST['arg1'];
  $k = $_POST['arg2'];
  $File = fopen("t2.txt", 'a');
  fwrite($File, "hi\n");
  fwrite($File, "$f\n$k\n");

  $cmd = escapeshellcmd("/usr/bin/python3 /var/www/html/testpy.py"); 
  $out = shell_exec($cmd);
  
  shell_exec("/usr/bin/python3 /var/www/html/testpy.py $f $k >> shellout.txt");

  shell_exec("/usr/bin/python3 /var/www/html/a.py $f $k >> debug.txt");
  fwrite($File, "bye\n");
  fclose($File);
$output = "Optimization process has been completed, please click OK to receive download link";
echo $output;
}
?> 




