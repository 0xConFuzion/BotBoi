<!DOCTYPE html>
<html>
  <head>
    <title>NeonHaze-WTF</title>
	<link href="favicon.ico">
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet"> 
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- (A) CSS & JS -->
    <link href="gallery.css" rel="stylesheet">
    <script src="gallery.js"></script>
      <!-- Global site tag (gtag.js) - Google Analytics -->
      <script async src="https://www.googletagmanager.com/gtag/js?id=G-J7H1L8MY8N"></script>
      <script>
        window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());

                gtag('config', 'G-J7H1L8MY8N');
      </script>
	  <div class="banner">
			<img class="displayed" src='neonhaze.gif' alt="NeonHazeBanner"> 
	   </div>
  </head>
  <body>

       <div class="topnav">
        <a class="active" href="index.php">Home</a>
        <a href="video.php">Video</a>
        <a href="#contact">Contact</a>
      </div> 
    <div class="gallery"><?php
    // (B) GET LIST OF IMAGE FILES FROM GALLERY FOLDER
    $dir = "/var/www/html/img/";
    $images = glob($dir . "*.{jpg,jpeg,gif,png,bmp,webp,mp4}", GLOB_BRACE);

    // (C) OUTPUT IMAGES    
foreach ($images as $i) {
  $parts = pathinfo($i);
  if ($parts['extension']=="mp4") {
    //printf("<video src='img/%s' controls></video>", basename($i));
  }
  else {
    printf("<img src='img/%s'/>", basename($i));
  }
}
    ?></div>

  </body>
</html>