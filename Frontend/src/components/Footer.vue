<template>
    <div id="Footer">
        <p>Develop by {{ author }}</p>
    </div>
</template>

<!-- 写法 1: 参见 HelloWorld.vue 的 script setup -->
<!-- 写法 2 -->
<script>
export default {
    data() {
        return {
            author: "Jerry Kwan"
        }
    }
}
</script>

<style scoped>
#Footer {
    background:#F2F6FC;
    padding: 2px;
    border-radius: 5px;
    height: 80px;
    margin: 0 auto;
    margin-top: 140px;
}

p {
    color: #21b3b9;
    text-align: center;
    margin: 30px auto;
    font-size: 1.1em;
}
</style>
