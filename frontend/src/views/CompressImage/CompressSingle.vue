<template>
    <div class="container mx-auto p-8">
        <div class="grid grid-cols-3 gap-4">
            <!-- 左侧原始图片信息 -->
            <div class="border p-4 rounded shadow-md  min-h-96">
                <h2 class="text-xl font-bold mb-4">{{ t('compress.compress_single.original_title') }}</h2>
                <div v-if="originalImage">
                    <img :src="originalInfo.img" alt="" class="w-32 h-32 object-cover mb-4 rounded">
                    <ul class="break-words">
                        <li><strong>{{ t('compress.compress_single.size') }}:</strong> {{ originalInfo.size }}</li>
                        <li><strong>{{ t('compress.compress_single.format') }}:</strong> {{ originalInfo.format }}</li>
                        <li><strong>{{ t('compress.compress_single.color_mode') }}:</strong> {{ originalInfo.colorMode }}</li>
                        <li><strong>{{  t('compress.compress_single.file_size') }}:</strong> {{ originalInfo.formatSize }}</li>
                        <li class="cursor-pointer" @click="openFile(originalInfo.path)"><strong>{{ t('compress.compress_single.path') }}:</strong> {{ originalInfo.path }}</li>
                    </ul>
                </div>
            </div>

            <!-- 中间的按钮区域 -->
            <div class="flex flex-col justify-center items-center space-y-4">
                <button @click="handleSelectFile"
                    class="bg-blue-500 btn text-white px-4 py-2 rounded-full btn-md hover:bg-blue-700">
                    {{ t('compress.compress_single.select_btn') }}
                </button>
                <button @click="handleCompressImage" :disabled="!originalImage"
                    class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md">
                    {{ t('compress.compress_single.compress_btn') }}
                </button>
            </div>

            <!-- 右侧压缩后的图片信息 -->
            <div class="border p-4 rounded shadow-md min-h-96">
                <h2 class="text-xl font-bold mb-4">{{ t('compress.compress_single.compressed_title') }}</h2>
                <div v-if="compressedImage">
                    <img :src="compressedInfo.img" alt="" class="w-32 h-32 object-cover mb-4 rounded">
                    <ul>
                        <li><strong>{{ t('compress.compress_single.size') }}:</strong> {{ compressedInfo.size }}</li>
                        <li><strong>{{ t('compress.compress_single.format') }}:</strong> {{ compressedInfo.format }}</li>
                        <li><strong>{{ t('compress.compress_single.color_mode') }}:</strong> {{ compressedInfo.colorMode }}</li>
                        <li><strong>{{  t('compress.compress_single.file_size') }}:</strong> {{ compressedInfo.formatSize }}</li>
                        <li><strong>{{ t('compress.compress_single.compress_rate') }}:</strong> {{ compressRate }}</li>
                        <li class="cursor-pointer" @click="openFile(compressedInfo.path)"><strong>{{ t('compress.compress_single.path') }}:</strong> {{ compressedInfo.path }}</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div v-if="loading" class="flex justify-center items-center">
      <div class="loader"></div>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import baseAPI from '@/api/base'
import { compressImageAPI } from '@/api/compress_image'
import message from "@/utils/message";
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const loading = ref(false)

const originalImage = ref(null);
const compressedImage = ref(null);

const originalInfo = ref({
    size: '',
    format: '',
    colorMode: '',
    fileSize: '',
    formatSize: '',
    path: '',
    img: '',
});

const compressedInfo = ref({
    size: '',
    format: '',
    colorMode: '',
    fileSize: '',
    formatSize: '',
    path: '',
    img: '',
});

const compressRate = computed(() => {
    if (originalInfo.value.fileSize && compressedInfo.value.fileSize) {
        return (
            (1 - (compressedInfo.value.fileSize / originalInfo.value.fileSize)) * 100
        ).toFixed(2) + "%"
    } else {
        return ""
    }
})


watch(originalImage, async (newVal) => {
    if (newVal) {
        loading.value = true
        const info = await getImageInfo(newVal)
        if (info) {
            originalInfo.value = info
        }
        loading.value = false
    }
})

watch(compressedImage, async (newVal) => {
    if (newVal) {
        loading.value = true
        const info = await getImageInfo(newVal)
        if (info) {
            compressedInfo.value = info
        }
        loading.value = false
    }
})


// 选择文件
const handleSelectFile = async () => {
    const res = await baseAPI("open_file_dialog", false)
    if (res.code === 200) {
        originalImage.value = res["data"]["file_path"]
    }
}

// 压缩图片
const handleCompressImage = async () => {
    console.log(originalImage.value)
    loading.value = true
    const res = await compressImageAPI("single_compress_image", originalImage.value)
    if (res.code === 200) {
        compressedImage.value = res["data"]["save_path"]
        message.success("success")
    }else{
       alert(res.error_msg)
    }
    loading.value = false
}


const getImageInfo = async (img_path) => {
    const res = await compressImageAPI("get_image_info", img_path)
    if (res.code === 200) {
        return res["data"]
    }else{
        alert(res.error_msg)
        return null
    }
}

// 打开文件
const openFile = async (path) => {
    await baseAPI('open_and_select_file', path)
}


</script>

<style scoped>
/* 自定义样式 */
ul {
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}

.btn.btn-disabled, .btn[disabled], .btn:disabled{
    background-color: #c6c6c6
}
</style>