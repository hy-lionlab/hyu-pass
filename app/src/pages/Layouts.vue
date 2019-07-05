<template>
  <a-layout>
    <a-layout-header :style="{ position: 'fixed', zIndex: 5, width: '100%' }">
      <router-link to="/list" class="logo">
        <img src="../assets/logo.png" />
      </router-link>
      <div class="right">
        <a-button :style="{ marginRight: '5px' }">
          <router-link to="/change">
            <a-icon type="question" :style="{ marginRight: '3px' }" />
            문의하기
          </router-link>
        </a-button>
        <a-button :style="{ marginRight: '5px' }">
          <router-link to="/list">
            <a-icon type="ordered-list" />
            목록보기
          </router-link>
        </a-button>
        <a-button type="primary">
          <router-link to="/make">
            신청하기
          </router-link>
        </a-button>
      </div>
    </a-layout-header>

    <router-view />

    <a-layout-footer>
      "한양인을 연결하는 가장 빠르고 편리한 길. 한양 하이패스"<br />
      'HYPASS 한양하이패스'는 한양대 전용 '단축 주소(URL)' 서비스 입니다.<br />
      한양대학교 미디어전략센터 | (04763) 서울특별시 성동구 왕십리로 222 | email
      : {{ reportMail }} | Made by Lionlab<br />
      COPYRIGHT@2019 HANYANG UNIVERISTY. ALL RIGHTS RESERVED<br />
      <a
        href="http://wiki.hanyang.ac.kr/%ED%95%9C%EC%96%91%ED%95%98%EC%9D%B4%ED%8C%A8%EC%8A%A4"
        target="_blank"
        >About HYPASS</a
      >
    </a-layout-footer>
  </a-layout>
</template>

<script>
export default {
  name: 'Layouts',

  computed: {
    reportMail() {
      return `${process.env.VUE_APP_REPORT_MAIL}`;
    },
  },
};
</script>
