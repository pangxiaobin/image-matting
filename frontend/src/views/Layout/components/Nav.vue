<template>
    <div :class="{
        'w-50': isSidebarOpen,
        'w-16': !isSidebarOpen,
    }" class="sidebar transition-all duration-300 relative">
        <div v-if="isSidebarOpen" class="p-4">
            <!-- logo -->
            <div class="avatar">
                <div class="w-20">
                    <img src="/logo.png" />
                </div>
            </div>
            <!-- 导航内容 -->
            <ul class="mt-4 space-y-2">
                <li>
                    <router-link to="/aimatting" class="flex items-center p-2 hover:bg-gray-100 rounded transition">
                        <i class="fa-solid fa-photo-film text-2xl mr-3  flex-shrink-0"></i>
                        <span class="text-base">{{ t('menu.ai_matting_name') }}</span>
                    </router-link>
                </li>
                <li>
                    <router-link to="/ai-photo" class="flex items-center p-2 hover:bg-gray-100 rounded transition">
                        <i class="fa-solid fa-id-card text-2xl mr-3  flex-shrink-0"></i>
                        <span class="text-base">{{ t('menu.ai_photo_name') }}</span>
                    </router-link>
                </li>
                <li>
                    <router-link to="/convert-home" class="flex items-center p-2 hover:bg-gray-100 rounded transition">
                        <i class="fa-solid fa-money-bill-transfer text-2xl mr-3  flex-shrink-0"></i>
                        <span class="text-base">{{ t('menu.convert_name') }}</span>
                    </router-link>
                </li>
                <li>
                    <router-link to="/compress-home" class="flex items-center p-2 hover:bg-gray-100 rounded transition">
                        <i class="fa-solid fa-file-zipper text-2xl mr-3  flex-shrink-0"></i>
                        <span class="text-base">{{ t('menu.compress_name') }}</span>
                    </router-link>
                </li>
                <li>
                    <router-link to="/setting" class="flex items-center p-2 hover:bg-gray-100 rounded transition">
                        <i class="fa-solid fa-gear text-2xl mr-3  flex-shrink-0"></i>
                        <span class="text-base">{{ t('menu.setting') }}</span>
                    </router-link>
                </li>
                <li>
                    <router-link to="/about" class="flex items-center p-2 hover:bg-gray-100 rounded transition">
                        <i class="fa-solid fa-info text-2xl mr-3  flex-shrink-0"></i>
                        <span class="text-base">{{ t('menu.about') }}</span>
                    </router-link>
                </li>
            </ul>


        </div>
        <div v-else class="flex flex-col items-center py-4">
            <div class="avatar">
                <div class="w-8 rounded-full">
                    <img src="/logo.png" />
                </div>
            </div>
            <div class="mt-4">
                <router-link to="/" :data-tip="t('menu.ai_matting_name')"
                    class="tooltip tooltip-right hover:underline flex items-center mb-4">
                    <i class="fa-solid fa-photo-film text-2xl "></i>
                </router-link>
                <router-link to="/ai-photo" :data-tip="t('menu.ai_photo_name')"
                    class="tooltip tooltip-right hover:underline flex items-center mb-4">
                    <i class="fa-solid fa-id-card text-2xl"></i>
                </router-link>
                <router-link to="/convert-home" :data-tip="t('menu.convert_name')"
                    class="tooltip tooltip-right hover:underline flex items-center mb-4">
                    <i class="fa-solid fa-money-bill-transfer text-2xl"></i>
                </router-link>
                <router-link to="/compress-home" :data-tip="t('menu.compress_name')"
                    class="tooltip tooltip-right hover:underline flex items-center mb-4">
                    <i class="fa-solid fa-file-zipper text-2xl"></i>
                </router-link>
                <router-link to="/setting" :data-tip="t('menu.setting')"
                    class="tooltip tooltip-right hover:underline flex items-center">
                    <i class="fa-solid fa-gear text-2xl"></i>
                </router-link>
                <router-link to="/about" :data-tip="t('menu.about')"
                    class="tooltip tooltip-right hover:underline flex items-center">
                    <i class="fa-solid fa-info text-2xl"></i>
                </router-link>
            </div>

        </div>

        <!-- 控制按钮 -->
        <label class="btn btn-circle swap swap-rotate absolute bottom-4 left-2">
            <!-- this hidden checkbox controls the state -->
            <input type="checkbox" v-model="isSidebarOpen" />
            <!-- hamburger icon -->
            <i class="fa-solid fa-bars swap-off"></i>
            <!-- close icon -->
            <i class="fa-solid fa-xmark swap-on"></i>
        </label>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const isSidebarOpen = ref(true)


</script>

<style lang="scss" scoped></style>