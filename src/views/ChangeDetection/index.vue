<template>
  <div class="app-container">
    <aside class="text-aside">
      第十一届中国软件杯大学生软件设计大赛-基于百度飞桨的遥感图像智能解译平台
    </aside>
    <box-card class="box-card"/>
  </div>
</template>

<script>
  import BoxCard from './components/BoxCard'

  export default {
    name: 'ChangeDetection',
    components: {
      BoxCard
    },
    data() {
      return {
      }      
  },
    methods: {
    }
  }
</script>

<style lang="scss" scoped>
  .app-container {
    position: relative;
    height: 100%;
    width: 100%;
  }

  .text-aside {
    position: relative;
    vertical-align: middle;
    font-size: 30px;
    text-align: center;
    text-size-adjust: auto;
  }

</style>
