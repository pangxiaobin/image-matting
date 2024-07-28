<template>
  <div class="relative overflow-x-auto mx-auto h-full flex flex-col items-center justify-center">
    <div v-if="!loading" class="w-full max-w-3xl p-4">
      <div class="flex items-center justify-center h-full">
        <VueCompareImage :left-image="img1" :right-image="img2" class="img-container img-transparent-bg" />
      </div>
      <div class="flex justify-center space-x-4 mt-4">
        <button @click="goBack()" class="bg-green-500 text-white px-4 py-2 rounded-full">
          {{ t('common.btn_back') }}
        </button>
        <button @click="reselectImage()" class="bg-green-500 text-white px-4 py-2 rounded-full">
          {{ t('common.btn_reselect') }}
        </button>
        <button @click="copyImage()" class="bg-green-500 text-white px-4 py-2 rounded-full">
          {{ t('common.btn_copy') }}
        </button>
        <button @click="downloadImage()" class="bg-green-500 text-white px-4 py-2 rounded-full">
          {{ t('common.btn_download') }}
        </button>
      </div>
    </div>
    <div v-else class="flex justify-center items-center h-full">
      <div class="loader"></div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { VueCompareImage } from 'vue3-compare-image'
import { aiMattingAPI } from '@/api/ai_matting'
import baseAPI from '@/api/base'
import { useI18n } from 'vue-i18n'
import message from '@/utils/message.js'
const { t } = useI18n()
const loading = ref(true);
const route = useRoute();
const filePath = ref('');
filePath.value = route.params.filePath;

const imgType = ref('');
imgType.value = route.params.imgType;

const img1 = ref('');
const img2 = ref('');

async function initImage1() {
  if (imgType.value === 'local') {
    const result = await aiMattingAPI('get_local_file_base64', filePath.value);
    console.log(result);
    if (result.code === 200) {
      img1.value = result.data.base64_image;
    } else {
      message.error(result.error_msg);
    }
  } else {
    img1.value = filePath.value;
  }
}

const leftStyle = ref({

})

// 返回
const goBack = () => {
  window.history.back();
};

// 重新选择图片
const reselectImage = async () => {
  const res = await baseAPI('open_file_dialog', '');
  loading.value = true;
  imgType.value = 'local';
  if (res.data.file_path) {
    filePath.value = res.data.file_path;
    console.log(filePath.value);
    await initImage1();
    await getMattingResult();
  }
  loading.value = false;
};

// 获取AI模型结果
async function getMattingResult() {
  const result = await aiMattingAPI('predict', filePath.value);
  if (result.code === 200) {
    img2.value = result.data.no_bg_image;
  } else {
    message.error(result.error_msg);
  }
  loading.value = false;
}

// base64转blob
function base64ToBlob(base64Data) {
  const parts = base64Data.split(';base64,');
  const contentType = parts[0].split(':')[1];
  const byteCharacters = atob(parts[1]);
  const byteArrays = [];

  for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
    const slice = byteCharacters.slice(offset, offset + 1024);
    const byteNumbers = new Array(slice.length);

    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    const byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);
  }

  return new Blob(byteArrays, { type: contentType });
}

// 复制图像到剪贴板
async function copyImage() {
  try {
    const blob = base64ToBlob(img2.value);
    const item = new ClipboardItem({ 'image/png': blob });
    await navigator.clipboard.write([item]);
    message.info(t('common.copy_success'));
  } catch (error) {
    message.error(t('common.copy_error'), error);
  }
}

// 下载图像
async function downloadImage() {
  const response = await baseAPI('save_png_dialog', img2.value)
  if (response.code === 200) {
    message.info(t('common.download_success'));
  } else {
    message.error(t('common.download_error'));
  }
}

onBeforeMount(async () => {
  await initImage1()
})

onMounted(async () => {
  await getMattingResult()
})

</script>

<style scoped>
.img-container {
  max-width: 80%;
  max-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader {
  border: 8px solid #e1dfdf;
  /* Light grey */
  border-top: 8px solid #3498db;
  /* Blue */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.img-transparent-bg {
  background-size: 20px 20px;
  background-position: 0 0, 10px 10px;
  background-image: linear-gradient(45deg,
      #eee 25%,
      transparent 0,
      transparent 75%,
      #eee 0,
      #eee), linear-gradient(45deg, #eee 25%, #fff 0, #fff 75%, #eee 0, #eee);
}
</style>