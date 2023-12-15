<template>
    <el-container id="container">
        <!-- Title -->
        <el-header id="header">
            <el-button type="primary" :onclick="handleSelect" style="margin-left: 10px" circle>
                <el-icon><ChatDotRound /> </el-icon>
            </el-button>
            <h1 id="title">{{ curRoleName }}</h1>

            <el-button type="primary" style="margin-right: 10px" circle>
                <el-icon><Setting /> </el-icon>
            </el-button>
        </el-header>

        <div id="content-container">
            <!-- select the role of bot-->
            <el-aside v-show="this.isSelecting" style="max-width: fit-content">
                <!-- @select call-back function, index: value -->
                <el-menu @select="handleCheckChangeRole" :default-active="String(this.curRoleId)" style="padding: 15px 0 0 15px; height: 100%">
                    <h2 style="margin-bottom: 15px; font-size: large">切换角色</h2>
                    <el-menu-item v-for="[i, role] of roleList.entries()" :key="i" :index="String(i)" style="padding: 0; margin-right: 15px">
                        <template #title>
                            <div style="display: flex; align-items: center">
                                <img :src="getProfileUrl(role.name)" class="profile" style="height: 36px; width: 36px" />
                                <span>{{ role.label }}</span>
                            </div>
                        </template>
                    </el-menu-item>
                    <a class="comment">v0.1.0 by Fucloud</a>
                </el-menu>
            </el-aside>

            <!-- talk content -->
            <el-main style="display: flex; flex-direction: column; justify-content: space-between; padding: 0">
                <!-- Messages Area-->
                <el-main id="message-container">
                    <div v-for="item in messageList" :key="item" id="message-list">
                        <div class="profile">
                            <el-image :src="curRoleProfileUrl" v-if="item.role == 'assistant'" class="profile" style="border-radius: 50%"></el-image>
                        </div>
                        <div class="message" :id="item.role">
                            <span>{{ item.content }}</span>
                        </div>
                    </div>
                </el-main>

                <!-- Talk  Area -->
                <el-footer id="talk-container">
                    <div id="talk-input">
                        <el-input v-model="input" type="textarea" :autosize="{ minRows: 1, maxRows: 2 }" resize="none" placeholder="输入文字与小助手交流"> </el-input>
                    </div>
                    <el-button :onclick="handleSend" type="primary" id="send-button" circle>
                        <el-icon><Right /></el-icon>
                    </el-button>
                </el-footer>
            </el-main>
        </div>
    </el-container>

    <!-- dialog -->
    <el-dialog title="提示" v-model="isChangingRole" style="min-width: 300px">
        <a>更换角色后，之前的聊天记录会被清除，你确定要更换吗？</a>
        <template #footer>
            <el-button @click="isChangingRole = false">取消</el-button>
            <el-button type="primary" @click="changeRole(this.roleToChange)"> 确定 </el-button>
        </template>
    </el-dialog>
</template>

<script>
import { Right, ChatDotRound, Setting } from '@element-plus/icons-vue'
import { chat } from '@/api'

export default {
    name: 'TalkRoom',
    components: {
        Right,
        ChatDotRound,
        Setting
    },
    data() {
        return {
            //init
            initRoleId: 1,
            //status
            curRoleId: -1,
            curRoleName: '',
            curRoleProfileUrl: null,
            isSelecting: false,
            roleList: [
                {
                    label: '父母',
                    name: 'parent'
                },
                {
                    label: '闺蜜',
                    name: 'bestie'
                },
                {
                    label: '朋友',
                    name: 'friend'
                },
                {
                    label: '心理医生',
                    name: 'doctor'
                }
            ],

            // dialog
            isChangingRole: false,
            roleToChange: -1,

            // talking
            input: '',
            messageList: [
                // {
                //     role: 'user',
                //     content: '你好'
                // },
                // {
                //     role: 'assistant',
                //     content: '你好，请问有什么可以帮到你的'
                // }
            ]
        }
    },
    mounted() {
        this.changeRole(this.initRoleId)
    },
    methods: {
        async handleSend() {
            // directly return when meet empty input
            if (this.input.length == 0) {
                return
            }

            this.pushUserMessage(this.input)
            this.input = ''

            const result = await chat(this.messageList)
            if (!result.flag) {
                this.pushAssistantMessage(result.data)
                return
            }

            this.pushAssistantMessage(result.data)
        },
        handleSelect() {
            this.isSelecting = !this.isSelecting
        },
        handleCheckChangeRole(index) {
            if (this.curRoleId == index) {
                return
            }

            this.isChangingRole = true
            this.roleToChange = index
        },
        pushUserMessage(message) {
            this.pushMessage('user', message)
        },
        pushAssistantMessage(message) {
            this.pushMessage('assistant', message)
        },
        pushMessage(role, message) {
            this.messageList.push({
                role: role,
                content: message
            })
        },
        changeRole(index) {
            this.curRoleId = index
            this.curRoleName = this.roleList[index]['label']
            this.curRoleProfileUrl = this.getProfileUrl(this.roleList[index]['name'])

            // change the status of those component
            this.isChangingRole = false
            this.isSelecting = false
        },
        getProfileUrl(name) {
            try {
                return require(`@/assets/profile/${name}.png`)
            } catch (error) {
                return require('@/assets/profile/bot.jpg')
            }
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
}

#header {
    background-color: #409eff;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    /* justify-content: center; */
    justify-content: space-between;
    align-items: center;
}
#title {
    /* font-size: 12; */
    font-size: 20px;
    font-family: Arial, sans-serif;
    color: white;
    /* margin: 15px 0 0 0; */
}
#content-container {
    display: flex;
    flex-direction: row;
    height: 100%;
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
.profile {
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
.el-icon {
    font-size: 20px;
    color: white;
}
.comment {
    position: absolute;
    bottom: 0;
    font-size: small;
    color: gray;
    margin-bottom: 10px;
}
</style>
