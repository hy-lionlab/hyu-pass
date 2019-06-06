<template>
  <div class="admin-keyword-wrap">
    <a-table :columns="columns" :dataSource="data">
      <a slot="keyword" slot-scope="text">{{ text }}</a>
      <a slot="url" slot-scope="text" :href="text" target="_blank">{{
        text
      }}</a>
      <div slot="expandedRowRender" slot-scope="record" style="margin: 0">
        <p>{{ record.description }}</p>
        <p :style="{ fontSize: '12px', fontWeight: 'bold' }">
          IP 주소 - {{ record.ip_address }}
        </p>
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
    title: '이메일',
    dataIndex: 'email',
    key: 'email',
  },
  {
    title: '신청일',
    dataIndex: 'created_at',
    key: 'created_at',
  },
];

export default {
  name: 'AdminSupport',

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
        .get(`${process.env.VUE_APP_API_HOST}/admin/api/supports`)
        .then(response => {
          $this.data = response.data.supports.map((value, index) => {
            return {
              key: index.toString(),
              keyword: value.keyword,
              url: value.url,
              email: value.email,
              description: value.description,
              ip_address: value.ip_address,
              created_at: value.created_at,
            };
          });
        })
        .catch(() => {
          $this.$message.error('정보를 불러오는 도중 오류가 발생했습니다.');
        });
    },
  },
};
</script>
