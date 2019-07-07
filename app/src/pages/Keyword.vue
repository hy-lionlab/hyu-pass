<template>
  <div class="keyword-wrap">
    <div class="keyword-content">
      <h1 class="title">목록 보기</h1>
      <a-table :columns="columns" :dataSource="data">
        <span slot="keyword" slot-scope="text">
          <b>{{ text }}</b>
          <a @click="doCopy(text)">
            <a-icon type="copy" />
          </a>
        </span>
        <a slot="url" slot-scope="text" :href="text" target="_blank" style="word-break: break-all;">
          {{ text }}
        </a>
        <p slot="expandedRowRender" slot-scope="record" style="margin: 0">
          <strong>{{ record.title }}</strong>
          <br /><br />
          {{ record.description }}
        </p>
      </a-table>
    </div>
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
    title: '시작일',
    dataIndex: 'created_at',
    key: 'created_at',
  },
];

export default {
  name: 'Keyword',

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
      axios
        .get(`${process.env.VUE_APP_API_HOST}/api/keywords`)
        .then(response => {
          this.data = response.data.keywords.map((value, index) => {
            return {
              key: index.toString(),
              keyword: value.keyword,
              url: value.url,
              title: value.title,
              description: value.description,
              created_at: value.created_at,
            };
          });
        })
        .catch(() => {
          this.$message.error('정보를 불러오는 도중 오류가 발생했습니다.');
        });
    },

    doCopy(keyword) {
      const url = `hyu.ac/${keyword}`;

      this.$copyText(url).then(() => {
        this.$message.success(`${url} 주소가 복사 되었습니다. 🎉`);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../styles/keyword';
</style>
