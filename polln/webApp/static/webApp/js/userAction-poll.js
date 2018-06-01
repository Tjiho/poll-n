UserAction = {}



document.querySelector('#answer-input').onkeyup = function(e) 
{
    if (e.keyCode === 13) 
    {  // enter, return
        UserAction.submitAnswer()
    }
};


document.querySelector('#option-annonymous-can-add-answer-label').onclick = function(e) 
{
    UserAction.changeAnnonymousCanAddAnswer()
};

document.querySelector('#option-annonymous-can-answer-label').onclick = function(e) 
{
    UserAction.changeAnnonymousCanAnswer()
};

document.querySelector('#title').onkeydown = function(e) 
{
    if (e.keyCode === 13) 
    {  // enter, return
        UserAction.submitTitle()
        return false
    }
};

document.addEventListener('click', editDom.clickOutside, false);


document.querySelector('#description').onkeydown = function(e) 
{
    if (e.keyCode === 13) 
    {  // enter, return
        UserAction.submitDescrition()
        return false
    }
};

document.querySelector('#answer-submit').onclick = function(e) {
    UserAction.submitAnswer()
};

document.querySelector('#description').onclick = function(e) {
    UserAction.editDescription()
}

document.querySelector('#title').onclick = function(e) {
    UserAction.editTitle()
}


UserAction.submitDescrition = function()
{
    document.execCommand('insertHTML', false, '');
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

UserAction.submitTitle = function()
{
    document.execCommand('insertHTML', false, '');
    titleDom = document.querySelector('#title')
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

UserAction.changeAnnonymousCanAddAnswer = function()
{
    var value = !document.querySelector('#option-annonymous-can-add-answer').checked;
    
    answerSocket.send(JSON.stringify({
        'type': 'new_option',
        'message': 'annonymous_can_add_answer',
        'value':value
    }));

    console.log(value)
}

UserAction.changeAnnonymousCanAnswer = function()
{
    var value = !document.querySelector('#option-annonymous-can-answer').checked;
    
    answerSocket.send(JSON.stringify({
        'type': 'new_option',
        'message': 'annonymous_can_answer',
        'value':value
    }));
    console.log(value)
}

UserAction.submitAnswer = function()
{
    var messageInputDom = document.querySelector('#answer-input');
    var message = messageInputDom.value;
    answerSocket.send(JSON.stringify({
        'type': 'new_answer',
        'message': message
    }));
    messageInputDom.value = '';
}


UserAction.clickRadioAnswer = function(element)
{
    value = element.value
    answerSocket.send(JSON.stringify({
        'type': 'new_check_answer',
        'answer': value,
        'checked': element.checked
    }));
}

UserAction.clickDeleteAnswer = function(value)
{
    answerSocket.send(JSON.stringify({
        'type': 'delete_answer',
        'answer': value,
    }));
}

UserAction.editTitle = function()
{
    if(is_admin)
    {
        titleDom = document.querySelector('#title')
        titleDom.contentEditable = true
        titleDom.classList.add("editable")
    }
}


UserAction.editDescription = function()
{
    if(is_admin)
    {
        desDom = document.querySelector('#description')
        desDom.contentEditable = true
        desDom.classList.add("editable")
    }
}

UserAction.clickOutside = function(e)
{
    if(e.target.id != "title")
        UserAction.saveTitle()
    
    if(e.target.id != "description")
        UserAction.saveDescription()
}