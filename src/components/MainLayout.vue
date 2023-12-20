<template>
    <el-container id="container">
        <el-header id="header">
            <div class="tool-container" style="margin-left: 10px">
                <slot name="leftTool"> </slot>
            </div>
            <h1 id="title">{{ title }}</h1>

            <div class="tool-container" style="margin-right: 10px">
                <slot name="rightTool"> </slot>
            </div>
        </el-header>

        <el-main><slot name="main"></slot> </el-main>

        <el-footer><slot name="footer"></slot> </el-footer>
    </el-container>
</template>

<script>
export default {
    name: 'MainLayout',
    props: {
        title: {
            type: String,
            default: 'Title'
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
    width: 100%;
}

#header {
    background-color: #409eff;

    height: 10%;
    padding: 0;
    margin: 0;

    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}
#title {
    font-size: 20px;
    font-family: Arial, sans-serif;
    color: white;
}
.el-main {
    display: flex;
    flex-direction: column;
    /* padding: 0 20px 10px 20px; */
    max-height: 90%;
    width: 100%;
}
.tool-container {
    min-width: 30px;
    width: 30px;
}

.el-icon {
    font-size: 24px;
    color: white;
}
.el-footer {
    flex-direction: row;
    height: 10%;
    padding: 10px;
    background: #f6f6f6;
}
</style>
