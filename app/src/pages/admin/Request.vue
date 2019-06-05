<template>
  <div class="admin-keyword-wrap">
    <a-table :columns="columns" :dataSource="data">
      <a slot="keyword" slot-scope="text">{{ text }}</a>
      <a slot="url" slot-scope="text" :href="text" target="_blank">{{
        text
      }}</a>
      <span slot="action" slot-scope="text, record">
        <a-button type="primary">승인</a-button>
        <a-divider type="vertical" />
        <a-button type="danger">반려</a-button>
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
    };
  },

  methods: {
    fetch() {
      const $this = this;

      axios
        .get(`${process.env.VUE_APP_API_HOST}/admin/api/requests`)
        .then(response => {
          $this.data = response.data.requests.map((value, index) => {
            return {
              key: index.toString(),
              keyword: value.keyword,
              url: value.url,
              title: value.title,
              description: value.description,
              email: value.email,
              name: value.name,
              group: value.group,
              created_at: value.created_at,
            };
          });
        })
        .catch(() => {
          $this.$message.error('정보를 불러오는 도중 오류가 발생했습니다.');
        });
    },
  },

  props: ['host'],
};
</script>
