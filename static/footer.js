var ScrollAmount;
var Footer = document.getElementById("Footer");

window.addEventListener("scroll", function() {
    ScrollAmount = window.scrollY;

    if (ScrollAmount > 60)
    {
        Footer.classList.add("Show");
        console.log("showing!");
    }
    else
    {
        Footer.classList.remove("Show");
        console.log("not showing.")
    }
});