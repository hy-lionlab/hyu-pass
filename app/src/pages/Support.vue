<template>
  <div class="support-wrap">
    <a-form
      class="support-form"
      :form="form"
      layout="vertical"
      @submit="handleSubmit"
    >
      <h1>문의하기</h1>
      <a-divider />
      <!--  ================== 연결 정보    -->
      <a-form-item label="신청한 키워드" :colon="false" :hasFeedback="true">
        <a-col span="16">
          <a-input
            addonBefore="hyu.ac/"
            v-decorator="[
              'keyword',
              {
                rules: [
                  { required: true, message: '신청한 키워드를 입력해주세요.' },
                ],
              },
            ]"
          />
        </a-col>
      </a-form-item>
      <a-form-item
        :colon="false"
        label="변경 요청할 연결 주소 (http[s]를 포함한 연결 주소)"
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
                ],
              },
            ]"
          />
        </a-col>
      </a-form-item>
      <a-form-item label="이메일 (한양 메일만 가능합니다.)">
        <a-input
          addonAfter="@hanyang.ac.kr"
          v-decorator="[
            'email',
            {
              rules: [{ required: true, message: '이메일을 입력해주세요.' }],
            },
          ]"
        />
      </a-form-item>
      <a-form-item
        :colon="false"
        label="문의 내용 (수정 또는 삭제 요청 등 문의 내용을 입력해주세요.)"
      >
        <a-col span="24">
          <a-textarea
            :autosize="{ minRows: 8 }"
            v-decorator="[
              'description',
              { rules: [{ required: true, message: '설명을 입력해주세요.' }] },
            ]"
          />
        </a-col>
      </a-form-item>
      <!--  ================== 문의하기    -->
      <a-divider />
      <a-form-item :style="{ textAlign: 'right' }">
        <a-button
          type="primary"
          size="large"
          :loading="is_requesting"
          :disabled="is_requesting"
          :style="{ width: '100%', height: '50px' }"
          html-type="submit"
        >
          문의하기
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import axios from 'axios';
import ATextarea from 'ant-design-vue/es/input/TextArea';

export default {
  name: 'Support',

  components: { ATextarea },

  data() {
    return {
      form: this.$form.createForm(this),
      is_requesting: false,
    };
  },

  methods: {
    handleSubmit(e) {
      this.is_requesting = true;

      e.preventDefault();

      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          axios
            .post(`${process.env.VUE_APP_API_HOST}/api/supports`, values)
            .then(response => {
              this.is_requesting = false;
              this.$message.success(response.data.message);

              // FIXME: 경로 수정하기
              this.$router.push('/');
            })
            .catch(error => {
              this.is_requesting = false;
              this.$message.error(error.response.data.message);
            });
        }
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../styles/support';
</style>
