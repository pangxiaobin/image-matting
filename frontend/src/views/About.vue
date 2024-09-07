<template>
  <div class="p-6 max-full flex flex-col items-center">
    <h2 class="text-2xl font-bold mb-3">{{ t('about.title') }}</h2>
    <div class="w-full max-w-lg p-6 rounded-lg shadow-md mb-6  select-text">
      <h3 class="text-xl font-semibold mb-2">{{ t('about.system_info') }}</h3>
      <p class=" mb-2">{{ t('about.author') }}: {{ systemInfo.author }}</p>
      <p class=" mb-2">{{ t('about.email') }}: {{ systemInfo.email }}</p>
      <p class="mb-2">Github:<span class="cursor-pointer text-blue-500" @click="openLink(systemInfo.github)">{{ systemInfo.github }}</span></p>
      <p class="mb-2">Website: <span class="cursor-pointer text-blue-500" @click="openLink(systemInfo.website)">{{ systemInfo.website }}</span></p>
      <p class=" mb-2">{{ t('about.version') }}: {{ systemInfo.version }}</p>
      <div class="flex justify-center">
        <img src="/wx_qr.png" alt="WeChat QR Code" class="w-full h-32 object-cover rounded-md" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import baseAPI from '@/api/base';


const { locale } = useI18n();
const { t } = useI18n()
const systemInfo = ref({
  'author': '',
  'email': '',
  'version': '',
  'github': '',
  'website': '',
})


const openLink = async (url) => {
  await baseAPI('open_link', url)
}


// 获取系统信息
const getSystemInfo = async () => {
  const res = await baseAPI('get_system_info')
  if (res.code === 200) {
    systemInfo.value = res.data
  }
}

onMounted(async () => {
  await getSystemInfo();
})

</script>