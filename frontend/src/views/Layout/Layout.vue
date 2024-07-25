<template>
    <div class="flex flex-col min-h-screen">

        <!-- Main Content -->
        <div class="flex flex-1">
            <Nav />

            <!-- Main Content -->
            <div class="flex-1 flex flex-col p-4">
                <!-- 主题切换按钮 -->
                <Header />
                <!-- 页面内容 -->
                <main class="flex-1 p-4">
                    <router-view></router-view>
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import Header from '@/views/Layout/components/Header.vue'
import Nav from '@/views/Layout/components/Nav.vue'

</script>

<style scoped>
/* 在此处添加任何自定义样式 */
</style>