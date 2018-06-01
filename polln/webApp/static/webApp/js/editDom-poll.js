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

editDom.changeDescription = function(content)
{
    desDom = document.querySelector('#description')
    desDom.innerText = content
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
        for(element of remplissage_elements)
        {
            var old_percentage = element.style.width.slice(0, -1);
            var new_percentage = (old_percentage * old_number_vote)/number_vote
            element.style.width=new_percentage+"%"
        }
    }

}

editDom.changeOptionAnnonymousCanAnswer = function(value)
{
    document.querySelector('#option-annonymous-can-answer').checked = value
    if(!is_login && !is_admin)
    {
        checkboxs = document.getElementsByClassName('option-checkbox')
        for(element of checkboxs)
        {
            console.log(element)
            if(value)
                element.removeAttribute("disabled")
            else
                element.setAttribute("disabled",'disabled')
        }
    }
}