<?php
    include_once 'db.php';
    $message='';
    if (isset($_POST['VIN'])) {
        $VIN = $_POST['VIN'];
        $trademark = $_POST['trademark'];
        $year = $_POST['year'];
        $odometer = $_POST['odometer'];
        $description = $_POST['description'];
        $file = '';
        // if (move_uploaded_file($_FILES['file']['tmp_name'], destination: 'files/' . basename($_FILES['file']['name']))){
        //     $file =  basename($_FILES['file']['name']);
        $uploads_dir = '/uploads';
        foreach ($_FILES["pictures"]["error"] as $key => $error) {
            if ($error == UPLOAD_ERR_OK) {
                $tmp_name = $_FILES["pictures"]["tmp_name"][$key];
                $name = $_FILES["pictures"]["name"][$key];
                move_uploaded_file($tmp_name, "$uploads_dir/$name");
            }
        }
        $db -> query(statement:"INSERT IGNORE INTO contact ('название полей дб') 
                VALUES('{$VIN}', '{$trademark}', '{$year}', '{$odometer}', '{$description}', '{$file}')");

        $message='Форма отправлена';
    }
?>
<!DOCTYPE HTML>
<html lang="ru">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="stylesheet" href="style.css">
    <title>Отправка отчета</title>
</head>
<body>
    <?php
        if(!empty($message)) { ?>
            <div class="alert_success> <?php echo $message; ?> </div>
        <?php }; ?>
<form enctype="multipart/form-data" method="post" id="feedback-form">
    <label for="VIN">VIN code:</label>
    <input type="text" name="VIN" id="VIN" required placeholder="например, 1KLBN52TWXM186109"  class="w100 border">
    
    <label for="trademark">Марка/модель:</label>
    <input type="text" name="trademark" id="trademark" required placeholder="например, BMW M5"  class="w100 border">
    
    <label for="year">Год выпуска:</label>
    <input type="text" name="year" id="year" required placeholder="например, 2007"  class="w100 border">
    
    <label for="odometer">Пробег:</label>
    <input type="text" name="odometer" id="odometer" required placeholder="например, 21378"  class="w100 border">
    
    <label for="description">Описание:</label>
    <textarea name="description" id="description" required rows="5" placeholder="Описание автомобиля…" class="w100 border"></textarea>
    
    <label for="fileFF">Прикрепить файл:</label>
    <input type="file" name="fileFF[]" multiple id="fileFF" class="w100">
    
    <br>
    <input value="Отправить" type="submit" id="submitFF">
    </form>
</body>
</html>

<?php

