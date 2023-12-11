import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createMainRouter } from './router';
import Main from './Main.vue';
import './main.scss';

const app = createApp(Main);

app.use(createPinia());
app.use(createMainRouter());

app.mount('#app');