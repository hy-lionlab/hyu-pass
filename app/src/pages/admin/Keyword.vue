<template>
  <div class="admin-keyword-wrap">
    <a-table :columns="columns" :dataSource="data">
      <span slot="keyword" slot-scope="text">
        <b>{{ text }}</b>
        <a @click="doCopy(text)" style="margin-left: 5px;">
          <a-icon type="copy" />
        </a>
        <a @click="qrDownload(text)" style="margin-left: 5px;">
          <a-icon type="download" />
        </a>
      </span>
      <a slot="url" slot-scope="text" :href="text" target="_blank">
        {{ text }}
      </a>
      <span slot="action" slot-scope="text, record">
        <a-button @click="showModal(record)">수정</a-button>
        <a-divider type="vertical" />
        <a-popconfirm
          :title="
            `해당 키워드를 ${record.is_active ? '비' : ''}활성화하시겠습니까?`
          "
          @confirm="confirmActive(record)"
          okText="승인"
          cancelText="취소"
        >
          <a-button :type="record.is_active ? 'danger' : 'primary'"
            >{{ record.is_active ? '비' : '' }}활성화</a-button
          >
        </a-popconfirm>
      </span>
      <p slot="expandedRowRender" slot-scope="record" style="margin: 0">
        <strong>{{ record.title }}</strong>
        <br /><br />
        {{ record.description }}
      </p>
    </a-table>
    <a-modal
      title="수정하기"
      v-model="visible"
      @ok="confirmModify"
      ok-text="수정"
      cancel-text="취소"
      :destroyOnClose="true"
      :okButtonProps="{
        props: { disabled: is_requesting, loading: is_requesting },
      }"
      :cancelButtonProps="{
        props: { disabled: is_requesting, loading: is_requesting },
      }"
    >
      <a-form :form="form">
        <a-form-item class="input-type-hidden-item">
          <a-col span="16">
            <a-input
              type="hidden"
              v-decorator="[
                'id',
                {
                  rules: [{ required: true, message: '' }],
                },
              ]"
            />
          </a-col>
        </a-form-item>
        <a-form-item label="신청 키워드" :colon="false">
          <a-col span="16">
            <a-input
              addonBefore="hyu.ac/"
              v-decorator="[
                'keyword',
                {
                  rules: [
                    { required: true, message: '키워드를 입력해주세요.' },
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

const columns = [
  {
    title: '키워드',
    dataIndex: 'keyword',
    key: 'keyword',
    scopedSlots: { customRender: 'keyword' },
  },
  {
    title: 'URL',
    dataIndex: 'url',
    key: 'url',
    scopedSlots: { customRender: 'url' },
  },
  {
    title: 'Hit',
    dataIndex: 'hit_count',
    key: 'hit_count',
  },
  {
    title: '생성일',
    dataIndex: 'created_at',
    key: 'created_at',
  },
  {
    title: 'Actions',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

export default {
  name: 'AdminKeyword',

  mounted() {
    this.fetch();
  },

  data() {
    return {
      data: [],
      columns,
      visible: false,
      selectedRecord: null,
      is_requesting: false,
      form: this.$form.createForm(this),
    };
  },

  methods: {
    fetch() {
      const $this = this;

      axios
        .get(`${process.env.VUE_APP_API_HOST}/admin/api/keywords`)
        .then(response => {
          $this.data = response.data.keywords.map(value => {
            return {
              id: value.id,
              key: value.id.toString(),
              keyword: value.keyword,
              url: value.url,
              title: value.title,
              description: value.description,
              created_at: value.created_at,
              hit_count: value.hit_count,
              is_active: value.is_active,
            };
          });
        })
        .catch(() => {
          $this.$message.error('정보를 불러오는 도중 오류가 발생했습니다.');
        });
    },

    doCopy(keyword) {
      const url = `hyu.ac/${keyword}`;
      const $this = this;

      this.$copyText(url).then(() => {
        $this.$message.success(`${url} 주소가 복사 되었습니다. 🎉`);
      });
    },

    qrDownload(keyword) {
      const url = `hyu.ac/${keyword}`;
      window.open(`/qrcode?data=${url}`, '_blank');
    },

    showModal(record) {
      this.visible = true;
      this.selectedRecord = record;

      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          keyword: record.keyword,
          url: record.url,
          title: record.title,
          description: record.description,
        });
      });
    },

    // 활성, 비활성 처리
    confirmActive(e) {
      const $this = this;

      axios
        .post(
          `${process.env.VUE_APP_API_HOST}/admin/api/keywords/active/status`,
          {
            id: e.id,
            is_active: !e.is_active,
          },
          {
            withCredentials: true,
          },
        )
        .then(response => {
          $this.$message.success(response.data.message);
          $this.fetch();
        })
        .catch(() => {
          $this.$message.error('승인 처리 도중 오류가 발생했습니다.');
          $this.fetch();
        });
    },

    // 수정
    confirmModify() {
      const $this = this;
      $this.is_requesting = true;

      $this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          axios
            .post(
              `${process.env.VUE_APP_API_HOST}/admin/api/keywords/${values.id}`,
              values,
            )
            .then(response => {
              $this.$message.success(response.data.message);
            })
            .catch(error => {
              $this.$message.error(error.response.data.message);
            })
            .finally(() => {
              $this.is_requesting = false;
              $this.visible = false;
              $this.fetch();
            });
        }
      });
    },
  },
};
</script>
