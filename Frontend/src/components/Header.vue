<template>
    <div id="Header">
        <div class="top-left-edition">
            <span style="color:#21b3b9;font-weight:bold;font-size: 35px;">
                Paper Web
            </span>
        </div>
        <div id="word">
            Get started by uploading a pdf paper!
        </div>
    </div>
</template>

<style scoped>
#Header {
    background: #F2F6FC;
    padding: 20px 70px 20px 180px;
    margin: 0 auto;
}

#word {
    display: flex;
    justify-content: center;
    align-items: center;
    color: #FF7F00;
    font-size: 25px;
}

.top-left-edition span i {
    float: left;
    margin-right: 10px;
}

i,
input,
label {
    vertical-align: middle;
}

i {
    border: 0;
    display: block;
    cursor: pointer;
}

.top-left-edition span {
    float: left;
    font-size: 16px;
    color: #999999;
    line-height: 24px;
    margin-right: 40px;
}
</style>
