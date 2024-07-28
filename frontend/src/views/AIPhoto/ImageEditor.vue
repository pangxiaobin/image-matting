<template>
  <div class="editor h-full flex flex-col items-center">
    <div class="canvas relative w-full h-96" @dblclick="dblclick">
      <img :src="data.url" ref="image" @load="onImageLoad" class="object-contain w-full h-full" />
    </div>
    <div v-if="cropper" class="toolbar flex mt-4" @click="handleClick">
      <button class="toolbar__button" data-action="move" title="Move (M)">
        <span class="fa fa-arrows"></span>
      </button>
      <button class="toolbar__button" data-action="crop" title="Crop (C)">
        <span class="fa fa-crop"></span>
      </button>
      <!-- cancle -->
      <button v-if="data.cropping" class="toolbar__button" data-action="cancle" title="Cancle (CTRL + Z)">
        <span class="fa fa-times"></span>
      </button>
      <!-- 确认 -->
      <button v-if="data.cropping" class="toolbar__button" data-action="confirm" title="Confirm (Enter)">
        <span class="fa fa-check"></span>
      </button>
      <button class="toolbar__button" data-action="zoom-in" title="Zoom In (I)">
        <span class="fa fa-search-plus"></span>
      </button>
      <button class="toolbar__button" data-action="zoom-out" title="Zoom Out (O)">
        <span class="fa fa-search-minus"></span>
      </button>
      <button class="toolbar__button" data-action="rotate-left" title="Rotate Left (L)">
        <span class="fa fa-rotate-left"></span>
      </button>
      <button class="toolbar__button" data-action="rotate-right" title="Rotate Right (R)">
        <span class="fa fa-rotate-right"></span>
      </button>
      <button class="toolbar__button" data-action="flip-horizontal" title="Flip Horizontal (H)">
        <span class="fa fa-arrows-h"></span>
      </button>
      <button class="toolbar__button" data-action="flip-vertical" title="Flip Vertical (V)">
        <span class="fa fa-arrows-v"></span>
      </button>

    </div>
    <div v-if="data.cropped" class="toolbar flex mt-4" @click="handleClick">
      <!-- 运行 -->
      <button v-if="data.cropped" class="toolbar__button" data-action="play" title="Play (S)">
        <i class="fa-solid fa-circle-play"></i>
      </button>
      <!-- 删除 -->
      <button v-if="data.cropped" class="toolbar__button" data-action="del" title="Delete (Delete)">
        <span class="fa fa-trash"></span>
      </button>
    </div>
    <div v-if="cropper" class="flex justify-center space-x-4 mt-4">
      <select v-model="cropSizeCommon" class="select select-bordered select-sm w-full max-w-xs px-4">
        <option value="">{{ t('ai_photo.common_label') }}</option>
        <option v-for="item in commonSelectOptions" :value="item.value" :key="item.key">{{ t('ai_photo.common_label_options.option' + item.key) }}</option>
      </select>

      <select v-model="cropSizeIdType" class="select select-bordered select-sm w-full max-w-xs px-4 ">
        <option value="">{{ t('ai_photo.id_type_label') }}</option>
        <option v-for="item in idTypeSelectOptions" :value="item.value" :key="item.key">{{ t('ai_photo.id_type_options.option' + item.key) }}</option>
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

    <div  v-if="loading" class="flex justify-center items-center">
      <div class="loader"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, onBeforeMount } from 'vue';
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'
import { useRoute, useRouter } from 'vue-router'
import { aiMattingAPI } from '@/api/ai_matting'
import baseAPI from '@/api/base'
import { useI18n } from 'vue-i18n'
import message from '@/utils/message.js'

const { t } = useI18n()
const route = useRoute();
const router = useRouter()

const filePath = ref('');
filePath.value = route.params.filePath;

const imgType = ref('');
imgType.value = route.params.imgType;
const loading = ref(false);

