function insert_log(data) {
var insert_log_url = "http://localhost:5000/insert_log";
var xhr = new XMLHttpRequest();
xhr.open("POST", insert_log_url, false);
xhr.setRequestHeader("Accept", "application/json");
xhr.setRequestHeader("Content-Type", "application/json");
var data_json = JSON.stringify(data);
xhr.send(data_json);
console.log(xhr.responseText);

}
