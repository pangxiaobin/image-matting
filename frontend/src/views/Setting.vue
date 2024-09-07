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

      <div class="mb-4">
        <label class="block text-md font-medium mb-2" for="api_key">{{ t('setting.tinify_key') }}          
          <span class="cursor-pointer text-blue-500" @click="openLink('https://tinypng.com/developers')" target="_blank">GET KEY</span>
        </label>
        <input ref="apiKeyInput" id="api_key" v-on:mouseenter="handleMouseEnter" v-on:mouseleave="handleMouseLeave" type="password"
          v-model="settingInfo.tinify.tinify_key" class="input input-bordered w-full" />
      </div>

      <div class="mb-4">
        <label class="block text-md font-medium mb-2" for="tinify_used_count">{{ t('setting.tinify_used_count') }}          
        </label>
        <input id="tinify_used_count" disabled type="text" v-model="settingInfo.tinify.compression_count" class="input input-bordered w-full" />
      </div>

      <div class="mb-4">
        <label class="block text-md font-medium mb-2" for="preserve">{{ t('setting.tinify_preserving') }} 
        </label>
        <MultiSelect id="preserve" v-model="settingInfo.tinify.preserve" :options="['copyright', 'creation', 'location']"
          placeholder="{{ t('setting.tinify_preserve_placeholder') }}" />
      </div>

      <button @click="saveSettings" class="btn btn-primary w-full">{{ t('setting.save_btn') }}</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { settingAPI } from '@/api/user';
import MultiSelect from '@/views/components/MultiSelect.vue';

import baseAPI from '@/api/base';
import { languageList } from '@/locales/index'
import { useI18n } from 'vue-i18n'
const { locale } = useI18n();
import message from '@/utils/message.js'
const { t } = useI18n()
const settingInfo = ref({
  'language': '',
  'tinify': {
    'tinify_key': '',
    'preserve': [],
    'compression_count': 0,
  }
})

const formData = ref({
  'language': '',
  'tinify.tinify_key': '',
  'tinify.preserve': []
})

const openLink = async (url) => {
   await baseAPI('open_link', url)
}

const apiKeyInput = ref(null)

// 鼠标移出隐藏API密钥
const handleMouseLeave = () => {
  apiKeyInput.value.type = 'password'
}
// 鼠标移入显示API密钥
const handleMouseEnter = () => {
  apiKeyInput.value.type = 'text'
}

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
  console.log(settingInfo.value)
  formData.value.language = settingInfo.value.language
  formData.value['tinify.tinify_key'] = settingInfo.value.tinify.tinify_key
  formData.value['tinify.preserve'] = settingInfo.value.tinify.preserve
  const res = await settingAPI('put', formData.value)
  if (res.code === 200) {
    message.info(res.msg);
    changeLanguage(settingInfo.value.language)
  } else {
    message.error(res.err_msg);
  }
}


onMounted(async () => {
  await getSettingInfo();
})

</script>