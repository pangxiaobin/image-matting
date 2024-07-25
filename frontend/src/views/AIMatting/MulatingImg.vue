<template>
    <div class="flex justify-center w-full h-full items-center ">
        <div class="w-3/4 max-w-2xl	 rounded-lg p-6">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-lg font-bold">{{ t('ai_matting.mult_matting.title') }}</h2>
                <span class="badge badge-info">{{ t('ai_matting.mult_matting.processing') }} {{ processed_count }} / {{
                    image_list.length }}</span>
            </div>
            <!-- 图片列表,最高显示5个，超出显示滚动条 -->
            <ul class="space-y-2 max-h-96 w-full overflow-y-auto ">
                <li v-for="(image, index) in image_list" :key="index" class="flex  p-2 rounded-lg">
                    <img :src="image.base64_image" alt="image" class="w-16 h-16 rounded flex-none" />
                    <div class="grow ml-4 flex flex-col truncate">
                        <p class="truncate" :title="image.image_name">{{ image.image_name }}</p>
                        <p class="text-xs text-gray-400 truncate" :title="image.image_path">{{
                            image.image_path }}</p>
                    </div>
                    <span class="flex-none  btn btn-circle btn-ghost ml-4">
                        <svg @click="openFile(image.image_path)" v-if="image.status === 'waiting'"
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            class="w-6 h-6 animate-spin">
                            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25">
                            </circle>
                            <path fill="currentColor" d="M4 12a8 8 0 017.5-7.98A4 4 0 104 12h4z" class="opacity-75">
                            </path>
                        </svg>
                        <svg @click="openFile(image.no_bg_image)" v-else-if="image.status === 'processed'"
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            class="w-6 h-6 text-green-500">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M5 13l4 4L19 7" />
                        </svg>
                        <svg @click="openFile(image.image_path)" v-else-if="image.status === 'error'"
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            class="w-6 h-6 text-red-500">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                    </span>
                </li>
            </ul>
            <div v-if="working" class="mt-6 text-center">
                <button @click="stopDealImage()"
                    class="bg-green-500 text-white px-4 py-2 rounded-full">{{ t('ai_matting.mult_matting.finish') }}</button>
            </div>
            <div v-else class="mt-6 text-center">
                <button @click="goBack()" class="bg-green-500 text-white px-4 py-2 rounded-full">{{
                    t('ai_matting.btn_back') }}</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { aiMattingAPI } from '@/api/ai_matting'
import { useI18n } from 'vue-i18n'
import message from '@/utils/message.js'
import baseAPI from '@/api/base'
const { t } = useI18n()
const route = useRoute();

const foldersPath = ref('')

const image_list = ref([])

const loading = ref(true)

const working = ref(true)

//  已处理图片数量
const processed_count = computed(() => {
    return image_list.value.filter(item => item.status === 'processed').length
})

// 处理图片
const dealImage = async () => {
    console.log('start deal image',)
    for (let i = 0; i < image_list.value.length; i++) {
        const image = image_list.value[i]
        if (working.value === true) {
            if (image.status === 'waiting') {
                console.log('deal image', image.image_path, foldersPath.value)
                const result = await aiMattingAPI('predict_from_folder_img', { image_path: image.image_path, folder_path: foldersPath.value })
                if (result.code === 200) {
                    image.status = 'processed'
                    image.no_bg_image = result.data.no_bg_image
                } else {
                    image.status = 'error'
                    message.error(result.error_msg)
                }
            }
        } else {
            return
        }
    }
    working.value = false
}
// 结束处理
const stopDealImage = () => {
    working.value = false
}

// 获取文件夹内图片
const getFolderImages = async () => {
    const result = await aiMattingAPI('get_folder_images', foldersPath.value)
    if (result.code === 200) {
        image_list.value = result.data.image_list
    } else {
        message.error(result.error_msg)
    }
}
// 返回
const goBack = () => {
    window.history.back();
};

// 打开文件
const openFile = async (path) => {
    await baseAPI('open_and_select_file', path)
}

onMounted(async () => {
    foldersPath.value = route.params.folderPath
    console.log(foldersPath.value, 'foldersPath')
    await getFolderImages()
    await dealImage()

})

onUnmounted(() => {
    console.log('unmounted')
    stopDealImage()
})
</script>

<style>
/* Add any additional custom styles here */
</style>