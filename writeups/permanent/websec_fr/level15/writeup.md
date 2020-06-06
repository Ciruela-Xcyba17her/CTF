# level15
## Source codes  
source.php
```php
 <?php
ini_set('display_errors', 'on');
ini_set('error_reporting', E_ALL);

$success = '
<div class="alert alert-success alert-dismissible" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
    Function declared.
</div>
';

include "flag.php";

if (isset ($_POST['c']) && !empty ($_POST['c'])) {
    $fun = create_function('$flag', $_POST['c']);
    print($success);
    //fun($flag);
    if (isset($_POST['q']) && $_POST['q'] == 'checked') {
        die();
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>#WebSec Level Fifteen</title>
    <link rel="stylesheet" href="/static/bootstrap.min.css" />
    <!-- Thanks for kpcyrd for the idea. -->
</head>
    <body>
        <div id="main">
            <div class="container">
                    <div class="row">
                        <h1>LevelFifteen <small>Arbitrary code non-execution</small></h1>
                    </div>
                    <div class="row">
                        <p class="lead">
                            You can provide us some PHP code, but we won't execute it, <a href="./source.php">check by yourself</a>.
                        </p>
                    </div>
                </div>
            </div>
            <div class="container">
                    <div class="row">
                        <form method="post" class="form-inline">
                            <div class="form-group">
                                <input type="text" class="form-control" id="c" name="c" placeholder="echo 1337;" required>
                            </div>
                            <div class="checkbox">
                                <label>
                                    <input type="checkbox" class="form-control" id="q" name="q" value="1"> Exit after declaration
                                </label>
                            </div>
                            <input type="submit" class="form-control btn btn-default" name="submit">
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
    <script src="/static/jquery.js" defer type="text/javascript"></script>
    <script src="/static/bootstrap.min.js" defer type="text/javascript"></script>
</html>

```
## Writeup
### Vulnerability  
`create_function()` is introduced in [manual](https://www.php.net/manual/en/function.create-function.php) like this:

>  This function internally performs an eval() and as such has the same security issues as eval(). Additionally it has bad performance and memory usage characteristics.
> If you are using PHP 5.3.0 or newer a native anonymous function should be used instead.  

It says create_function() uses `eval()`. eval(string $code) is a function which executes $code, and often leads to arbitrary code execution.  
According to this [page](https://www.securityfocus.com/archive/1/496728), create_function() uses eval() to create an anonymous function.
```php
function create_function($args, $code) {
  eval("
    function lambda_1 ($args) { $code }
  ");
  return 'lambda_1';
}
```
We can use this eval() function to execute arbitrary codes.

### Arbitrary code execution
Let's try to execute arbitrary codes. According to source.php, `$args` is always `$flag`.  
When we set $code to `}; echo $flag; //`, then `eval(" function lambda_1 ($flag) { }; echo $flag; // } ");` will be executed. The code in eval() first defines an anonymous function which has no codes, then executes `echo $flag`. We can get the flag by the output of echo.  

### Other solutions  
1. Overwrite $success  
`}; $success = $flag; //`
2. Show "flag.php"  
`}; show_source("flag.php"); //`