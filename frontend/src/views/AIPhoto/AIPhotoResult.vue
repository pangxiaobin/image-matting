<template>
    <div class="relative overflow-x-auto w-full h-full flex flex-col items-center justify-center">
        <div class="flex items-center justify-center" style="height: 60vh; width: auto;">
            <img :src="imageSrc" :class="{ 'img-transparent-bg': selectedColor === 'transparent' }"
                class="relative z-10 border border-indigo-600 object-contain" :style="containerStyle" style="max-width: 100%;max-height: 100%; width: auto; height: auto;" />
        </div>
        <div class="flex space-x-2 mb-4 mt-4 ">
            <button @click="selectColor('transparent')"
                :class="{ 'border-2 border-black': selectedColor === 'transparent' }"
                class="bg-transparent w-10 h-10 border img-transparent-bg">
                <div class="w-full h-full"></div>
            </button>
            <button @click="selectColor('#FFFFFF')" :class="{ 'border-2 border-black': selectedColor === '#FFFFFF' }"
                class="bg-white w-10 h-10 border"></button>
            <button @click="selectColor('#808080')" :class="{ 'border-2 border-black': selectedColor === '#808080' }"
                class="bg-gray-500 w-10 h-10 border"></button>
            <button @click="selectColor('#0000FF')" :class="{ 'border-2 border-black': selectedColor === '#0000FF' }"
                class="bg-blue-500 w-10 h-10 border"></button>
            <button @click="selectColor('#FF0000')" :class="{ 'border-2 border-black': selectedColor === '#FF0000' }"
                class="bg-red-500 w-10 h-10 border"></button>

            <button @click="selectColor('#008000')" :class="{ 'border-2 border-black': selectedColor === '#008000' }"
                class="bg-green-500 w-10 h-10 border"></button>

            <div class="relative w-10 h-10 border stacked-linear">
                <input type="color" v-model="backgroundColor" @change="handleColorChange"
                    class="absolute top-0 left-0 w-full h-full opacity-0 cursor-pointer" />
                <!-- <div class="w-full h-full bg-gray-500"></div> -->
            </div>
            <!-- <input type="color" v-model="backgroundColor" @change="handleColorChange"
                class="w-12 h-12   border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /> -->
        </div>
        <div class="flex justify-center space-x-4 mt-4">
            <button @click="goBack()" class="bg-green-500 text-white px-4 py-2 rounded-full">
                {{ t('common.btn_back') }}
            </button>
            <button @click="downloadImage()" class="bg-green-500 text-white px-4 py-2 rounded-full">
                {{ t('common.btn_download') }}
            </button>
        </div>

    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n'
import baseAPI from '@/api/base'
import message from '@/utils/message.js'

const { t } = useI18n()
const route = useRoute();
const imageSrc = ref(route.params.imgUrl);
const backgroundColor = ref('transparent');
const selectedColor = ref('transparent');

const containerStyle = computed(() => ({
    backgroundColor: backgroundColor.value,
}));

// const isTransparent = computed(() => backgroundColor.value === 'transparent');

const handleColorChange = (e) => {
    selectColor(e.target.value);
};

const selectColor = (color) => {
    backgroundColor.value = color;
    selectedColor.value = color;
};

// 返回
const goBack = () => {
    window.history.back();
};

// 下载图像
async function downloadImage() {
    console.log(selectedColor.value, "selectedColor")
    const response = await baseAPI('save_png_add_bg_dialog', { "base64_data": imageSrc.value, "hex_color": selectedColor.value })
    if (response.code === 200) {
        message.info(t('common.download_success'));
    } else {
        message.error(t('common.download_error'));
    }
}



</script>

<style scoped>
img {
    width: 100%;
    height: 100%;
}

.img-transparent-bg {
    background-size: 20px 20px;
    background-position: 0 0, 10px 10px;
    background-image: linear-gradient(45deg, #eee 25%, transparent 0, transparent 75%, #eee 0, #eee), linear-gradient(45deg, #eee 25%, #fff 0, #fff 75%, #eee 0, #eee);
}

.stacked-linear {
    background: linear-gradient(217deg,
            rgba(255, 0, 0, 0.8),
            rgba(255, 0, 0, 0) 70.71%),
        linear-gradient(127deg, rgba(0, 255, 0, 0.8), rgba(0, 255, 0, 0) 70.71%),
        linear-gradient(336deg, rgba(0, 0, 255, 0.8), rgba(0, 0, 255, 0) 70.71%);
}
</style>
