<!DOCTYPE html>
<html>
  <head>
	<title><?php echo $title; ?></title>
	<link rel="stylesheet" type="text/css" href="<?php echo $style; ?>"/>
  <link rel="icon" href="media/medium.png" type="image/png"/>
  </head>
  <body>
    <div class="header">
      <?php echo $header; ?>
    </div>
    <div class="left sidebar">
      <?php echo $sidebar; ?>
    </div>
    <div class="content">
      <?php echo $content; ?>
    </div>
    <div class="footer">
      <?php echo $footer; ?>
    </div>    
  <script src="js/common.js"></script>
  <script src="js/client_area.js"></script>
  </body>
</html>