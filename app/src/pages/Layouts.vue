<template>
  <a-layout>
    <a-layout-header
      :style="{ position: 'fixed', zIndex: 9998, width: '100%' }"
    >
      <router-link to="/" class="logo">
        <a-icon
          type="tag"
          theme="twoTone"
          :style="{ fontSize: '16px', marginRight: '4px' }"
          twoToneColor="#025baf"
        />
        <span class="name">바로</span>
        <span class="colored-name">한양</span>
      </router-link>
      <div class="right">
        <a-button :style="{ marginRight: '5px' }">
          <router-link to="/supports">
            <a-icon type="question" :style="{ marginRight: '3px' }" />
            문의하기
          </router-link>
        </a-button>
        <a-button :style="{ marginRight: '5px' }">
          <router-link to="/keywords">
            <a-icon type="ordered-list" />
            목록보기
          </router-link>
        </a-button>
        <a-button type="primary">
          <router-link to="/requests">
            신청하기
          </router-link>
        </a-button>
      </div>
    </a-layout-header>

    <router-view />
  </a-layout>
</template>

<script>
export default {
  name: 'Layouts',
};
</script>
