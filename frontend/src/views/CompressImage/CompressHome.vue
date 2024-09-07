<template>
    <div class="h-full flex flex-col items-center justify-center p-4">
        <div class="text-center">
            <h1 class="text-3xl font-bold mb-4">{{ t('compress.compress_home.title') }}</h1>
            <p class="mb-8">{{ t('compress.compress_home.desc') }}</p>
            <button class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md" @click="goToConvertPage">
                <i class="fa-solid fa-image mr-2"></i>
                {{ t('compress.compress_home.simple_compress_btn') }}
            </button>

            <button class="bg-green-500 btn text-white px-4 py-2 rounded-full btn-md ml-4" @click="goMultConvertPage">
                <i class="fa-regular fa-folder-open mr-2"></i>
                {{ t('compress.compress_home.mult_compress_btn') }}
            </button>


            <p class="text-gray-500 mb-4 mt-8">
                {{ t('compress.compress_home.tips') }}
            </p>
        </div>
        <div class="mt-8">
            <img src="/compress.png" alt="compress" class="rounded shadow-lg h-80 object-cover mx-2">
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
    router.push('/comporess-single')
}

function goMultConvertPage() {
    router.push('/compress-multi')
}


</script>

<style scoped></style>