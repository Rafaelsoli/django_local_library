import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// CSS do Tabler
import '@tabler/core/dist/css/tabler.min.css'
import '@tabler/core/dist/js/tabler.min.js'

axios.defaults.baseURL = 'http://localhost:8000/api/' 

// axios.defaults.withCredentials = true 

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const app = createApp(App)

app.config.globalProperties.$http = axios

app.use(createPinia())
app.use(router)
app.mount('#app')