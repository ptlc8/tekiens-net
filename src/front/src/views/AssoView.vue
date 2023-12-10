<script>
import Api from '../api';
import { marked } from 'marked';
import { mangle } from 'marked-mangle';
import DOMPurify from 'dompurify';
import EventPreview from '../components/EventPreview.vue';
import Switch from '../components/Switch.vue';
import { useSessionStore } from "../stores/session";
import { RouterLink } from 'vue-router';

const baseUrl = import.meta.env.VITE_BASE_URL ?? '';

marked.use(mangle(), { breaks: true });

export default {
    setup() {
        return {
            sessionStore: useSessionStore()
        }
    },
    data() {
        return {
            asso: null,
            error: null,
            events: [],
            showPastEvents: false
        }
    },
    mounted() {
        Api.assos.getOne(this.$route.params.id)
            .then(asso => this.asso = asso)
            .catch(error => this.error = error);
    },
    computed: {
        socials() {
            return this.asso.socials?.map(social => 
                ({ type: social.split(':', 1)[0], value: social.substring(social.indexOf(':') + 1) })
            ) ?? [];
        },
        color() {
            return '#' + this.asso?.color?.toString(16)?.padStart(6, 0);
        },
        backgroundColor() {
            return this.color + '44';
        },
        description() {
            if (!this.asso.description) return '';
            return DOMPurify.sanitize(marked.parse(this.asso.description));
        },
        editable() {
            if (!this.sessionStore.session) // not logged in
                return false;
            return this.sessionStore.session.asso_id == this.asso.id;
        },
        icsUrl() {
            return location.host + baseUrl + '/api/assos/' + this.asso.id + '/events.ics';
        }
    },
    methods: {
        updateEvents(params = { after: new Date() }) {
            Api.assos.getEvents(this.$route.params.id, params)
                .then(events => this.events = events)
                .catch(error => this.error = error);
        }
    },
    watch: {
        asso() {
            this.updateEvents();
            document.title = this.asso.names?.[0] + ' - Tekiens.net';
        },
        '$route.params.id'() {
            Api.assos.getOne(this.$route.params.id)
                .then(asso => this.asso = asso)
                .catch(error => this.error = error);
        },
        showPastEvents() {
            this.updateEvents({ [this.showPastEvents ? 'before' : 'after']: new Date(), desc: this.showPastEvents });
        }
    },
    components: {
        EventPreview,
        Switch
    }
}
</script>

