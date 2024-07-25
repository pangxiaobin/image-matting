import { createI18n } from 'vue-i18n';
import en_US from './en-US';
import zh_CN from './zh-CN';

export const languageList = {
    'zh-CN': '中文',
    'en-US': 'English',
}

const i18n = createI18n({
    legacy: false, // 在 Vue 3 中，默认使用 Composition API，设置 legacy 为 false 表示不使用 Vue 2 的语法。
    allowComposition: true, // 允许在 vue-i18n 的组合式 API 中使用 reactive、ref 等响应式系统。
    globalInjection: true, // 全局注入，即所有的组件都可以直接使用 this.$t() 等方法。
    global: true, // 全局配置，即所有组件都共用同一个 i18n 实例。
    locale: localStorage.getItem("language") || 'zh-CN', // 语言标识符，默认 zh-CN。
    fallbackLocale: localStorage.getItem("language") || 'zh-CN', // 回退语言标识符，默认 zh-CN。
    messages: {
        'zh-CN': zh_CN,
        'en-US': en_US,
    }
})

export default i18n;