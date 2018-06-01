console.log("load websocket script...")

var answerSocket = new WebSocket(url_ws);

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
                editDom.changeOptionAnnonymousCanAnswer(data['value'])
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

