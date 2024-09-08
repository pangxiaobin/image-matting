<template>
  <div class="container mx-auto">
  
    <ImageEditor v-if="!isCropped" :imageUrl="imageUrl" :toolbarOptions="toolbarOptions" :cropSize="cropSize" @confirm="onCropConfirm"
      @cancel="onCropCancel" />
    <ImageEditor v-if="isCropped" :imageUrl="croppedImage" :toolbarOptions="coppedToolbarOptions" :delete="onCropDelete" :play="onCropPlay" />
    <div v-if="!isCropped" class="flex justify-center space-x-4 mt-4">
      <select v-model="cropSizeCommon" class="select select-bordered select-sm w-full max-w-xs px-4">
        <option value="">{{ t('ai_photo.common_label') }}</option>
        <option v-for="item in commonSelectOptions" :value="item.value" :key="item.key">{{
          t('ai_photo.common_label_options.option' + item.key) }}</option>
      </select>

      <select v-model="cropSizeIdType" class="select select-bordered select-sm w-full max-w-xs px-4 ">
        <option value="">{{ t('ai_photo.id_type_label') }}</option>
        <option v-for="item in idTypeSelectOptions" :value="item.value" :key="item.key">{{
          t('ai_photo.id_type_options.option' + item.key) }}</option>
      </select>

    </div>
    <div class="flex justify-center space-x-4 mt-4">
      <button @click="goBack()" class="bg-green-500 text-white px-4 py-2 rounded-full">
        {{ t('common.btn_back') }}
      </button>
      <button @click="reselectImage()" class="bg-green-500 text-white px-4 py-2 rounded-full">
        {{ t('common.btn_reselect') }}
      </button>
    </div>

    <div v-if="loading" class="flex justify-center items-center">
      <div class="loader"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import ImageEditor from '@/views/components/ImageCroperView.vue';
import { aiMattingAPI } from '@/api/ai_matting';
import baseAPI from '@/api/base';
import message from '@/utils/message.js';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();


const imageUrl = ref('');
const isCropped = ref(false);
const croppedImage = ref('');
const loading = ref(false);
const cropSizeCommon = ref('');
const cropSizeIdType = ref('');
const cropSize = ref('');

const commonSelectOptions = [
  { key: 1, value: "295x413" },
  { key: 2, value: "390x567" },
  { key: 3, value: "413x531" },
  { key: 4, value: "1050x1500" },
  { key: 5, value: "1500x1050" }
];

const idTypeSelectOptions = [
  { key: 1, value: "295x413" },
  { key: 2, value: "402x531" },
  { key: 3, value: "130x170" },
  { key: 4, value: "114x156" },
  { key: 5, value: "413x626" },
  { key: 6, value: "144x192" },
  { key: 7, value: "114x156" },
  { key: 8, value: "160x210" },
  { key: 9, value: "413x579" },
  { key: 10, value: "480x640" },
  { key: 11, value: "360x480" },
  { key: 12, value: "358x441" },
  { key: 13, value: "358x441" },
  { key: 14, value: "480x640" },
  { key: 15, value: "295x413" },
  { key: 16, value: "390x567" },
  { key: 17, value: "800x800" },
  { key: 18, value: "700x700" }
];

const toolbarOptions = ref({
  move: true,
  crop: true,
  cancel: true,
  confirm: true,
  zoomIn: true,
  zoomOut: true,
  rotateLeft: true,
  rotateRight: true,
  flipHorizontal: true,
  flipVertical: true,
  background: true,
  delete: false,
  play: false,
});

const coppedToolbarOptions = ref({
  move: true,
  crop: false,
  cancel: false,
  confirm: false,
  zoomIn: true,
  zoomOut: true,
  rotateLeft: false,
  rotateRight: false,
  flipHorizontal: false,
  flipVertical: false,
  background: false,
  delete: true,
  play: true,
});

// 获取路由参数中的图片数据
const filePath = ref(route.query.filePath || '');
const imgType = ref(route.query.imgType || '');

// 根据图片路径获取base64数据
const getFileLocalBase64 = async (filePath) => {
  const result = await baseAPI('get_local_file_base64', filePath);
  if (result.code === 200) {
    return result.data.base64_image;
  } else {
    message.error(result.error_msg);
    return '';
  }
};

// 初始化图片
const initImage = async () => {
  if (imgType.value === 'local') {
    imageUrl.value = await getFileLocalBase64(filePath.value);
  } else {
    imageUrl.value = filePath.value;
  }
  croppedImage.value = ''; // 清空之前的裁剪数据
  isCropped.value = false; // 重置裁剪状态
};

// 重新选择图片
const reselectImage = async () => {
  const res = await baseAPI('open_file_dialog', false);
  imgType.value = 'local';
  if (res.data.file_path) {
    filePath.value = res.data.file_path;
    await initImage();
  }
};


const goBack = () => {
  router.back();
};

const onCropPlay = async () => {
  if (croppedImage.value) {
    loading.value = true;
    const res = await aiMattingAPI('predict', croppedImage.value);
    if (res.code === 200) {
      // 跳转到结果页
      // imageUrl.value = res.data.no_bg_image;
      router.push({
        name: 'AIPhotoResult',
        query: {
          imgUrl: res.data.no_bg_image,
        },
      });
    } else {
      message.error(res.error_msg);
    }
    loading.value = false;
  }
};

const onCropDelete = ()=> {
  console.log('Crop deleted');
  croppedImage.value = '';
  isCropped.value = false;
}


const onCropConfirm = (croppedImageDataUrl) => {
  console.log('Crop confirmed');
  croppedImage.value = croppedImageDataUrl;
  isCropped.value = true;
};

const onCropCancel = () => {
  console.log('Crop canceled');
};


watch([cropSizeCommon, cropSizeIdType], ([newSizeCommon, newSizeIdType], [oldSizeCommon, oldSizeIdType]) => {
  if (newSizeIdType !== oldSizeIdType) {
    cropSize.value = newSizeIdType;
    cropSizeCommon.value = '';
  }
  if (newSizeCommon !== oldSizeCommon) {
    cropSize.value = newSizeCommon;
    cropSizeIdType.value = '';
  }
});


// 在组件挂载时初始化图片
onMounted(async () => {
  await initImage();
});
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}
</style>
