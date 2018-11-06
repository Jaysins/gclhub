var error = document.getElementById('error');
var btn = document.getElementById('load');
var spin = document.getElementById('spin');
$('#form').submit(function(e){    
    error.className = 'alert '
    btn.disabled = true;
    spin.className = 'fa fa-spinner fa-spin';    
    let name = document.getElementById('name');
    let password = document.getElementById('password');
    let confirm = document.getElementById('confirm');
    var willReturn = true;
    if(name.value.length <= 3){
        error.innerText = 'Name too short';
        error.className += 'alert-danger'
        willReturn = false
    }    
    else if (password.value.length <= 6){
        error.innerText = 'Password too short';
        error.className += 'alert-danger'
        willReturn = false;
    }
    else if ((confirm !== null) && (password.value.length !== confirm.value.length)){
        error.innerText = 'passwords dont match';
        error.className += 'alert-danger'
        willReturn = false;
    }
    if (willReturn === false){        
        btn.disabled = false;
        spin.className = '';
    }    
    return willReturn
})
