<template>
    <div class="container mx-auto">
        <ImageEditor :imageUrl="imageUrl" :toolbarOptions="coppedToolbarOptions" />
        <div class="flex justify-center space-x-10 mt-4">
            <!--tailwindcss  选择文件按钮  转换类型下拉框  转换按钮 -->
            <button class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md" @click="handleSelectFile">
                {{ t("convert.convert_image.select_btn") }}
            </button>

            <select v-model="selectFileType" class="select select-bordered w-32  px-4 ">
                <option v-for="item in imageTypes" :value="item">{{ item }}</option>
            </select>

            <button :disabled="!selectFile" @click="handleConvertImage"
                class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md">
                {{ t("convert.convert_image.convert_btn") }}
            </button>

        </div>
    </div>
</template>

<script setup>
import { ref, watch } from "vue"
import ImageEditor from "@/views/components/ImageCroperView.vue";
// 路由to 转换页面
import { useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import { convertImageAPI } from "@/api/convert_image"
import baseAPI from "@/api/base";
import message from "@/utils/message";

const { t } = useI18n()

const router = useRouter()

const imageUrl = ref("")
const selectFile = ref("")
const selectFileType = ref("PNG")

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
    delete: false,
    play: false,
});


const imageTypes = ["PNG", "JPEG", "GIF", "BMP", "WEBP", "ICO", "ICNS", "TIFF", "PDF"]

// 根据图片路径获取base64数据
const getFileLocalBase64 = async (filePath) => {
    const result = await baseAPI("get_local_file_base64", filePath);
    if (result.code === 200) {
        return result.data.base64_image;
    } else {
        message.error(result.error_msg);
        return "";
    }
};


const handleSelectFile = async () => {
    const res = await baseAPI("open_file_dialog", false)
    if (res.code === 200) {
        selectFile.value = res["data"]["file_path"]
    }
}

// 监听文件路径变化
watch(selectFile, async (newVal) => {
    if (newVal) {
        imageUrl.value = await getFileLocalBase64(newVal)
    }
})

//   转换图片
const handleConvertImage = async () => {
    const res = await convertImageAPI("get_convert_image", { "input_path": selectFile.value, "output_format": selectFileType.value })
    if (res.code === 200) {
        message.info("success")
    } else {
        loading.value = false
        message.error(res.error_msg)
    }
}


</script>
<style scoped>
.btn.btn-disabled, .btn[disabled], .btn:disabled{
    background-color: #c6c6c6
}
</style>