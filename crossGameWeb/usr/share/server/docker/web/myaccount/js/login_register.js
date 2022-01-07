function Swap(name)
{
    history.pushState({}, null, name);
}

window.addEventListener('locationchange', async() =>
{
    var name = window.location.pathname.split("/")[2];

    container = document.getElementsByClassName("form-container")[0];
    container.style.top = '10%';
    container.style.opacity = '0';

    await new Promise(r => setTimeout(r, 250));
    
    current = name == "register" ? "login" : "register";
    
    document.getElementById(current).style.display = "none";
    document.getElementById(name).style.display = "block";

    container.style.top = '25%';
    container.style.opacity = '1';
});