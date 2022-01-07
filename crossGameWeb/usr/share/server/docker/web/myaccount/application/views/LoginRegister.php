<!DOCTYPE html>
<html>
	<head>
		<title><?php echo $title; ?></title>
		<link rel="stylesheet" type="text/css" href="<?php echo $style; ?>"/>
        <link rel="icon" href="media/medium.png" type="image/png"/>
	</head>
	<body>
	<div class="background-video-container">
	<?php 
        require_once "application/helpers/LoginRegisterHelper.php";

        $isLogin = strpos($title, "Login");

        $video = "media/video.mp4";        
        if (file_exists($video)):
    ?>
        <video class="background-video" muted autoplay loop>
            <source src="<?php echo $video; ?>" type="video/mp4">
            <img class="background-video" src="https://narkocentr.com/sites/default/files/camps/god_of_war_ps4-wallpaper-1920x1080.jpg"/>
        </video>
    <?php else: ?>
        <img class="background-video" src="https://narkocentr.com/sites/default/files/camps/god_of_war_ps4-wallpaper-1920x1080.jpg"/>
    <?php endif; ?>
	</div>
	<div class="background-video-overlay">
        <div class="form-container">
            <a href="http://crossgame.sytes.net/">
                <img class="cross-game-logo" src="http://crossgame.sytes.net/wp-content/uploads/2021/04/CrossGame-1.png"/>
            </a>
            <div id="login" style="display:<?php echo $isLogin ? "block" : "none"; ?>;">	
                <h3>¡Hola de nuevo!</h3>
                <form method="post" class="<?php if ($error_code == 1) echo "error-form"; ?>">
                    <p>CORREO ELECTRÓNICO <?php if ($error_code == 1) echo GetErrorMsg(0); ?></p>
                    <input type="text" name="username" value="<?php echo isset($_POST["username"]) ? $_POST["username"] : ""; ?>" required/>
                    <p>CONTRASEÑA <?php if ($error_code == 1) echo GetErrorMsg(0); ?></p>
                    <input type="password" name="password" value="<?php echo isset($_POST["password"]) ? $_POST["password"] : ""; ?>" required/><br/>
                    <a href="./forgot-password">¿Has olvidado la contraseña?</a><br/><br/>
                    <div class="blue custom_button">
                        Iniciar sesión
                        <input type="submit" name="login" class="button"/>
                    </div>
                </form>
                <p>¿Todavía no tienes una cuenta? <a onclick="Swap('register')">Regístrate</a></p>
            </div>
            <div id="register" style="display:<?php echo $isLogin ? "none" : "block"; ?>;">	
                <h3>Crear una cuenta</h3>
                <form method="post">
                    <div class="<?php if ($error_code == 1 || $error_code == 4) echo "error-form"; ?>">
                        <p>CORREO ELECTRÓNICO <?php if ($error_code == 1 || $error_code == 4) echo GetErrorMsg($error_code); else echo "(Ahora con 100% menos de spam)" ?></p>
                        <input type="text" name="username" value="<?php echo isset($_POST["username"]) ? $_POST["username"] : ""; ?>" required oninvalid="this.setCustomValidity('Casi se te olvida poner el correo.')" oninput="this.setCustomValidity('')"/>
                    </div>
                    <div class="<?php if ($error_code == 2) echo "error-form"; ?>">
                        <p>NOMBRE DE USUARIO <?php if ($error_code == 2) echo GetErrorMsg($error_code); ?></p>
                        <input type="text" name="name" value="<?php echo isset($_POST["name"]) ? $_POST["name"] : ""; ?>" required oninvalid="this.setCustomValidity('Necesitas un nombre para poder encontrar a tus amigos.')" oninput="this.setCustomValidity('')"/>
                    </div>
                    <div class="<?php if ($error_code == 3) echo "error-form"; ?>">
                        <p>CONTRASEÑA <?php if ($error_code == 3) echo GetErrorMsg($error_code); ?></p>
                        <input type="password" name="password" value="<?php echo isset($_POST["password"]) ? $_POST["password"] : ""; ?>" required  oninvalid="this.setCustomValidity('Este campo también tienes que rellenarlo.')" oninput="this.setCustomValidity('')"/><br/><br/>
                    </div>
                    <div class="blue custom_button">
                        Registrarse
                        <input type="submit" name="register" class="button"/>
                    </div>
                </form>
                <p>¿Ya tienes una cuenta? <a onclick="Swap('login')">Inicia sesión</a></p>
            </div>
        </div>
	</div>    
    <script src="js/common.js"></script>
    <script src="js/login_register.js"></script>
  </body>
</html>