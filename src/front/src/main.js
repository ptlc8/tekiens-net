import { createApp } from 'vue';
import router from './router';
import { createPinia } from 'pinia';
import Main from './Main.vue';
import './main.scss';

const app = createApp(Main)

app.use(router)
app.use(createPinia())

app.mount('#app')