const image = ref(null);
const data = ref({
  name: '',
  url: '',
  cropped: false,
  cropping: false,
  previousUrl: '',
  type: '',
});
const cropper = ref(null);
const canvasData = ref(null);
const cropBoxData = ref(null);
const croppedData = ref(null);
const cropSizeCommon = ref('');
const cropSizeIdType = ref('');

// 定义常规尺寸选项
const commonSelectOptions = [
  {
    key: 1,
    value: "295x413"
  },
  {
    key: 2,
    value: "390x567"
  },
  {
    key: 3,
    value: "413x531"
  },
  {
    key: 4,
    value: "1050x1500"
  },{
    key: 5,
    value: "1500x1050"
  }
]

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



// 重新选择图片
const reselectImage = async () => {
  const res = await baseAPI('open_file_dialog', '');
  imgType.value = 'local';
  if (res.data.file_path) {
    filePath.value = res.data.file_path;
    console.log(filePath.value);
    await initImage();
  }
  // 重新选择图片后，清空之前的裁剪数据
  del();
  // 重新选择图片后，初始化cropper
  initializeCropper();
};

async function getFileLocalBase64(filePath) {
  const result = await aiMattingAPI('get_local_file_base64', filePath);
  console.log(result);
  if (result.code === 200) {
    return result.data.base64_image;
  } else {
    message.error(result.error_msg);
    return '';
  }
}

async function initImage() {
  if (imgType.value === 'local') {
    data.value.url = await getFileLocalBase64(filePath.value);
  } else {
    data.value.url = filePath.value;
  }

}


function onImageLoad() {
  if (!data.value.cropped) {
    initializeCropper();
  }
}

const updateCropper = (size) => {
  if (!cropper.value || !size) return;
  const [width, height] = size.split('x').map(Number);
  console.log(width, height);
  cropper.value.setDragMode('crop');
  cropper.value.setAspectRatio(width / height);
  cropper.value.setCropBoxData({ width, height });
  cropper.value.crop();
};

watch([cropSizeIdType, cropSizeCommon], ([newSizeIdType, newSizeCommon], [oldSizeIdType, oldSizeCommon]) => {
  if (newSizeIdType !== oldSizeIdType){
      updateCropper(newSizeIdType);
      cropSizeCommon.value = '';
  }
  if (newSizeCommon !== oldSizeCommon){ 
      updateCropper(newSizeCommon);
      cropSizeIdType.value = '';
  }
});


const initializeCropper = () => {
  if (cropper.value) {
    cropper.value.destroy()
    cropper.value = null
  }
  cropper.value = new Cropper(image.value, {
    autoCrop: false,
    dragMode: 'move',
    background: true,
    ready: () => {
      if (croppedData.value) {
        cropper.value
          .crop()
          .setData(croppedData.value)
          .setCanvasData(canvasData.value)
          .setCropBoxData(cropBoxData.value);

        croppedData.value = null;
        canvasData.value = null;
        cropBoxData.value = null;
      }
    },
    crop: ({ detail }) => {
      if (detail.width > 0 && detail.height > 0 && !data.cropping) {
        update({ cropping: true });
      }
    }
  })
}

// 返回
const goBack = () => {
  window.history.back();
};


const stop = () => {
  if (cropper.value) {
    cropper.value.destroy();
    cropper.value = null;
  }
  console.log('stop');
};

const update = (newData) => {
  Object.assign(data.value, newData);
};

const crop = () => {
  if (data.value.cropping) {
    croppedData.value = cropper.value.getData();
    canvasData.value = cropper.value.getCanvasData();
    cropBoxData.value = cropper.value.getCropBoxData();
    update({
      cropped: true,
      cropping: false,
      previousUrl: data.value.url,
      url: cropper.value
        .getCroppedCanvas(data.value.type === 'image/png' ? {} : { fillColor: '#fff' })
        .toDataURL(data.value.type),
    });
    stop();
  }
};

const clear = () => {
  if (data.value.cropping) {
    cropper.value.clear();
    update({ cropping: false });
  }
};



