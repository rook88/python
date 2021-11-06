
function element_from_task(task) {
//    console.log(task)
    var task_el = document.createElement("button");
    task_el.jira_id = task.jira_id
    task_el.className = 'task';
    var jira_id = document.createElement("p");
    jira_id.innerHTML = task['jira_id'];
    task_el.appendChild(jira_id);
    function task_el_onclick() {
//        alert (this.jira_id)
        if (this.jira_id == 'NEW') {
            this.jira_id = prompt("New jira_id");
        }
        this.description = prompt("description");
        insert_log(this);
        refresh_logs();
    }
    task_el.onclick = task_el_onclick; 
    document.getElementById("tasks").appendChild(task_el)
}

function refresh_tasks() {
var url = "http://localhost:5000/get_tasks";
var xhr = new XMLHttpRequest();
xhr.open("GET", url, false);
xhr.setRequestHeader("Accept", "application/json");
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send(null);
tasks_response = JSON.parse(xhr.responseText);
tasks = tasks_response['tasks'];
document.getElementById("tasks").innerHTML = "";
tasks.forEach(element_from_task);
element_from_task(JSON.parse('{ "jira_id":"NEW", "description":"nil" }'))
};
