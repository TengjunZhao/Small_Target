import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// 引入全局样式
import './assets/main.css'
// 引入WindiCSS样式
import 'virtual:windi.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