const del = () => {
  stop();
  update({
    cropped: false,
    cropping: false,
    name: '',
    previousUrl: '',
    type: '',
    url: '',
  });
};


// 运行ai模型
const play = async () => {
  if (data.value.cropped) {
    loading.value = true;
    const res = await aiMattingAPI('predict', data.value.url);
    if (res.code === 200) {
      //  跳转到结果页
      data.value.url = res.data.no_bg_image;
      router.push({
        name: 'AIPhotoResult',
        params: {
          imgUrl: res.data.no_bg_image
        },
      });
      
    } else {
      message.error(res.error_msg);
    }
  }
  loading.value = false;
};


const handleClick = ({ target }) => {
  const action = target.getAttribute('data-action') || target.parentElement.getAttribute('data-action');

  switch (action) {
    case 'move':
    case 'crop':
      cropper.value.setDragMode(action);
      cropper.value.setAspectRatio(null);
      break;
    case 'cancle':
      clear();
      break;
    case 'confirm':
      crop();
      break;
    case 'zoom-in':
      cropper.value.zoom(0.1);
      break;
    case 'zoom-out':
      cropper.value.zoom(-0.1);
      break;
    case 'rotate-left':
      cropper.value.rotate(-90);
      break;
    case 'rotate-right':
      cropper.value.rotate(90);
      break;
    case 'flip-horizontal':
      cropper.value.scaleX(-cropper.value.getData().scaleX || -1);
      break;
    case 'flip-vertical':
      cropper.value.scaleY(-cropper.value.getData().scaleY || -1);
      break;
    case 'del':
      del();
      break;
    case 'play':
      play();
      break;
    default:
  }
};


const keydown = (e) => {
  if (!cropper.value) return;

  switch (e.key) {
    case 'z':
      if (e.ctrlKey) {
        e.preventDefault();
        clear();
      }
      break;
    case 'Delete':
      reset();
      break;
    case 'Enter':
      crop();
      break;
    case 'Escape':
      console.log('Escape');
      clear();
      break;
    case 'ArrowLeft':
      e.preventDefault();
      cropper.value.move(-1, 0);
      break;
    case 'ArrowUp':
      e.preventDefault();
      cropper.value.move(0, -1);
      break;
    case 'ArrowRight':
      e.preventDefault();
      cropper.value.move(1, 0);
      break;
    case 'ArrowDown':
      e.preventDefault();
      cropper.value.move(0, 1);
      break;
    case 'c':
      cropper.value.setDragMode('crop');
      break;
    case 'm':
      cropper.value.setDragMode('move');
      break;
    case 'i':
      cropper.value.zoom(0.1);
      break;
    case 'o':
      cropper.value.zoom(-0.1);
      break;
    case 'l':
      cropper.value.rotate(-90);
      break;
    case 'r':
      cropper.value.rotate(90);
      break;
    case 'h':
      cropper.value.scaleX(-cropper.value.getData().scaleX || -1);
      break;
    case 'v':
      cropper.value.scaleY(-cropper.value.getData().scaleY || -1);
      break;
  }
};

const dblclick = (e) => {
  if (e.target.className.indexOf('cropper-face') >= 0) {
    e.preventDefault();
    e.stopPropagation();
    crop();
  }
};

onBeforeMount(async () => {
  await initImage()
})


onMounted(() => {
  window.addEventListener('keydown', keydown);
  //  监听click事件
  // 判断是否是第一次加载，如不是，则清空之前的裁剪数据
  if (!filePath.value) {
    del();
  }

});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', keydown);
  stop();
});
</script>

<style scoped>
.editor {
  height: 100%;
}

.canvas {
  display: flex;
  align-items: center;
  justify-content: center;
}

.toolbar {
  background-color: rgba(0, 0, 0, 0.5);
  height: 2rem;
  width: 16rem;
  color: #fff;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.toolbar__button {
  background-color: transparent;
  border: 0;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  width: 2rem;
  height: 2rem;
}

.toolbar__button:hover {
  background-color: #0074d9;
}

/* loader */
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

</style>
