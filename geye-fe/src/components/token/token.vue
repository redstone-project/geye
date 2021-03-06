<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <font-awesome-icon icon="bars" fixed-width></font-awesome-icon>
                    Token管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <div class="container">
            <div>
                <el-button type="primary" size="small" round @click="handleOpenDialog('add', -1, null)">添加Token
                </el-button>
            </div>
            <el-table :data="tokenData" style="width: 100%" v-loading="loading">
                <el-table-column prop="id" label="#" width="100px"></el-table-column>
                <el-table-column prop="tokenName" label="Token名称"></el-table-column>
                <el-table-column prop="tokenContent" label="Token"></el-table-column>
                <el-table-column label="状态" width="100px">
                    <template slot-scope="scope">
                        <el-tag type="success" v-if="scope.row.status === 1"
                                style="cursor: pointer"
                                @click.native="handleChangeStatus(scope.row, scope.$index)">开启
                        </el-tag>
                        <el-tag type="danger" v-else-if="scope.row.status === 0"
                                style="cursor: pointer"
                                @click.native="handleChangeStatus(scope.row, scope.$index)">关闭
                        </el-tag>
                        <el-tag v-else>未知</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="remainLimit" label="可用次数" width="100px"></el-table-column>
                <el-table-column label="操作" width="180px">
                    <template slot-scope="scope">
                        <el-button size="mini" type="primary"
                                   @click="handleOpenDialog('edit', scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>


        <!-- 添加token的dialog -->
        <el-dialog :title="dialogTitle" :visible.sync="showTokenDialog">
            <el-form label-width="100px" :model="tokenForm" :disabled="isDisableForm">
                <el-form-item label="Token名称">
                    <el-input v-model="tokenForm.tokenName" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="Token">
                    <el-input type="textarea" :autosize="{minRows: 3, maxRows: 3}"
                              v-model="tokenForm.tokenContent"></el-input>
                </el-form-item>
                <el-form-item label="状态">
                    <el-select v-model="tokenForm.status" :value="1" style="max-width: 100%">
                        <el-option label="关闭" :value="0"></el-option>
                        <el-option label="开启" :value="1"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="handleConfirm">{{dialogConfirmButtonText}}</el-button>
                <el-button type="danger" @click="showTokenDialog = false">关闭</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>

  import tokenService from "@/services/token";
  import ApiConstant from "@/utils/constant";

  export default {
    name: "token",
    data() {
      return {
        tokenData: [],
        loading: false,

        // 表单数据
        tokenForm: {
          id: 0,
          tokenName: "",
          tokenContent: "",
          status: 1,
        },

        // dialog 相关的变量
        showTokenDialog: false,
        dialogTitle: "添加新Token",
        isDisableForm: false,
        dialogConfirmButtonText: "",
        dialogType: "",
        tableIdx: -1,
      }
    },
    mounted() {
      this.loading = true;
      tokenService.getAllTokens(this)
        .then(resp => {
          if (resp.data.code === 1001) {
            this.tokenData = resp.data.data;
          } else {
            this.$message.error(resp.data.message);
          }
        })
        .catch(err => {
          console.log("error: ", err);
          this.$message.error(ApiConstant.error_500);
        })
        .then(() => {
          this.loading = false;
        })
    },
    methods: {

      initForm: function () {
        this.tokenForm.id = 0;
        this.tokenForm.tokenName = "";
        this.tokenForm.tokenContent = "";
        this.tokenForm.status = 1;
      },

      handleDelete: function (tableIdx, row) {
        let tokenId = row.id;
        tokenService.deleteToken(this, {"id": tokenId})
          .then(resp => {
            if (resp.data.code === 1001) {
              this.tokenData.splice(tableIdx, 1);
              this.$message.success(resp.data.message);
            } else {
              this.$message.error(resp.data.message);
            }
          })
          .catch(err => {
            console.log("error: ", err);
            this.$message.error(ApiConstant.error_500);
          });
      },

      handleConfirm: function () {
        if (this.dialogType === "add") {
          tokenService.addToken(this, this.tokenForm)
            .then(resp => {
              if (resp.data.code === 1001) {
                this.$message.success(resp.data.message);
                this.tokenData.push(resp.data.data);
                this.showTokenDialog = false;
              } else {
                this.$message.error(resp.data.message);
              }
            })
            .catch(err => {
              console.log("error: ", err);
              this.$message.error(ApiConstant.error_500);
            });
        } else if (this.dialogType === "edit") {
          tokenService.updateToken(this, this.tokenForm)
            .then(resp => {
              if (resp.data.code === 1001) {
                this.$message.success(resp.data.message);
                this.tokenData[this.tableIdx].tokenName = resp.data.data.tokenName;
                this.tokenData[this.tableIdx].tokenContent = resp.data.data.tokenContent;
                this.tokenData[this.tableIdx].status = resp.data.data.status;
              } else {
                this.$message.error(resp.data.message);
              }
            })
            .catch(err => {
              console.log("error: ", err);
              this.$message.error(ApiConstant.error_500);
            })
        } else {
          this.$message.error("未知错误");
        }
      },

      handleChangeStatus: function (row, tableIdx) {
        tokenService.changeTokenStatus(this, {"id": row.id})
          .then(resp => {
            if (resp.data.code === 1001) {
              this.$message.success(resp.data.message);
              this.tokenData[tableIdx].status = this.tokenData[tableIdx].status === 1 ? 0 : 1
            } else {
              this.$message.error(resp.data.message);
            }
          })
          .catch(err => {
            console.log("error: ", err);
            this.$message.error(ApiConstant.error_500);
          });
      },

      handleOpenDialog: function (type, tableIdx, row) {

        this.tableIdx = tableIdx;

        if (type === "add") {
          this.dialogTitle = "添加Token";
          this.dialogConfirmButtonText = "添加";
          this.dialogType = type;
          this.initForm();
          this.showTokenDialog = true;
        } else if (type === "edit") {
          // 编辑token
          this.dialogTitle = "编辑Token";
          this.dialogConfirmButtonText = "更新";
          this.dialogType = type;
          // 获取详情，更新form
          tokenService.getTokenDetail(this, {"id": row.id})
            .then(resp => {
              if (resp.data.code === 1001) {
                this.showTokenDialog = true;
                this.tokenForm.status = resp.data.data.status;
                this.tokenForm.tokenContent = resp.data.data.tokenContent;
                this.tokenForm.tokenName = resp.data.data.tokenName;
                this.tokenForm.id = resp.data.data.id;
              } else {
                this.$message.error(resp.data.message);
              }
            })
            .catch(err => {
              console.log("error: ", err);
              this.$message.error(ApiConstant.error_500);
            });
        } else {
          this.$message.error("未知错误");
        }
      },
    }
  }
</script>

<style scoped>

</style>
