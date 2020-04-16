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

    const openPrivateChat = () => {
        const ids = event.target.id;
        const author_id = ids.split('-')[0];
        const receiver_id = ids.split('-')[1];
        const chatUrl = '/chat/'+author_id+'/'+receiver_id;
        location.href = chatUrl; // redirect to /chat/<author_id>/<receiver_id>
    };

    // whenever a user clicks another users name
    // deconstruct the id of the div clicked and get the users' ids
    // these ids are then used to contruct the link to the chat
    $(".online-user").click((event) => openPrivateChat())

    $(".offline-user").click((event) => openPrivateChat())
});