<template>
    <header class="p-4 flex justify-end items-center">
        <label class="flex cursor-pointer gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5" />
                <path
                    d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
            </svg>
            <input type="checkbox" :checked="isDarkTheme" @change="toggleTheme" class="toggle theme-controller" />
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
        </label>

        <div class="tooltip tooltip-bottom ml-4 text-xl	" :data-tip="!windowPinned ? t('basicHeader.pin_window') : t('basicHeader.unpin_window')">
            <i v-if="!windowPinned" class="fa-solid fa-arrow-up" @click="toggleWindowPin"></i>

            <i v-else class="fa-solid fa-arrow-down" @click="toggleWindowPin"></i>
        </div>

    </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { settingAPI } from '@/api/user';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const isDarkTheme = ref(false)

const theme = ref('light')

const windowPinned = ref(false)
const toggleWindowPin = async () => {
  windowPinned.value = !windowPinned.value
  const resp = await settingAPI('update_window_setting', { pin_window: windowPinned.value })
  if (resp.code !== 200) {
    windowPinned.value = !windowPinned.value
  }
}

// 获取设置信息
const getSettingInfo = async () => {
    const res = await settingAPI('get', '')
    theme.value = res.data.theme
    if (res.data.theme === 'dark') {
        isDarkTheme.value = true
    } else {
        isDarkTheme.value = false
    }
    windowPinned.value = res.data.window.on_top
}

// 保存设置
const saveTheme = async () => {
    const res = await settingAPI('put', { theme: theme.value })
}

const toggleTheme = async () => {
    if (theme.value === 'dark') {
        theme.value = 'light'
        isDarkTheme.value = false
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark')
        }
    } else {
        theme.value = 'dark'
        isDarkTheme.value = true
        document.documentElement.classList.add('dark')
    }
    await saveTheme()
}

onMounted(async () => {
    await getSettingInfo()
    if (theme.value === 'dark') {
        isDarkTheme.value = true
        document.documentElement.classList.add('dark')
    } else {
        isDarkTheme.value = false
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark')
        }
    }

})
</script>

<style scoped>
/* 在此处添加任何自定义样式 */
</style>