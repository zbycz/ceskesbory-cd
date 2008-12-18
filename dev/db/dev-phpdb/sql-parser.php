


$delimiter = ";";
$offset = 0;
$empty = true;
while (rtrim($query)) {
	if (!$offset && preg_match('~^\\s*DELIMITER\\s+(.+)~i', $query, $match)) {
		$delimiter = preg_quote($match[1], '~');
		$query = substr($query, strlen($match[0]));
	} elseif (preg_match("~$delimiter|['`\"]|/\\*|-- |\$~", $query, $match, PREG_OFFSET_CAPTURE, $offset)) {
		if ($match[0][0] && $match[0][0] != $delimiter) {
			$pattern = ($match[0][0] == "-- " ? '~.*~' : ($match[0][0] == "/*" ? '~.*\\*/~sU' : '~\\G([^\\\\' . $match[0][0] . ']+|\\\\.)*(' . $match[0][0] . '|$)~s'));
			preg_match($pattern, $query, $match, PREG_OFFSET_CAPTURE, $match[0][1] + 1);
			$offset = $match[0][1] + strlen($match[0][0]);
		} else {
			$empty = false;
			echo "<pre class='jush-sql'>" . htmlspecialchars(substr($query, 0, $match[0][1])) . "</pre>\n";
			//! don't allow changing of character_set_results, convert encoding of displayed query
			if (!$mysql->multi_query(substr($query, 0, $match[0][1]))) {
				echo "<p class='error'>" . lang('Error in query') . ": " . htmlspecialchars($mysql->error) . "</p>\n";
			} else {
				do {
					$result = $mysql->store_result();
					if (is_object($result)) {
						select($result);
					} else {
						if (preg_match("~^\\s*(CREATE|DROP)(\\s+|/\\*.*\\*/|-- [^\n]*\n)+DATABASE\\b~sU", $query)) {
							unset($_SESSION["databases"][$_GET["server"]]);
						}
						echo "<p class='message'>" . lang('Query executed OK, %d row(s) affected.', $mysql->affected_rows) . "</p>\n";
					}
				} while ($mysql->next_result());
			}
			$query = substr($query, $match[0][1] + strlen($match[0][0]));
			$offset = 0;
		}
	}
}
if ($empty) {
	echo "<p class='message'>" . lang('No commands to execute.') . "</p>\n";
}
