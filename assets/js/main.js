---
---

{% include_relative /updateLinkTargets.js %}
{% include_relative /enableTooltips.js %}
{% include_relative /copyText.js %}


window.addEventListener("DOMContentLoaded", function() {
  getRemovedPosts();
  markRemovedPosts();
  updatePostCounts();
  expandCategories();
  showRemovedPosts();
  showFilteredPosts();
  addTableClasses();
  showContent();
  enableTooltips();
});


{%- assign project_ids = "" -%}
{%- for project in site.data.watchlist -%}
  {%- if project.forum and project.status == "live" -%}
    {%- assign project_ids = project_ids | append: "," | append: project.id -%}
  {%- endif -%}
{%- endfor -%}
{%- assign project_ids = project_ids | remove_first: "," -%}
{%- assign project_ids = project_ids | split: "," | uniq | sort_natural -%}

const projects = {{project_ids | jsonify}};


// ids of removed posts
let removedPosts = [];
function getRemovedPosts() {
  // get removed posts or create localstorage item
  if (localStorage.getItem("removedPosts") === null) {
    localStorage.setItem("removedPosts", JSON.stringify(removedPosts));
  } else {
    removedPosts = JSON.parse(localStorage.getItem("removedPosts"));
  }
}
function removePost(postId, projectId) {
  if (!removedPosts.includes(postId)) {
    removedPosts.push(postId);
    localStorage.setItem("removedPosts", JSON.stringify(removedPosts));
    document.getElementById(postId).classList.add("removed");
    updatePostCount(projectId);
  }
}
// add class to identify removed posts
function markRemovedPosts() {
  document.querySelectorAll('.card-post').forEach(el => {
    if (removedPosts.includes(el.id)) {
      el.classList.add("removed");
    }
  });
}


// show content when page is loaded
function showContent() {
  document.getElementById("loading").classList.add("d-none");
  document.querySelectorAll(".tab-pane").forEach((el) => {
    el.classList.remove("d-none");
  });
}


// add classes to tables
function addTableClasses() {
  document.querySelectorAll(".md-table").forEach((el) => {
    el.classList.add("table-responsive");
  });
  document.querySelectorAll(".table-responsive table").forEach((el) => {
    el.classList.add("table");
    el.classList.add("table-bordered");
  });
}


// show/hide filtered posts
function showFilteredPosts(show=null) {
  if (show == null) {
    show = JSON.parse(localStorage.getItem("showFilteredPosts"));
    document.getElementById("showFilteredPosts").checked = show;
  }
  if (show) {
    document.querySelectorAll(".card-post.filtered").forEach((el) => {
      el.classList.remove("d-none");
    });
  } else {
    document.querySelectorAll(".card-post.filtered").forEach((el) => {
      el.classList.add("d-none");
    });
  }
  localStorage.setItem("showFilteredPosts", JSON.stringify(show));
  updatePostCounts();
}
// show/hide removed posts
function showRemovedPosts(show=null) {
  if (show == null) {
    show = JSON.parse(localStorage.getItem("showRemovedPosts"));
    document.getElementById("showRemovedPosts").checked = show;
  }
  if (show) {
    document.querySelectorAll(".card-post.removed").forEach((el) => {
      el.classList.add("unremoved");
    });
  } else {
    document.querySelectorAll(".card-post.removed").forEach((el) => {
      el.classList.remove("unremoved");
    });
  }
  localStorage.setItem("showRemovedPosts", JSON.stringify(show));
  updatePostCounts();
}


function updatePostCount(project) {
  let postCount = document.getElementById(`${project}-count`).innerHTML.replace("(","").replace(")","");
  postCount = Number(postCount) - 1;
  document.getElementById(`${project}-count`).innerHTML = `(${postCount})`;
}
function updatePostCounts() {
  let showFilteredPosts = document.getElementById("showFilteredPosts").checked
  let showRemovedPosts = document.getElementById("showRemovedPosts").checked
  projects.forEach((project) => {
    if (document.getElementById(project)) {
      let postCount;
      if (showFilteredPosts && showRemovedPosts) {
        postCount = document.querySelectorAll(`#${project} .card-post`).length;
      } else if (showFilteredPosts) {
        postCount = document.querySelectorAll(`#${project} .card-post:not(.removed)`).length;
      } else if (showFilteredPosts) {
        postCount = document.querySelectorAll(`#${project} .card-post:not(.removed)`).length;
      } else {
        postCount = document.querySelectorAll(`#${project} .card-post:not(.removed):not(.filtered)`).length;
      }
      document.getElementById(`${project}-count`).innerHTML = `(${postCount})`;
    }
  });
}


// expand/collapse categories
function expandCategories(expand=null) {
  if (expand == null) {
    expand = JSON.parse(localStorage.getItem("expandCategories"));
    document.getElementById("expandCategories").checked = expand;
  }
  if (expand) {
    document.querySelectorAll("details.category").forEach((el) => {
      el.setAttribute("open", "");
    });
  } else {
    document.querySelectorAll("details.category").forEach((el) => {
    el.removeAttribute("open");    });
  }
  localStorage.setItem("expandCategories", JSON.stringify(expand));
}
