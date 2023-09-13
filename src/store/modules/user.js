/*
 * @Description: 用户登录状态模块
 * @Author: hai-27
 * @Date: 2020-02-19 17:42:11
 * @LastEditors: hai-27
 * @LastEditTime: 2020-02-26 23:14:32
 */
export default {
  state: {
    user: "", // 登录的用户,
    showLogin: false, // 用于控制是否显示登录组件
    showUpdatePw: false,
    addMyAddr: false,
    // 地址列表
    address: [],
    

  },
  getters: {
    //
    getUser(state) {//传入state
      return state.user
    },
    getShowLogin(state) {
      return state.showLogin
    },
    getUpdatePw(state) {
      return state.showUpdatePw
    },

    getAddMyAddr(state) {
      return state.addMyAddr
    },
    getAddress(state) {
      return state.address
    },
  },
  mutations: {
    // 传入第一个参数state, 第二个传入的数据data
    setUser(state, data) {
      state.user = data;
    },
    setShowLogin(state, data) {
      // 接收登录的按钮传递的值,把默认的不显示登录组件改成显示登录组件
      state.showLogin = data;
    },
    setUpdatePw(state, data) {
      state.showUpdatePw = data
    },

    setAddMyAddr(state, data) {
      state.addMyAddr = data
    },
  },
  actions: {
    //传入的第一个参数是context---->获取{commit}
    setUser({ commit }, data) {
      commit('setUser', data);
    },
    setShowLogin({ commit }, data) {
      commit('setShowLogin', data);
    },

    setUpdatePw({ commit }, data) {
      commit("setUpdatePw", data)
    },

    setAddMyAddr({ commit }, data) {
      commit("setAddMyAddr", data)
    },
  }
}