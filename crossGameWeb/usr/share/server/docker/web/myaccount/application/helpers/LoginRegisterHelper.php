<?php	 
	function GetErrorMsg($error_number)
	{
		$errorMsg = "";
		switch ($error_number)
		{
			case 0: $errorMsg = "<span> - El correo electrónico o la contraseña no son válidos.</span>"; break;
			case 1: $errorMsg = "<span> - El formato del correo electrónico no es válido.</span>"; break;
			case 2: $errorMsg = "<span> - El nombre de usuario no puede contener caracteres especiales y su longitud debe de tener entre 3 y 20 caracteres.</span>"; break;
			case 3: $errorMsg = "<span> - La longitud de la contraseña debe de ser entre 6 y 30 caracteres.</span>"; break;
			case 4: $errorMsg = "<span> - El correo electrónico introducido ya tiene un usuario asociado.</span>"; break;
			case 5: $errorMsg = "<span> - Error interno del servidor, por favor vuelva a intentarlo en unos instantes.</span>"; break;
		}
		return $errorMsg;
	}
?>