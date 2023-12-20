<template>
    <el-container id="container">
        <!-- Title -->
        <el-header id="header">
            <el-button type="primary" @click="this.isSelecting = !this.isSelecting" style="margin-left: 10px" circle>
                <el-icon><ChatDotRound /> </el-icon>
            </el-button>
            <h1 id="title">{{ curRole.label }}</h1>

            <el-button type="primary" @click="this.showRolePromptDialog = true" style="margin-right: 10px" circle>
                <el-icon><Setting /> </el-icon>
            </el-button>
        </el-header>

        <div id="content-container">
            <!-- select the role of bot-->
            <el-aside v-show="this.isSelecting" style="max-width: fit-content">
                <!-- @select call-back function, index: value -->
                <el-menu @select="changeRole" :default-active="String(this.curRoleId)" style="padding: 15px 0 0 15px; height: 100%">
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
                    <InfiniteLoading @infinite="handleScroll" :top="true" :identifier="curRole" target="#message-container">
                        <template #spinner> <span style="display: flex; justify-content: center; padding: 5px; color: gray"> loading</span> </template>
                        <template #complete><div></div> </template>
                    </InfiniteLoading>
                    <div v-for="[i, item] of curMessageList.entries()" :key="i" id="message-list">
                        <div class="profile">
                            <el-image :src="curRoleProfileUrl" v-if="item.role == 'assistant'" class="profile" style="border-radius: 50%"></el-image>
                        </div>
                        <div class="message" :id="item.role">
                            <div v-loading="checkNeedLoading(i)" style="min-width: 30px" element-loading-background="#f1f1f1">
                                <span>{{ item.content }}</span>
                            </div>
                        </div>
                    </div>
                    <!-- </ul> -->
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

    <RolePromptDialog title="自定义角色描述" v-if="showRolePromptDialog" :closed="() => (showRolePromptDialog = false)" :bot-role="curRole.name"></RolePromptDialog>
</template>

<script>
import { Right, ChatDotRound, Setting } from '@element-plus/icons-vue'
import { sendMessage, getNewestMessages } from '../api/message'
import { ref } from 'vue'
import InfiniteLoading from 'v3-infinite-loading'
import 'v3-infinite-loading/lib/style.css'

import RolePromptDialog from './RolePromptDialog.vue'

// https://github.com/element-plus/element-plus/pull/12484

export default {
    name: 'TalkRoom',
    components: {
        Right,
        ChatDotRound,
        Setting,
        InfiniteLoading,
        RolePromptDialog
    },
    data() {
        return {
            //init
            initRoleId: 0,
            curRoleId: -1,
            curRole: { name: 'parent' },
            curRoleProfileUrl: null,
            curMessageList: [],
            //status
            isSelecting: false,
            isReceiving: false,
            isCompeted: false,
            showRolePromptDialog: false,
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
    },
    methods: {
        // handle function
        async handleSend() {
            // directly return when meet empty input
            if (this.input.length == 0 || this.isReceiving) {
                return
            }

            this.pushUserMessage(this.input)
            const messageToSend = this.input
            this.input = ''

            // append empty message
            this.isReceiving = true
            this.pushAssistantMessage('')

            // receive message
            const phone = this.$store.state.userInfo.phone
            const result = await sendMessage(phone, this.curRole.name, messageToSend)
            if (!result.flag) {
                // this.pushAssistantMessage(result.data)
                this.modifyLastMessage('不好意思，我有点事情，稍后再回复你。')
                this.isReceiving = false
                return
            }
            // update the message
            this.modifyLastMessage(result.data)
            this.isReceiving = false
        },
        async handleScroll($state) {
            if (this.isCompeted) {
                $state.complete()
            } else if (await this.pushHistoryMsg()) {
                this.isCompeted = true
                $state.complete()
            } else {
                $state.loaded()
            }
        },
        pushUserMessage(message) {
            this.pushMessage('user', message)
        },
        pushAssistantMessage(message) {
            this.pushMessage('assistant', message)
        },
        pushMessage(role, message) {
            this.curMessageList.push({
                role: role,
                content: message
            })
        },
        async pushHistoryMsg() {
            const curUserPhone = this.$store.state.userInfo.phone
            const result = await getNewestMessages(curUserPhone, this.curRole.name, 10, this.curMessageList.length)

            if (result.data.length == 0) {
                return true
            }
            this.curMessageList = result.data.concat(this.curMessageList)
            return false
        },
        modifyLastMessage(message) {
            const curRoleName = this.curRole.name
            this.curMessageList[this.curMessageList.length - 1].content = message
        },
        changeRole(index) {
            // backup previous message list
            this.messageList[this.curRole.name] = this.curMessageList.slice(-10)

            // modify current role and messageList
            this.curRole = this.roleList[index]
            this.curRoleProfileUrl = this.getProfileUrl(this.curRole.name)
            this.curMessageList = this.messageList[this.curRole.name]

            this.isCompeted = false
            this.isSelecting = false
        },
        getProfileUrl(name) {
            try {
                // return require(`../assets/profile/${name}.png`)
                return `/src/assets/profile/${name}.png`
            } catch (error) {
                // return require('../assets/profile/bot.jpg')
                return '/src/assets/profile/bot.jpg'
            }
        },
        checkNeedLoading(index) {
            return this.isReceiving && index === this.curMessageList.length - 1
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
    padding: 0 20px 10px 20px;
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
