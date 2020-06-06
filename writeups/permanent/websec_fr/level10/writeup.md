# level 10
## Source files  
source.php
```php
<?php include "flag.php"; ?>

<!DOCTYPE html>
<html>
<head>
    <title>#WebSec Level Ten</title>
    <link rel="stylesheet" href="../static/bootstrap.min.css"/>
</head>
<body>
<div id="main">
    <div class="container">
        <div class="row">
            <h1>LevelTen<small> - Awesome File Downloader.</small></h1>
        </div>
        <div class="row">
            <p class="lead">
        Here we have a <a href="source.php">cool file downloader</a>. It allows you to download arbitrary files, even <mark>flag.php</mark>,
        as long as it's a legit request!<br>
                Thanks to an <mark>anonymous contributor</mark> for this challenge.
            </p>
        </div>
    </div>
    <div class="container">
        <div class="row">
            <form name="username" method="post" class="form-inline">
                    <div class="form-group">
                        <label for="f">File</label>
                        <span class='text-success'></span>
                        <input type="text" class="form-control" required id="f" value="index.php" name="f">
                    </div>
                    <div class="form-group">
                        <label for="hash">Secret hash</label>
            <input type="text" class="form-control" required id="hash" value="<?php echo substr (md5 ($flag . 'index.php' . $flag), 0, 8); ?>" name="hash" >
                    </div>
                <button type="submit" class="btn btn-default">Get!</button>
            </form>
        </div>
        <?php
        if (isset ($_REQUEST['f']) && isset ($_REQUEST['hash'])) {
            $file = $_REQUEST['f'];
            $request = $_REQUEST['hash'];

            $hash = substr (md5 ($flag . $file . $flag), 0, 8);

            echo '<div class="row"><br><pre>';
            if ($request == $hash) {
            show_source ($file);
            } else {
            echo 'Permission denied!';
            }
            echo '</pre></div>';
        }
        ?>
    </div>
</div>
<link rel="stylesheet" href="../static/bootstrap.min.js"/>
</body>
</html>
```  
## Writeup  
The key point is loose comparison `==` used for hash validation. In loose comparison, if its left side or right side is a string which starts from `0e` followed by digit characters, it is treated as an exponential number `pow(0, digit_character_string)`, that is `0`. So, when both sides of loose comparison `==` are expressed like `0e[0-9]+`, they are different strings, but treated as same value because both of them are treated as a number 0.  
Okay, let's try to get the flag. First, set loose comparison's left side `$_REQUEST['hash']` to `0e1`, that is 0. Then, varying the amount of slashes, set `$_REQUEST['f']` to `./flag.php`. We can not specify the right side `$hash`, but its value is `$hash = substr (md5 ($flag . $file . $flag), 0, 8);`, so we can vary the `$hash` value by changing the number of slashes of $_REQUEST['f']. In this way, the specified path $_REQUEST['f'] is always `./flag.php`, but we can vary the `$hash`. After a lot of attempt, there is a possibility that `$hash` value being string `0e[0-9]`, then we can get the content of flag.php finally.  
`solver.py` is the code to get the flag.