# level 17  
## Source files  
source.php  
```php
<?php
include "flag.php";

function sleep_rand() { /* I wish php5 had random_int() */
        $range = 100000;
        $bytes = (int) (log($range, 2) / 8) + 1;
        do {  /* Side effect: more random cpu cycles wasted ;) */
            $rnd = hexdec(bin2hex(openssl_random_pseudo_bytes($bytes)));
        } while ($rnd >= $range);
        usleep($rnd);
}
?>
<!DOCTYPE html>
<html>
<head>
        <title>#WebSec Level Seventeen</title>
        <link rel="stylesheet" href="../static/bootstrap.min.css" />
    <meta http-equiv="content-type" content="text/html;charset=UTF-16">
</head>
        <body>
                <div id="main">
                        <div class="container">
                                <div class="row">
                                        <h1>Level Seventeen <small> - Guessing is fun!</small></h1>
                                </div>
                                <div class="row">
                                        <p class="lead">
                    Can you guess the flag?  You can check the sources <a href="source.php">here</a>.
                                        </p>
                                </div>
                        </div>
                        <div class="container">
                            <div class="row">
                                <form class="form-inline" method='post'>
                                    <input name='flag' class='form-control' type='text' placeholder='Guessed flag'>
                                    <input class="form-control btn btn-default" name="submit" value='Go' type='submit'>
                                </form>
                            </div>
                        </div>
                        <?php
                        if (isset ($_POST['flag'])):
                            sleep_rand(); /* This makes timing-attack impractical. */
                        ?>
            <br>
                        <div class="container">
                            <div class="row">
                                <?php
                                if (! strcasecmp ($_POST['flag'], $flag))
                                    echo '<div class="alert alert-success">Here is your flag: <mark>' . $flag . '</mark>.</div>';   
                                else
                                    echo '<div class="alert alert-danger">Invalid flag, sorry.</div>';
                                ?>
                            </div>
                        </div>
                        <?php endif ?>
                </div>
        </body>
</html>
```
## Writeup  
This web service uses `strcasecmp()` function to validate flag input. However, if we set array valiable as an argument, it always returns 0, so we can bypass `strcasecmp()` validation by making `flag` valiable an array variable.  
The value of `flag` variable is set through POST request, like `flag=1`. In this way, of course `flag` variable will be a string valiable. But using `flag[]=1` notation, `flag` valiable is treated as an array valiable, and we can bypass the validation.  

`curl -X POST -d 'flag[]=1' http://www.websec.fr/level17/index.php | grep alert`