<template>
    <div class="mx-auto">
        <div class="flex justify-center space-x-10 mt-4">

            <button class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md" @click="handleGetFolder">
                {{ t('convert.mult_convert_image.select_folder_btn') }}
            </button>

            <select v-model="selectFileType" class="select select-bordered w-32  px-4 ">
                <option v-for="item in imageTypes" :value="item">{{ item }}</option>
            </select>

            <button :disabled="!selectFileType || !selectFolder" @click="handleConvertImage"
                class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md">
                {{ t('convert.mult_convert_image.start_convert_btn') }}
            </button>
        </div>

        <div class="mt-4 flex justify-center items-center">
            <ul class="space-y-2 max-h-96 max-w-3xl overflow-y-auto ">
                <li v-for="(image, index) in convertImageList" :key="index" class="flex  p-2 rounded-lg">
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
                        <svg @click="openFile(image.convert_result)" v-else-if="image.status === 'processed'"
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
        </div>

        <div v-if="working" class="mt-6 text-center">
            <button @click="stopConvertImage()" class="bg-green-500 text-white px-4 py-2 rounded-full">{{
                t('convert.mult_convert_image.finish') }}</button>
        </div>
        
        <div v-if="loading" class="flex justify-center items-center">
            <div class="loader"></div>
        </div>


    </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from "vue"
import baseAPI from "@/api/base";
import message from "@/utils/message";
import { convertImageAPI } from "@/api/convert_image"
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const loading = ref(false)

const imageTypes = ["PNG", "JPEG", "GIF", "BMP", "WEBP", "ICO", "ICNS", "TIFF", "PDF"]
const selectFileType = ref("PNG")
const selectFolder = ref(null)
const working = ref(false)

const convertImageList = ref([])

const handleGetFolder = async () => {
    const res = await baseAPI('open_folder_dialog', '')
    if (res.code === 200) {
        selectFolder.value = res.data.folder_path
    } else {
        message.error(res.error_msg)
    }
}

const stopConvertImage = () => {
    working.value = false
    //  把convertImageList中的数据所有waitting状态设置为空
    for (let i = 0; i < convertImageList.value.length; i++) {
        const image = convertImageList.value[i]
        if (image.status === 'waiting') {
            image.status = ''
        }
    }
}

// 获取转换的文件列表
const getConvertFileList = async () => {
    loading.value = true

    const res = await convertImageAPI('get_folder_convert_images', selectFolder.value)
    console.log('getConvertFileList', res)
    if (res.code === 200) {
        convertImageList.value = res.data.convert_images
    } else {
        message.error(res.error_msg)
    }
    loading.value = false
}

//  监听文件夹选择
watch(selectFolder, async () => {
    if (selectFolder.value) {
        await getConvertFileList()
    }
})

// 打开文件
const openFile = async (path) => {
    await baseAPI('open_and_select_file', path)
}

// 开始转换
const handleConvertImage = async () => {
    if (working.value) {
        return
    }
    working.value = true
    console.log('start deal image',)
    //  把convertImageList中的数据所有状态为空的，设置为watting状态
    for (let i = 0; i < convertImageList.value.length; i++) {
        const image = convertImageList.value[i]
        if (image.status === '') {
            image.status = 'waiting'
        }
    }

    //  开始处理
    for (let i = 0; i < convertImageList.value.length; i++) {
        const image = convertImageList.value[i]
        if (working.value === true) {
            if (image.status === 'waiting') {
                console.log('deal image', image.image_path, selectFolder.value)
                const result = await convertImageAPI('convert_image_from_folder', { image_path: image.image_path, folder_path: selectFolder.value, output_format: selectFileType.value })
                if (result.code === 200) {
                    image.status = 'processed'
                    image.convert_result = result.data.convert_result
                } else {
                    image.status = 'error'
                    message.error(result.error_msg)
                }
            }
        } else {
            break
        }
    }
    working.value = false
}


onUnmounted(() => {
    working.value = false
    convertImageList.value = []
    selectFolder.value = null
})

</script>

<style scoped>
.btn.btn-disabled,
.btn[disabled],
.btn:disabled {
    background-color: #c6c6c6
}
</style>