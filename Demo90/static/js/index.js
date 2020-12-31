//Index page functions
var toggleCameraBtnFlag = true;
var toggleInfoCanvasFlag = false;
var toggleLabels = true;//On by default
var toggleScores = true;
var span; 
var modal;
var modalOpen = false;
var preLoadedModel = ['Demo90','Model01.Deer', 'Model02.Head', 'Model03.Eyes', 'Model04.Tree'];
var customModel = ['Custom.04','Check.ID','Custom.01','Custom.02', 'Custom.03'];
var customModelIndex = 0;

var preLoadedModelSelected = 'Demo90';//Default Model
var preLoadedModelIndex = 0;

var modelType = 'preLoaded';


function init(){
var toggleLabelsBtn = document.getElementById("toggleLabelsBtn");
var toggleScoresBtn = document.getElementById("toggleCameraBtn");
//Clear Modal on outside click
document.getElementById("main").addEventListener("click", function() {
 postAPI('restore_tesnorFlow');
 modal.style.display = "none";
 modalOpen = false;
});
//modal = document.getElementById("sfModal");
modal = document.getElementsByClassName("modal")[0];

// Get the button that opens the modal
var btn = document.getElementsByClassName("myBtn");
var btnLength = btn.length;

// Get the <span> element that closes the modal
span = document.getElementsByClassName("close")[0];
span.onclick = function() {
   postAPI('restore_tesnorFlow');
   modal.style.display = "none";
    modalOpen = false;
    
    
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
   postAPI('restore_tesnorFlow');
   modal.style.display = "none";
   modalOpen = false;
  }

  var status1 = document.getElementById("annotateFileStatus");
  status1.innerText = "";

 }

document.body.onkeydown = function(e){
 // console.log(String.fromCharCode(e.keyCode)+"-->"+e.keyCode);

if (modalOpen == false){
  if(e.keyCode =='32'){//SPACEBAR
      modal1_click('annotate');
    }else if(e.keyCode == '81'){//Q
      postAPI('quit');
    }else if(e.keyCode == '70'){
      postAPI('fps')
    } 
  }
 }

//Load stored Model setting
modelType = getCookie('modelType');

if (modelType == 'preLoaded'|| modelType ==""){
  preLoadedModelIndex = getCookie('modelIndex');
   
  if(preLoadedModelIndex == ""){
    setCookie("modelIndex", "0", 30);
    setCookie("modelType", "preLoaded", 30);
    setCookie("customModelIndex", "0", 30);//Reset CustomModel Index
    
    preLoadedModelIndex = 0;
  }
    document.getElementById('switchModelImg').src = 'http://localhost:5000/static/assets/models_icon_selected_001.png'; 
    document.getElementById('switchCustomImg').src = 'http://localhost:5000/static/assets/models_icon_001.png'; 
  
}else{
   customModelIndex = getCookie('customModelIndex');
   
   if(customModelIndex == ""){
    setCookie("modelIndex", "0", 30); //Reset PreLoaded Model Index
    preLoadedModelIndex = 0;
    setCookie("customModelIndex", customModelIndex, 30);
    setCookie("modelType", "Custom", 30);
    
   }
    document.getElementById('switchModelImg').src = 'http://localhost:5000/static/assets/models_icon_001.png'; 
    document.getElementById('switchCustomImg').src = 'http://localhost:5000/static/assets/models_icon_selected_001.png'; 
  
}

document.getElementById('switchModelLabel').innerText = preLoadedModel[preLoadedModelIndex];
document.getElementById('switchCustomLabel').innerText = customModel[customModelIndex];
     
}


