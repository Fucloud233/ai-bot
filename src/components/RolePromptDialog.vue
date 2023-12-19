<template>
    <el-dialog :title="title" v-model="isVisible" @closed="closed" style="width: 80%; max-width: 300px; padding-top: 10px">
        <p>请使用第二人称（“你”）的口吻描述你设想的角色。</p>
        <el-input v-loading="isLoading" :readonly="!isEditing" v-model="curRolePrompt" rows="5" type="textarea" placeholder=""></el-input>

        <template #footer>
            <el-button type="primary" @click="toEdit">{{ getPrimaryLabel() }}</el-button>
            <el-button @click="toCancel">返回</el-button>
        </template>
    </el-dialog>
</template>

<script>
import { getRolePrompt, postRolePrompt } from '../api/rolePrompt'

export default {
    name: 'RolePromptDialog',
    model: {
        prop: 'value',
        event: 'changeVisible'
    },
    props: {
        title: {
            type: String,
            default: '自定义角色描述'
        },
        botRole: {
            type: String
        },
        // using an callback function to listen close
        closed: {
            type: Function
        }
    },
    async mounted() {
        this.phone = this.$store.state.userInfo.phone

        this.isLoading = true
        const rolePrompt = await getRolePrompt(this.phone, this.botRole)

        this.curRolePrompt = rolePrompt
        this.originRolePrompt = rolePrompt
        this.isLoading = false
    },
    data() {
        return {
            phone: '',
            // botRole: '',

            isLoading: true,
            isVisible: true,
            isEditing: false,
            originRolePrompt: '',
            curRolePrompt: '',

            primaryLabel: '修改'
        }
    },
    methods: {
        async toEdit() {
            if (this.isEditing && this.curRolePrompt !== this.originRolePrompt.trim()) {
                this.isLoading = true
                const result = await postRolePrompt(this.phone, this.botRole, this.curRolePrompt)
                if (!result.flag) {
                    console.log('error')
                }
                this.isLoading = false
            }
            this.isEditing = !this.isEditing
        },
        toCancel() {
            if (this.isEditing) {
                this.curRolePrompt = this.originRolePrompt
                this.isEditing = !this.isEditing
            } else {
                this.isVisible = false
            }
        },
        getPrimaryLabel() {
            if (this.isEditing) {
                return '确定'
            } else {
                return '修改'
            }
        }
    }
}
</script>

<style scoped>
.el-dialog {
    /* padding: 10%; */
    min-width: 400px;
}

.el-input {
    min-height: 200px;
}
</style>
