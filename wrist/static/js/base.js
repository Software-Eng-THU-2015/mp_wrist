function getData(url, callback)
{
    var xhr = new XMLHttpRequest();
    xhr.open("get", url, true);
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200)
            callback(xhr.responseText);
    }
    xhr.send(null);
}

function postData(url, data, callback)
{
    var xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200)
            callback(xhr.responseText);
    }
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(data);
}

//domain = "http://softeng3.zjzs.levy.at";
domain = "http://wrist.ssast2015.com";