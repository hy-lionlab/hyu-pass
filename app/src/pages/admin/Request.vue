<template>
  <div class="admin-keyword-wrap">
    <a-table
      :columns="columns"
      :dataSource="data"
      :default-expand-all-rows="true"
    >
      <a slot="keyword" slot-scope="text">{{ text }}</a>
      <a slot="url" slot-scope="text" :href="text" target="_blank" style="word-break: break-all;">{{
        text
      }}</a>
      <span slot="status" slot-scope="text">
        <span v-if="text !== 'WAITING'">
          <a-tag :color="text === 'APPROVE' ? 'blue' : 'red'">{{
            text === 'APPROVE' ? '승인' : '반려'
          }}</a-tag>
        </span>
        <span v-else>
          <a-tag>대기</a-tag>
        </span>
      </span>
      <span slot="action" slot-scope="text, record">
        <span v-if="record.status === 'WAITING'">
          <a-popconfirm
            title="해당 키워드를 승인하시겠습니까?"
            @confirm="confirmApprove(record)"
            okText="승인"
            cancelText="취소"
          >
            <a-button type="primary">승인</a-button>
          </a-popconfirm>
          <a-divider type="vertical" />
          <a-button type="danger" @click="showModal(record)">반려</a-button>
        </span>
      </span>
      <div slot="expandedRowRender" slot-scope="record" style="margin: 0">
        <p>
          <strong>{{ record.title }}</strong>
        </p>
        <p>{{ record.description }}</p>
        <p>{{ record.name }} ({{ record.group }})</p>
        <p>{{ record.email }}</p>
      </div>
    </a-table>
    <a-modal
      title="반려하기"
      v-model="visible"
      @ok="confirmDisapprove"
      ok-text="반려"
      cancel-text="취소"
    >
      <a-form :form="form">
        <a-form-item :colon="false" label="반려 사유를 적어주세요.">
          <a-col span="24">
            <a-textarea
              :autosize="{ minRows: 10 }"
              v-decorator="[
                'disapproved_reason',
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
    title: '승인 상태',
    dataIndex: 'status',
    key: 'status',
    scopedSlots: { customRender: 'status' },
  },
  {
    title: '신청일',
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
  name: 'AdminRequest',

  mounted() {
    this.fetch();
  },

  data() {
    return {
      data: [],
      columns,
      visible: false,
      selectedRecord: null,
      form: this.$form.createForm(this),
    };
  },

  methods: {
    fetch() {
      axios
        .get(`${process.env.VUE_APP_API_HOST}/admin/api/requests`)
        .then(response => {
          this.data = response.data.requests.map(value => {
            let status = 'WAITING';
            if (value.is_approved !== null) {
              status = value.is_approved ? 'APPROVE' : 'DISAPPROVE';
            }

            return {
              key: value.id.toString(),
              id: value.id,
              keyword: value.keyword,
              url: value.url,
              title: value.title,
              description: value.description,
              email: value.email,
              name: value.name,
              group: value.group,
              status,
              created_at: value.created_at,
            };
          });
        })
        .catch(() => {
          this.$message.error('정보를 불러오는 도중 오류가 발생했습니다.');
        });
    },

    // 승인 처리
    confirmApprove(e) {
      axios
        .post(
          `${process.env.VUE_APP_API_HOST}/admin/api/requests/approve`,
          {
            id: e.id,
          },
          {
            withCredentials: true,
          },
        )
        .then(response => {
          this.$message.success(response.data.message);
          this.fetch();
        })
        .catch(() => {
          this.$message.error('승인 처리 도중 오류가 발생했습니다.');
        });
    },

    showModal(record) {
      this.visible = true;
      this.selectedRecord = record;
    },

    // 반려 처리
    confirmDisapprove(e) {
      this.is_requesting = true;

      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          const newValues = { ...values, id: this.selectedRecord.id };

          axios
            .post(
              `${process.env.VUE_APP_API_HOST}/admin/api/requests/disapprove`,
              newValues,
              {
                withCredentials: true,
              },
            )
            .then(response => {
              this.$message.success(response.data.message);
              this.fetch();
            })
            .catch(error => {
              this.$message.error(error.response.data.message);
            })
            .finally(() => {
              this.is_requesting = false;
              this.visible = false;
              this.selectedRecord = null;
              this.form.setFieldsValue({
                disapproved_reason: '',
              });
            });
        }
      });
    },
  },
};
</script>
