function commentDisplay() {
    const com = document.getElementById("commentForm");
    const but = document.getElementById("commentButton");
    const add = document.getElementById("addComment");

    if (com.style.display === "none" || com.style.display === "") {
        com.style.display = "block";
    }
    if (but.style.display === "none" || but.style.display === "") {
        but.style.display = "block";
    }
    if (com.style.display = "block") {
        add.style.display = "none";
    }
}