<template>
    <section>
        <article :style="{ '--accent-color': color, '--bg-color': backgroundColor }">
            <h2 v-if="error == 'Not found'">Association "{{ $route.params.id }}" non trouvée.</h2>
            <span v-else-if="error">Erreur: {{ error }}</span>
            <h2 v-if="asso">
                <img :src="asso.logos?.[0]" width="200" height="200">
                {{ asso.names?.[0] }}
            </h2>
            <div v-if="asso" class="asso">
                <div class="main">
                    <div class="description markdown" v-html="description" />
                    <div class="events">
                        <h3>Événements</h3>
                        <div class="parameters">
                            <label>
                                Afficher les événements passés
                                <Switch v-model="showPastEvents" class="switch" />
                            </label>
                        </div>
                        <div class="events-container">
                            <EventPreview v-for="event in events" :key="event.id" :event="event" :asso="asso" />
                        </div>
                        <span v-if="events.length == 0">
                            Aucun événement {{ showPastEvents ? 'passé' : 'à venir' }}
                        </span>
                    </div>
                </div>
                <div class="infos">
                    <template v-if="editable">
                        <RouterLink :to="'/assos/' + asso.id + '/edit'">
                            <button>Éditer l'association</button>
                        </RouterLink>
                        <RouterLink to="/events/create">
                            <button>Créer un événement</button>
                        </RouterLink>
                        <hr />
                    </template>
                    <span v-if="asso.theme">🧩 Thème : {{ asso.theme }}</span>
                    <span v-if="asso.start">🆕 Année de création : {{ asso.start }}</span>
                    <span v-if="asso.end">💥 Année de dissolution : {{ asso.end }}</span>
                    <span v-if="asso.campus">📍 Campus : {{ asso.campus }}</span>
                    <span v-if="asso.room">📦 Salle : {{ asso.room }}</span>
                    <hr />
                    <template v-for="social in socials">
                        <a v-if="social.type == 'web'" target="_blank" :href="'https://' + social.value">
                            <img src="/assets/socials/web.svg" width="16" height="16" />
                            {{ social.value }}
                        </a>
                        <a v-else-if="social.type == 'telegram'" target="_blank" :href="'https://t.me/' + social.value">
                            <img src="/assets/socials/telegram.svg" width="16" height="16" />
                            Telegram
                        </a>
                        <a v-else-if="social.type == 'twitter'" target="_blank" :href="'https://twitter.com/' + social.value">
                            <img src="/assets/socials/twitter.svg" width="16" height="16" />
                            Twitter @{{ social.value }}
                        </a>
                        <a v-else-if="social.type == 'discord'" target="_blank" :href="'https://discord.gg/' + social.value">
                            <img src="/assets/socials/discord.svg" width="16" height="16" /> 
                            Discord
                        </a>
                        <a v-else-if="social.type == 'instagram'" target="_blank" :href="'https://instagram.com/' + social.value">
                            <img src="/assets/socials/instagram.svg" width="16" height="16" />
                            Instagram @{{ social.value }}
                        </a>
                        <a v-else-if="social.type == 'email'" target="_blank" :href="'mailto:' + social.value">
                            <img src="/assets/socials/email.svg" width="16" height="16" />
                            {{ social.value }}
                        </a>
                        <a v-else-if="social.type == 'links'" target="_blank" :href="'https://' + social.value">
                            🖇 Liens
                        </a>
                        <a v-else-if="social.type == 'facebook'" target="_blank" :href="'https://facebook.com/' + social.value">
                            <img src="/assets/socials/facebook.svg" width="16" height="16" />
                            Facebook <template v-if="!social.value.match(/[\?\/\=]/)">({{ social.value }})</template>
                        </a>
                        <a v-else-if="social.type == 'linkedin'" target="_blank" :href="'https://linkedin.com/' + social.value">
                            <img src="/assets/socials/linkedin.svg" width="16" height="16" />
                            LinkedIn
                        </a>
                    </template>
                    <hr />
                    <a target="_blank" :href="'webcal://' + icsUrl">
                        <button>Ajouter à votre agenda</button>
                    </a>
                    URL de l'agenda :
                    <input type="text" :value="icsUrl" readonly />
                    <hr />
                    <span v-if="asso.names?.length > 1">{{ asso.names.length > 2 ? 'Anciens noms' : 'Ancien nom' }} :</span>
                    <ul v-if="asso.names?.length > 1">
                        <li v-for="name in asso.names.slice(1)">{{ name }}</li>
                    </ul>
                    <span v-if="asso.logos?.length > 1">{{ asso.logos.length > 2 ? 'Anciens logos' : 'Ancien logo' }} :</span>
                    <div v-if="asso.logos?.length > 1" class="logos">
                        <img v-for="logo in asso.logos.slice(1)" :src="logo" width="64" height="64" />
                    </div>
                </div>
            </div>
        </article>
    </section>
</template>

<style scoped lang="scss">
h2 {
    img {
        vertical-align: middle;
        object-fit: contain;
        height: 3em;
        width: 4em;
    }
}
.asso {
    display: flex;
    gap: 1em;

    .main {
        flex: 4;
        display: flex;
        flex-direction: column;
        gap: 1em;

        .description, .events {
            padding: 1em;
            border-radius: 8px;
            background-color: var(--bg-color);
            flex: 1;
        }

        .events-container {
            display: flex;
            flex-wrap: wrap;
        }
    }

    .infos {
        display: flex;
        flex-direction: column;
        flex: 1;
        padding: 1em;
        border-radius: 8px;
        background-color: var(--bg-color);

        span img, a img {
            vertical-align: text-bottom;
            height: 1em;
            width: auto;
        }
        
        ul {
            margin: 0;
            list-style: '– ';
            padding-inline-start: 2em;
        }

        .logos {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5em;
            align-self: center;

            img {
                height: 4em;
                width: auto;
            }
        }

        a > * {
            width: 100%;
        }
    }

    @media (max-width: 600px) {
        flex-direction: column;
    }
}
</style>