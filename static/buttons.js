// button.js
document.addEventListener('DOMContentLoaded', function() {

    const userButton = document.getElementById('userButton');
    const loginButton = document.getElementById('loginButton');
    const openButton = document.getElementById('openButton');
    const signupButton = document.getElementById('signupButton');
    const navLoginButton = document.getElementById('navLoginButton');
    const navSignupButton = document.getElementById('navSignupButton');
    const navHomeButton = document.getElementById('navHomeButton');

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

    if(navLoginButton){
        navLoginButton.addEventListener('click', navLogin);
    }

    if(navSignupButton){
        navSignupButton.addEventListener('click', navSignup);
    }

    if(navHomeButton){
        navHomeButton.addEventListener('click', navHome);
    }

    function showUsers(){
        location.href='users.html'
    }

    async function login(){
        const user = document.getElementById('usrnameLog').value;
        const password = document.getElementById('pswordLog').value;

        const userdata = {
            username: user,
            password: password
        };

        try {
            const response = await fetch('/api/v1/auth/request', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(userdata)
            });

            if(response.status === 200) {
                const result = await response.json();
                alert(`Session ID: ${result.session_id}, Seed: ${result.seed}, Challenge: ${result.challenge}`);   
            } else {
                const result = await response.json();
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
        }
        
        const result = await response.json();
        alert('Respomse: ${result.message}')
    }

    function openDoor(){
        alert('Door Open');
    }

    async function signUp(){
        const user = document.getElementById('usrnameSign').value;
        const password = document.getElementById('pswordSign').value;
        
        const userData = {
            username: user,
            password_hash: password,
            seed: 123,
        };

        try {
            const response = await fetch('/api/v1/auth/create', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(userData)
            });

            if(response.status === 201) {
                const result = await response.json();
                alert(result.message);   
            } else {
                const result = await response.json();
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function navLogin(){
        location.href='login.html'
    }

    function navSignup(){
        location.href='signup.html'
    }

    function navHome(){
        location.href='index.html'
    }
});


