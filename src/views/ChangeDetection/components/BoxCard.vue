<template>
  <div class="upload-container">
    <el-row>
      <el-col :span="16">
        <el-card class="detected-card">
          <div class="box-card-header" style="display: flex; justify-content: space-between">
            <span class="timelabel1">
              检测图片
            </span>
            <el-button :style="{background: color, borderColor: color}"
                       :disabled ="disabled"
                       icon="el-icon-mouse"
                       size="mini"
                       type="primary"
                       @click="sendImage">check</el-button>
          </div>
        </el-card>
        <div class="detected-body">
          <img v-if="imageUrl3" :src="imageUrl3" class="avatar" />
        </div>
      </el-col>
      <el-col :span="8">
        <el-row :span="4">
          <el-card class="analyse-card">
            <div slot="header" class="box-card-header" style="display: flex; justify-content: space-between">
              <span class="timelabel4">
                结果分析
              </span>
            </div>
            <div class="box-card-body">
              <div class="progress-item">
                <span>变化面积所占比例</span>
                <el-progress :percentage="percent" />
              </div>
            </div>
          </el-card>
        </el-row>
        <el-row :span="4">
          <el-card class="box-card-component">
            <div class="box-card-header" slot="header">
              <span class="timelabel2">
                原始图片
              </span>
              <el-button :style="{background:color,borderColor:color}"
                          icon="el-icon-upload"
                          size="mini"
                          type="primary"
                          @click="dialog1Visible=true">upload</el-button>
              <el-dialog :visible.sync="dialog1Visible">
                <el-upload :multiple="false"
                            class="avatar-uploader"
                            :action="uploadUrl"
                            :show-file-list="true"
                            :before-upload="handleBefore1Upload"
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
                <el-button @click="dialog1Visible = false">Cancel</el-button>
                <el-button type="primary" @click="handleSubmit">Confirm</el-button>
              </el-dialog>
            </div>
            <div class="box-card-body">
              <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            </div>
          </el-card>
        </el-row>
        <el-row :span="4">
          <el-card class="box-card-component">
            <div slot="header" class="box-card-header">
              <span class="timelabel3">
                变化图片
              </span>
              <el-button :style="{background:color,borderColor:color}"
                          icon="el-icon-upload"
                          size="mini"
                          type="primary"
                          @click="dialog2Visible=true">upload</el-button>
              <el-dialog :visible.sync="dialog2Visible">
                <el-upload :multiple="false"
                            class="avatar2-uploader"
                            :action="uploadUrl"
                            :show-file-list="true"
                            :before-upload="handleBefore2Upload"
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
                <el-button @click="dialog2Visible = false">Cancel</el-button>
                <el-button type="primary" @click="handle2Submit">Confirm</el-button>
              </el-dialog>
            </div>
            <div class="box-card-body">
              <img v-if="imageUrl2" :src="imageUrl2" class="avatar2" />
            </div>
          </el-card>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import splitPane from 'vue-splitpane'
  import { postStorgeImage, postStorge2Image, postFindImage, postFind2Image, sendImage } from "../../../api/update";
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
        imageUrl3: "",
        disabled: false,
        uploaded1: false,
        uploaded2: false,
        dialog1Visible: false,
        dialog2Visible: false,
        fileList: [],
        uploadUrl: "http://localhost:3001/upload",
        base64: [],
        percent:0
      };
    },
    mounted() {
      this.postFindImage();
      this.postFind2Image();
    },
    methods: {
      postStorgeImage() {
        postStorgeImage(this.imageUrl).then(res => {
          //console.log(res);
        });
      },
      postStorge2Image() {
        postStorge2Image(this.imageUrl2).then(res => {
          //console.log(res);
        });
      },
      sendImage() {
        if (this.imageUrl=="") {
          this.$message('原始图片未上传或未加载成功!');
          return;
        }
        if (this.imageUrl2=="") {
          this.$message('变化图片未上传或未加载成功!');
          return;
        }
        this.disabled = true;
        sendImage(this.imageUrl, this.imageUrl2).then(res => {
          //console.log(res);
          this.imageUrl3 = res.data.img;
          this.percent = res.data.percent;
          this.disabled = false;
        });
      },
      postFindImage() {
        postFindImage().then(res => {
          var result1 = res.data.result;
          if (result1.length > 0) {
            this.imageUrl = result1[result1.length - 1].imgSrc;
            this.uploaded1 = true;
          }
        });
      },
      postFind2Image() {
        postFind2Image().then(res => {
          var result2 = res.data.result;
          if (result2.length > 0) {
            this.imageUrl2 = result2[result2.length - 1].imgSrc;
            this.uploaded2 = true;
          }
        });
      },
      handleBefore1Upload(file) {
        this.uploaded1 = false;
        const uploadTypes = ['jpg', 'png'];
        const filetype = file.name.replace(/.+\./, '');
        if (uploadTypes.indexOf(filetype.toLowerCase()) === -1) {
          this.$message.warning({
            message: '请上传后缀名为jpg、png的附件'
          });
          return false;
        }
        return true;
      },
      handleBefore2Upload(file) {
        this.uploaded2 = false;
        const uploadTypes = ['jpg', 'png'];
        const filetype = file.name.replace(/.+\./, '');
        if (uploadTypes.indexOf(filetype.toLowerCase()) === -1) {
          this.$message.warning({
            message: '请上传后缀名为jpg、png的附件'
          });
          return false;
        }
        return true;
      },
      handleSubmit() {
        if (!this.uploaded1) {
          this.$message('请等待原始图片上传成功。 如果出现网络问题，请刷新页面重新上传!');
          return;
        }
        this.postStorgeImage();
        this.dialog1Visible = false;
      },
      handle2Submit() {
        if (!this.uploaded2) {
          this.$message('请等待变化图片上传成功。 如果出现网络问题，请刷新页面重新上传!');
          return;
        }
        this.postStorge2Image();
        this.dialog2Visible = false;
      },
      // 成功的回调
      handlePictureCardPreview(file) {
        this.imageUrl = file;
        this.base64.push(file);
        this.uploaded1 = true;
      },
      // 成功的回调
      handle2PictureCardPreview(file) {
        this.imageUrl2 = file;
        this.base64.push(file);
        this.uploaded2 = true;
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
        display: flex;
        justify-content: space-between;

        .timelabel2 {
          font-size: 18px;
          text-shadow: 1px 0px lightslategrey;
          font-weight: bold;
          color: lightslategrey;
        }

        .timelabel3 {
          font-size: 18px;
          text-shadow: 1px 0px lightslategrey;
          font-weight: bold;
          color: lightslategrey;
        }
      }
    }

    .timelabel1 {
      font-size: 18px;
      text-shadow: 1px 0px lightslategrey;
      font-weight: bold;
      color: lightslategrey;
    }

    .timelabel4 {
      font-size: 18px;
      text-shadow: 1px 0px lightslategrey;
      font-weight: bold;
      color: lightslategrey;
    }

    .box-card-body {
      position: relative;

      img {
        width: 100%;
        height: 100%;
      }
    }

    .detected-body {
      position: relative;

      img {
        width: 100%;
        height: 100%;
      }
    }

    .avatar-uploader {
      width: 100%;
      margin-bottom: 20px;
    }
  }
</style>
