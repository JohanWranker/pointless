function showHint(str)
{
    var xmlhttp;
    if (str.length==0)
    { 
        for (var row=0;row<childNodes.length;row++)
        {
            item = childNodes[row]
            item.parentNode.removeChild(item);
        }
    }
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
    {
        
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            var table = document.getElementById("Suggestions")
            var tbody = table.getElementsByTagName("tbody")[0];
            var childNodes = tbody.childNodes;
            for (var row=0;row<childNodes.length;row++)
            {
                var item = childNodes[row];
                item.parentNode.removeChild(item);
            }
            
            //var parser=new DOMParser();
            //var xmlTxt= "ghjhgj";
            var xmlTxt = loadXMLString(xmlhttp.responseText);
            var s=xmlTxt.getElementsByTagName('sailor');
            for (var i=0;i<s.length;i++)
            {
                var row   = document.createElement("tr");
                row.onClick = "Clicked('111')";
                tbody.appendChild(row);
                var td    =  document.createElement("td");
                row.appendChild(td);
                td.appendChild(document.createTextNode(s[i].getAttribute('sailNo')));
                td.appendChild(document.createTextNode(s[i].getAttribute('surName')));
                td.appendChild(document.createTextNode(s[i].getAttribute('lastName')));
            } 
        }
    }
    xmlhttp.open("GET","gethint?q="+str,true);
    xmlhttp.send();
}
