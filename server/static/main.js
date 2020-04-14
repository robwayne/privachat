$(document).ready(() => {
    var scrolled = false;
    function updateScroll(){
        if(!scrolled){
            var element = document.getElementById("chat-container");
            element.scrollTop = element.scrollHeight;
            scrolled = false;
        }
    }

    $("#chat-container").on('scroll', function(){
        scrolled=true;
    });

    setInterval(() => updateScroll(), 5000);

    $(".online-user").click(() => {
        $.getJSON('/test', data => {
            console.log(data);
        });
    })
});