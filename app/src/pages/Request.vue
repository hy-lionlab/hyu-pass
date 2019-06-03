<template>
  <div class="request-wrap">
    <a-form
      class="request-form"
      :form="form"
      layout="vertical"
      @submit="handleSubmit"
    >
      <h1>신청하기</h1>
      <a-divider />
      <!--  ================== 연결 정보    -->
      <a-form-item label="신청 키워드" :colon="false" :hasFeedback="true">
        <a-col span="16">
          <a-input
            addonBefore="hyu.ac/"
            v-decorator="[
              'keyword',
              {
                rules: [
                  { required: true, message: '키워드를 입력해주세요.' },
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
                  { required: true, message: '연결 주소는 필수 입력해주세요.' },
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
              { rules: [{ required: true, message: '제목을 입력해주세요.' }] },
            ]"
          />
        </a-col>
      </a-form-item>
      <a-form-item :colon="false" label="설명 (신청 사유 및 용도를 적어주세요)">
        <a-col span="24">
          <a-textarea
            :autosize="{ minRows: 5 }"
            v-decorator="[
              'description',
              { rules: [{ required: true, message: '설명을 입력해주세요.' }] },
            ]"
          />
        </a-col>
      </a-form-item>
      <!--  ================== 기본 정보    -->
      <a-divider />
      <a-form-item :colon="false" label="신청자 구분">
        <a-col span="12">
          <a-select
            v-decorator="[
              'person_type',
              {
                rules: [
                  { required: true, message: '신청자 구분을 선택해주세요.' },
                ],
              },
            ]"
            placeholder="신청자 구분을 선택해주세요."
          >
            <a-select-option value="1">
              직원
            </a-select-option>
            <a-select-option value="2">
              교수
            </a-select-option>
            <a-select-option value="3">
              학생
            </a-select-option>
          </a-select>
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
      <a-form-item :colon="false" label="이름">
        <a-col span="14">
          <a-input
            v-decorator="[
              'name',
              {
                rules: [{ required: true, message: '이름을 입력해주세요.' }],
              },
            ]"
          />
        </a-col>
      </a-form-item>
      <a-form-item :colon="false" label="소속">
        <a-col span="14">
          <a-input
            v-decorator="[
              'group',
              {
                rules: [{ required: true, message: '소속을 입력해주세요.' }],
              },
            ]"
          />
        </a-col>
      </a-form-item>
      <!--  ================== 신청하기    -->
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
          신청하기
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import axios from 'axios';
import ATextarea from 'ant-design-vue/es/input/TextArea';

export default {
  name: 'Request',

  components: { ATextarea },

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

      $this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          axios
            .post(`${process.env.VUE_APP_API_HOST}/keywords`, values)
            .then(response => {
              $this.is_requesting = false;
              alert(response.data.message);
              $this.$router.push('/');
            })
            .catch(error => {
              $this.is_requesting = false;
              alert(error.response.data.message);
            });
        }
      });
    },

    handleKeywordsCheck(rule, value, callback) {
      if (!value) {
        callback();

        return false;
      }

      const $this = this;
      $this.is_requesting = true;

      return axios
        .get(`${process.env.VUE_APP_API_HOST}/keywords/check?q=${value}`)
        .then(response => {
          $this.is_requesting = false;
          callback();
        })
        .catch(error => {
          $this.is_requesting = false;
          callback('사용할 수 없는 키워드입니다.');
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../styles/request';
</style>
