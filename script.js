// initialize variables
const left_div = document.querySelector('#page-left');
const count_element = document.createElement('p');

// get page count from db
let page_count = localStorage.getItem('page_view'); // from db

// detect new page visitor & update locally
if (page_count) {
    page_count = Number(page_count) + 1;
    localStorage.setItem('page_view', page_count)
} else {
    page_count = 1;
    localStorage.setItem('page_view', 1)
}

// display page count on index.html
count_element.textContent = page_count;
left_div.append(count_element);

// put new page count to db