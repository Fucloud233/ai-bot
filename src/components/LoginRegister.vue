<template>
    <div class="main">
        <h1 style="color: white; margin-top: 20%">Ai解压小助手</h1>
        <div class="container">
            <div v-if="isLogin">
                <h2>登录</h2>
                <el-form ref="loginForm" :model="loginInfo" :rules="rules" label-width="80px" label-position="left" class="form">
                    <el-form-item label="电话" prop="phone"> <el-input v-model="loginInfo.phone" /></el-form-item>
                    <el-form-item label="密码" prop="password"> <el-input v-model="loginInfo.password" /></el-form-item>
                </el-form>
                <div>
                    <el-button type="primary" @click="login">确定</el-button>
                    <el-button type="info" @click="toRegister">注册</el-button>
                </div>
            </div>
            <div v-if="!isLogin">
                <h2>注册</h2>
                <el-form ref="registerForm" :model="registerInfo" :rules="rules" label-width="80px" label-position="left" class="form">
                    <el-form-item label="电话" prop="phone"> <el-input v-model="registerInfo.phone" /></el-form-item>
                    <el-form-item label="性别" prop="isMale">
                        <el-radio-group v-model="registerInfo.isMale">
                            <el-radio :label="1" size="large">男</el-radio>
                            <el-radio :label="2" size="large">女</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input show-password v-model="registerInfo.password" />
                    </el-form-item>
                    <el-form-item label="确认密码" prop="passwordAgain">
                        <el-input show-password v-model="registerInfo.passwordAgain" />
                    </el-form-item>
                </el-form>
                <div style="margin-top: 30px">
                    <el-button type="primary" @click="register">注册</el-button>
                    <el-button type="info" @click="returnLogin">取消</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        // validate passwd and passwdAgain
        const validatePasswdSame = (rule, value, callback) => {
            if (value === '') {
                callback()
            } else if (value !== this.registerInfo.password) {
                callback(new Error('两次输入密码不一致'))
            } else {
                callback()
            }
        }

        return {
            // status
            isLogin: true,

            loginInfo: {
                phone: '',
                password: ''
            },
            registerInfo: {
                phone: '18212345678',
                isMale: 1,
                password: '123456',
                passwordAgain: '123456'
            },
            rules: {
                phone: [
                    { required: true, message: '手机号必填', trigger: 'blur' },
                    { pattern: /^1[3456789]\d{9}$/, message: '手机号码格式不正确', trigger: 'blur' }
                ],
                isMale: [{ required: true, type: 'integer', message: '请选择性别', trigger: 'blur' }],
                password: [
                    {
                        required: true,
                        message: '密码必填',
                        trigger: 'blur'
                    },
                    {
                        min: 6,
                        max: 18,
                        message: '密码必须在6到16位之间'
                    }
                ],
                passwordAgain: [
                    {
                        required: true,
                        message: '密码必填',
                        trigger: 'blur'
                    },
                    {
                        min: 6,
                        max: 18,
                        message: '密码必须在6到16位之间'
                    },
                    {
                        required: true,
                        validator: validatePasswdSame
                    }
                ]
            }
        }
    },
    methods: {
        login() {
            this.$refs.loginForm.validate((valid) => {
                if (!valid) {
                    return
                }
                // TODO: check phone and password

                this.loginInfo = {}
                this.$router.push('/talk')
            })
        },
        toRegister() {
            this.loginInfo = {}
            this.isLogin = false
        },
        register() {
            this.$refs.registerForm.validate((valid) => {
                if (!valid) {
                    return
                }

                this.loginInfo.phone = this.registerInfo.phone
                this.isLogin = true
                this.registerInfo = {}
            })
        },
        returnLogin() {
            this.isLogin = true
            this.registerInfo = {}
        }
    }
}
</script>

<style scoped>
.main {
    display: flex;
    align-items: center;
    flex-direction: column;

    background-color: #409eff;
    height: 100%;
}
.container {
    display: flex;
    align-items: center;
    justify-content: start;
    flex-direction: column;
    text-align: center;

    max-width: 300px;
    border-radius: 10px;
    padding: 10px 15px 30px 15px;
    background-color: white;
}
.form {
    margin: 0 20px 0 20px;
}
.el-input {
    width: 200px;
}
</style>
