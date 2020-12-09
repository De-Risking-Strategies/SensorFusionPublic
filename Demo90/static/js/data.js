//data function to get stereaming data from python
setInterval(function() {
    var req = new XMLHttpRequest();
    req.open('GET', '/refresh_data?time=234', true);
    req.onreadystatechange = function(e) {
        if(req.readyState !== 4) {
            return;
        }
        if ([200, 304].indexOf(req.status) === -1) {
            console.warn('Error! XHR failed.');
        }
        else {
            data = JSON.parse(e.target.responseText);
            console.log("Receiving FPS Data Stream in Browser: "+data)
        }
    };
    req.send();
}, 5000);  // time in milliseconds (e.g. 10000 = every 10 seconds)
