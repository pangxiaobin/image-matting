<template>
  <router-view />
</template>

<script setup>
import { onBeforeMount } from 'vue'
import { settingAPI } from '@/api/user';
import { useI18n } from 'vue-i18n'
import { useRouter } from "vue-router"


const { locale } = useI18n();
// 获取用户设置的语言
onBeforeMount(async () => {
  const settingInfo = await settingAPI('get', '')
  if (settingInfo.data.language) {
    locale.value = settingInfo.data.language
  } else {
    locale.value = 'zh-CN'
  }
  if(settingInfo.data.theme){
    document.documentElement.setAttribute('data-theme', settingInfo.data.theme)
  }

})

</script>
<style>
/* 在此处添加任何全局样式 */
</style>
