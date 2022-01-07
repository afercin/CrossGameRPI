<?php
    function printBorder($name, $svg, $status, $id = -1, $n_connections = -1, $max_connections = -1)
    {
        $type = $max_connections != -1 ? "computer" : "friend";
        $form = $id != -1 && ($type == "friend" || $status < 1);
        switch ($status)
        {
            case 0: $status = "disconnected"; break;
            case 1: $status = "connected"; break;
            case 2: $status = "playing"; break;
            case 3: $status = "busy"; break;
        }
        if ($form)
        {
            ?>
            <form action="./<?php echo $type; ?>_info" method="post">
            <?php
        }
        ?>
        <div class="border custom_button <?php echo $status; ?>">
            <p><?php echo $name; ?></p>
            <svg><use xlink:href="#<? echo $svg; ?>"/></svg>
            <?php if ($n_connections != -1 && $status != "disconnected") echo "<h5>$n_connections/$max_connections</h5>"; ?>
            <input type="submit" name="<?php echo $type; ?>_info" value="<?php echo $id; ?>" class="button"/>
        </div>
        <?php
        if ($form)
            echo "</form>";
    }
    function printSearch()
    {
    ?>
        <form class="search" action="./search_users" method="post">
            <input type="text" name="pattern">
                <div class="custom_button">
                    <svg><use xlink:href="#search"/></svg>
                    <input class="button" type="submit" name="search"/>
                </div>
            </input>
        </form>
    <?php
    }
    function printFriend($name, $number, $action)
    {
    ?>
        <form class="friend" method="post">
            <p><?php echo "$name#$number"; ?></p>
            <div class="<?php echo $action; ?> custom_button">
                <svg><use xlink:href="#<?php echo $action; ?>"/></svg>
                <input class=" button" type="submit" name="friend" value="<?php echo $action; ?>"/>
            </div>
        </form>
    <?php
    }
?>
<div id="account" style="display: <?php echo $submenu == "account" ? "block" : "none"; ?>;">
    <form method="post">
        <table>
            <tr><td colspan="2">Correo electrónico:</td></tr>
            <tr>
                <td><input type="text" name="email" value="<?php echo $_SESSION["user"][0]; ?>"/></td>            
                <td>
                    <div class="white custom_button">
                        Guardar Cambios
                        <input type="submit" name="change-email" class="button"/>
                    </div>
                </td>
            </tr>
        </table>
        <hr/>
        <table>
            <tr><td colspan="2">Nombre de usuario:</td></tr>
            <tr>
                <td><input type="text" name="name" value="<?php echo $user; ?>"/></td>            
                <td>
                    <div class="white custom_button">
                        Guardar Cambios
                        <input type="submit" name="change-username" class="button"/>
                    </div>
                </td>
            </tr>
        </table>
        <hr/>
        <table>
            <tr>
                <td>Antigua contraseña:</td>
                <td>Nueva contraseña:</td>
                <td>Repetir contraseña:</td>
            </tr>
            <tr>
                <td><input type="password" name="old-password"></td>
                <td><input type="password" name="new-password"></td>
                <td><input type="password" name="renew-password"></td>
                <td>
                    <div class="white custom_button">
                        Guardar Cambios
                        <input type="submit" name="change-password" class="button"/>
                    </div>
                </td>
            </tr>
        </table>    
    </form>
</div>
<div id="computers" style="display: <?php echo $submenu == "computers" ? "block" : "none"; ?>;">
    <h2>Mis ordenadores</h2>
    <div class="container">
        <?php
            if (count($my_computers) > 0)
                foreach ($my_computers as $computer)
                {
                    switch ($computer["status"])
                    {
                        case 0: $status = 0; break;
                        case 1: 
                            if ($computer["n_connections"] == 0)
                                $status = 1;
                            elseif ($computer["n_connections"] == $computer["max_connections"])
                                $status = 3;
                            else
                                $status = 2;
                    }
                    printBorder($computer["name"], "screen", $status, $computer["MAC"], $computer["n_connections"], $computer["max_connections"]);
                }
            else
                echo "<p>Actualmente no tienes registrado ningun ordenador en tu cuenta.</p>";
        ?>
    </div>
    <hr/>
    <h2>Ordenadores compartidos conmigo</h2>
    <div class="container">
        <?php
            if (count($other_computers) > 0)
                foreach ($other_computers as $computer)
                {
                    switch ($computer["status"])
                    {
                        case 0: $status = 0; break;
                        case 1: 
                            if ($computer["n_connections"] == 0)
                                $status = 1;
                            elseif ($computer["n_connections"] == $computer["max_connections"])
                                $status = 3;
                            else
                                $status = 2;
                    }
                    printBorder($computer["name"], "screen", $status, -1, $computer["n_connections"], $computer["max_connections"]);
                }
            else
                echo "<p>Actualmente no te estan compartiendo ningún ordenador.</p>";
        ?>
    </div>
