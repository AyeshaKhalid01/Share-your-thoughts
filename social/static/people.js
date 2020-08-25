/* ********************************************************************************************
   | Handle Submiting Friend Requests - called by $('.like-button').click(submitLike)
   ********************************************************************************************
   */
function frResponse(data,status) {
    if (status == 'success') {
        // reload page to update like count
        location.reload();
    }
    else {
        alert('failed to create friend request ' + status);
    }
}

function friendRequest(event) {
    // the id of the current button, should be fr-name where name is valid username
//    this.disabled = true
    let frID = event.target.id;
    //document.getElementById(buttonid).disabled = true;
    let json_data = { 'frID' : frID };
    // globally defined in messages.djhtml using i{% url 'social:like_view' %}
    let url_path = friend_request_url;
    // AJAX post
    $.post(url_path,
           json_data,
           frResponse);
}

/* ********************************************************************************************
   | Handle Requesting More People - called by $('#more-ppl-button').click(submitMorePpl)
   ********************************************************************************************
   */
function morePplResponse(data,status) {
    if (status == 'success') {
        // reload page to display new Post
        location.reload();
    }
    else {
        alert('failed to request more ppl' + status);
    }
}
