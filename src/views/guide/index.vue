<template>
  <div class="app-container">
    <aside class="text-aside">
      第十一届中国软件杯大学生软件设计大赛-基于百度飞桨的遥感图像智能解译平台
    </aside>
    <el-col :xs="{span: 96}" :sm="{span: 48}" :md="{span: 48}" :lg="{span: 24}" :xl="{span: 24}" style="margin-bottom:30px;">
      <box-card />
    </el-col>
    <el-button icon="el-icon-question" type="primary" @click.prevent.stop="guide">
      Show Guide
    </el-button>
  </div>
</template>

<script>
import Driver from 'driver.js' // import driver.js
import 'driver.js/dist/driver.min.css' // import driver.js css
import steps from './steps'
import BoxCard from './components/BoxCard'

export default {
  name: 'Guide',
  components: {
    BoxCard
  },
  data() {
    return {
      driver: null
    }
  },
  mounted() {
    this.driver = new Driver()
  },
  methods: {
    guide() {
      this.driver.defineSteps(steps)
      this.driver.start()
    }
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
