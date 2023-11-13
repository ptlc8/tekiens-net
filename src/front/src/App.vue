<script setup>
import { RouterLink, RouterView } from 'vue-router';
import Api from './api.js'

</script>

<template>
    <header>
        <h1>
            Tekiens<span class="extension">.net</span>
        </h1>
        <!--<img src="https://ambi.dev/assets/unset.png" />-->
        <nav>
            <RouterLink to=".">Accueil</RouterLink>
            <RouterLink to="assos">Associations</RouterLink>
            <RouterLink to="events">Événements</RouterLink>
            <RouterLink to=".#links">Liens de l'école</RouterLink>
            <a href="https://archive.tekiens.net" target="_blank">Archives</a>
            <RouterLink to="about">À propos</RouterLink>
            <span class="open-button" onclick="this.parentElement.classList.toggle('open')"></span>
        </nav>
    </header>
    <main>
        <RouterView />
    </main>
</template>

<style lang="scss">
header {
    h1 {
        margin: .5em 1em;
        display: inline-block;

        .extension {
            color: orange;
            text-transform: uppercase;
            font-size: .8em;
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
