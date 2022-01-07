<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class CrossGameController extends CI_Controller 
{
    const LR_STYLE = "styles\LoginRegister.css";
    const CA_STYLE = "styles\ClientArea.css";

    function __construct()
    {
        parent::__construct();
        
        $this->load->library("layouts.php");
	
        $this->load->model("CrossGameModel", "CrossGameModel");
        
        session_start();
    }

    public function index()
	{        
        $this->client_area("account");
	}

    public function computer_info()
    {
        if (isset($_POST["computer_info"]))
            $this->client_area("computer_info", $this->CrossGameModel->GetComputerInfo($_POST["computer_info"]));
        elseif (isset($_POST["change_computer"]))
        {
            $this->CrossGameModel->SetComputerInfo($_POST["change_computer"], $_POST["name"], $_POST["tcp"], $_POST["udp"], $_POST["max_connections"], $_POST["fps"]);
            header("Location: " . htmlspecialchars("./computers"));
        }
        else
            header("Location: " . htmlspecialchars("./computers"));
    }

    public function computers()
    {
        $this->client_area("computers");
    }

    public function friend_info()
    {
        if (isset($_POST["friend_info"]))
            $this->client_area("friend_info", $this->CrossGameModel->GetFriendSharedComputers($_POST["friend_info"]));
        elseif (isset($_POST["change_shared"]))
        {
            $shared = array();
            foreach ($_POST as $input_name => $key)
                if ($input_name != "change_shared")
                    array_push($shared, $input_name);
            
            foreach ($this->CrossGameModel->GetMyComputers($_SESSION["user"][1]) as $computer)
                $this->CrossGameModel->ShareComputer($_POST["change_shared"], $computer["MAC"], in_array($computer["MAC"], $shared));
            
            header("Location: " . htmlspecialchars("./friends"));
        }
        else
            header("Location: " . htmlspecialchars("./friends"));
    }

    public function friends()
    {
        $this->client_area("friends");
    }

    public function logout()
    {
        $this->CrossGameModel->Logout($_SESSION["user"][1]);
        session_destroy();
        header("Location: " . htmlspecialchars("./login"));
    }

	public function login()
	{
        if (isset($_SESSION["user"]))
            header("Location: " . htmlspecialchars(dirname($_SERVER["PHP_SELF"], 1)));

        $error_code = 0;

        if (isset($_POST["login"]))
        {			
            $error_code = $this->CrossGameModel->CheckLogin($_POST["username"], $_POST["password"]);
            if ($error_code > 1)
            {
                $error_code -= 5;
                $_SESSION["user"] = array($_POST["username"], $error_code);
                header("Location: " . htmlspecialchars(dirname($_SERVER["PHP_SELF"], 1)));
            }
        }
        if ($error_code != -1)
            $this->load->view("LoginRegister.php", array(
                "error_code" => $error_code,
                "title" => "Cross Game - Login",
                "style" => self::LR_STYLE
            ));
        else
            echo "No se ha obtenido respuesta de la base de datos";
	}

    public function search_users()
    {
        $this->client_area("search_users", $this->CrossGameModel->SearchFriends($_POST["pattern"], $_SESSION["user"][1]));
    }

	public function register()
	{
        if (isset($_SESSION["user"]))
            header("Location: " . htmlspecialchars(dirname($_SERVER["PHP_SELF"], 1)));

        $error_code = 0;
    
        if (isset($_POST["register"]))
        {			
            $error_code = $this->CrossGameModel->AddUser($_POST["username"], $_POST["name"], $_POST["password"]);
            if ($error_code > 5)
            {
                $error_code -= 5;
                $_SESSION["user"] = array($_POST["username"], $error_code);
                header("Location: " . htmlspecialchars(dirname($_SERVER["PHP_SELF"], 1)));
            }
        }
        
        if ($error_code != -1)$this->load->view("LoginRegister.php", array(
            "error_code" => $error_code,
            "title" => "Cross Game - Register",
            "style" => self::LR_STYLE
        ));
        else
            echo "No se ha obtenido respuesta de la base de datos";
	}

    public function recover()
    {
        $this->load->view('recover');
    }

    public function client_area($submenu, $info = null)
    {
        if (isset($_SESSION["user"]))
        {
            $user = $this->CrossGameModel->GetFormatedName($_SESSION["user"][1]);
            $data = array
            (
                "submenu" => $submenu,
                "user" => explode("#", $user)[0],
                "my_computers" => $this->CrossGameModel->GetMyComputers($_SESSION["user"][1]),
                "other_computers" => $this->CrossGameModel->GetOtherComputers($_SESSION["user"][1]),
                "friends" => $this->CrossGameModel->GetFriends($_SESSION["user"][1]),
                "header" => $this->load->view("header.php", array("user" => $user), TRUE),
                "sidebar" =>  $this->load->view("sidebar.php", array("submenu" => $submenu), TRUE),
                "footer" =>  $this->load->view("footer.php", "", TRUE),
                "info" => $info
            );
            
            $this->view("client_area.php", $data, "ClientArea.php", "Panel de control - Cross Game", self::CA_STYLE);
        }
        else
            header("Location: " . "login");
    }

    function view($view, $params, $layout, $title, $style)
    {
		$this->layouts->view(array(
            "view" => $view,
            "params" => $params,
            "layout" => $layout,
            "title" => $title,
            "style" => $style
        ));
    }
}