function toggleCamera(){
  camera1 = document.getElementById("cameraStream");
  toggleCameraBtn = document.getElementById("toggleCameraBtn");
  var sensorTitleText = document.getElementById("sensor_toggle_title");
  var infoCam = document.getElementById("infoCam");
  
   if (toggleCameraBtnFlag == false) {//turn camera on
      toggleCameraBtnFlag = true
      //camera1.src = "{{ url_for('video_feed') }}";
      //camera1.src = "http://localhost:5000/video_feed";
      camera1.style.display = "block";
      sensorTitleText.innerText="SENSOR 1: ON";
      infoCam.style.display = "none";
      toggleCameraBtn.src = "/static/assets/toggle_switch_on_001.png";
      
    }else{
      toggleCameraBtnFlag = false
      //camera1.src = "";
      camera1.style.display = "none";
      sensorTitleText.innerText="SENSOR 1: OFF";
      toggleCameraBtn.src = "/static/assets/toggle_switch_off_001.png";
      infoCam.style.display = "block";
    }
  
}
function postAPI(command) {
// POST commands to Flask/Python API route
  console.log('Posting: '+ command);
  sfCommandAnnotate = false;
  var annotateName
  
  if(command == 'annotate'){
    sfCommandAnnotate = true;
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
   if(command == 'custom'){//CUSTOM MODEL
      //switchCustomImage();
      var len = customModel.length;
      var customModelIndex = parseInt(getCookie('customModelIndex'));
      
      if (isNaN(customModelIndex)){customModelIndex = 0};
      
      //if (customModelIndex == 0){customModelIndex = 1};//Skip 0th
      
      if(customModelIndex >= 5){
        customModelIndex = 0;//Skip over the initial placeholder 'custom'
      }else{
        customModelIndex += 1;
      }
      
      if(customModelIndex >= len){
        customModelIndex = 0;
      }
      setCookie("modelType", "Custom", 30);
      setCookie('customModelIndex', customModelIndex, 30);
      command += ','+ customModel[customModelIndex];
      document.getElementById('switchCustomLabel').innerText = customModel[customModelIndex];
      document.getElementById('switchModelImg').src = 'http://localhost:5000/static/assets/models_icon_001.png'; 
      document.getElementById('switchCustomImg').src = 'http://localhost:5000/static/assets/models_icon_selected_001.png'; 
      
      console.log('Switch Custom Model: '+ customModel[customModelIndex])
      timeRefresh(3);//Reload broswer

   }

   if(command == 'model'){//PRE LOADED MODEL
      //switchModelImage();
      var len = preLoadedModel.length;
      var preLoadedModelIndex = parseInt(getCookie('modelIndex'));
      customModelIndex = 0;
      if (isNaN(preLoadedModelIndex)){preLoadedModelIndex = 0}
      
      preLoadedModelIndex += 1;
      if(preLoadedModelIndex >= len){
        preLoadedModelIndex = 0;
      }
      setCookie("modelType", "preLoaded", 30);
      setCookie('modelIndex', preLoadedModelIndex, 30);
      command += ','+ preLoadedModel[preLoadedModelIndex];
      document.getElementById('switchModelLabel').innerText = preLoadedModel[preLoadedModelIndex];
      
      document.getElementById('switchCustomLabel').innerText = customModel[customModelIndex];
      document.getElementById('switchModelImg').src = 'http://localhost:5000/static/assets/models_icon_selected_001.png'; 
      document.getElementById('switchCustomImg').src = 'http://localhost:5000/static/assets/models_icon_001.png'; 
     
      console.log('Switch PreLoaded Model'+ preLoadedModel[preLoadedModelIndex])
      timeRefresh(3);//Reload broswer

   }   
   if(command == 'quit'){
      console.log('quitting')
      timeRefresh(6);//Reload broswer
    }
   if(command == 'kill_tesnorFlow'){
      console.log('kill_tesnorFlow')
    } 
   if(command == 'restore_tensorFlow'){

      console.log('restore_tensorFlow')
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
          var status1 = document.getElementById("annotateFileStatus");
          var link = "/home/pi/SensorFusion/Pictures/"+ annotateName
          
          status1.innerText = "Your files are saving to: "+link;
          modal.style.display = "none";
        }
      
       var cd = command.split(",");     
       if (json.status == 403 && cd[0] =='dirCheck'){
         alert('This Name is already Taken, please try again');
         document.getElementById('aName').value='';
         
       }
    })
 modalOpen = false;
    
}
 function timeRefresh(time) {
      setTimeout("location.reload(true);", time);
    }

function switchTrainImageOn(){
    document.getElementById('switchTrainImg').src = 'http://localhost:5000/static/assets/train_model_selected_001.png'; 
    setTimeout(function(){switchTrainImageOff(); }, 3000);
  }
function switchTrainImageOff(){ 
   document.getElementById('switchTrainImg').src = 'http://localhost:5000/static/assets/train_model_001.png'; 
 
}

function display_info(){
  var infoPic = document.getElementById("infoPic");
  
    if (toggleInfoCanvasFlag == false) {//turn info canvas  on
      toggleInfoCanvasFlag = true
      infoPic.style.display = "block";
      
      }else{
      toggleInfoCanvasFlag = false
      infoPic.style.display = "none";
    }
}
function setCookie(cname,cvalue,exdays){
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = 'expires'+ d.toGMTString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  
}


function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function close_info(){
   toggleCameraBtnFlag = false;
   toggleInfoCanvasFlag = false;
   infoPic.style.display = "none";
   infoCam.style.display= "none";
}
function checkDirectoryExists(dir){
    console.log('Check Directory Exists '+dir)
    checkDir = document.getElementById('aName').value
    
    postAPI('dirCheck,'+checkDir)
    
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
    
    postAPI('kill_tesnorFlow');
    mTitle = 'Capture Images for Annotation';
    mHtml1 ='<br><strong>Name, Number and Description</strong><br>';
    
    //Annotation Form - values to pass to Flask/Python
    var row0 = '<table border="1">';
    var row1 = '<tr><td id="ic1">Name</td><td id="ic2"><input id="aName" type="text" style="width:150px" onchange="checkDirectoryExists(this)"></input><br/>';
    var row2 = '<strong style="color:red">Files are saved in /home/pi/SensorFusion/name</strong></td></tr>';
    var row3 = '<tr><td id="ic3">Images to Capture</td><td id="ic4"><input id="aImages" type="text" style="width:50px">&nbsp;2,000 MAX!</input></td></tr>';
    var row4 = '<tr><td id="ic5">Description</td><td id="ic6"><input id="aDescription" type="text" style="width:300px"></input></td></tr>';
    var row5 = '</table>'
    var row6 = "<br><input type='button' value='Submit' onclick=postAPI('annotate')>";
    mHtml2 = row0+row1+row2+row3+row4+row5+row6;
    
  }
 
  
  //Draw the Modal
  modalOpen = true;
  hdr.innerHTML  = mTitle
  modal1.innerHTML = mHtml1;
  modal2.innerHTML = mHtml2;
  ftr.innerHTML = mFooter;
  modal.style.display = "block";
  document.getElementById("aName").focus;
  
}
function selectFile(){
  switchTrainImageOn();
  var input = document.createElement('input')
  input.type = 'file';
  input.click();
  var file;
  var fName
  var fType
  var fSize

  input.onchange = e =>{
   file = e.target.files[0];
   fName = file.name;
   fType = file.type;
   fSize = file.size;    

   //document.getElementById('fileSelected').innerHTML = fName +":"+ fSize +":"+ fType ||'no file selected';
   
  switchTrainImageOff();

  if (fSize > 90000000){alert("File Size too large, please try again")}
  
  if (fType != 'application/zip'){alert("File must be a ZIP archive, please try again")
  }
 }
}




