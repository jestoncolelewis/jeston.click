// initialize variables
const left_div = document.querySelector('#page-left');
const count_element = document.createElement('p');

// get page count from db
fetch("https://0cxjlr27zj.execute-api.us-west-2.amazonaws.com/my-function")
.then((response) => response.text())
.then((data) => {
    // display page count on index.html
    count_element.textContent = data;
    left_div.append(count_element);
});

// detect new page visitor & update locally



// put new page count to db