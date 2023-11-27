<script>
import { RouterLink, RouterView } from 'vue-router';
import { useSessionStore } from './stores/session';
import { ref } from 'vue';

export default {
    setup() {
        var sessionStore = useSessionStore();
        var nav = ref(null);
        return { sessionStore, nav };
    },
    computed: {
        session() {
            return this.sessionStore.session;
        }
    },
    methods: {
        logout() {
            this.sessionStore.sessionId = null;
        }
    },
    watch: {
        $route() {
            this.nav.classList.remove('open');
        }
    }
};
</script>

<template>
    <header>
        <RouterLink to="/" custom v-slot="{ navigate }">
            <h1 @click="navigate">
                Tekiens<span class="extension">.net</span>
            </h1>
        </RouterLink>
        <div class="account" tabindex="0">
            <template v-if="session != null">
                <div class="header">
                    <template v-if="session.asso">
                        <span>{{ session.asso.names[0] }}</span>
                        <img :src="session.asso.logos[0]" width="48" height="48" alt="Logo de l'association">
                    </template>
                </div>
                <RouterLink :to="'/assos/' + session.asso_id" custom v-slot="{ navigate }">
                    <button @click="navigate">Ma page</button>
                </RouterLink>
                <RouterLink to="/dashboard" custom v-slot="{ navigate }">
                    <button @click="navigate">Dashboard</button>
                </RouterLink>
                <button @click="logout">Se déconnecter</button>
            </template>
            <template v-else>
                <div class="header">
                    <RouterLink :to="'/login?redirect=' + encodeURIComponent($route.fullPath)" custom v-slot="{ navigate }">
                        <button @click="navigate">Se connecter</button>
                    </RouterLink>
                </div>
            </template>
        </div>
        <nav ref="nav">
            <RouterLink to="/">Accueil</RouterLink>
            <RouterLink to="/assos">Associations</RouterLink>
            <RouterLink to="/events">Événements</RouterLink>
            <a target="_blank" href="https://archive.tekiens.net">Archives</a>
            <RouterLink to="/about">À propos</RouterLink>
            <div class="school-links" tabindex="0">
                <a>Liens de l'école</a>
                <div>
                    <a target="_blank" href="https://cytech.cyu.fr/">Site de CY Tech</a>
                    <a target="_blank" href="https://mycy.cyu.fr/">MyCY</a>
                    <a target="_blank" href="https://arel.cy-tech.fr/">AREL : plateforme pédagogique</a>
                    <a target="_blank" href="https://services-web.u-cergy.fr/calendar">Celcat : emploi du temps</a>
                    <a target="_blank" href="https://glpi.cy-tech.fr/">GLPI : support informatique</a>
                    <a target="_blank" href="https://doc.eisti.fr/">Documentation EISTI</a>
                </div>
            </div>
            <span class="open-button" onclick="this.parentElement.classList.toggle('open')"></span>
        </nav>
    </header>
    <main>
        <RouterView />
    </main>
    <footer>
        <span></span>
        <span>
            Fait par <a href="https://atilla.org" target="_blank">ATILLA</a> avec &lt;3
        </span>
    </footer>
</template>

<style lang="scss">
header {
    position: relative;

    h1 {
        margin: .5em 1em;
        display: inline-block;
        cursor: pointer;
        color: inherit;
        font-size: 2em;

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
                width: auto;
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

            &:hover, &:focus-within {
                background-color: #444;
            }

            &.router-link-active {
                background-color: #555;
            }
        }

        .school-links {
            flex: 1;
            position: relative;

            > div {
                position: absolute;
                top: 100%;
                left: 0;
                width: 100%;
                background-color: #333;
                height: 0;
                overflow: hidden;
                z-index: 5;
            }

            &:hover > div, &:focus-within > div {
                height: auto;
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
            overflow: hidden;

            .school-links > div {
                position: static;
            }
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
main {
    flex: 1;
}
footer {
    display: flex;
    background-color: var(--accent-color);
    color: #424242;
    padding: 2em;
    
    > * {
        margin: auto;
    }

    a {
        color: white;
        text-decoration: none;
    }
}
</style>