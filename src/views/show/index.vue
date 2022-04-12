<template>
  <div class="app-container">
    <aside class="text-aside">
      第十一届中国软件杯大学生软件设计大赛-基于百度飞桨的遥感图像智能解译平台
    </aside>
    <el-col :xs="{span: 96}" :sm="{span: 48}" :md="{span: 48}" :lg="{span: 24}" :xl="{span: 24}" style="margin-bottom:30px;">
      <box-card />
    </el-col>
    <div class="editor-custom-btn-container">
      <editorImage color="#1890ff" class="editor-upload-btn" @successCBK="imageSuccessCBK" />
    </div>
  </div>
</template>

<script>
  import BoxCard from './components/BoxCard'
  import editorImage from './components/EditorImage'


export default {
  name: 'Show',
  components: {
    BoxCard,
    editorImage
  }
}
</script>

<style lang="scss" scoped>
  .text-aside {
    position: relative;
    vertical-align: middle;
    font-size: 30px;
    text-align: center;
    text-size-adjust: auto;
  }
</style>
