// button.js
document.addEventListener('DOMContentLoaded', function() {

    const userButton = document.getElementById('userAction');
    const loginButton = document.getElementById('loginAction');
    const openButton = document.getElementById('openAction');
    const signupButton = document.getElementById('signupAction');

    if(loginButton){
        loginButton.addEventListener('click', login);
    }   
    
    if(userButton){
        userButton.addEventListener('click', showUsers);
    }

    if(openButton){
        openButton.addEventListener('click', openDoor);
    }
    
    if(signupButton){
        signupButton.addEventListener('click', signUp);
    }

    function showUsers(){
        location.href='users.html'
    }

    function login(){
        location.href='login.html'
    }

    function openDoor(){
        alert('Door Open');
    }

    function signUp(){
        location.href='signup.html'
    }
});


