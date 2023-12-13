<template>
    <el-container id="container">
        <el-header id="header">
            <h1 id="title">AI解压小助手</h1>
        </el-header>
        <el-main id="message-container">
            <div v-for="item in messageList" :key="item" id="message-list">
                <div id="bot-profile">
                    <el-image :src="botProfileUrl" v-if="item.role == 'assistant'" id="bot-profile" style="border-radius: 50%"></el-image>
                </div>
                <div class="message" :id="item.role">
                    <span>{{ item['message'] }}</span>
                </div>
            </div>
        </el-main>

        <el-footer id="talk-container">
            <div id="talk-input">
                <el-input v-model="input" type="textarea" :autosize="{ minRows: 1, maxRows: 2 }" resize="none" placeholder="输入文字与小助手交流"> </el-input>
            </div>
            <el-button type="primary" id="send-button" style="font-size: large" circle>
                <el-icon><Right /></el-icon>
            </el-button>
        </el-footer>
    </el-container>
</template>

<script>
import { Right } from '@element-plus/icons-vue'

export default {
    name: 'TalkRoom',
    components: {
        Right
    },
    data() {
        return {
            botProfileUrl: require('@/assets/botProfile.jpg'),
            input: '',
            messageList: [
                {
                    role: 'user',
                    message: '你好'
                },
                {
                    role: 'assistant',
                    message: '你好，请问有什么可以帮到你的'
                }
            ]
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#container {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-around;
}

#header {
    background-color: #409eff;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    justify-content: center;
}
#title {
    /* font-size: 12; */
    font-size: 20px;
    font-family: Arial, sans-serif;
    color: white;
    margin: 15px 0 0 0;
}

#message-container {
    display: flex;
    flex-direction: column;
    padding: 20px;
}
#message-list {
    display: flex;
}

#message-container .message {
    display: flex;
    padding: 10px 12px;
    margin-bottom: 10px;
    border-radius: 10px;
    max-width: 60%;
    font-size: 16px;
}
#assistant {
    margin-right: auto;
    color: black;
    background-color: #f1f1f1;
}
#user {
    margin-left: auto;
    color: white;
    background-color: #409eff;
}
#bot-profile {
    width: 40px;
    height: 40px;
    margin-right: 10px;
    border-radius: 50%;
}

#talk-container {
    display: flex;
    align-items: center;
    /* width: 100%; */
    padding: 5px;
    margin: 10px;
    min-height: 50px;
    border: solid 1px #409eff;
    border-radius: 12px;
}
#talk-input {
    width: 100%;
    :deep(.el-textarea__inner) {
        box-shadow: 0 0 0 0px;
        background-color: transparent;
    }
    :deep.el-textarea__inner:hover {
        box-shadow: 0 0 0 0px;
    }
}
#send-button {
    min-width: 36px;
    min-height: 36px;
    margin: 0 5px;
}
</style>
