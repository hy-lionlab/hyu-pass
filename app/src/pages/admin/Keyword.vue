<template>
  <div class="admin-keyword-wrap">
    <a-table :columns="columns" :dataSource="data">
      <a slot="keyword" slot-scope="text">{{ text }}</a>
      <a slot="url" slot-scope="text" :href="text" target="_blank">{{
        text
      }}</a>
      <span slot="action" slot-scope="text, record">
        <a href="javascript:;">수정</a>
        <a-divider type="vertical" />
        <a href="javascript:;">삭제</a>
      </span>
      <p slot="expandedRowRender" slot-scope="record" style="margin: 0">
        <strong>{{ record.title }}</strong>
        <br /><br />
        {{ record.description }}
      </p>
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
    title: 'Hit',
    dataIndex: 'click_count',
    key: 'click_count',
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
    };
  },

  methods: {
    fetch() {
      const $this = this;

      axios
        .get(`${process.env.VUE_APP_API_HOST}/admin/api/keywords`)
        .then(response => {
          $this.data = response.data.keywords.map((value, index) => {
            return {
              key: index.toString(),
              keyword: value.keyword,
              url: value.url,
              title: value.title,
              description: value.description,
              created_at: value.created_at,
              click_count: value.click_count,
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
