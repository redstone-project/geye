<template>
  <div class="sidebar">
    <el-menu class="sidebar-el-menu" background-color="#324157"
             text-color="#bfcbd9" active-text-color="#20a0ff" :collapse="collapse"
             @select="handleSelect" :default-active="onRoutes" router>

      <template v-for="item in items">
        <template v-if="item.subs">
          <el-submenu :index="item.index" :key="item.index">
            <template slot="title">
              <font-awesome-icon :icon="item.icon" fixed-width=""/>
              <span class="menu-item">{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-menu-item :index="subItem.index" :key="subItem.index">
                <font-awesome-icon :icon="['far', 'circle']" fixed-width size="xs"/>
                <span> {{ subItem.title }}</span>
              </el-menu-item>
            </template>
          </el-submenu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index" :key="item.index">
            <font-awesome-icon :icon="item.icon" fixed-width=""/>
            <span class="menu-item">{{ item.title }}</span>
          </el-menu-item>
        </template>
      </template>

    </el-menu>
  </div>
</template>

<script>
  import globalData from "./data";

  export default {
    name: "Sidebar",
    data() {
      return {
        collapse: false,
        items: [
          {
            icon: "tachometer-alt",
            index: "/dashboard",
            title: "Dashboard",
          },
          {
            icon: "list",
            index: "rule",
            title: "规则管理",
            subs: [
              {
                index: "/rule/global/filter",
                title: "全局过滤规则管理",
              },
              {
                index: "/rule/search/all",
                title: "搜索规则管理",
              },
              {
                index: "/monitor/rules",
                title: "监控规则管理",
              },
            ]
          },
          {
            icon: "paper-plane",
            index: "handleCenter",
            title: "处理中心",
            subs: [
              {
                index: "/handleCenter/search",
                title: "搜索结果",
              },
              {
                index: "/handleCenter/monitor",
                title: "监控结果",
              }
            ]
          },
          {
            icon: "key",
            index: "/token",
            title: "Token管理"
          },
          {
            icon: "money-check-alt",
            index: "/leaks",
            title: "泄露信息管理",
          },
        ]
      }
    },
    created() {
      globalData.$on("collapse", msg => {
        console.log("receive message: " + msg);
        this.collapse = msg;
      })
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log("key: " + key + " keyPath: " + keyPath);
        if (keyPath[0] === "rule-management") {
          console.log("hit");

        }
      },
    },
    computed: {
      onRoutes() {
        console.log("onRoutes: " + this.$route.path);
        return this.$route.path;
        // return this.$route.path.replace("/", "");
      }
    }
  }
</script>

<style scoped>
  .sidebar {
    display: block;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .sidebar::-webkit-scrollbar {
    width: 0;
  }

  .sidebar-el-menu:not(.el-menu--collapse) {
    width: 200px;
  }

  .sidebar > ul {
    height: 100%;
  }

  .menu-item {
    margin-left: 10px;
  }

</style>
