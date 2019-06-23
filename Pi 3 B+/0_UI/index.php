<!DOCTYPE html>
<html lang="en">
<head>
  <title>Sensors</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>

  <style>
    /* Remove the navbar's default margin-bottom and rounded borders */ 
    .navbar {
      margin-bottom: 0;
      border-radius: 0;
    }
    
    /* Set height of the grid so .sidenav can be 100% (adjust as needed) */
    .row.content {height: 450px}
    
    /* Set gray background color and 100% height */
    .sidenav {
      padding-top: 20px;
      background-color: #f1f1f1;
      height: 100%;
    }
    
    /* Set black background color, white text and some padding */
    footer {
      background-color: #555;
      color: white;
      padding: 15px;
    }
    
    /* On small screens, set height to 'auto' for sidenav and grid */
    @media screen and (max-width: 767px) {
      .sidenav {
        height: auto;
        padding: 15px;
      }
      .row.content {height:auto;} 
    }

    /*body {background-color: gray;}*/

  </style>
</head>
<body>

<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>                        
      </button>
      <a class="navbar-brand" href="index.php">Smart Home</a>
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav">
        <li class="active"><a href="index.php">Sensors</a></li>
        <li><a href="relays.php">Relays</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="index.php"><span class="glyphicon glyphicon-log-in"></span> Coming Soon</a></li>
      </ul>
    </div>
  </div>
</nav>
  
<div class="container-fluid text-center">    
  <div class="row content">
      <?php
        $servername = "localhost";
        $username = "admin";
        $password = "test";
        $dbname = "DevicesDB";
        
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        
        $sql = "SELECT * FROM Devices WHERE Type = \"Sensor\" ORDER BY Location";
        $result = $conn->query($sql);
        $table_was_opened = false;
        if ($result->num_rows > 0) {
          $iter = 1;
          $is_first = true;
          $current_cat = null;
          while ($row = $result->fetch_assoc()) {
            if ($row["Location"] != $current_cat) {
              if (!$is_first) {
                echo "</tbody>";
                echo "</table></p>";
                echo "<hr></div>";
              }
              $iter = 1;
              echo "<div class=\"col-sm-8 text-left\">";
              $current_cat = $row["Location"];
              echo "<h1>$current_cat</h1>\n";
              $is_first = false;
              echo "<p><table class=\"table table-hover table-dark\">";
              echo "  <thead>";
              echo "    <tr>";
              echo "      <th scope=\"col\">#</th>";
              echo "      <th scope=\"col\">Name</th>";
              echo "      <th scope=\"col\">Value</th>";
              echo "    </tr>";
              echo "  </thead>";
              echo "  <tbody>";
              $table_was_opened = true;
            }
            echo "<tr>";
            echo "<th scope=\"row\">" . $iter++ . "</th>";
            echo "<td>" . $row["Name"] . "</td>";
            echo "<td>" . $row["Value"] . "</td>";
            echo "</tr>";
          }
          if ($table_was_opened) {
            echo "</tbody>";
            echo "</table></p>";
            echo "<hr></div>";
          }
          

            
        } else {
            echo "0 results";
        }
        $conn->close();
      ?>

    <div class="col-sm-8 text-left">
      <p></p>
      <hr>
    </div>

  </div>
</div>

<div class="footer navbar-fixed-bottom">
  <footer class="container-fluid text-center">
    <p>Lucrare licenta 2019, Horia COSTINA ©</p>
  </footer>
</div>

</body>
</html>

