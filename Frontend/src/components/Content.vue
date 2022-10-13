<template>
    <div id="Content">
        <!-- ToDo: add el-progress -->

        <!-- Part3: upload and table-->
        <div id="CT">
            <!-- upload -->
            <div id="CT_image">
                <el-card id="CT_image_1" class="box-card"
                    style="border-radius: 8px;width:800px;height:360px;margin-bottom:-30px;">
                    <div class="demo-image__preview1">
                        <div v-loading="loading" element-loading-text="上传中" element-loading-spinner="el-icon-loading">
                            <el-image :src="img_src_1" class="image_1" style="border-radius: 3px 3px 0 0"></el-image>
                        </div>
                        <div class="img_info_1" style="border-radius:0 0 5px 5px;">
                            <el-button v-show="showbutton" type="primary" v-on:click="true_upload">
                                Upload Pdf Paper
                                <input ref="upload" style="display: none" name="file" type="file" @change="update">
                            </el-button>
                        </div>
                    </div>
                </el-card>
            </div>

            <!-- table -->
            <div id="info_patient">
                <el-card style="border-radius: 8px;">
                    <el-tabs v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="References List" name="first">
                            <!-- 表格 -->
                            <el-table ref="singleTableRef" :data="ref_list" highlight-current-row border height="400"
                                style="width:800px" @current-change="handleCurrentChange">
                                <el-table-column prop="no" label="No" />
                                <el-table-column prop="ref" label="Ref" />
                            </el-table>
                        </el-tab-pane>
                    </el-tabs>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { saveAs } from 'file-saver'; // 好像只放在 main.js 也行

export default {
    data() {
        return {
            server_url: 'http://127.0.0.1:5003',
            img_src_1: '/imgs/pdf01.jpeg',
            activeName: 'first',
            uniqueId: '',
            loading: false,
            showbutton: true,
            ref_list: []
        }
    },
    methods: {
        true_upload() {
            // 获取整个 Vue 实例中所有的引用（ref 属性），然后再找到 upload 这个引用
            // Vue3 好像一般不这么写
            this.$refs.upload.click();
        },
        update(e) {
            function Ref(no, ref) {
                this.no = no;
                this.ref = ref;
            }

            this.ref_list = [];
            this.loading = true;
            this.uniqueId = Math.random().toString(36).slice(-8);

            let file = e.target.files[0];
            let config = {
                headers: { "Content-Type": "multipart/form-data" }
            }; // 添加请求头

            let param = new FormData(); // 创建 form 对象
            param.append("file", file, file.name);
            param.append("uniqueId", this.uniqueId); // 生成随机意义下近似唯一的 id，用于区别不同的上传，便于后端知道获取那个 paper 的 ref 的 bib

            axios.post(this.server_url + "/upload", param, config).then(response => {
                this.loading = false;

                for (let i = 0; i < response.data.ref_list.length; ++i) {
                    this.ref_list.push(new Ref(i + 1, response.data.ref_list[i]));
                }

            });

            e.target.value = ''; // 解决同一个文件做两次上传操作，第二次没反应的问题
        },
        handleCurrentChange(currR) {
            // 元素还未创建时 currR 为 null
            if (currR === null) {
                return;
            }

            let param = new FormData();
            let config = {
                headers: { "Content-Type": "multipart/form-data" }
            }; // 添加请求头

            param.append("uniqueId", this.uniqueId);
            param.append("no", currR.no);
            console.log("currR.no: " + currR.no);
            alert('wait about 20 seconds');

            axios.post(this.server_url + "/bib", param, config).then(response => {
                let str = new Blob([response.data.text], {type: 'text/plain;charset=utf-8'});
                saveAs(str, currR.no + ".bib");
                this.$refs.singleTableRef.setCurrentRow();
            });
        },
        handleClick(tab, event) { }
    }
}
</script>

<style scoped>
.el-button {
    padding: 12px 20px !important;
}

#hello p {
    font-size: 15px !important;
    /*line-height: 25px;*/
}

.n1 .el-step__description {
    padding-right: 20%;
    font-size: 14px;
    line-height: 20px;
    /* font-weight: 400; */
}
</style>

