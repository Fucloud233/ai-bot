<template>
    <el-container id="container">
        <!-- Title -->
        <el-header id="header">
            <el-button type="primary" @click="this.isSelecting = !this.isSelecting" style="margin-left: 10px" circle>
                <el-icon><ChatDotRound /> </el-icon>
            </el-button>
            <h1 id="title">{{ curRole.label }}</h1>

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
            <div style="display: flex; flex-direction: column; padding: 0; width: 100%">
                <!-- Messages Area-->
                <el-main id="message-container" style="overflow: auto">
                    <el-scrollbar @scroll="handleScroll" :always="true" ref="scrollbar" style="padding-right: 20px">
                        <!-- it must use ul and li for v-infinite-scroll -->
                        <!-- <ul v-infinite-scroll="loadNewMessages" :infinite-scroll-disabled="isLoadingNewMessages" style="padding: 0; display: flex; flex-direction: column-reverse"> -->
                        <li v-for="[i, item] of messageList[curRole.name].entries()" :key="i" id="message-list">
                            <div class="profile">
                                <el-image :src="curRoleProfileUrl" v-if="item.role == 'assistant'" class="profile" style="border-radius: 50%"></el-image>
                            </div>
                            <div class="message" :id="item.role">
                                <div v-loading="checkNeedLoading(i)" style="min-width: 30px" element-loading-background="#f1f1f1">
                                    <span>{{ item.content }}</span>
                                </div>
                            </div>
                        </li>
                        <!-- </ul> -->
                    </el-scrollbar>
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
            </div>
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
import { chatWithRole } from '../api/api'
import { getNewestMessages } from '../api/db'
import { ref } from 'vue'

// https://github.com/element-plus/element-plus/pull/12484

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
            initRoleId: 0,
            //status
            curRoleId: -1,
            curRole: { name: 'null' },
            curRoleProfileUrl: null,
            isSelecting: false,
            isReceiving: false,
            isLoadingNewMessages: false,

            // dialog
            isChangingRole: false,
            roleToChange: -1,

            // talking
            input: ''
        }
    },
    setup() {
        // role
        const roleList = ref([
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
        ])
        var messageList = ref({})
        for (let role of roleList.value) {
            messageList.value[role.name] = []
        }

        // append a empty array for render
        messageList.value['null'] = []

        return {
            roleList,
            messageList
        }
    },
    async mounted() {
        this.changeRole(this.initRoleId)
        // this.getNewestMessages
        await this.pushHistoryMsg()
        // set a very big number to scroll to the bottom
        this.$refs.scrollbar.setScrollTop(999999999)

        for (let i = 0; i < 20; i++) {
            this.messageList[this.curRole.name].push({
                role: 'user',
                content: i
            })
        }
    },
    methods: {
        // handle function
        async handleSend() {
            // directly return when meet empty input
            if (this.input.length == 0 || this.isReceiving) {
                return
            }

            this.pushUserMessage(this.input)
            this.input = ''

            // append empty message
            this.isReceiving = true
            this.pushAssistantMessage('')

            // receive message
            const roleName = this.roleList[this.curRoleId].name
            const result = await chatWithRole(this.messageList.slice(0, -1), roleName)
            if (!result.flag) {
                // this.pushAssistantMessage(result.data)
                this.modifyLastMessage('不好意思，我有点事情，稍后再回复你。')
                return
            }
            // update the message
            this.modifyLastMessage(result.data)
            this.isReceiving = false
        },
        handleCheckChangeRole(index) {
            if (this.curRoleId == index) {
                return
            }

            this.isChangingRole = true
            this.roleToChange = index
        },
        async handleScroll({ scrollTop }) {
            if (scrollTop != 0) {
                return
            }

            await this.pushHistoryMsg()
            this.$refs.scrollbar.setScrollTop(1)
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
        async pushHistoryMsg() {
            const curRoleName = this.curRole.name
            const result = await getNewestMessages('12345678910', this.messageList[curRoleName].length)
            console.log(result)
            // update the messageList

            // this.messageList[curRoleName] = this.messageList[curRoleName].concat(result.data)

            // this.messageList[curRoleName] = result.data.concat(this.messageList[curRoleName])
        },
        modifyLastMessage(message) {
            this.messageList[this.messageList.length - 1].content = message
        },
        async loadNewMessages() {
            console.log('hello')
            // this.isLoadingNewMessages = true
            // const curRoleName = this.curRole.name
            // // get newest message from database
            // const result = await getNewestMessages('12345678910', this.messageList[curRoleName].length)
            // // update the messageList
            // this.messageList[curRoleName] = this.messageList[curRoleName].concat(result.data)
            // this.isLoadingNewMessages = false
        },
        changeRole(index) {
            this.curRoleId = index
            this.curRole = this.roleList[index]
            this.curRoleProfileUrl = this.getProfileUrl(this.curRole.name)

            // change the status of those component
            this.isChangingRole = false
            this.isSelecting = false
        },
        getProfileUrl(name) {
            try {
                // return require(`../assets/profile/${name}.png`)
            } catch (error) {
                // return require('../assets/profile/bot.jpg')
            }
        },
        checkNeedLoading(index) {
            return this.isReceiving && index === this.messageList.length - 1
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

    height: 8%;
    padding: 0;
    margin: 0;

    display: flex;
    flex-direction: row;
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
    height: 92%;
}

#message-container {
    display: flex;
    flex-direction: column;
    padding: 0 0 10px 20px;
    max-height: 90%;
    width: 100%;
}
#message-list {
    display: flex;
    margin-top: 10px;
}

#message-container .message {
    display: flex;
    padding: 10px 12px;
    border-radius: 10px;
    max-width: 60%;
    font-size: 16px;

    /* modify the loading icon */
    /* :deep(.el-loading-spinner .path) {
        stroke: black;
    } */
    :deep(.el-loading-spinner .circular) {
        width: 30px;
    }
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
