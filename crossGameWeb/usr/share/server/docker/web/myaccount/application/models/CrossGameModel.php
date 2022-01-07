<?php

if (!defined("BASEPATH")) exit("No direct script access allowed");

class CrossGameModel extends CI_Model
{
    private $db = null;

    function __construct()
    {
        parent::__construct();
        $this->db = $this->load->database("crossgame", true);
    }

	public function GetFormatedName($user_id)
	{
		$result = $this->Query(
			"SELECT name, number 
			 FROM users 
			 WHERE user_id =" . intval($user_id)
		);
		return $result[0]["name"] . "#" . $result[0]["number"];
	}

	public function GetMyComputers($user_id)
	{
		return $this->Query(
			"SELECT MAC, LocalIP, PublicIP, name, status, max_connections, n_connections
			 FROM computers
			 WHERE owner = $user_id"
		);
	}

	public function GetComputerInfo($computer_id)
	{
		return $this->Query(
			"SELECT name, TCP, UDP, max_connections, FPS
			 FROM computers
			 WHERE MAC = '$computer_id'"
		);
	}

	public function SetComputerInfo($MAC, $name, $TCP, $UDP, $max_connections, $FPS)
	{
		$this->Query(
			"UPDATE computers
			 SET name = '$name',
			 	 TCP = $TCP,
				 UDP = $UDP,
				 max_connections = $max_connections,
				 FPS = $FPS
			 WHERE MAC = '$MAC'");
	}

	public function GetOtherComputers($user_id)
	{
		return $this->Query(
			"SELECT name, status, max_connections, n_connections, accepted, revoke_permission
			 FROM users_computers INNER JOIN computers
			 ON users_computers.computer_id = computers.MAC
			 WHERE user_id = $user_id"
		);
	}

	public function GetFriends($user_id)
	{
		return $this->Query(
			"SELECT *
			 FROM friendlist, users
			 WHERE (user1 = user_id AND user2 = $user_id)
			 OR (user2 = user_id AND user1 = $user_id)"
		);
	}

	public function GetFriendSharedComputers($friend_id)
	{
		return $this->Query(
			"SELECT MAC
			 FROM computers			 
			 WHERE MAC IN (
				SELECT computer_id
				FROM users_computers
				WHERE user_id = $friend_id
			 )"
		);
	}

	public function ShareComputer($friend_id, $computer_id, $share)
	{
		if ($share)
		{
			if (count($this->Query("SELECT * FROM users_computers WHERE user_id = $friend_id AND computer_id = '$computer_id'")) == 0)
				$this->Query("INSERT INTO users_computers VALUES ($friend_id, '$computer_id', 1, NULL)");
		}
		else
			if (count($this->Query("SELECT * FROM users_computers WHERE user_id = $friend_id AND computer_id = '$computer_id'")) > 0)
				$this->Query("DELETE FROM users_computers WHERe user_id = $friend_id AND computer_id = '$computer_id'");
	}

	public function SearchFriends($pattern, $user)
	{
		return $this->Query(
			"SELECT user_id, name , number 
			 FROM users 
			 WHERE name LIKE '%$pattern%'
			 AND user_id != $user
			 AND user_id NOT IN (
			 	 SELECT user1
				 FROM friendlist
				 WHERE user2 = $user)
			 AND user_id NOT IN (
			 	 SELECT user2
				 FROM friendlist
				 WHERE user1 = $user)");
	}
	
	public function GetReceivedFriendRequests($user_id)
	{
		return $this->Query(
			"SELECT name, number
			 FROM friendlist, users
			 WHERE (status = 1 AND user1 = $user_id AND user2 = user_id)
			 OR (status = 2 AND user2 = $user_id AND user1 = user_id)"
		);
	}

	public function GetSendedFriendRequests($user_id)
	{
		return $this->Query(
			"SELECT name, number
			 FROM friendlist, users
			 WHERE (status = 1 AND user1 = $user_id AND user2 = user_id)
			 OR (status = 2 AND user2 = $user_id AND user1 = user_id)"
		);
	}

    public function CheckLogin($email, $password)
	{
		$error_code = 1;
		if ($this->IsValidPassword($password) && $this->IsValidEMail($email))
		{
			try
			{
				$sha256_pass = hash("sha256", $password);
				$result = $this->Query(
					"SELECT user_id 
					 FROM users 
					 WHERE email = '$email' AND password = '$sha256_pass'"
				);
				if (count($result) > 0)
				{
					$user_id = $result[0]["user_id"];
					$error_code = $user_id + 5;
					$this->Login($user_id);
				}
			}
			catch (ErrorException $e)
			{
				$error_code = -1;
			}
		}
		
		return $error_code;
	}
	
	public function AddUser($email, $username, $password)
	{
		$error_code = 0;
		if ($this->IsValidEMail($email))
			if ($this->IsValidUserName($username))
				if ($this->IsValidPassword($password))
					try
					{				
						if (count($this->Query("SELECT user_id FROM users WHERE email = '$email'")) == 0)
						{
							$user_ID = $this->GenerateNextUserID();
							$number = $this->GenerateRandomUserNumber();
							$sha256_pass = hash("sha256", $password);
							if ($this->Query("INSERT INTO users VALUES ('$user_ID', '$username', '$number', '$email', '$sha256_pass', 1)"))
								$error_code = $user_ID + 5;
							else
								$error_code = 5;
						}
						else
							$error_code = 4;
					}
					catch (ErrorException $e)
					{
						$error_code = -1;
					}
				else
					$error_code = 3;
			else
				$error_code = 2;
		else
			$error_code = 1;
		
		return $error_code;
	}
	
	public function DeleteUser($email, $password)
	{
		$error_code = 0;
		if (CheckLogin($email, $password) > 1)
			try
			{
				$conn = DatabaseConnect();		
				if (!$conn->query("DELETE FROM users WHERE email = '" . $email . "')"))
					$error_code = 5;
				mysqli_close($conn);
			}
			catch (ErrorException $e)
			{
				$error_code = -1;
			}
		
		return $error_code;
	}
    
    function Query($sql)
    {
        $query = $this->db->query($sql);
		try
		{
			$rows = $query->result_array();
			$query->free_result();
			return ($rows);
		}
		catch (Error $e)
		{
			return $query;
		}
    }

	function Login($user_id)
	{
		$this->Query("UPDATE users SET status = 1 WHERE user_id = " . intval($user_id));
	}

	function Logout($user_id)
	{
		$this->Query("UPDATE users SET status = 0 WHERE user_id = " . intval($user_id));
	}

	function GenerateRandomUserNumber()
	{
		return rand(1000, 9999);
	}

    function GenerateNextUserID()
	{
		$last_id = $this->Query("SELECT MAX(user_id) as last_id FROM users")[0]["last_id"] ?? 1;
		if ($last_id < 1)
			$last_id = 1;
		return $last_id + 1;
	}
	
	function IsValidEMail($email)
	{
		return preg_match("/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/", $email);
	}
	
	function IsValidPassword($password)
	{
		return preg_match("/^.{6,30}$/", $password);
	}
	
	function IsValidUserName($username)
	{
		return preg_match("/^[A-Z0-9]{4,30}$/i", $username);
	}
}
?>