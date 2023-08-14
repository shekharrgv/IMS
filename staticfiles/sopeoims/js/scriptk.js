// JavaScript code to add HTML content dynamically
document.addEventListener('DOMContentLoaded', function() {
    // Get the element where you want to add the HTML content
    const contentDiv = document.getElementById('content');

    // Create a new HTML element dynamically
    const dynamicElement = document.createElement('p');
    dynamicElement.textContent = 'This is dynamically added content.';

    // Add the new HTML element to the contentDiv
    contentDiv.appendChild(dynamicElement);
});
function toggleMenu() {
    const menu = document.querySelector('.menu');
    menu.classList.toggle('show');
}
function toggleSliderBox() {
    const sliderBox = document.getElementById('sliderBox');
    sliderBox.classList.toggle('show');
}
