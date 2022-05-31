<template>
  <div class="app-container">
    <aside class="text-aside">
      第十一届中国软件杯大学生软件设计大赛-基于百度飞桨的遥感图像智能解译平台
    </aside>
    <el-col :xs="{span: 96}" :sm="{span: 48}" :md="{span: 48}" :lg="{span: 24}" :xl="{span: 24}" style="margin-bottom:30px;">
      <box-card />
      <el-table v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%">
        <el-table-column align="center" label="ID" width="80px">
          <template slot-scope="{row}">
            <span>{{ row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column width="180px" align="center" label="Date">
          <template slot-scope="{row}">
            <span>{{ row.timestamp | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
          </template>
        </el-table-column>
        <el-table-column width="120px" align="center" label="Author">
          <template slot-scope="{row}">
            <span>{{ row.author }}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="Picture1" min-width="100px">
          <template slot-scope="{row}">
            <el-tag :type="row.img1">
              {{ row.img1 }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column align="center" label="Picture2" min-width="100px">
          <template slot-scope="{row}">
            <el-tag :type="row.img2">
              {{ row.img2 }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column class-name="status-col" label="Status" width="110px">
          <template slot-scope="{row}">
            <el-tag :type="row.status | statusFilter">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column align="center" label="Actions" width="120">
          <template slot-scope="{row}">
            <el-button v-if="row.edit"
                       type="success"
                       size="small"
                       icon="el-icon-circle-check-outline"
                       @click="confirmEdit(row)">
              Ok
            </el-button>
            <el-button v-else
                       type="primary"
                       size="small"
                       icon="el-icon-edit"
                       @click="row.edit=!row.edit">
              Edit
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </div>
</template>

<script>
  import BoxCard from './components/BoxCard'
  //import editorImage from './components/EditorImage'


  export default {
    name: 'Show',
    components: {
      BoxCard,
      //editorImage
    },
    data() {
      return {
        listLoading: false,
      }      
  },
    methods: {
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
