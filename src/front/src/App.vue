<script>
import { RouterLink, RouterView } from 'vue-router';
import { useSessionStore } from './stores/session';

export default {
    setup() {
        var sessionStore = useSessionStore();
        return { sessionStore };
    },
    computed: {
        session() {
            return this.sessionStore.session;
        }
    },
    methods: {
        logout() {
            this.sessionStore.setSessionId(null);
        },
        async login() {
            let session = await this.sessions.create(assoId, password);
            this.sessionStore.setSessionId(session.id);
        }
    }
};
</script>

<template>
    <header>
        <h1>
            Tekiens<span class="extension">.net</span>
        </h1>
        <div class="account" tabindex="0">
            <template v-if="session != null">
                <div class="header">
                    <template v-if="session.asso">
                        <span>{{ session.asso.names.slice(-1)[0] }}</span>
                        <img :src="session.asso.logos.slice(-1)[0]" />
                    </template>
                </div>
                <RouterLink :to="'/assos/' + session.asso_id" tag="button" custom v-slot="{ navigate }">
                    <button @click="navigate">Ma page</button>
                </RouterLink>
                <RouterLink to="/dashboard" tag="button" custom v-slot="{ navigate }">
                    <button @click="navigate">Dashboard</button>
                </RouterLink>
                <button @click="logout">Se déconnecter</button>
            </template>
            <template v-else>
                <div class="header">
                    <RouterLink to="login" custom v-slot="{ navigate }">
                        <button @click="navigate">Se connecter</button>
                    </RouterLink>
                </div>
            </template>
        </div>
        <nav>
            <RouterLink to="/">Accueil</RouterLink>
            <RouterLink to="/assos">Associations</RouterLink>
            <RouterLink to="/events">Événements</RouterLink>
            <RouterLink to="/#links">Liens de l'école</RouterLink>
            <a href="https://archive.tekiens.net" target="_blank">Archives</a>
            <RouterLink to="/about">À propos</RouterLink>
            <span class="open-button" onclick="this.parentElement.classList.toggle('open')"></span>
        </nav>
    </header>
    <main>
        <RouterView />
    </main>
</template>

<style lang="scss">
header {
    position: relative;

    h1 {
        margin: .5em 1em;
        display: inline-block;

        .extension {
            color: var(--accent-color);
            text-transform: uppercase;
            font-size: .8em;
        }
    }

    .account {
        position: absolute;
        right: 0;
        top: 0;
        max-height: 3em;
        margin: .5em 1em;
        padding: .5em 1em;
        background-color: #eee;
        border-radius: 8px;
        z-index: 10;
        overflow: hidden;
        transition: max-height .2s;
        display: flex;
        flex-direction: column;

        &:hover, &:focus-within {
            max-height: 12em;
        }

        .header {
            height: 3em;
            flex: 0 0 3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1em;

            img {
                height: 100%;
                border-radius: 8px;
            }

            button {
                margin: 0;
            }

            + * {
                margin-top: .5em;
            }
        }
    }

    nav {
        background: #333;
        color: white;
        position: relative;
        overflow: hidden;
        display: flex;
        padding: 0 1em;

        a {
            display: block;
            flex: 1;
            color: inherit;
            padding: 1em;
            text-decoration: none;
            text-align: center;
            cursor: pointer;
            transition: background-color .2s;

            &:hover {
                background-color: #444;
            }

            &.router-link-active {
                background-color: #555;
            }
        }

        .open-button {
            display: none;
            position: absolute;
            top: 0;
            left: 0;
            width: 80%;
            padding: 1em 10%;
            line-height: 1;
            cursor: pointer;
            color: inherit;

            &:before {
                content: "☰";
            }
        }

        &.open .open-button:before {
            content: "✕";
        }
    }

    @media (max-width: 600px) {
        nav {
            height: 0;
            padding: 3em 0 0 0;
            margin: 0;
            flex-direction: column;
        }
        nav.open {
            height: auto;
        }
        nav a {
            display: block;
        }
        nav .open-button {
            display: block;
        }
    }
}
</style>