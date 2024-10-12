<template>
  <div class="relative overflow-x-auto mx-auto flex flex-col items-center justify-center">
    <div v-if="!loading" class="w-full max-w-3xl p-4">
      <div class="flex items-center justify-center h-full">
        <VueCompareImage :left-image="img1" :right-image="img2" :style="containerStyle" class="img-container"
          :class="{ 'img-transparent-bg': selectedColor === 'transparent' }" />
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
        <button @click="showPopup = true" class="bg-green-500 text-white px-4 py-2 rounded-full">
          {{ t('common.btn_edit') }}
        </button>
        <div class="relative inline-block">
          <div @click="toggleColorPicker" class="relative w-10 h-10 border stacked-linear">
          </div>
          <!-- 颜色选择弹窗 -->
          <div v-if="showColorPicker"
            class="absolute left-0 bottom-full mb-2 bg-white p-2 shadow-lg rounded-lg border z-10 w-24">
            <div class="grid grid-cols-2 gap-1">
              <!-- 颜色选项 -->
              <div v-for="color in colors" :key="color" :style="{ backgroundColor: color }"
                @click="handleColorChange(color)" class="w-10 h-10 cursor-pointer border"
                :class="{ 'border-black': selectedColor === color, 'img-transparent-bg': color === 'transparent' }">
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
    <div v-else class="flex justify-center items-center h-full">
      <div class="loader"></div>
    </div>

    <!-- 调用弹窗组件，并传递 showModal 属性和标题 -->
    <ModalPopup v-model="showPopup" :title="t('common.btn_edit')" :showCancelButton="true" :showConfirmButton="false">
      <!-- 在弹窗插槽中放入图片编辑器内容 -->
      <ImageEditor :initialBase64="img2" @exportImage="handleExportImage" />
    </ModalPopup>
  </div>
</template>
<script setup>
import { ref, onMounted, onBeforeMount, computed } from 'vue'
import { useRoute } from 'vue-router'
import { VueCompareImage } from 'vue3-compare-image'
import { aiMattingAPI } from '@/api/ai_matting'
import baseAPI from '@/api/base'
import { useI18n } from 'vue-i18n'
import message from '@/utils/message.js'
import ImageEditor from '@/views/components/ImageEditor.vue';
import ModalPopup from '@/views/components/ModalPopup.vue';

const showPopup = ref(false)
// 导出编辑后的图片
const handleExportImage = (base64_data) => {
  showPopup.value = false;
  img2.value = base64_data;
}

const { t } = useI18n()
const loading = ref(true);
const route = useRoute();
const filePath = ref('');
filePath.value = route.query.filePath;

const imgType = ref('');
imgType.value = route.query.imgType;

const img1 = ref('');
const img2 = ref('');

const showColorPicker = ref(false);

const backgroundColor = ref('transparent');
const selectedColor = ref('transparent');

const containerStyle = computed(() => ({
  backgroundColor: backgroundColor.value,
}));

const selectColor = (color) => {
  backgroundColor.value = color;
  selectedColor.value = color;
};

// 颜色选项
const colors = ['transparent', '#FFFFFF', '#000000', '#FF0000', '#00FF00', '#FFFF00', '#0000FF', '#FF00FF', '#00FFFF', '#C0C0C0' ];

// Toggles the color picker modal
const toggleColorPicker = () => {
  showColorPicker.value = !showColorPicker.value;
};

// Updates the selected color
const handleColorChange = (color) => {
  selectColor(color);
  // toggleColorPicker();
};

async function initImage1() {
  if (imgType.value === 'local') {
    const result = await baseAPI('get_local_file_base64', filePath.value);
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
  const res = await baseAPI('open_file_dialog', false);
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
  max-width: 100%;
  max-height: 70vh; /* 限制最大高度为视口高度的70% */
  display: flex;
  justify-content: center;
  align-items: center;
}

.img-container >>> img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* 保持图片比例 */
}

.stacked-linear {
  background: linear-gradient(217deg,
      rgba(255, 0, 0, 0.8),
      rgba(255, 0, 0, 0) 70.71%),
    linear-gradient(127deg, rgba(0, 255, 0, 0.8), rgba(0, 255, 0, 0) 70.71%),
    linear-gradient(336deg, rgba(0, 0, 255, 0.8), rgba(0, 0, 255, 0) 70.71%);
}
</style>
