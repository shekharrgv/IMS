// Get references to the div elements by class name
var additionalBox = document.querySelector('.additional-box');
var secondBox = document.querySelector('.second-box');
var thirdBox = document.querySelector('.third-box');
var fourthBox = document.querySelector('.fourth-box');
var fifthBox = document.querySelector('.fifth-box');
var sixthBox = document.querySelector('.sixth-box');
var seventhBox = document.querySelector('.seventh-box');
var eightBox = document.querySelector('.eight-box');
var nineBox = document.querySelector('.nine-box');

// Fetch JSON data from management.json
fetch('management.json')
    .then(response => response.json())
    .then(data => {
        var jsonData = data.key_metrics;

        // Populate the div elements with JSON data
        additionalBox.innerHTML = '<p>Total Count: ' + jsonData.total.count + '</p>';
        secondBox.innerHTML = '<p>Triage Done Count: ' + jsonData.triage_done.count + ', Time: ' + jsonData.triage_done.time + '</p>';
        thirdBox.innerHTML = '<p>Triage Waiting Count: ' + jsonData.triage_waiting.count + ', Time: ' + jsonData.triage_waiting.time + '</p>';
        fourthBox.innerHTML = '<p>Cons Done Count: ' + jsonData.cons_done.count + ', Time: ' + jsonData.cons_done.time + '</p>';
        fifthBox.innerHTML = '<p>Cons Waiting Count: ' + jsonData.cons_waiting.count + ', Time: ' + jsonData.cons_waiting.time + '</p>';
        sixthBox.innerHTML = '<p>In Zone Count: ' + jsonData.in_zone.count + ', Time: ' + jsonData.in_zone.time + '</p>';
        seventhBox.innerHTML = '<p>IP Transfers Completed Count: ' + jsonData.ip_transfers.completed.count + ', Time: ' + jsonData.ip_transfers.completed.time + '</p>';
        eightBox.innerHTML = '<p>IP Transfers In Progress Count: ' + jsonData.ip_transfers.inprogress.count + ', Time: ' + jsonData.ip_transfers.inprogress.time + '</p>';
        nineBox.innerHTML = '<p>Treatment Count: ' + jsonData.treatment.count + ', Time: ' + jsonData.treatment.time + '</p>';
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });
