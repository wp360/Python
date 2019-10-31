<template>
  <div id="app">
    <div class="all">
      <div class="one">
        <div class="onetype" v-for="(item,index) in one" :key="index">
          <b>{{one[index]}}</b>
        </div>
      </div>
      <div class="twothreefour">
        <div class="two">
          <div class="twotype" 
          v-for="(item,index) in two" :key="index"
           @mouseenter="open(index)">
            <b>{{two[index]}}</b>
          </div>
        </div>
        <div class="threefour" v-if="flag"
           @mouseleave="close()">
          <div class="threefourtype" v-for="(item,index) in three" :key="index">
            <span class="three">{{three[index]}}</span>
            <span class="four" v-for="(item4,index4) in four" :key="index4">{{four[index4]}}</span>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
export default {
  name: 'app',
  data () {
    return {
      one:['一级类目','一级类目','一级类目','一级类目','一级类目'],
      two:['二级类目1','二级类目2','二级类目3','二级类目4','二级类目5'],
      three:[],
      four:['四级类目','四级类目','四级类目','四级类目','四级类目'],
      flag:false
    }
  },
  methods: {
    open(index){
      var index=index+1;
      var i=index+"";
      this.three=['三级目录'+i,'三级目录'+i,'三级目录'+i,'三级目录'+i,'三级目录'+i]
      this.flag=true
    },
    close(){
      this.flag=false
    }
  },
}
</script>
<style>
*{
  /* 样式初始化 */
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
.all{
  /* 将整个导航栏组件做整体设置 */
  /*宽度占浏览器80%，高度400px；背景灰色；上外边距50px; 左右居中*/
  /* 设置为flex弹性盒子，并且定义为高度不够自动折行模式，用于横向排列子元素 */
  width: 80%;
  height: 400px;
  background:#eee;
  margin: 50px auto;
  display: -webkit-flex; /* Safari */
  display: flex;
  flex-wrap: wrap;
}
.one{
  /* 设置一级类目所占地区的样式，宽度占满all盒子的100% */
  width: 100%;
  height: 50px;
  background: #FF8888;
  display: flex;
  display: -webkit-flex; /* Safari */
  flex-wrap: wrap;
  /* 弹性盒子内部的子元素都均匀排列成一横排，并且左右两边都留有一定空隙 */
  justify-content: space-around;
}
.onetype{
  width: 20%;
  height: 50px;
  line-height: 50px;
  text-align: center;
}
.onetype:hover{ 
  background-color:chocolate;
  color: #eee;
}
.twothreefour{
  /* 盛放二三四级目录的盒子 */
  width: 100%;
  height: 350px;
  background: #66FF66;
  display: -webkit-flex; /* Safari */
  display: flex;
  flex-wrap: wrap;
  /* 弹性盒子内部的子元素都均匀排列成一横排，并且左右两边都不留空隙 */
  justify-content: space-between;
}
.two{
  /* 设置盛放二级类目的弹性盒子 */
  width: 15%;
  height: 100%;
  background: #77FFCC;
  display: -webkit-flex; /* Safari */
  display: flex;
  /* 弹性盒子内部的子元素从上到下排成一列 */
  flex-direction: column;
}
.twotype{
  width: 100%;
  height: 40px;
  line-height: 40px;
  text-align: center;
  background: #EEFFBB;
}
.twotype:hover{ 
  background-color:black;
  color: #eee;
}
.threefour{
  width: 40%;
  margin-right: 45%;
  height: 100%;
  background: #33FFDD;
  display: -webkit-flex; /* Safari */
  display: flex;
  flex-direction: column;
}
.threefourtype{
  margin: 10px auto;
}
.three{
  font-family: 微软雅黑, 黑体;
  font-size: 16px;
  font-weight: 800;
}
.four{
  font-family: 宋体;
  font-size: 12px;
  font-weight: 400;
}
</style>
