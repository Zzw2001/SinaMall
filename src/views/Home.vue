<!--
 * @Description: 首页组件
 * @Author: hai-27
 * @Date: 2020-02-07 16:23:00
 * @LastEditors: hai-27
 * @LastEditTime: 2020-02-27 13:36:12
 -->
<template>
  <div class="home" id="home" name="home">
    <!-- 轮播图 -->
    <div class="block">
      <el-carousel height="460px">
        <el-carousel-item v-for="item in carousel" :key="item.id">
          <img
            style="height: 460px"
            :src="item.imgPath"
            :alt="item.describes"
          />
        </el-carousel-item>
      </el-carousel>
    </div>
    <!-- 轮播图END -->

    <div class="main-box">
      <div class="main">
        <!-- 手机商品展示区域 -->
        <div class="phone">
          <div class="box-hd">
            <div class="title">手机</div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <!-- 路由跳转，相当于超链接a 手机>图片-->
              <router-link to>
                <img
                  :src="
                    imgHost +
                    '/mi-mall/ac5cafc68c10ce4471869d378f594b52.png?thumb=1&w=468&h=1228&f=webp&q=90'
                  "
                />
              </router-link>
            </div>
            <!-- 手机类   的商品列表 -->
            <div class="list">
              <!-- 整个块  是MyList组件 -->
              <MyList
                :list="phoneList"
                :isMore="true"
                :isDelete="false"
              ></MyList>
            </div>
          </div>
        </div>
        <!-- 手机商品展示区域END -->

        <!-- 家电商品展示区域 -->
        <div class="appliance" id="promo-menu">
          <div class="box-hd">
            <div class="title">家电</div>
            <div class="more" id="more">
              <!-- 右上角的菜单组件 -->
              <MyMenu :val="2" @fromChild="getChildMsg">
                <span slot="1">热门</span>
                <span slot="2">电视影音</span>
              </MyMenu>
            </div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <ul>
                <!-- 家电类别的两张图 -->
                <li>
                  <img
                    :src="
                      imgHost +
                      '/mi-mall/3d47879ec183e25a36e67e0219636e60.jpg?thumb=1&w=468&h=600&f=webp&q=90'
                    "
                  />
                </li>
                <li>
                  <img
                    :src="
                      imgHost +
                      '/mi-mall/229bbaccda43f32f464c0a810b800106.jpg?thumb=1&w=468&h=600&f=webp&q=90'
                    "
                  />
                </li>
              </ul>
            </div>
            <!-- 右侧商品列表 -->
            <div class="list">
              <MyList :list="applianceList" :isMore="true"></MyList>
            </div>
          </div>
        </div>
        <!-- 家电商品展示区域END -->

        <!-- 配件商品展示区域 -->
        <div class="accessory" id="promo-menu">
          <div class="box-hd">
            <div class="title">配件</div>
            <div class="more" id="more">
              <MyMenu :val="3" @fromChild="getChildMsg2">
                <span slot="1">热门</span>
                <span slot="2">保护套</span>
                <span slot="3">充电器</span>
              </MyMenu>
            </div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <ul>
                <li>
                  <img
                    :src="
                      imgHost +
                      '/mi-mall/c5769bd53177a9301113f799fdc8511d.jpg?thumb=1&w=468&h=600&f=webp&q=90'
                    "
                    alt
                  />
                </li>
                <li>
                  <img
                    :src="
                      imgHost +
                      '/mi-mall/bb115b0d5e6cc24c39c1ae818b63bf1a.jpg?thumb=1&w=400&h=400&f=webp&q=90'
                    "
                    alt
                  />
                </li>
              </ul>
            </div>
            <div class="list">
              <MyList :list="accessoryList" :isMore="true"></MyList>
            </div>
          </div>
        </div>
        <!-- 配件商品展示区域END -->
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      // 使用别的服务器的图片
      imgHost: "https://cdn.cnbj1.fds.api.mi-img.com/",
      carousel: "", // 轮播图数据
      phoneList: "", // 手机商品列表v
      miTvList: "", // 小米电视商品列表v

      applianceList: "", // 展示的家电商品列表

      applianceHotList: "", //热门家电商品列表
      accessoryList: "", //配件商品列表
      accessoryHotList: "", //热门配件商品列表
      protectingShellList: "", // 保护套商品列表v
      chargerList: "", //充电器商品列表v
      applianceActive: 1, // 家电当前选中的商品分类
      accessoryActive: 1, // 配件当前选中的商品分类
    };
  },
  watch: {
    // 家电当前选中的'热门'和'电视影音'，响应不同的商品数据
    applianceActive: function (val) {
      // 页面初始化的时候把applianceHotList(热门家电商品列表)直接赋值给applianceList(家电商品列表)
      // 在切换商品列表时判断applianceHotList是否为空,为空则是第一次切换,把applianceList赋值给applianceHotList
      if (this.applianceHotList == "") {
        this.applianceHotList = this.applianceList;
      }
      if (val == 1) {
        // 1为热门商品
        this.applianceList = this.applianceHotList;
        return;
      }
      if (val == 2) {
        // 2为电视商品
        this.applianceList = this.miTvList;
        return;
      }
    },
    accessoryActive: function (val) {
      // 页面初始化的时候把accessoryHotList(热门配件商品列表)直接赋值给accessoryList(配件商品列表)
      // 所以在切换商品列表时判断accessoryHotList是否为空,为空则是第一次切换,把accessoryList赋值给accessoryHotList
      if (this.accessoryHotList == "") {
        this.accessoryHotList = this.accessoryList;
      }
      if (val == 1) {
        // 1为热门商品
        this.accessoryList = this.accessoryHotList;
        return;
      }
      if (val == 2) {
        // 2为保护套商品
        this.accessoryList = this.protectingShellList;
        return;
      }
      if (val == 3) {
        //3 为充电器商品
        this.accessoryList = this.chargerList;
        return;
      }
    },
  },
  // 组件创建完成时，加载数据
  created() {
    // 获取轮播图数据
    this.$axios
      .get("/goods/carouseles/", {})
      .then((res) => {
        console.log("@@carousel res:", res.data);
        this.carousel = res.data;
      })
      .catch((err) => {
        return Promise.reject(err);
      });

    // 通过getPromo方法 获取各类商品数据
    this.getPromo("手机", "phoneList"); //获取手机类的所有商品{}，存入phoneList
    this.getPromo("电视机", "miTvList");
    this.getPromo("保护套", "protectingShellList");
    this.getPromo("充电器", "chargerList");

    // 有API传入
    this.getPromo(
      ["电视机", "空调", "洗衣机"],
      "applianceList",
      "/goods/getHotProduct/"
    );
    this.getPromo(
      ["保护套", "保护膜", "充电器", "充电宝"],
      "accessoryList",
      "/goods/getHotProduct/"
    );
  },
  methods: {
    // 获取家电模块 MyMenu子组件传过来的数据, 即激活项的切换
    getChildMsg(val) {
      //MyMenu菜单项的激活状态
      console.log(val); //slot 1/2
      this.applianceActive = val;
    },
    // 获取配件模块子组件传过来的数据
    getChildMsg2(val) {
      this.accessoryActive = val;
    },

    // 获取各类商品数据
    getPromo(categoryName, val, api) {
      // 有API传入时，例子
      // categoryName:["电视机", "空调", "洗衣机"],
      // val:"applianceList",
      // api:"/goods/getHotProduct/"
      // 判断是否有api传进来
      // 调件?真执行的结果:假执行的结果
      api = api != undefined ? api : "/goods/oneCategory/goods/";
      this.$axios
        .post(api, {
          categoryName,
        })
        .then((res) => {
          // console.log("@@获取" + categoryName + "的响应", res);
          //获取属性，并赋值，如'phoneList'
          this[val] = res.data;
        })
        .catch((err) => {
          return Promise.reject(err);
        });
    },
  },
};
</script>

<style scoped>
@import "../assets/css/index.css";
</style>