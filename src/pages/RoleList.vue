<template>
    <MainLayout title="Ai解压小助手">
        <template #main>
            <div v-for="[i, role] of roleList.entries()" :key="i" :index="String(i)" class="role-container">
                <el-button style="width: 100%; height: 50px; justify-content: start" text>
                    <template #icon>
                        <div style="display: flex; align-items: center; justify-content: start; width: 100%">
                            <img :src="getProfileUrl(role.name)" class="profile" />
                            <span style="font-style: normal">{{ role.label }}</span>
                        </div>
                    </template>
                </el-button>
            </div>
        </template>
        <template #footer>
            <div class="function-bar">
                <el-button text class="function-button">
                    <div style="display: flex; flex-direction: column; align-items: center">
                        <el-icon><ChatDotRound /></el-icon>
                        <span style="font-size: 10px; margin: 5px 0 0 0">聊天</span>
                    </div>
                </el-button>
                <el-button text class="function-button">
                    <div style="display: flex; flex-direction: column; align-items: center">
                        <el-icon><User /></el-icon>
                        <span style="font-size: 10px; margin: 5px 0 0 0">个人</span>
                    </div>
                </el-button>
            </div>
        </template>
    </MainLayout>
</template>

<script setup></script>

<script>
import MainLayout from '../components/MainLayout.vue'
import { ChatDotRound, User } from '@element-plus/icons-vue'
import { ref } from 'vue'

export default {
    name: 'RoleList',
    components: {
        MainLayout,
        ChatDotRound,
        User
    },
    setup() {
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

        return { roleList }
    },
    data() {},
    methods: {
        getProfileUrl(name) {
            return `/src/assets/profile/${name}.png`
        }
    }
}
</script>

<style scoped>
.role-container {
    margin: 8px 0 8px 0;
    padding-bottom: 5px;
    border-bottom: solid 1px #f1f1f1;
}
.profile {
    width: 40px;
    height: 40px;
    margin-right: 10px;
    border-radius: 5px;
}

.el-icon {
    font-size: 24px;
    /* color: white; */
}
.function-bar {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    height: 100%;
}
.function-button {
    min-width: 36px;
    min-height: 36px;
}
</style>
