<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

<form action="http://10.1.0.135/devices/status.php" method="post">
Device(IP:PORT): <input type="text" name="ip">
Community: <input type="text" name="comm">
<input type="submit" value="Add Device">
</form>

<?php

    /* Attempt MySQL server connection. Assuming you are running MySQL

    server with default setting (user 'root' with no password) */

    $link = mysqli_connect("localhost", "root", "sting901", "anm");

     

    // Check connection

    if($link === false){

        die("ERROR: Could not connect. " . mysqli_connect_error());

    }

  //var_dump($_POST);

  if(isset($_POST['ip']) && $_POST['ip'] !='' && $_POST['comm'] && $_POST['comm'] != ''){

    $newdevice  = $_POST['ip'];
    //$splited    = split(":", $newdevice);
    //$ip         = $splited[0];
    //$port       = $splited[1];
    $commun     = $_POST['comm'];

    //echo $newdevice;
    //echo $commun;

    $sql = "DELETE FROM `device` WHERE 1";
    mysqli_query($link, $sql);
    $sql = "INSERT INTO `anm`.`device` (`ip_port`, `community`) VALUES ('".$newdevice."', '".$commun."');";
    mysqli_query($link, $sql); 
  }
    $sql = "SELECT * FROM device";    
    if($result = mysqli_query($link, $sql)){
        
      echo "<h2>Device Information</h2>";

        if(mysqli_num_rows($result) > 0){
            echo "<table class='table table-inverse'>";
                echo "<tr>";
                    echo "<th>Device</th>";
                    echo "<th>Community</th>";
                echo "</tr>";
            while($row = mysqli_fetch_array($result)){
                echo "<tr>";
                    echo "<td>" . $row['ip_port'] . "</td>";
                    echo "<td>" . $row['community'] . "</td>";
                echo "</tr>";
            }
            echo "</table>";
            // Close result set
            mysqli_free_result($result);
        } else{
            echo "No records matching your query were found.";
        }
    } else{
        echo "ERROR: Could not able to execute $sql. " . mysqli_error($link);
    }



    // Attempt select query execution
    echo "<h2>Status of all devices that have reported</h2>";
    $sql = "SELECT * FROM snmptraps";
    if($result = mysqli_query($link, $sql)){
        
        if(mysqli_num_rows($result) > 0){

            echo "<table class='table table-inverse'>";
                echo "<tr>";
                    echo "<th>#</th>";
                    echo "<th>Device</th>";
                    echo "<th>Status</th>";
                    echo "<th>Tme</th>";
                    echo "<th>OldStatus</th>";
                    echo "<th>oldTme</th>";
                echo "</tr>";
            while($row = mysqli_fetch_array($result)){
                echo "<tr>";
                    echo "<td scope='row'>" . $row['id'] . "</td>";
                    echo "<td>" . $row['device'] . "</td>";
                    echo "<td>" . $row['status'] . "</td>";
                    echo "<td>" . $row['time'] . "</td>";
                    echo "<td>" . $row['p_status'] . "</td>";
                    echo "<td>" . $row['p_time'] . "</td>";
                echo "</tr>";
            }
            echo "</table>";
            // Close result set
            mysqli_free_result($result);
        } else{
            echo "No records matching your query were found.";
        }
    } else{
        echo "ERROR: Could not able to execute $sql. " . mysqli_error($link);
    }
    // Close connection

    mysqli_close($link);

    ?>



