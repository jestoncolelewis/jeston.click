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
});

// show 5 projects
const projects = document.querySelectorAll('.project');
const more = document.getElementById('more');
let num_clicks = 1;
function show_posts(to_show) {
    if (to_show > projects.length)  {
        to_show = projects.length;
        more.hidden = true;
    }
    for (let i = 0; i < to_show; i++) {
        const project = projects[i];
        if (project.hidden === true)
        {
            project.hidden = false;
        }
    }
}
function show_next() {
    num_clicks++;
    show_posts(num_clicks * 5);
}

show_posts(5);
more.addEventListener('click', show_next);
