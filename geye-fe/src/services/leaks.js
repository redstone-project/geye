"use strict";

import config from "@/config/index";

const BASE_API = config.BASE_API;
const API_LIST = {
  getLeaks: BASE_API + "/api/v1/leaks/all",
  deleteLeak: BASE_API + "/api/v1/leaks/delete",
};

export default {
  getLeaks(ctx, currentPage, status) {
    let data = {
      page: currentPage,
      status: status,
    };
    return ctx.axios.get(API_LIST.getLeaks, {params: data});
  },

  deleteLeak(ctx, id) {
    let data = {
      id: id
    };
    return ctx.axios.post(API_LIST.deleteLeak, data);
  }

}
