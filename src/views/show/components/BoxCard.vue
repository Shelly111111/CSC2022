<template>
  <div class="upload-container">
    <el-card class="box-card-component">
      <div class="box-card-header">
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
      </div>
    </el-card>
    <el-button
      :style="{background:color,borderColor:color}"
      icon="el-icon-upload"
      size="mini"
      type="primary"
      @click=" dialogVisible=true"
    >upload</el-button>
    <el-dialog :visible.sync="dialogVisible">
      <el-upload
        class="avatar-uploader"
        :action="uploadUrl"
        :show-file-list="true"
        :on-success="handlePictureCardPreview"
        :on-remove="handleRemove"
        name="avatar"
        drag
        method="post"
        enctype="multipart/form-data"
      >
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <i class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
      <el-button @click="dialogVisible = false">Cancel</el-button>
      <el-button type="primary" @click="handleSubmit">Confirm</el-button>
    </el-dialog>
  </div>
</template>

<script>
import { postStorgeImage, postFindImage } from "../../../api/update";
export default {
  props: {
    color: {
      type: String,
      default: "#1890ff"
    }
  },
  data() {
    return {
      imageUrl: "",
      dialogVisible: false,
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
    postFindImage() {
      postFindImage().then(res => {
        // console.log(res);
        this.result = res.data.result;
        this.imageUrl = this.result[0].imgSrc;
        console.log(this.result);
      });
    },
    handleSubmit() {
      this.postStorgeImage();
    },
    // 成功的回调
    handlePictureCardPreview(file) {
      this.imageUrl = file;
      // this.dialogVisible = false;
      // console.log(file);
      this.base64.push(file);
      // console.log(this.base64);
      // console.log(file);
    },
    // 移除图片
    handleRemove(file, fileList) {
      this.base64 = [];
      fileList.forEach(item => {
        this.base64.push(item.response);
      });
      // console.log("this.base64", this.base64);
    }
  }
};
</script>

<style lang="scss" scoped>
.box-card-component {
  .box-card-header {
    position: relative;

    img {
      width: 33%;
      height: 33%;
    }
  }
}

.editor-slide-upload {
  margin-bottom: 60px;

  ::v-deep .el-upload--picture-card {
    width: 100%;
  }
}
</style>
