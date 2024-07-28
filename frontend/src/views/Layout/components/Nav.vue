<template>
    <div :class="{
        'w-44': isSidebarOpen,
        'w-16': !isSidebarOpen,
    }" class="sidebar transition-all duration-300 relative">
        <div v-if="isSidebarOpen" class="p-4">
            <!-- logo -->
            <div class="avatar">
                <div class="w-20 rounded-full">
                    <img src="/logo.png" />
                </div>
            </div>
            <!-- 导航内容 -->
            <ul class="mt-4">
                <li class="py-2">
                    <router-link to="/aimatting" class="hover:underline flex items-center">
                        <i class="fa-brands fa-airbnb text-2xl mr-2"></i> {{ t('menu.ai_matting_name') }}
                    </router-link>
                </li>
                <li class="py-2">
                    <router-link to="/ai-photo" class="hover:underline flex items-center">
                        <i class="fa-solid fa-id-card text-2xl mr-2"></i>{{ t('menu.ai_photo_name') }}
                    </router-link>
                </li>
                <li class="py-2">
                    <router-link to="/setting" class="hover:underline flex items-center">
                        <i class="fa-solid fa-gear text-2xl mr-2"></i> {{ t('menu.setting') }}
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
                    <i class="fa-brands fa-airbnb text-2xl "></i>
                </router-link>
                <router-link to="/ai-photo" :data-tip="t('menu.ai_photo_name')"
                    class="tooltip tooltip-right hover:underline flex items-center mb-4">
                    <i class="fa-solid fa-id-card text-2xl"></i>
                </router-link>
                <router-link to="/setting" :data-tip="t('menu.setting')"
                    class="tooltip tooltip-right hover:underline flex items-center">
                    <i class="fa-solid fa-gear text-2xl"></i>
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