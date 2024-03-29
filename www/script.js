// initialize variables
const footer = document.querySelector('footer');
const count_element = document.createElement('p');
const count_title = document.createElement('p')
const url = 'https://rogn9gsh2e.execute-api.us-east-1.amazonaws.com/prod/jestonclick-page-count-31ee36e'

// get page count from db
fetch(url)
.then((response) => response.text())
.then((data) => {
    // display page count on index.html
    count_title.textContent = 'Page Views';
    count_title.textAlign = 'center';
    count_element.textContent = data;
    count_element.style.textAlign = 'center';
    footer.append(count_title);
    footer.append(count_element);
    console.log(data);
});