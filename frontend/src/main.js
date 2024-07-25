import { createApp } from 'vue'
import App from './App.vue'
import i18n from './locales/index.js'; // i18n
import router from './router/index.js'; // router
import '@fortawesome/fontawesome-free/css/all.css';
import './style.css'
import './dark.css'


const app = createApp(App);

app.use(router);
app.use(i18n)
app.mount('#app');