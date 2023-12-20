<template>
    <MainLayout :title="curRoleLabel">
        <template #leftTool>
            <el-button type="primary" @click="$router.push('/main')" circle>
                <el-icon><ArrowLeft /> </el-icon>
            </el-button>
        </template>
        <template #rightTool>
            <el-button type="primary" @click="this.showRolePromptDialog = true" circle>
                <el-icon><Setting /> </el-icon>
            </el-button>
        </template>

        <template #main>
            <div id="message-container">
                <InfiniteLoading @infinite="handleScroll" :top="true" target="#message-container">
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
            <div class="footer">
                <el-button @click="showCheckDelete = true" type="info" style="margin-right: 10px" class="talk-button" circle>
                    <el-icon><Delete /></el-icon>
                </el-button>

                <div id="talk-container">
                    <div id="talk-input">
                        <el-input v-model="input" type="textarea" :autosize="{ minRows: 1, maxRows: 1 }" resize="none" placeholder="输入文字与小助手交流"> </el-input>
                    </div>
                    <el-button @click="handleSend" type="primary" class="talk-button" circle>
                        <el-icon><Right /></el-icon>
                    </el-button>
                </div>
            </div>
        </template>
    </MainLayout>

    <el-dialog title="提示" v-model="showCheckDelete" style="max-width: 300px; width: 80%">
        <p>聊天记录删除后将无法恢复，你确定要删除吗？</p>
        <template #footer>
            <el-button type="danger" @click="handleDelete">确定</el-button>
            <el-button @click="showCheckDelete = false"> 取消 </el-button>
        </template>
    </el-dialog>

    <RolePromptDialog title="自定义角色描述" v-if="showRolePromptDialog" :closed="() => (showRolePromptDialog = false)" :bot-role="curRole"></RolePromptDialog>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

import { Right, ArrowLeft, Setting, Delete } from '@element-plus/icons-vue'
import InfiniteLoading from 'v3-infinite-loading'
import 'v3-infinite-loading/lib/style.css'

import RolePromptDialog from '../components/RolePromptDialog.vue'
import MainLayout from '../components/MainLayout.vue'
import { sendMessage, getNewestMessages, deleteAllMessage } from '../api/message'
import { getRoleLabel, getRoleProfileUrl } from '../utils'

// https://github.com/element-plus/element-plus/pull/12484

export default {
    name: 'TalkRoom',
    components: {
        ArrowLeft,
        Right,
        Setting,
        Delete,
        InfiniteLoading,
        RolePromptDialog,
        MainLayout
    },
    data() {
        return {
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
        const curRole = ref(useRoute().params.role)
        const curRoleLabel = ref(getRoleLabel(curRole.value))
        const curRoleProfileUrl = ref(getRoleProfileUrl(curRole.value))

        return { curRole, curRoleLabel, curRoleProfileUrl }
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
            const result = await sendMessage(phone, this.curRole, messageToSend)
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
                await deleteAllMessage(this.$store.state.userInfo.phone, this.curRole)
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
            const result = await getNewestMessages(curUserPhone, this.curRole, 10, this.curMessageList.length)

            if (result.data.length == 0) {
                return true
            }
            this.curMessageList = result.data.concat(this.curMessageList)
            return false
        },
        modifyLastMessage(message) {
            this.curMessageList[this.curMessageList.length - 1].content = message
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
.footer {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
    height: 100%;
}
</style>
