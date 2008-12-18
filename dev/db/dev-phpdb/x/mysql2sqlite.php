<?php



$cr_regs = array(
    array("[^\n]* KEY [^\n]*", ""),
    array(" unsigned ", " "),
    array(" (NOT )?NULL", ""),
    array(" auto_increment", " primary key autoincrement"),
    array(" (tiny|small)?int\([0-9]*\) ", " integer "),
    array(" default( '[^']*')?", " "),
    array(" character set [^ ]* ", " "),
    array(" enum([^)]*) ", " varchar(255) "),
    array(" on update [^,]*", ""),
    array(",[^,)]*)[^)]*$", "\n)"),
);

$cre = file_get_contents("import.mysql");

foreach($cr_regs as $reg)
    $cre = ereg_replace($reg[0], $reg[1], $cre);

file_put_contents("import.sqlite", $cre);

echo "ok";

