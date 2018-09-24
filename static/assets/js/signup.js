$('#form').submit(function(e){
    e.preventDefault()
    let name = document.getElementById('name');
    let password = document.getElementById('password');
    let confirm = document.getElementById('confirm');
    if(name.value.length <= 3){
        alert('Name too short');
        return false;
    }    
    if (password.value.length <= 6){
        alert('Password too short');
        return false;
    }
    if (password.value.length !== confirm.value.length){
        alert('passwords dont match');
    }
})
