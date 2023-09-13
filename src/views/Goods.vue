<!--
 * @Description: 全部商品页面组件(包括全部商品,商品分类,商品搜索)
 * 
 -->
<template>
  <div class="goods" id="goods" name="goods">
    <!-- 面包屑导航 -->
    <div class="breadcrumb">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item to="/">首页</el-breadcrumb-item>
        <el-breadcrumb-item>全部商品</el-breadcrumb-item>
        <el-breadcrumb-item v-if="search">搜索</el-breadcrumb-item>
        <el-breadcrumb-item v-else>分类</el-breadcrumb-item>
        <el-breadcrumb-item v-if="search">{{ search }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 面包屑END -->

    <!-- 分类标签 -->
    <div class="nav">
      <div class="product-nav">
        <div class="title">分类</div>
        <el-tabs v-model="activeName" type="card">
          <el-tab-pane
            v-for="item in categoryList"
            :key="item.id"
            :label="item.cate_name"
            :name="'' + item.id"
          />
        </el-tabs>
      </div>
    </div>
    <!-- 分类标签END -->

    <!-- 主要内容区 -->
    <div class="main">
      <div class="list">
        <MyList :list="product" v-if="product.length > 0"></MyList>
        <div v-else class="none-product">
          抱歉没有找到相关的商品，请看看其他的商品
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="pageSize"
          :total="total"
          @current-change="currentChange"
        ></el-pagination>
      </div>
      <!-- 分页END -->
    </div>
    <!-- 主要内容区END -->
  </div>
</template>
<script>
export default {
  data() {
    return {
      categoryList: "", //分类列表
      categoryID: "", // 分类id
      product: [], // 商品列表
      total: 0, // 商品总量
      pageSize: 10, // 每页显示的商品数量
      currentPage: 1, //当前页码
      activeName: "-1", // 分类列表当前选中的id
      search: "", // 搜索条件
    };
  },
  // 页面加载后执行的方法
  created() {
    // 获取分类列表
    this.getCategory();
  },
  activated() {
    //跳转到Goods组件后触发。
    this.activeName = "-1"; // 初始化分类列表当前选中的id为-1
    this.total = 0; // 初始化商品总量为0
    this.currentPage = 1; //初始化当前页码为1
    // 如果路由没有传递参数，默认为显示全部商品
    console.log("路由激活：", this.$route.query);
    if (Object.keys(this.$route.query).length == 0) {
      // console.log("这里是否有问题？1没问题")
      // console.log("执行第一个if");
      this.categoryID = [];
      this.activeName = "0"; //
      return;
    }
    // 如果路由传递了{categoryID:array(1)}，则显示对应的分类商品
    if (this.$route.query.categoryID != undefined) {
      // console.log("执行第二个if");
      // 获取点击更多时传递的categoryID
      this.categoryID = this.$route.query.categoryID;
      if (this.categoryID.length == 1) {
        // 点击分类标签，改变activeName的值
        this.activeName = "" + this.categoryID[0];
      }
      return;
    }
    // 如果路由传递了search，则为搜索，显示对应的分类商品
    if (this.$route.query.search != undefined) {
      console.log("执行第三个if");
      this.search = this.$route.query.search;
    }
  },
  watch: {
    // 监听点击了哪个分类标签，通过修改分类id，响应相应的商品
    activeName: function (val) {
      console.log("当前activeName:", val, typeof val);
      // 字符串可以与数字比较
      if (val == 0) {
        this.categoryID = []; //显示所有商品
      }
      if (val > 0) {
        this.categoryID = [Number(val)]; //如[5]
      }
      // 初始化商品总量和当前页码
      this.total = 0;
      this.currentPage = 1;
      // 更新地址栏链接，如/goods?categoryID=5
      this.$router.push({
        path: "/goods",
        query: { categoryID: this.categoryID[0] }, //值为数组
      });
    },
    // 监听搜索条件，响应相应的商品
    search: function (val) {
      if (val != "") {
        console.log("当前搜索：", val);
        this.getProductBySearch(val); //val -->如'小米手机'
      }
    },
    // 监听分类id，响应相应的商品
    categoryID: function () {
      this.getData();
      this.search = "";
    },
    // 监听路由变化，更新路由传递了搜索条件
    $route: function (val) {
      if (val.path == "/goods") {
        if (val.query.search != undefined) {
          this.activeName = "-1";
          this.currentPage = 1;
          this.total = 0;
          this.search = val.query.search;
        }
      }
    },
  },
  methods: {
    // 返回顶部
    backtop() {
      const timer = setInterval(function () {
        const top =
          document.documentElement.scrollTop || document.body.scrollTop;
        const speed = Math.floor(-top / 5);
        document.documentElement.scrollTop = document.body.scrollTop =
          top + speed;

        if (top === 0) {
          clearInterval(timer);
        }
      }, 20);
    },
    // 页码变化调用currentChange方法
    currentChange(currentPage) {
      // 当前的页数, 第几页
      this.currentPage = currentPage;
      // console.log("当前的页数>>", this.currentPage);
      if (this.search != "") {
        this.getProductBySearch();
      } else {
        this.getData();
      }
      this.backtop();
    },
    // 向后端请求商品类别----laufing
    getCategory() {
      this.$axios
        .post("/goods/cates/", {})
        .then((res) => {
          // 获取种类的响应
          console.log("@@获取商品所有种类的响应：", res.data);
          const val = {
            // category_id: 0,
            id: 0, //种类id
            // category_name: "全部"
            cate_name: "全部", //种类名
          };
          // 接收后端返回的数据
          const cate = res.data;
          cate.unshift(val);
          this.categoryList = cate;
        })
        .catch((err) => {
          return Promise.reject(err);
        });
    },

    // 向后端请求全部商品或指定分类id的商品数据
    getData() {
      // 如果categoryID为空则请求全部商品数据，否则请求分类id的商品数据
      console.log("类别id是>>>>", this.categoryID);
      const api =
        this.categoryID.length == 0
          ? "/goods/good/getAllProduct/"
          : "/goods/good/getProductByCategory/";
      // 获取类别下的所有商品
      this.$axios
        .get(api, {
          params: {
            categoryID: this.categoryID[0],
            page: this.currentPage, // 当前是第几页
            pageSize: this.pageSize, // 限制每页显示的条数
          },
        })
        .then((res) => {
          // console.log("响应的数据是~~~~~~~", res.data);
          if ("results" in res.data) {
            // console.log("分页数据是>>>", res.data.results);
            this.product = res.data.results;
            this.total = res.data.count;
          } else {
            // console.log("此类别下的商品是>>", res.data);
            this.product = res.data;
          }
        })
        .catch((err) => {
          return Promise.reject(err);
        });
    },

    // 通过搜索条件向后端请求商品数据
    getProductBySearch() {
      // {
      //  currentPage: this.currentPage,
      //  pageSize: this.pageSize
      // }
      this.$axios
        .get("/search/?q=" + this.search)
        .then((res) => {
          console.log("@@搜索的响应：", res);
          this.product = res.data.product;
          this.total = res.data.total;
        })
        .catch((err) => {
          return Promise.reject(err);
        });
    },
  },
};
</script>

<style scoped>
.goods {
  background-color: #f5f5f5;
}
/* 面包屑CSS */
.el-tabs--card .el-tabs__header {
  border-bottom: none;
}
.goods .breadcrumb {
  height: 50px;
  background-color: white;
}
.goods .breadcrumb .el-breadcrumb {
  width: 1225px;
  line-height: 30px;
  font-size: 16px;
  margin: 0 auto;
}
/* 面包屑CSS END */

/* 分类标签CSS */
.goods .nav {
  background-color: white;
}
.goods .nav .product-nav {
  width: 1225px;
  height: 40px;
  line-height: 40px;
  margin: 0 auto;
}
.nav .product-nav .title {
  width: 50px;
  font-size: 16px;
  font-weight: 700;
  float: left;
}
/* 分类标签CSS END */

/* 主要内容区CSS */
.goods .main {
  margin: 0 auto;
  max-width: 1225px;
}
.goods .main .list {
  min-height: 650px;
  padding-top: 14.5px;
  margin-left: -13.7px;
  overflow: auto;
}
.goods .main .pagination {
  height: 50px;
  text-align: center;
}
.goods .main .none-product {
  color: #333;
  margin-left: 13.7px;
}
/* 主要内容区CSS END */
</style>