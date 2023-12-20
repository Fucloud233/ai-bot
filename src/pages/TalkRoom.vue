<template>
    <MainLayout :title="curRole.label">
        <template #rightTool>
            <el-button type="primary" @click="this.showRolePromptDialog = true" style="margin-right: 10px" circle>
                <el-icon><Setting /> </el-icon>
            </el-button>
        </template>

        <template #main>
            <div id="message-container">
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
            </div>
        </template>

        <template #footer>
            <el-button @click="showCheckDelete = true" type="info" style="margin-right: 10px" class="talk-button" circle>
                <el-icon><Delete /></el-icon>
            </el-button>

            <div id="talk-container">
                <div id="talk-input">
                    <el-input v-model="input" type="textarea" :autosize="{ minRows: 1, maxRows: 1 }" resize="none" placeholder="输入文字与小助手交流"> </el-input>
                </div>
                <el-button @click="handleSend" type="primary" class="talk-button" circle>
                    <el-icon><Right /></el-icon>
                </el-button></div
        ></template>
    </MainLayout>

    <el-dialog title="提示" v-model="showCheckDelete" style="max-width: 300px; width: 80%">
        <p>聊天记录删除后将无法恢复，你确定要删除吗？</p>
        <template #footer>
            <el-button type="danger" @click="handleDelete">确定</el-button>
            <el-button @click="showCheckDelete = false"> 取消 </el-button>
        </template>
    </el-dialog>

    <RolePromptDialog title="自定义角色描述" v-if="showRolePromptDialog" :closed="() => (showRolePromptDialog = false)" :bot-role="curRole.name"></RolePromptDialog>
</template>

<script>
import { Right, ChatDotRound, Setting, Delete } from '@element-plus/icons-vue'
import { sendMessage, getNewestMessages, deleteAllMessage } from '../api/message'
import { ref } from 'vue'
import InfiniteLoading from 'v3-infinite-loading'
import 'v3-infinite-loading/lib/style.css'

import RolePromptDialog from '../components/RolePromptDialog.vue'
import MainLayout from '../components/MainLayout.vue'

// https://github.com/element-plus/element-plus/pull/12484

export default {
    name: 'TalkRoom',
    components: {
        Right,
        ChatDotRound,
        Setting,
        Delete,
        InfiniteLoading,
        RolePromptDialog,
        MainLayout
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
            showCheckDelete: false,

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
        async handleDelete() {
            if (this.curMessageList.length != 0) {
                this.curMessageList = []
                await deleteAllMessage(this.$store.state.userInfo.phone, this.curRole.name)
            }

            this.showCheckDelete = false
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
#message-container {
    display: flex;
    flex-direction: column;
    /* padding: 0 20px 10px 20px; */
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
    width: 100%;
    padding: 5px;
    background-color: white;
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
.talk-button {
    min-width: 36px;
    min-height: 36px;
    margin: 0 5px;
}
.el-icon {
    font-size: 24px;
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
