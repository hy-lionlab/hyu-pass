<template>
  <div class="baro-admin">
    <a-layout>
      <a-layout-header
        :style="{
          position: 'fixed',
          zIndex: 9998,
          width: '980px',
          padding: '0',
        }"
      >
        <router-link to="/admin/requests" class="logo">
          <a-icon
            type="tag"
            theme="twoTone"
            :style="{ fontSize: '16px', marginRight: '4px' }"
            twoToneColor="#025baf"
          />
          <span class="name">바로</span>
          <span class="colored-name">한양</span>
        </router-link>
        <a-menu
          mode="horizontal"
          :defaultSelectedKeys="[pathname]"
          :style="{
            lineHeight: '59px',
            background: 'none',
            border: 'none',
            display: 'inline-block',
            width: '300px',
            marginLeft: '25px',
          }"
        >
          <a-menu-item key="/admin/requests">
            <router-link to="/admin/requests">
              신청 목록
            </router-link>
          </a-menu-item>
          <a-menu-item key="/admin/keywords">
            <router-link to="/admin/keywords">
              키워드 목록
            </router-link>
          </a-menu-item>
          <a-menu-item key="/admin/supports">
            <router-link to="/admin/supports">
              문의 목록
            </router-link>
          </a-menu-item>
        </a-menu>
      </a-layout-header>
    </a-layout>
    <div class="admin-wrap">
      <keyword-add-form />
      <router-view />
    </div>
  </div>
</template>

<script>
import KeywordAddForm from '../../components/admin/KeywordAddForm';

export default {
  name: 'Index',
  components: { KeywordAddForm },

  data() {
    return {
      pathname: window.location.pathname,
    };
  },
};
</script>

<style lang="scss" scoped>
@import '../../styles/admin';
</style>
