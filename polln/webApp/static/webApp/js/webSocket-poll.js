console.log("load websocket script...")

editDom = {}

editDom.addAnswer = function(title)
{
    document.querySelector('#list-answer').innerHTML += `
        <div class="line-answer">
            <div class="remplissage remplissage-middle"></div>
            <div class="content"><input type="radio"><label class="radio"></label>`+ title +`</div>
        </div>
        <div class="list-users"></div>
    `
}

editDom.changeTitle = function(content)
{
    titleDom = document.querySelector('#title')
    titleDom.innerText = content
}

editDom.editTitle = function()
{
    if(is_admin)
    {
        titleDom = document.querySelector('#title')
        titleDom.contentEditable = true
        titleDom.classList.add("editable")
    }
}

editDom.saveTitle = function()
{
    titleDom = document.querySelector('#title')
    console.log(titleDom.contentEditable)
    if (titleDom.contentEditable && titleDom.contentEditable ==  "true")
    {
        titleDom.contentEditable = false
        titleDom.removeAttribute("contentEditable")
        titleDom.classList.remove("editable")

        answerSocket.send(JSON.stringify({
            'type': 'new_title',
            'message': titleDom.innerText
        }));
    }
}

editDom.editDescription = function()
{
    if(is_admin)
    {
        desDom = document.querySelector('#description')
        desDom.contentEditable = true
        desDom.classList.add("editable")
    }
}


editDom.changeDescription = function(content)
{
    desDom = document.querySelector('#description')
    desDom.innerText = content
}

editDom.saveDescription = function()
{
    desDom = document.querySelector('#description')
    if (desDom.contentEditable && desDom.contentEditable ==  "true")
    {
        desDom.contentEditable = false
        desDom.removeAttribute("contentEditable")
        desDom.classList.remove("editable")
        answerSocket.send(JSON.stringify({
            'type': 'new_description',
            'message': desDom.innerText
        }));
    }
}


editDom.clickOutside = function(e)
{
    console.log(e.target.id != "description")
    if(e.target.id != "title")
        editDom.saveTitle()
    
    if(e.target.id != "description")
        editDom.saveDescription()
}

//var roomName = {{ room_name_json }};

var answerSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/poll/'+poll_token+'/answer/');

answerSocket.onmessage = function(e) 
{
    console.log(e.data)
    var data = JSON.parse(e.data);
    console.log(data)
    var data_type = data['type'];
    var message = data['message'];

    switch(data_type) {
        case 'new_answer':
            editDom.addAnswer(message)
        break;
        case 'new_title':
            editDom.changeTitle(message)
        break;
        case 'new_description':
            editDom.changeDescription(message)
        break;
    }
};

answerSocket.onclose = function(e) 
{
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#answer-input').onkeyup = function(e) 
{
    if (e.keyCode === 13) 
    {  // enter, return
        document.querySelector('#answer-submit').click();
    }
};

document.querySelector('#title').onkeydown = function(e) 
{
    if (e.keyCode === 13) 
    {  // enter, return
        document.execCommand('insertHTML', false, '');
        editDom.saveTitle()
        return false
    }
};

/*
document.querySelector('#title').oninput = function()
{

}
*/

document.addEventListener('click', editDom.clickOutside, false);


document.querySelector('#description').onkeydown = function(e) 
{
    if (e.keyCode === 13) 
    {  // enter, return
        document.execCommand('insertHTML', false, '');
        editDom.saveDescription()
        return false
    }
};

document.querySelector('#answer-submit').onclick = function(e) {
    var messageInputDom = document.querySelector('#answer-input');
    var message = messageInputDom.value;
    answerSocket.send(JSON.stringify({
        'type': 'new_answer',
        'message': message
    }));

    messageInputDom.value = '';
};


document.querySelector('#description').onclick = function(e) {
    editDom.editDescription()
}

document.querySelector('#title').onclick = function(e) {
    editDom.editTitle()
}

