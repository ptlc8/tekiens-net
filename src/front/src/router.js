import { createRouter as create, createWebHistory } from 'vue-router';
import { useStateStore } from './stores/state';
import Nprogress from 'nprogress';
import 'nprogress/nprogress.css';

export function createMainRouter() {
    var router = create({
        base: "./",
        history: createWebHistory(import.meta.env.BASE_URL),
        routes: [
            {
                path: '/',
                name: 'index',
                component: () => import('./views/IndexView.vue'),
                meta: {
                    title: 'Tekiens.net'
                }
            },
            {
                path: '/assos',
                name: 'assos',
                component: () => import('./views/AssosView.vue'),
                meta: {
                    title: 'Associations - Tekiens.net'
                }
            },
            {
                path: '/assos/:id',
                name: 'asso',
                component: () => import('./views/AssoView.vue'),
                meta: {
                    title: 'Association - Tekiens.net'
                }
            },
            {
                path: '/events',
                name: 'events',
                component: () => import('./views/EventsView.vue'),
                meta: {
                    title: 'Événements - Tekiens.net'
                }
            },
            {
                path: '/events/:id(\\d+)',
                name: 'event',
                component: () => import('./views/EventView.vue'),
                meta: {
                    title: 'Événement - Tekiens.net'
                }
            },
            {
                path: '/faq',
                name: 'faq',
                component: () => import('./views/FaqView.vue'),
                meta: {
                    title: 'FAQ - Tekiens.net'
                }
            },
            {
                path: '/login',
                name: 'login',
                component: () => import('./views/LoginView.vue'),
                meta: {
                    title: 'Connexion - Tekiens.net'
                }
            },
            {
                path: '/assos/:id/edit',
                name: 'asso-edit',
                component: () => import('./views/AssoEditView.vue'),
                meta: {
                    title: 'Éditer une association - Tekiens.net'
                }
            },
            {
                path: '/events/create',
                name: 'event-create',
                component: () => import('./views/EventCreateView.vue'),
                meta: {
                    title: 'Créer un événement - Tekiens.net'
                }
            },
            {
                path: '/events/:id(\\d+)/edit',
                name: 'event-edit',
                component: () => import('./views/EventEditView.vue'),
                meta: {
                    title: 'Éditer un événement - Tekiens.net'
                }
            },
            {
                path: '/:pathMatch(.*)*',
                name: '404',
                component: () => import('./views/404View.vue'),
                meta: {
                    title: '404 - Tekiens.net'
                }
            }
        ]
    });

    const state = useStateStore();

    router.beforeEach((to, _from, next) => {
        document.title = to.meta.title;
        app.loading = true;
        Nprogress.start();
        next();
    });

    router.afterEach((_to, _from, _failure) => {
        state.error = null;
        state.loading = false;
        Nprogress.done();
    });

    router.onError(error => {
        state.error = error;
        state.loading = false;
        Nprogress.done();
    });

    return router;
};