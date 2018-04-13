console.log("load websocket script...")

editDom = {}

editDom.addAnswer = function(title,pk)
{
    htmlAnswer =`
        <div id="answer`+pk+`">
            <div class="line-answer">
                <div class="remplissage" id="remplissage-${pk}" style="width: 0%"></div>
                <div class="content"><input type="checkbox" value="`+pk+`" id='answer`+pk+`radio' onclick="clickRadioAnswer(this)"><label for='answer`+pk+`radio' class="radio"></label>`+ title +`</div>`
            
    if(is_admin)
        htmlAnswer += `<img src="/static/webApp/imgs/garbage.svg" class="delete" onclick="clickDeleteAnswer(`+pk+`)"/>`
        
    htmlAnswer += `
            </div>
            <div class="list-users">
                <span class="list-login-user" id="list-login-user-${pk}">
                </span>
                <span class="list-anonymous-user" id="list-anonymous-user-${pk}">
                </span>
            </div>
        </div>`
    document.querySelector('#list-answer').innerHTML += htmlAnswer
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
    if(e.target.id != "title")
        editDom.saveTitle()
    
    if(e.target.id != "description")
        editDom.saveDescription()
}


editDom.addUserLoginOnAnswer = function(username,answer,user_pk,state)
{
    userDom = document.querySelector('#user-login-'+user_pk+"-"+answer);
    answer_dom = document.querySelector('#list-login-user-'+answer);
    check_dom = document.querySelector('#answer'+answer+'radio');
    if(userDom && !state && answer_dom)//delete user
    {
        userDom.parentNode.removeChild(userDom);
        check_dom.checked = false
    }
    else if(!userDom && state && answer_dom)//add user
    {
        answer_dom.innerHTML += `
            <span class="user" id="user-login-`+ user_pk +`-`+ answer +`">`+ username +`</span>
        `

        check_dom.checked = true
    }
}

editDom.addUserAnonymOnAnswer = function(username,answer,user_pk,state)
{
    user_dom = document.querySelector('#user-anonymous-'+user_pk+"-"+answer);
    answer_dom = document.querySelector('#list-anonymous-user-'+answer);

    if(user_dom && !state && answer_dom)//delete user
    {
        user_dom.parentNode.removeChild(user_dom);
    }
    else if(!user_dom && state && answer_dom)//add user
    {
        answer_dom.innerHTML += `
            <span class="user" id="user-anonymous-`+ user_pk +`-`+ answer +`">`+ username +`</span>
        `
    }
}

editDom.changeStat = function(number_accounts,number_vote,number_views)
{
    document.querySelector('#number-accounts').innerText = number_accounts
    document.querySelector('#number-vote').innerText = number_vote
    document.querySelector('#number-views').innerText = number_views
}

editDom.changePercentage = function(percentage,answer,number_vote)
{
    old_number_vote = document.querySelector('#number-vote').innerText
    document.querySelector('#remplissage-'+answer).style.width=percentage+"%"

    if(old_number_vote != number_vote)
    {
        remplissage_elements = document.getElementsByClassName('remplissage')
        console.log(remplissage_elements)
        for(element of remplissage_elements)
        {
            var old_percentage = element.style.width.slice(0, -1);
            var new_percentage = (old_percentage * old_number_vote)/number_vote
            element.style.width=new_percentage+"%"
        }
    }

}

var answerSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/poll/'+poll_token+'/answer/');

answerSocket.onmessage = function(e) 
{
    var data = JSON.parse(e.data);
    var data_type = data['type'];
    var message = data['message'];

    switch(data_type) {
        case 'new_answer':
            editDom.addAnswer(message,data['pk'])
        break;
        case 'new_title':
            editDom.changeTitle(message)
        break;
        case 'new_description':
            editDom.changeDescription(message)
        break;
        case 'new_check_answer':
            editDom.changePercentage(data['percentage'],data['answer'],data['number_vote'])
            editDom.changeStat(data['number_accounts'],data['number_vote'],data['number_views'])
            if (data['is_login'])
                editDom.addUserLoginOnAnswer(data['username'],data['answer'],data['user_pk'],data['state'])
            else
                editDom.addUserAnonymOnAnswer(data['username'],data['answer'],data['user_pk'],data['state'])
        break;
        case 'new_option':
            if (message == "annonymous_can_add_answer")
                document.querySelector('#option-annonymous-can-add-answer').checked = data['value']
            else if(message == "annonymous_can_answer")
                document.querySelector('#option-annonymous-can-answer').checked = data['value']
        break;
        case 'delete_answer':
            answer = document.querySelector('#answer'+data['answer'])
            answer.parentNode.removeChild(answer);
        break;


    }
};

answerSocket.onclose = function(e) 
{
    console.error('Chat socket closed unexpectedly');
    document.querySelector('#error').style.display = "block"
};

document.querySelector('#answer-input').onkeyup = function(e) 
{
    if (e.keyCode === 13) 
    {  // enter, return
        document.querySelector('#answer-submit').click();
    }
};


document.querySelector('#option-annonymous-can-add-answer-label').onclick = function(e) 
{
    var value = !document.querySelector('#option-annonymous-can-add-answer').checked;
    
    answerSocket.send(JSON.stringify({
        'type': 'new_option',
        'message': 'annonymous_can_add_answer',
        'value':value
    }));

    console.log(value)
};

document.querySelector('#option-annonymous-can-answer-label').onclick = function(e) 
{
    var value = !document.querySelector('#option-annonymous-can-answer').checked;
    
    answerSocket.send(JSON.stringify({
        'type': 'new_option',
        'message': 'annonymous_can_answer',
        'value':value
    }));
    console.log(value)
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

function clickRadioAnswer(element)
{
    value = element.value
    answerSocket.send(JSON.stringify({
        'type': 'new_check_answer',
        'answer': value,
        'checked': element.checked
    }));
}

function clickDeleteAnswer(value)
{
    answerSocket.send(JSON.stringify({
        'type': 'delete_answer',
        'answer': value,
    }));
}