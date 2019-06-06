<template>
  <div class="keyword-add-form">
    <a-form layout="inline" :form="form" @submit="handleSubmit">
      <a-form-item :hasFeedback="true" help="">
        <a-input
          addonBefore="hyu.ac/"
          :style="{ width: '350px' }"
          v-decorator="[
            'keyword',
            {
              rules: [
                { required: true },
                { validator: this.handleKeywordsCheck },
              ],
            },
          ]"
          placeholder="키워드 입력"
        />
      </a-form-item>
      <a-form-item help="">
        <a-input
          :style="{ width: '350px' }"
          v-decorator="[
            'url',
            { rules: [{ required: true }, { type: 'url' }] },
          ]"
          placeholder="주소 입력"
        />
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          :disabled="is_requesting"
          :loading="is_requesting"
        >
          키워드 등록하기
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'KeywordAddForm',

  data() {
    return {
      form: this.$form.createForm(this),
      is_requesting: false,
    };
  },

  methods: {
    handleSubmit(e) {
      const $this = this;
      $this.is_requesting = true;

      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          axios
            .post(
              `${process.env.VUE_APP_API_HOST}/admin/api/keywords`,
              values,
              {
                withCredentials: true,
              },
            )
            .then(response => {
              $this.is_requesting = false;
              $this.$message.success(response.data.message);
              $this.$router.push('/admin/keywords');
            })
            .catch(error => {
              $this.is_requesting = false;
              $this.$message.error(error.response.data.message);
            });
        }
      });
    },

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
  },
};
</script>

<style></style>
