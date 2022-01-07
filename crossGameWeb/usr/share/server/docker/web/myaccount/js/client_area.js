var elements = ["computers", "account"];

function Display(name)
{
    history.pushState({}, null, name); 
}

window.addEventListener('locationchange', () =>
{
    var name = window.location.pathname.split("/")[2];
    name = name.length > 0 ? name : "account";
    
    var active = document.getElementsByClassName("active")[0];
    
    if (active.id != name + "_link")
    {
        var clicked = document.getElementById(name + "_link");

        active.classList.remove("active");
        active.classList.add("link");
        clicked.classList.add("active");
        clicked.classList.remove("link");

        document.getElementById(name).style.display = "block";
        document.getElementById(active.id.split("_link")[0]).style.display = "none";
    }
});