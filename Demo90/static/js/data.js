//Function to get data from python to Javascript
//CAUTION - DO NOT USE on real-time data, as it will lslow things down alot!

document.addEventListener("DOMContentLoaded", function(event){
    
        /*for Future Reference
         setInterval(function() {
            var req = new XMLHttpRequest();
            req.open('GET', '/refresh_data?time=234', true);
            req.onreadystatechange = function(e) {
                if(req.readyState !== 4) {
                    return;
                }
                if ([200, 304].indexOf(req.status) === -1) {
                    console.log('Error! XHR failed.');
                }
                else {
                    data = JSON.parse(e.target.responseText);
                    jsonString = JSON.stringify(data);
                    
                     /*xMin =data.xMin; - NOTE - Very costly performance overhead without multi-threading
                     yMin =data.yMin;
                     label=data.Label;//This has the %%
                     //Get just the numbers 
                     var len = label.length
                     var start = parseInt(len -3)
                     var end = parseInt(len -1)
                     label = label.slice(start,end)
                     
                     //Position Elements
                     rangeBar1.style.left = xMin;
                     rangeBar1.style.top = yMin;
                     
                     name=data.Name;
                    * /
                    //console.log("name: "+name+" label: "+label+" xMin: "+xMin+" yMin: "+yMin);
                    //console.log("dataStream: "+jsonString);
                }
            };
            req.send();
        }, 100000);  // time in milliseconds (e.g. 10000 = every 10 seconds)
        */
});

