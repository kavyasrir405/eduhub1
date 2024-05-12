const sidebar = document.querySelector('.sidebar');
const container = document.querySelector('.container');

sidebar.addEventListener('mouseover', () => {
  container.style.marginLeft = '200px';
});

sidebar.addEventListener('mouseout', () => {
  container.style.marginLeft = "60px";
});

document.getElementById('uploadBtn').addEventListener('click', function() {
  // Retrieve information from local storage
  var uploadedInfo = localStorage.getItem('uploadedInfo');

  // Parse the JSON string into an object
  var courseInfo = JSON.parse(uploadedInfo);
  console.log.out(courseInf0)

  // Create a new course-item div
  var newCourseItem = document.createElement('div');
  newCourseItem.className = 'course-item';

  // Populate the newCourseItem div with information
  newCourseItem.innerHTML = '<h3>' + courseInfo.course_name + '</h3>' +
                            '<p>' + courseInfo.course_description + '</p>' +
                            '<p>Price: ' + courseInfo.course_price + '</p>' +
                            '<p>Category: ' + courseInfo.category + '</p>';

  // Add the newCourseItem div to the courseList
  document.querySelector('.courseList').appendChild(newCourseItem);
});