<template>

    <div class="materialContainer">
        <div class="box">

            <div class="title" v-if="loginMode">LOGIN</div>
            <div class="title" v-else>REGISTER</div>

            <div class="input">
                <input type="text" name="name" placeholder="Username" id="name" v-model="username">
                <span class="spin"></span>
            </div>

            <div class="input">
                <input type="password" name="pass" placeholder="Password" id="pass" v-model="password">
                <span class="spin"></span>
            </div>

            <div class="button login" v-if="loginMode">
                <button @click="login()"><span>Login</span> <i class="fa fa-check"></i></button>
            </div>

            <div class="button login" v-else>
                <button @click="register()"><span>Register</span> <i class="fa fa-check"></i></button>
            </div>

            <p class="pass-forgot"  @click="loginMode = false" v-if="loginMode">
                Don't have an account? Register here
            </p>
            <p class="pass-forgot"  @click="loginMode = true" v-else>
                You already have an account. Login here
            </p>

            <div class="pass-forgot" v-if="errors.length">
                <br>
                <p class="title title-2">Correct the following errors:</p>
                <ul>
                    <li v-for="error in errors" :key="error">{{ error }}</li>
                </ul>
            </div>

        </div>
    </div>
</template>

<script>
export default ({
    name: 'Auth',
    data() {
        return {
            username: '',
            password: '',
            token: '',
            errors: [],
            loginMode: true
        }
    },
    methods: {
        login() {
            if (!this.checkForm()) 
                return 
            fetch(`http://127.0.0.1:8000/auth/`, {
                method: 'post',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({username: this.username, password: this.password}) 
            })
            .then(res => res.json())
            .then(res => {
                if (res.token) {
                    this.token = res.token;
                    this.$cookie.set('auth-token', this.token, { expires: '1M' });
                    this.$router.push("/"); 
                } else {
                    alert('Error')
                }
            })
            .catch(error => console.log(error))
        },
        register() {
            if (!this.checkForm()) 
                return 
            fetch(`http://127.0.0.1:8000/core/users/`, {
                method: 'post',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({username: this.username, password: this.password}) 
            })
            .then(() => {
                this.login()
            })
            .catch(error => console.log(error))
        },
        checkForm() {
            this.errors = [];
            if(!this.username) 
                this.errors.push("Username is required.");
            if(!this.password) 
                this.errors.push("Password is required.");
            if(this.password && this.password.length < 6 && !this.loginMode) 
                this.errors.push("Password should be at least 6 characters long");

            if(this.errors.length)
                return false;

            return true;
        }
    },
    created() {
        if (this.$cookie.get("auth-token")) {
            this.$router.push("/")
        }
    },
})
</script>



<style scoped>
    p {
        cursor: pointer;
    }
    .title-2 {
        line-height: 26px;
        font-size: 24px;
        font-weight: 400;
    }
</style>
