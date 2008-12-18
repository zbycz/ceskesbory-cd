<?php


//unlink("ucps.db");

try {
    $dbh = new PDO('sqlite:'.dirname(__FILE__).'/ucps.db');
}catch( PDOException $exception ){
    die($exception->getMessage());
}
$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING );

mysql_connect("localhost","root","") or exit;
mysql_select_db("ucps");

ini_set("max_execution_time", 3600);
mysql_query("SET CHARACTER SET 'utf8'");
header("Content-Type: text/html; charset=utf-8");





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


foreach(array("dopl_char","druhy","katalog_status", "kraje", "zanr","katalog") as $tbl){ 
	
	$resCreate = mysql_query("SHOW CREATE TABLE `$tbl`");
	$cre = mysql_result($resCreate, 0, 1);
	mysql_free_result($resCreate);
	
    foreach($cr_regs as $reg)
        $cre = ereg_replace($reg[0], $reg[1], $cre);
    
    echo $cre;
	$dbh->exec($cre);
	echo "created $tbl<br>";
	
	$resData = mysql_query("SELECT * FROM `$tbl`");
	$num = mysql_num_rows($resData);
    if(mysql_num_rows($resData)){
		while($rr=mysql_fetch_row($resData)){
			array_walk($rr, "eachEscape");
			echo "INSERT INTO `$tbl` VALUES ('" . implode($rr,"','") . "')";
			$dbh->exec("INSERT INTO `$tbl` VALUES ('" . implode($rr,"','") . "')");
			
        }
	}
	mysql_free_result($resData);
	flush();
	
	echo "exported $num lines from $tbl<br>";
}




function eachEscape(&$val, $key){
 	$val = str_replace(array("'","\n", "\\"), array("''","\\n", "\\\\"), str_replace("\r\n", "\n", $val));
}
function eachHtmlspec(&$val, $key){$val = htmlspecialchars($val,ENT_NOQUOTES);}