</div>
<div id="friends" style="display: <?php echo $submenu == "friends" ? "block" : "none"; ?>;">
    <?php
        printSearch();
        $amigos = $peticiones_entrantes = $peticiones_salientes = array();
        foreach ($friends as $friend)
        {
            $values = array(
                "name" => $friend["name"] . "#" . $friend["number"],
                "status" => $friend["status"],
                "id" => $friend["user_id"]
            );
            switch ($friend["accepted"])
            {
                case 0: array_push($amigos, $values);; break;
                case 1: 
                    if ($friends["user1"] == $_SESSIOM["user"][1])
                        array_push($peticiones_salientes, $values);
                    else
                        array_push($peticiones_entrantes, $values);
                    break;
            }
        }
        echo "<h2>Mis amigos</h2>";
        echo "<div class='container'>";
        if (count($amigos) > 0)
            foreach ($amigos as $amigo)
                printBorder($amigo["name"], "group", $amigo["status"], $amigo["id"]);
        else 
            echo "<p>Que triste, no tienes amigos</p>";

        echo "</div>";
        echo "<hr/>";

        echo "<h2>Peticiones entrantes</h2>";
        echo "<div class='container'>";
        if (count($peticiones_entrantes) > 0)
        {
            foreach ($peticiones_entrantes as $pe)
            {
                echo "$pe<br/>";
            }
        }
        else 
            echo "<p>Ninguna petición entrante</p>";

        echo "</div>";
        echo "<hr/>";

        echo "<h2>Peticiones realizadas</h2>";
        echo "<div class='container'>";
        if (count($peticiones_salientes) > 0)
        {
            foreach ($peticiones_salientes as $ps)
            {
                echo "$ps<br/>";
            }
        }
        else 
            echo "<p>Ninguna petición en progreso.</p>";
        echo "</div>";
    ?>
</div>
<?php
if ($submenu == "computer_info")
{
?>
    <div id="computer_info" style="display: block;">
        <form method="post">
            <table>
                <tr>
                    <td>Nombre:</td>
                    <td><input type="text" name="name" value="<?php echo $info[0]["name"]?>"/></td>
                </tr>
                <tr>
                    <td>Puerto TCP:</td>
                    <td><input type="number" name="tcp" value="<?php echo $info[0]["TCP"]?>" min="1" max="65535"/></td>
                </tr>
                <tr>
                    <td>Puerto UDP:</td>
                    <td><input type="number" name="udp" value="<?php echo $info[0]["UDP"]?>" min="1" max="65535"/></td>
                </tr>
                <tr>
                    <td>Conexiones máximas:</td>
                    <td><input type="number" name="max_connections" value="<?php echo $info[0]["max_connections"]?>" min="1" max="99"/></td>
                </tr>
                <tr>
                    <td>Cantidad de FPS:</td>
                    <td><input type="number" name="fps" value="<?php echo $info[0]["FPS"]?>" min="15" max="60"/></td>
                </tr>
                <tr>
                    <td colspan="2">
                        <div class="white custom_button" style="width: 100%;">
                            Guardar Cambios
                            <input type="submit" name="change_computer" class="button" value="<?php echo $_POST["computer_info"]; ?>"/>
                        </div>
                    </td>
                </tr>
            </table>            
        </form>
    </div>
<?php
}
elseif ($submenu == "friend_info")
{
?>
    <div id="friend_info" style="display: block;">
        <form method="post">
            <table class="computer_table">
                <tr>
                    <th>Nombre</th>
                    <th>IP local</th>
                    <th>IP pública</th>
                    <th>Compartido</th>
                </tr>
                <?php
                    foreach ($my_computers as $computer)
                    {
                        $checked = false;
                        foreach ($info as $computer_info)
                            if ($computer["MAC"] == $computer_info["MAC"])
                            {
                                $checked = true;
                                break;
                            }                                
                    ?>
                    <tr>
                        <td><?php echo $computer["name"]; ?></td>
                        <td><?php echo $computer["LocalIP"]; ?></td>
                        <td><?php echo $computer["PublicIP"]; ?></td>
                        <td> <input class="center" type="checkbox" name="<?php echo $computer["MAC"]; ?>" <?php echo $checked ? "checked" : ""; ?>/> </td>
                    </tr>
                <?php
                    }
                ?>
                <tr>
                    <td colspan="4">
                        <div class="white custom_button" style="width: 100%;">
                            Guardar Cambios
                            <input type="submit" name="change_shared" class="button" value="<?php echo $_POST["friend_info"]; ?>"/>
                        </div>
                    </td>
                </tr>
            </table>            
        </form>
    </div>
<?php
}
elseif ($submenu == "search_users")
{
?>        
    <div id="search_users" style="display: block;">
        <?php printSearch(); ?>
        <h2>Resultados de la búsqueda <?php echo "\"" . $_POST["pattern"] . "\""; ?></h2>
    <?php
        foreach ($info as $friend)
            printFriend($friend["name"], $friend["number"], "add")
    ?>
    </div>
<?php
}
?>