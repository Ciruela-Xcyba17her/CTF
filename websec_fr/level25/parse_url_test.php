<?php

// the last case is not effective on my environment...
$uris = array(
    '/index.php?page=flag',
    '///level25/index.php?page=flag',
    '////////level25/index.php?page=flag',
    '//websec.fr/level25/index.php?XXX=XXX:80/XXX&page=flag',
);

foreach($urls as $url){
    echo '--- parse_url('.$url.') ---'."\n";
    var_dump(parse_url($url)['query']);
}

?>