
function element_from_log(log) {
//    console.log(log)
    var log_el = document.createElement("tr");
    log_el.className = 'log';
    var jira_id = document.createElement("td");
    jira_id.innerHTML = log['jira_id'];
    log_el.appendChild(jira_id);
    var description = document.createElement("td");
    description.innerHTML = log['description'];
    log_el.append(description)
    var log_time = document.createElement("td");
    log_time.innerHTML = log['log_time'];
    log_el.append(log_time)
    document.getElementById("logs").appendChild(log_el)
}

function refresh_logs() {
var url = "http://localhost:5000/get_logs";

var xhr = new XMLHttpRequest();
xhr.open("GET", url, true);

xhr.setRequestHeader("Accept", "application/json");
xhr.setRequestHeader("Content-Type", "application/json");

xhr.onreadystatechange = function () {
   if (xhr.readyState === 4) {
      console.log(xhr.status);
       logs_response = JSON.parse(xhr.responseText);
        logs = logs_response['logs'];
       document.getElementById("logs").innerHTML = "";
        logs.forEach(element_from_log);

   }};

xhr.send(null);
}

