// initialize variables
const left_div = document.querySelector('#page-left');
const count_element = document.createElement('p');
const url = 'https://0cxjlr27zj.execute-api.us-west-2.amazonaws.com/my-function'

// get page count from db
fetch(url)
.then((response) => response.text())
.then((data) => {
    // display page count on index.html
    count_element.textContent = data;
    left_div.append(count_element);
    
    // detect new page visitor & update locally
    let new_count = Math.floor(data) + 1;
    
    // put new page count to db
    /* fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'applications/json'
        },
        body: new_count
    }); */
});