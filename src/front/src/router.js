import { createRouter, createWebHistory } from 'vue-router';

var router = createRouter({
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
            path: '/assos/:id/events',
            name: 'asso-events',
            component: () => import('./views/AssoEventsView.vue'),
            meta: {
                title: 'Événements - Tekiens.net'
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
            path: '/events/:id',
            name: 'event',
            component: () => import('./views/EventView.vue'),
            meta: {
                title: 'Événement - Tekiens.net'
            }
        },
        {
            path: '/links',
            name: 'links',
            component: () => import('./views/LinksView.vue'),
            meta: {
                title: 'Liens de l\'école - Tekiens.net'
            }
        },
        {
            path: '/about',
            name: 'about',
            component: () => import('./views/AboutView.vue'),
            meta: {
                title: 'À propos - Tekiens.net'
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
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('./views/DashboardView.vue'),
            meta: {
                title: 'Dashboard - Tekiens.net'
            }
        }
    ]
});

router.beforeEach((to, from, next) => {
    document.title = to.meta.title;
    next();
});

export default router;