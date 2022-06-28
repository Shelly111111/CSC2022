<template>
  <div class="upload-container">
    <el-row>
      <el-col :span="18">
        <el-card class="detected-card">
          <div class="box-card-header" style="display: flex; justify-content: space-between">
            <span class="timelabel1">
              检测图片
            </span>
            <el-button :style="{background: color, borderColor: color}"
                       icon="el-icon-mouse"
                       size="mini"
                       type="primary"
                       @click="sendImage2tc">check</el-button>
          </div>
        </el-card>
        <div class="detected-body">
          <img v-if="imageUrl2" :src="imageUrl2" class="avatar" />
        </div>
      </el-col>
      <el-col :span="6">
        <el-row :span="4">
          <el-card class="box-card-component">
            <div class="box-card-header" slot="header">
              <div class="timelabel3">
                结果分析
              </div>
            </div>
            <div class="box-card-body">
              <div style="padding-top:35px;" class="progress-item">
                <span>房屋</span>
                <el-progress :percentage="class1" />
              </div>
              <div class="progress-item">
                <span>森林</span>
                <el-progress :percentage="class2" />
              </div>
              <div class="progress-item">
                <span>道路</span>
                <el-progress :percentage="class3" />
              </div>
              <div class="progress-item">
                <span>田地</span>
                <el-progress :percentage="class4"/>
              </div>
            </div>
          </el-card>
        </el-row>
        <el-row :span="4">
          <el-card class="box-card-component">
            <div slot="header" class="box-card-header">
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
                           :before-upload="handleBeforeUpload"
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
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import splitPane from 'vue-splitpane'
  import { postTerrainClassificationImage, FindTerrainClassificationImage, sendImage2tc } from "../../../api/update";
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
        uploaded: false,
        fileList: [],
        uploadUrl: "http://localhost:3001/upload",
        base64: [],
        class1: 0,
        class2: 0,
        class3: 0,
        class4: 0
      };
    },
    mounted() {
      this.FindTerrainClassificationImage();
    },
    methods: {
      postTerrainClassificationImage() {
        postTerrainClassificationImage(this.imageUrl).then(res => {
          //console.log(res);
        });
      },
      sendImage2tc() {
        sendImage2tc(this.imageUrl).then(res => {
          //console.log(res);
          this.imageUrl2 = res.data.img;
          this.class1 = res.data.class1;
          this.class2 = res.data.class2;
          this.class3 = res.data.class3;
          this.class4 = res.data.class4;
        });
      },
      FindTerrainClassificationImage() {
        FindTerrainClassificationImage().then(res => {
          this.result = res.data.result;
          this.imageUrl = this.result[this.result.length - 1].imgSrc;
        });
      },
      handleBeforeUpload(file) {
        this.uploaded = false;
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
        if (!this.uploaded) {
          this.$message('请等待图片上传成功。 如果出现网络问题，请刷新页面重新上传!')
          return;
        }
        this.postTerrainClassificationImage();
        this.dialog1Visible = false;
      },
      // 成功的回调
      handlePictureCardPreview(file) {
        this.imageUrl = file;
        this.base64.push(file);
        this.uploaded = true;
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
