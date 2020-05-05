<html class="no-js" lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Andrew C. Trapp</title>
        <link rel="stylesheet" href="css/foundation.css" />
        <link rel="stylesheet" href="style.css" />
        <script src="js/vendor/modernizr.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <style>
              .optimize_btn {
                background-color: #AC2937;
                border: none;
                width: 200;
                height: 65;
	        padding: 20px 10px;
                text-align: left;
	        text-decoration: none;
	        font-size: 22px;
                font-family: "Myriad Pro", Myriad, sans-serif;
	        font-weight: bold;
	        color: black ;
	        border-radius: 10px;
	        cursor: pointer;
	        margin: 0px;
                box-shadow: 10px 10px 20px #888888;
                display: table;
                -webkit-user-select: none;  /* Chrome all / Safari all */
                -moz-user-select: none;     /* Firefox all */
                -ms-user-select: none;      /* IE 10+ */
                 user-select: none;
              }

              .optimize_btn:hover {
               filter: brightness(90%);
              }

              .optimize_btn:focus {outline:0;} 

              .optimize_btn span{
	       position: relative;
	       top:0px;
              }

              .cog1 {
               position: relative;
               top: -30px;
               left: +60px;
               -webkit-animation:spin 4s linear infinite paused;
               -moz-animation:spin 4s linear infinite paused;
               animation:spin 4s linear infinite paused;
               
              }
              .cog2 {
              
               -webkit-animation:spin 4s linear infinite paused;               
               -moz-animation:spin 4s linear infinite paused;
               animation:spin 4s linear infinite paused;
               position:relative;
               top: -65px;
               left: 99px;
               } 
               @-moz-keyframes spin { 100% { -moz-transform: rotate(360deg); } }
               @-webkit-keyframes spin { 100% { -webkit-transform: rotate(360deg); } }
               @keyframes spin { 100% { -webkit-transform: rotate(360deg); transform:rotate(360deg); } }
        </style>
    </head>
    <body>
        <!-- Header and Nav -->
        <div class="row">
            <div class="large-5 columns">
                <a target="_blank" href="https://www.wpi.edu/">
                    <img src="./img/WPI_400x100.png" />
                </a>
            </div>
            <div class="large-7 columns">
                <h1 style="line-height: 200%">Andrew C. Trapp</h1>
            </div>             
            <hr style="height:2px;border:none;color:#3399ff;background-color:#cccccc;" />
        </div>
        <div class="row">
            <div class="large-6 columns">
                <p style="font-size:13.5px" class="text-left"> <a href="http://www.wpi.edu/" title="Worcester Polytechnic Institute">Worcester Polytechnic Institute</a> | <a href="http://www.wpi.edu/academics/business/" title="WPI Foisie Business School">WPI Foisie Business School</a> |         <a href="http://www.wpi.edu/academics/business/ie.html" title="WPI Industrial Engineering">WPI Industrial Engineering</a> |<a target="_blank" href="cv.pdf"> CV</a></p> 
            </div>             
            <div class="large-6 columns">
                <div class="button-group float-right">
                    <a href="http://users.wpi.edu/~atrapp/index.htm" class="button" style="color: #ffffff">Home</a>
                    <a href="http://users.wpi.edu/~atrapp/publications.htm" class="button" style="color: #ffffff">Publications</a>
                    <a href="http://users.wpi.edu/~atrapp/teaching.htm" class="button" style="color: #ffffff">Teaching</a>
                    <a href="http://users.wpi.edu/~atrapp/students.htm" class="button" style="color: #ffffff">Students</a>
                    <a href="http://users.wpi.edu/~atrapp/tools-and-software.htm" class="button" style="color: #ffffff">Tools & Software</a>
                </div>
            </div>
        </div>
        <!-- End Header and Nav -->
        <div class="row">
            <!-- Main Content Section -->
            <!-- This has been source ordered to come first in the markup (and on small devices) but to be to the right of the nav on larger screens -->
            <div class="columns large-12 medium-push-1">
                <h3>Finding diverse optima and near-optima to binary integer programs</h3>
                <?php
		ini_set('display_errors', 1);
		ini_set('display_startup_errors', 1);
		error_reporting(E_ALL);
//  header('Content-Type: application/download');


$target_dir = "../uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$ip=$_SERVER['REMOTE_ADDR'];

echo "<pre>";
$file_name=basename($_FILES["fileToUpload"]["name"]);
$file_name_complete= explode(".",$file_name);
$file_name_without_extenstions=$file_name_complete[0];
$file_name_to_download=$file_name_without_extenstions.'.out';

$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
$file_name_path= "/var/www/uploads/".$file_name;
echo "<br />";

// This is the data you want to pass to Python
$data=$_POST["kvalue"];

//With timestamp
$ts = date('m_d_Y_h_i_s', time());
$filets=$file_name_without_extenstions.'_k='.$data.'_'.$ts;
$filetsex=$filets.'.'.$imageFileType;
$target_file2=$target_dir.$filetsex;
$file_name_path2="/var/www/uploads/".$filetsex;
$file_name_to_download2=$filets.'.out';
//echo $target_file2;

//$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if the file is a actual file or fake file

// Check if file already exists
if (file_exists($target_file)) {
    echo "Sorry, file already exists. Please try using a different name.";
    echo "<br />";
    $uploadOk = 0;
}
// Check file size
if ($_FILES["fileToUpload"]["size"] > 50000000) {
    echo "Sorry, your file is too large.";
    echo "<br />";
        $uploadOk = 0;
}
// Allow certain file formats
if($imageFileType != "lp" && $imageFileType != "mps") {
    echo "Upload not successful. Please check the file format. It has to be either .lp or .mps";
    $uploadOk = 0;
} /*else{
    echo "Upload successful. File format is correct.";
    echo "<br />";
    $uploadOk = 1;
}*/


// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "<br /> Your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file2)) {
	echo "The file ". basename($_FILES["fileToUpload"]["name"]). " has been uploaded successfully. A date and time stamp has been appended to the filename.";
 	
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}


$link_address='http://diverseoptima.wpi.edu/results/'.$filets.'.out';
$dlink="<a href='".$link_address."' download='".$file_name_to_download2."' id='d_link'>Click here to download your output file.</a>";
$goBack="<a href='http://diverseoptima.wpi.edu'><input type='button' name='goBackButton' value='Go Back'></input></a>";
///End php
?>


<br />
<button id="optimize_btn" class="optimize_btn"> <span> Optimize </span>
        <img ID= "cogbig" class="cog1" src = "img\cog1.png" width ="40px;" height= "40px;"/> 
        <img ID= "cogsmall" class="cog2" src = "img\cog2.png" width ="25px;" height= "25px;"/> 
 </button>

<br />

<p id="msg"></p>

<p id="result_link"></p>

<script type="text/javascript">
  var first_click = 1;  

  $(document).ready(function(){
    $("#optimize_btn").click(function(){ 
      if (first_click==1){
        var k_value = "<?php echo $data; ?>";
        var input_file = "<?php echo $file_name_path2; ?>";
        var result_link = "<?php echo $dlink;?>";


        $.ajax({

          method: "POST",
          url: "run_py_script.php",
          beforeSend:function(){
            $("#cogbig").css("-webkit-animation-play-state", "running"); 
            $("#cogsmall").css("-webkit-animation-direction", "reverse"); 
            $("#cogsmall").css("-webkit-animation-play-state", "running"); 
            $("#msg").html("Optimization is running...Sometimes it might take a while ^-^");
            first_click = 0;
         },
         data: {action:'run_python',arg1:input_file , arg2:k_value},
         success:function(data){
           $("#msg").html("Optimization finished");
           $("#cogbig").css("-webkit-animation-play-state", "paused"); 
           $("#cogsmall").css("-webkit-animation-play-state", "paused"); 
           $("#result_link").append(result_link);
         }
      });//end ajax
    }//end if  
  });//end click button
});// end document ready

//document.write("<?php echo $dlink;?>");
//document.write("<br>");
//document.write("<br>"); 
//document.write("<?php echo $goBack;?>");
//}
</script>

<a href="http://diverseoptima.wpi.edu"><input type="button" name="goBackButton" value="Go Back"></input></a> 
           </div>
            <!-- Nav Sidebar -->
            <!-- This is source ordered to be pulled to the left on larger screens -->
        </div>
        <!-- Footer -->
        <footer class="row">
            <div class="large-12 columns">
                <hr style="height:2px;border:none;color:#cccccc;background-color:#cccccc;" />
                <div class="row">
                    <div class="large-6 columns">
                        <p>Contact Me:</p>
                        <a href="http://www.wpi.edu/academics/business/" title="Worcester Polytechnic Institute School of Business">Robert A. Foisie Business School</a>
                        <br />
                        <a href="http://www.wpi.edu/" title="Worcester Polytechnic Institute">Worcester Polytechnic Institute</a>
                        <br />100 Institute Rd.
                        <br />Worcester, MA 01609
                        <!-- <p>Phone: (412) 624-9830</p> -->
                        <!-- <p>Fax: (412) 624-9831</p> -->
                        <br />Email: atrapp "at" wpi "dot" edu
                    </a>
                    <br><a href="https://www.linkedin.com/in/andytrapp">LinkedIn</a>
		    <br><a href="https://scholar.google.com/citations?user=ZASbboYAAAAJ&hl=en&oi=ao">Google Scholar</a>
                </div>
                <div class="large-6 columns">
                    <ul class="float-right menu">
                        <li style="display:inline;padding: 2px 1px;display:inline-block;">
                            <a href="http://users.wpi.edu/~atrapp/index.htm">Home</a>
                        </li>
                        <li style="display:inline;padding: 2px 1px;display:inline-block;">
                            <a href="http://users.wpi.edu/~atrapp/publications.htm">Publications</a>
                        </li>
                        <li style="display:inline;padding: 2px 1px;display:inline-block;">
                            <a href="http://users.wpi.edu/~atrapp/teaching.htm">Teaching</a>
                        </li>
                        <li style="display:inline;padding: 2px 1px;display:inline-block;">
                            <a href="http://users.wpi.edu/~atrapp/students.htm">Students</a>
                        </li>
                        <li style="display:inline;padding: 2px 1px;display:inline-block;">
                            <a href="http://users.wpi.edu/~atrapp/tools-and-software.htm">Tools & Software</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>
    <script src="js/vendor/jquery.min.js"></script>
    <script src="js/foundation.min.js"></script>
    <script>
      $(document).foundation();
    </script>
    <!-- Start of StatCounter Code for Default Guide -->
    <script type="text/javascript">
var sc_project=7139907; 
var sc_invisible=1; 
var sc_security="48ef0ec4"; 
</script>
    <script type="text/javascript" src="http://www.statcounter.com/counter/counter.js"></script>
    <noscript>
        <div class="statcounter">
            <a title="tumblr
counter" href="http://statcounter.com/tumblr/" target="_blank">
                <img class="statcounter" src="http://c.statcounter.com/7139907/0/48ef0ec4/1/" alt="tumblr counter">
            </a>
        </div>
    </noscript>
    <!-- End of StatCounter Code for Default Guide -->
</body>
</html>
