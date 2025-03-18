import { createRouter, createWebHistory } from 'vue-router';
import ChatbotHomeVue from '../components/ChatbotHomeVue.vue';
import ChatbotHomeVueInteraction from '../components/ChatbotHomeVueInteraction.vue';
import TestVue from '@/components/TestVue.vue';

const routes = [
    {
        path: '/',
        name: 'Chatbot',
        component: ChatbotHomeVue,
    },
    {
        path: '/interaction',
        name: 'interaction',
        component: ChatbotHomeVueInteraction,
    },
    {
        path: '/test',
        name: 'test',
        component: TestVue,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
