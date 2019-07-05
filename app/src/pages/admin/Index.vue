<template>
  <div class="baro-admin">
    <a-layout>
      <a-layout-header
        :style="{
          position: 'fixed',
          zIndex: 5,
          width: '980px',
          padding: '0',
        }"
      >
        <router-link to="/admin/requests" class="logo">
          <img src="../../assets/logo.png" />
        </router-link>
        <a-menu
          mode="horizontal"
          :defaultSelectedKeys="[pathname]"
          :style="{
            lineHeight: '59px',
            background: 'none',
            border: 'none',
            display: 'inline-block',
            width: '300px',
            marginLeft: '25px',
          }"
        >
          <a-menu-item key="/admin/requests">
            <router-link to="/admin/requests">
              신청 목록
            </router-link>
          </a-menu-item>
          <a-menu-item key="/admin/keywords">
            <router-link to="/admin/keywords">
              키워드 목록
            </router-link>
          </a-menu-item>
          <a-menu-item key="/admin/supports">
            <router-link to="/admin/supports">
              문의 목록
            </router-link>
          </a-menu-item>
        </a-menu>
        <div class="right-button">
          <a-button type="primary" html-type="submit" @click="showModal">
            키워드 등록하기
          </a-button>
        </div>
      </a-layout-header>
    </a-layout>
    <div class="admin-wrap">
      <router-view />
    </div>
    <a-modal
      title="키워드 등록하기"
      v-model="visible"
      @ok="confirmRegister"
      ok-text="등록"
      cancel-text="취소"
      :destroyOnClose="true"
      class="keyword-add-modal"
    >
      <a-form :form="form">
        <a-form-item
          label="신청 키워드"
          :colon="false"
          :hasFeedback="true"
          help=""
        >
          <a-col span="16">
            <a-input
              addonBefore="hyu.ac/"
              v-decorator="[
                'keyword',
                {
                  rules: [
                    { required: true },
                    { validator: this.handleKeywordsCheck },
                  ],
                },
              ]"
            />
          </a-col>
        </a-form-item>
        <a-form-item
          :colon="false"
          label="연결 주소 (http[s]를 포함한 연결 주소)"
        >
          <a-col span="24">
            <a-input
              v-decorator="[
                'url',
                {
                  rules: [
                    {
                      type: 'url',
                      message: 'http(s)를 포함한 연결 주소를 입력해주세요.',
                    },
                    {
                      required: true,
                      message: '연결 주소는 필수 입력해주세요.',
                    },
                  ],
                },
              ]"
            />
          </a-col>
        </a-form-item>
        <a-form-item :colon="false" label="제목">
          <a-col span="24">
            <a-input
              v-decorator="[
                'title',
                {
                  rules: [{ required: true, message: '제목을 입력해주세요.' }],
                },
              ]"
            />
          </a-col>
        </a-form-item>
        <a-form-item
          :colon="false"
          label="설명 (신청 사유 및 용도를 적어주세요)"
        >
          <a-col span="24">
            <a-textarea
              :autosize="{ minRows: 5 }"
              v-decorator="[
                'description',
                {
                  rules: [{ required: true, message: '설명을 입력해주세요.' }],
                },
              ]"
            />
          </a-col>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Index',

  data() {
    return {
      // 키워드 등록 모달을 위한
      visible: false,
      is_requesting: false,
      form: this.$form.createForm(this),

      pathname: window.location.pathname,
    };
  },

  methods: {
    showModal() {
      this.visible = true;
    },

    // 키워드 등록 모달 - 키워드 체크
    handleKeywordsCheck(rule, value, callback) {
      if (!value) {
        callback();

        return false;
      }

      return axios
        .get(`${process.env.VUE_APP_API_HOST}/api/keywords/check?q=${value}`)
        .then(() => {
          callback();
        })
        .catch(() => {
          callback('사용할 수 없는 키워드입니다.');
        });
    },

    // 키워드 등록 모달 - 등록
    confirmRegister() {
      if (this.is_requesting) {
        return false;
      }

      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          axios
            .post(`${process.env.VUE_APP_API_HOST}/admin/api/keywords/`, values)
            .then(response => {
              this.$message.success(response.data.message);
              window.location.reload();
            })
            .catch(error => {
              this.$message.error(error.response.data.message);
            })
            .finally(() => {
              this.is_requesting = false;
              this.visible = false;
            });
        }
      });

      return true;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../../styles/admin';
</style>
