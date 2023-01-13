import { createApp } from 'vue'
import App from './App.vue'
import antd from 'ant-design-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'ant-design-vue/dist/antd.css';
import './style.css';

createApp(App)
    .use(antd)
    .mount('#app')
