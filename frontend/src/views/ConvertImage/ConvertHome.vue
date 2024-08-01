<template>
    <div class="h-full flex flex-col items-center justify-center p-4">
        <div class="text-center">
            <h1 class="text-3xl font-bold mb-4">{{ t('convert.convert_home.title') }}</h1>
            <p class="mb-8">{{ t('convert.convert_home.desc') }}</p>
            <button class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md" @click="goToConvertPage">
                <i class="fa-solid fa-image mr-2"></i>
                {{ t('convert.convert_home.simple_convert_btn') }}
            </button>

            <button class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md ml-4" @click="goMultConvertPage">
                <i class="fa-regular fa-folder-open mr-2"></i>
                {{ t('convert.convert_home.mult_convert_btn') }}
            </button>


            <p class="text-gray-500 mb-4 mt-8">
                {{ t('convert.convert_home.tips') }}
            </p>
        </div>
        <div class="mt-8">
            <img src="/convert.png" alt="convert" class="rounded shadow-lg h-80 object-cover mx-2">
        </div>
    </div>
</template>

<script setup>
// 路由to 转换页面
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const router = useRouter()



function goToConvertPage() {
    router.push('/convert-image-editor')
}

function goMultConvertPage() {
    router.push('/multi-convert-image')
}


</script>
.demo {
margin-top:10px;
margin-bottom:10px;
}

<style scoped></style>