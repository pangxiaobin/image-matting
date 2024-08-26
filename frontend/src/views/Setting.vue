<template>
  <div class="p-6 max-full flex flex-col items-center">
    <h2 class="text-2xl font-bold mb-3">{{ t('setting.title') }}</h2>

    <div class="w-full max-w-lg p-3 rounded-lg shadow-md mb-3">
      <div class="mb-4">
        <label class="block text-md font-medium mb-2" for="language">{{ t('setting.language') }}</label>
        <select id="language" v-model="settingInfo.language" class="select select-bordered w-full">
          <option v-for="(key, val, index) in languageList" :key="index" :value="val">{{ key }}</option>
        </select>
      </div>

      <!-- <div class="mb-4">
        <label class="block text-md font-medium mb-2" for="storagePath">{{ t('setting.save_dir') }}</label>
        <input type="text" id="storagePath" v-model="settingInfo.save_dir" class="input input-bordered w-full" />
      </div> -->

      <button @click="saveSettings" class="btn btn-primary w-full">{{ t('setting.save_btn') }}</button>
    </div>

    <div class="w-full max-w-lg p-6 rounded-lg shadow-md mb-6  select-text">
      <h3 class="text-xl font-semibold mb-2">{{ t('setting.system_info') }}</h3>
      <p class=" mb-2">{{ t('setting.author') }}: {{ systemInfo.author }}</p>
      <p class=" mb-2">{{ t('setting.email') }}: {{ systemInfo.email }}</p>
      <p class="mb-2">Github: {{ systemInfo.github }}</p>
      <p class="mb-2">Website: {{ systemInfo.website }}</p>
      <p class=" mb-2">{{ t('setting.version') }}: {{systemInfo.version }}</p>
      <div class="flex justify-center">
        <img src="/wx_qr.png" alt="WeChat QR Code" class="w-full h-32 object-cover rounded-md" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { settingAPI } from '@/api/user';
import baseAPI from '@/api/base';
import { languageList } from '@/locales/index'
import { useI18n } from 'vue-i18n'
const { locale } = useI18n();
import message from '@/utils/message.js'
const { t } = useI18n()
const settingInfo = ref({
  'language': '',
  // 'save_dir': '',
})

const systemInfo = ref({
  'author': '',
  'email': '',
  'version': '',
  'github': '',
  'website': '',
})

// 获取设置信息
const getSettingInfo = async () => {
  const res = await settingAPI('get', '')
  settingInfo.value = res.data
  console.log(settingInfo.value)
  locale.value = settingInfo.value.language
}
// 切换语言
const changeLanguage = (lang) => {
  locale.value = lang;
};

// 保存设置
const saveSettings = async () => {
  const res = await settingAPI('put', settingInfo.value)
  if (res.code === 200) {
    message.info(res.msg);
    changeLanguage(settingInfo.value.language)
  } else {
    message.error(res.err_msg);
  }
}
// 获取系统信息
const getSystemInfo = async () => {
  const res = await baseAPI('get_system_info')
  if (res.code === 200) { 
    systemInfo.value = res.data
  }
}

onMounted(async () => {
  await getSettingInfo();
  await getSystemInfo();
})

</script>