<style scoped>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.dialog_info {
    margin: 20px auto;
}

.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both;
}

.box-card {
    width: 680px;
    height: 200px;
    border-radius: 8px;
    margin-top: -20px;
}

.divider {
    width: 50%;
}

#CT {
    display: flex;
    height: 100%;
    width: 80%;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0 auto;
    /* margin-right: 0px; */
    max-width: 1200px;
    /* background-color: RGB(239, 249, 251); */
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#CT_image_1 {
    width: 90%;
    height: 40%;
    /* background-color: RGB(239, 249, 251); */
    margin: 0px auto;
    padding: 0px auto;
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
    /* margin-right: 180px; */
    margin-bottom: 0px;
    border-radius: 4px;
}

#CT_image {
    margin-bottom: 60px;
    /* margin-left: 30px; */
    margin-top: 5px;
}

.image_1 {
    width: 275px;
    height: 260px;
    background: #ffffff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info_1 {
    height: 30px;
    width: 275px;
    text-align: center;
}

.demo-image__preview1 {
    width: 250px;
    height: 290px;
    margin: 20px auto;
}

.demo-image__preview2 {
    width: 250px;
    height: 290px;

    margin: 20px 460px;
    /* background-color: green; */
}

.error {
    margin: 100px auto;
    width: 50%;
    padding: 10px;
    text-align: center;
}

.block-sidebar {
    position: fixed;
    display: none;
    left: 50%;
    margin-left: 600px;
    top: 350px;
    width: 60px;
    z-index: 99;
}

.block-sidebar .block-sidebar-item {
    font-size: 50px;
    color: lightblue;
    text-align: center;
    line-height: 50px;
    margin-bottom: 20px;
    cursor: pointer;
    display: block;
}

div {
    display: block;
}

.block-sidebar .block-sidebar-item:hover {
    color: #187aab;
}

.download_bt {
    padding: 10px 16px !important;
}

#upfile {
    width: 104px;
    height: 45px;
    background-color: #187aab;
    color: #fff;
    text-align: center;
    line-height: 45px;
    border-radius: 3px;
    box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
    color: #fff;
    font-family: "Source Sans Pro", Verdana, sans-serif;
    font-size: 0.875rem;
}

.file {
    width: 200px;
    height: 130px;
    position: absolute;
    left: -20px;
    top: 0;
    z-index: 1;
    -moz-opacity: 0;
    -ms-opacity: 0;
    -webkit-opacity: 0;
    opacity: 0;
    /*css属性&mdash;&mdash;opcity不透明度，取值0-1*/
    filter: alpha(opacity=0);
    cursor: pointer;
}

#upload {
    position: relative;
    margin: 0px 0px;
}

#download {
    padding: 0px;
    margin: 0px 0px;
}

.patient {
    margin: 50px auto;
    margin-bottom: 100px;
    /* margin-right: 100px; */
    background-color: #187aab;
    border-radius: 5px;
    box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
    color: #fff;
    font-family: "Source Sans Pro", Verdana, sans-serif;
    font-size: 0.875rem;
    line-height: 1;
    padding: 0.75rem 1.5rem;
}

#Content {
    width: 85%;
    height: 800px;
    background-color: #ffffff;
    margin: 15px auto;
    display: flex;
    min-width: 1200px;
    /* border: 1px solid #e4e7ed; */
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#aside {
    width: 25%;
    background-color: #ffffff;
    padding: 30px;
    margin-right: 80px;
    /* background-color: RGB(239, 249, 251); */
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
    height: 800px;
}

.divider {
    background-color: #eaeaea !important;
    height: 2px !important;
    width: 100%;
    margin-bottom: 50px;
}

.divider_1 {
    background-color: #ffffff;
    height: 2px !important;
    width: 100%;
    margin-bottom: 20px;
    margin: 20px auto;
}

.steps {
    font-family: "lucida grande", "lucida sans unicode", lucida, helvetica,
        "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
    color: #21b3b9;
    text-align: center;
    margin: 15px auto;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}

.step_1 {
    /*color: #303133 !important;*/
    margin: 20px 26px;
}

#info_patient {
    margin-top: 10px;
    /* margin-right: 160px; */
}
</style>
