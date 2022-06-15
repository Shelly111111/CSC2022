<template>
  <div class="upload-container">
    <el-row>
      <el-col :span="12">
        <el-card class="box-card-component">
          <div class="box-card-header" slot="header">
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
          </div>
          <div class="box-card-body">
            <el-button
                       :style="{background:color,borderColor:color}"
                       icon="el-icon-upload"
                       size="mini"
                       type="primary"
                       @click="dialog1Visible=true">upload</el-button>
            <el-dialog :visible.sync="dialog1Visible">
              <el-upload :multiple="false"
                         class="avatar-uploader"
                         :action="uploadUrl"
                         :show-file-list="true"
                         :on-success="handlePictureCardPreview"
                         :on-remove="handleRemove"
                         name="avatar"
                         drag
                         method="post"
                         enctype="multipart/form-data">
                <i class="el-icon-upload" />
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
              </el-upload>
              <el-button @click="dialogVisible = false">Cancel</el-button>
              <el-button type="primary" @click="handleSubmit">Confirm</el-button>
            </el-dialog>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card-component">
          <div slot="header" class="box-card-header">
            <img v-if="imageUrl2" :src="imageUrl2" class="avatar2" />
          </div>
          <div class="box-card-body">
            <el-button :style="{background:color,borderColor:color}"
                       icon="el-icon-upload"
                       size="mini"
                       type="primary"
                       @click="dialog2Visible=true">upload</el-button>
            <el-button :style="{background:color,borderColor:color}"
                       size="mini"
                       type="primary"
                       @click="sendImage">check</el-button>
            <el-dialog :visible.sync="dialog2Visible">
              <el-upload :multiple="false"
                         class="avatar2-uploader"
                         :action="uploadUrl"
                         :show-file-list="true"
                         :on-success="handle2PictureCardPreview"
                         :on-remove="handleRemove"
                         name="avatar"
                         drag
                         method="post"
                         enctype="multipart/form-data">
                <i class="el-icon-upload" />
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
              </el-upload>
              <el-button @click="dialogVisible = false">Cancel</el-button>
              <el-button type="primary" @click="handle2Submit">Confirm</el-button>
            </el-dialog>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import splitPane from 'vue-splitpane'
  import { postStorgeImage, postFindImage, sendImage } from "../../../api/update";
  export default {
    props: {
      color: {
        type: String,
        default: "#1890ff"
      }
    },
    components: { splitPane },
    data() {
      return {
        imageUrl: "",
        imageUrl2: "",
        dialog1Visible: false,
        dialog2Visible: false,
        fileList: [],
        uploadUrl: "http://localhost:3001/upload",
        base64: []
      };
    },
    mounted() {
      this.postFindImage();
    },
    methods: {
      postStorgeImage() {
        postStorgeImage(this.imageUrl).then(res => {
          console.log(res);
        });
      },
      postStorge2Image() {
        postStorgeImage(this.imageUrl2).then(res => {
          console.log(res);
        });
      },
      sendImage() {
        sendImage(this.imageUrl, this.imageUrl2);
      },
      postFindImage() {
        postFindImage().then(res => {
          this.result = res.data.result;
          this.imageUrl = this.result[this.result.length - 1].imgSrc;
          this.imageUrl2 = this.result[this.result.length - 2].imgSrc;
        });
      },
      handleSubmit() {
        this.postStorgeImage();
        this.dialog1Visible = false
      },
      handle2Submit() {
        this.postStorge2Image();
        this.dialog2Visible = false
      },
      // 成功的回调
      handlePictureCardPreview(file) {
        this.imageUrl = file;
        this.base64.push(file);
      },
      // 成功的回调
      handle2PictureCardPreview(file) {
        this.imageUrl2 = file;
        this.base64.push(file);
      },
      // 移除图片
      handleRemove(file, fileList) {
        this.base64 = [];
        fileList.forEach(item => {
          this.base64.push(item.response);
        });
      }
    }
  };
</script>

<style lang="scss" scoped>

  .upload-container {
    width: 100%;

    .box-card-component {
      .box-card-header {
        position: relative;

        img {
          width: 100%;
          height: 100%;
        }
      }
    }

    .avatar-uploader {
      width: 100%;
      margin-bottom: 20px;
    }
  }
</style>
