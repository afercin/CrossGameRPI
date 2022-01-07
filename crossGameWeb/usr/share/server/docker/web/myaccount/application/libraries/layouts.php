<?php

if (!defined("BASEPATH")) exit("No direct script access allowed");

class layouts
{
    private $CI = null;

    function __construct()
    {
        $this->CI =& get_instance();
    }
    
    public function view($data = array())
    {
        $view_content = $this->CI->load->view($data["view"], $data["params"], TRUE);

        $this->CI->load->view("layouts/" . $data["layout"], array(
            "content" => $view_content,
            "title" => $data["title"],
            "style" => $data["style"]
        ));
    }
}
?>