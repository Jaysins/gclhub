var error = document.getElementById('error')
$('#form').submit(function(e){
    let name = document.getElementById('name');
    let password = document.getElementById('password');
    let confirm = document.getElementById('confirm');
    if(name.value.length <= 3){
        error.innerText = 'Name too short';
        return false;
    }    
    if (password.value.length <= 6){
        error.innerText = 'Password too short';
        return false;
    }
    if (password.value.length !== confirm.value.length){
        error.innerText = 'passwords dont match';
        return false
    }
})
