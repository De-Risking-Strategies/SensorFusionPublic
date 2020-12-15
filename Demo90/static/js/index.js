//Index page functions
var toggleCameraBtnFlag = true;
var toggleLabels = true;//On by default
var toggleScores = true;
var span; 
var modal 

function init(){
var toggleLabelsBtn = document.getElementById("toggleLabelsBtn");
var toggleScoresBtn = document.getElementById("toggleCameraBtn");
//Clear Modal on outside click
document.getElementById("main").addEventListener("click", function() {
 modal.style.display = "none";
});
//modal = document.getElementById("sfModal");
modal = document.getElementsByClassName("modal")[0];

// Get the button that opens the modal
var btn = document.getElementsByClassName("myBtn");
var btnLength = btn.length;

// Get the <span> element that closes the modal
span = document.getElementsByClassName("close")[0];
span.onclick = function() {
   modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
 }

document.body.onkeydown = function(e){
  console.log(String.fromCharCode(e.keyCode)+"-->"+e.keyCode);
  if(e.keyCode =='32'){
    modal1_click('annotate');
  }else if(e.keyCode == '70'){
    postAPI('fps')
  }
  
}

}


function toggleCamera(){
  camera1 = document.getElementById("cameraStream");
  var toggleCameraBtn = document.getElementById("toggleCameraBtn");
  var sensorTitleText = document.getElementById("sensor_toggle_title");
    if (toggleCameraBtnFlag == false) {//turn camera on
      toggleCameraBtnFlag = true
      //camera1.src = "{{ url_for('video_feed') }}";
      //camera1.src = "http://localhost:5000/video_feed";
      camera1.style.display = "block";
      sensorTitleText.innerText="CAMERA 1: ON";
      
      toggleCameraBtn.src = "/static/assets/toggle_switch_on_001.png";
    }else{
      toggleCameraBtnFlag = false
      //camera1.src = "";
      camera1.style.display = "none";
      sensorTitleText.innerText="CAMERA 1: OFF";
      toggleCameraBtn.src = "/static/assets/toggle_switch_off_001.png";
    }
  
}
function getAPI(command) {
// GET is the default method, don't need to set it, but is not used in SF for now.
  fetch('/api')
    .then(function (response) {
        return response.json(); //  parse it as JSON 
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); 
    })
}
function postAPI(command) {
// POST commands to Flask/Python API route
  console.log('Posting: '+ command);
  var sfCommandAnnotate = false;
  var annotateName
  
  if(command == 'annotate'){
    var sfCommandAnnotate = true;
        annotateName = document.getElementById('aName').value;
        console.log(annotateName);
    var annotateImages = document.getElementById('aImages').value;
        console.log(annotateImages);    
    var annotateDescription = document.getElementById('aDescription').value;
        console.log(annotateDescription);
        
    if (annotateName == "" || annotateImages == "" || annotateDescription ==""){
      alert("No Blank Fields Allowed! Try Again.");
    }else{    
      command = command+','+annotateName+','+annotateImages+','+ annotateDescription
   }
  }             
  if(command == 'labels'){
    if(toggleLabels == true){
      toggleLabels = false;
      command = command + '_off';
      toggleLabelsBtn.src = "/static/assets/toggle_switch_off_001.png";
    
    }else{
      toggleLabels = true;
      toggleLabels = true;
      command = command + '_on';
      toggleLabelsBtn.src = "/static/assets/toggle_switch_on_001.png";
    }
  }
    if(command == 'scores'){
      if(toggleScores == true){
      toggleScores = false;
      command = command + '_off';
      toggleScoresBtn.src = "/static/assets/toggle_switch_off_001.png";
    
    }else{
      toggleScores = true;
      command = command + '_on';
      toggleScoresBtn.src = "/static/assets/toggle_switch_on_001.png";
   
    }
   }
  

  fetch('/api',{
    method: 'post',
    headers:{
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body:JSON.stringify(command)
    }).then(function (response) {
        //return response.json(); //Its already in JSON coming back from Flask, so don't need to parse it
        return response; 
    })
    .then(function (json) {
        console.log('POST response from Flask');
        console.log(json); 
        
        if(json.status== 200 && sfCommandAnnotate ){
          var modal1 = document.getElementById("modal_body1");
          var modal2 = document.getElementById("modal_body2");
          modal1.innerHTML = "<h2>Your Files are saving to: <br><br/>/home/pi/Pictures/"+ annotateName+"</h2>";
          modal2.innerHTML = "<p>Next, select Main Menu item 3 Run Image Labeler to annotate them!</p><strong style='color:red'>IF YOU USE AN EXISTING FOLDER NAME PREVIOUS FILES WILL BE OVERWRITTEN</strong>";
        }
    })
}

function modal1_click(event){
  var hdr = document.getElementById("modal_header");
  var modal1 = document.getElementById("modal_body1");
  var modal2 = document.getElementById("modal_body2");
  var ftr = document.getElementById("modal_footer");

  var mTitle= 'Not Implemented Yet'; 
  var mHtml1='<br><strong>Please come back soon!</strong>'; 
  var mHtml2= '<br>';
  var mFooter='Click out or X to Exit';

  if(event =='annotate'){
    mTitle = 'Capture Images for Annotation';
    mHtml1 ='<br><strong>Name, Number and Description</strong><br>';
    
    //Annotation Form - values to pass to Flask/Python
    var row0 = '<table border="1">';
    var row1 = '<tr><td id="ic1">Name</td><td id="ic2"><input id="aName" type="text" style="width:150px"></input></td></tr>';
    var row2 = '<tr><td id="ic3">Images to Capture</td><td id="ic4"><input id="aImages" type="text" style="width:50px">500</input></td></tr>';
    var row3 = '<tr><td id="ic5">Description</td><td id="ic6"><input id="aDescription" type="text" style="width:300px"></input></td></tr>';
    var row4 = '</table>'
    var row5 = "<br><input type='button' value='Submit' onclick=postAPI('annotate')>";
    mHtml2 = row0+row1+row2+row3+row4+row5;

  }
  //Draw the Modal
  hdr.innerHTML  = mTitle
  modal1.innerHTML = mHtml1;
  modal2.innerHTML = mHtml2;
  ftr.innerHTML = mFooter;
  modal.style.display = "block";
  
}

