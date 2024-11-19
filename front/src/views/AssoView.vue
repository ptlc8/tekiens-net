<script>
import Api from '../api';
import { marked } from 'marked';
import { mangle } from 'marked-mangle';
import DOMPurify from 'dompurify';
import EventPreview from '../components/EventPreview.vue';
import SwitchButton from '../components/SwitchButton.vue';
import WebCalLink from '../components/WebCalLink.vue';
import { useSessionStore } from "../stores/session";
import { RouterLink } from 'vue-router';

marked.use(mangle(), { breaks: true });

export default {
    components: {
        EventPreview,
        SwitchButton,
        WebCalLink
    },
    setup() {
        return {
            sessionStore: useSessionStore()
        }
    },
    data() {
        return {
            asso: null,
            events: []
        }
    },
    computed: {
        socials() {
            return this.asso.socials?.map(social => 
                ({ type: social.split(':', 1)[0], value: social.substring(social.indexOf(':') + 1) })
            ) ?? [];
        },
        backgroundColor() {
            return this.asso?.color + '44';
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
        icsPath() {
            return '/assos/' + encodeURIComponent(this.asso.id) + '/events.ics';
        },
        showPastEvents: {
            get() {
                return 'past' in this.$route.query;
            },
            set(value) {
                value = value ? null : undefined;
                this.$router.replace({ query: { ...this.$route.query, past: value } });
            }
        },
        filteredEvents() {
            let events = this.events.filter(event => {
                if (this.showPastEvents)
                    return new Date(event.date + 'Z') <= new Date();
                return new Date(Date.parse(event.date + 'Z') + (event.duration ?? 0) * 60 * 1000) > new Date();
            });
            if (this.showPastEvents)
                events.reverse();
            return events;
        }
    },
    methods: {
        canShare() {
            return 'share' in navigator;
        },
        share() {
            navigator.share({
                title: this.asso.names?.[0],
                text: "Découvre l'association " + this.asso.names?.[0],
                url: location.href
            });
        }
    },
    watch: {
        asso(asso) {
            document.title = `${asso.names?.[0]} - Tekiens.net`;
        }
    },
    beforeRouteEnter(to, _from, next) {
        Promise.all([Api.assos.getOne(to.params.id), Api.assos.getEvents(to.params.id)])
            .then(([asso, events]) => next(view => {
                view.asso = asso;
                view.events = events;
            }))
            .catch(error => next(view => view.$state.error = error));
    },
    beforeRouteUpdate(to, _from, next) {
        Promise.all([Api.assos.getOne(to.params.id), Api.assos.getEvents(to.params.id)])
            .then(([asso, events]) => {
                this.asso = asso;
                this.events = events;
            })
            .catch(error => this.$state.error = error)
            .finally(next);
    }
}
</script>

<template>
    <section>
        <article :style="{ '--accent-color': asso?.color, '--bg-color': backgroundColor }">
            <h2 v-if="asso">
                <img :src="asso.logos?.[0]" width="200" height="200" />
                {{ asso.names?.[0] }}
            </h2>
            <div v-if="asso" class="asso">
                <div class="main">
                    <div class="description markdown" v-html="description"></div>
                    <div class="events">
                        <h3>Événements</h3>
                        <div class="parameters">
                            <label>
                                Afficher les événements passés
                                <SwitchButton v-model="showPastEvents" class="switch" />
                            </label>
                        </div>
                        <div class="events-container">
                            <EventPreview v-for="event in filteredEvents" :key="event.id" :event="event" :asso="asso" />
                        </div>
                        <span v-if="events.length == 0">
                            Aucun événement {{ showPastEvents ? 'passé' : 'à venir' }}
                        </span>
                    </div>
                </div>
                <div class="infos">
                    <template v-if="editable">
                        <RouterLink :to="'/assos/' + encodeURIComponent(asso.id) + '/edit'">
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
                    <a v-for="social in asso.socials" :key="social.id" target="_blank" :href="social.link">
                        <img :src="'../assets/socials/' + social.id + '.svg'" width="16" height="16" />
                        {{ social.display }}
                    </a>
                    <hr />
                    <button v-if="canShare()" @click="share">Partager l'association</button>
                    <WebCalLink :path="icsPath" />
                    <hr />
                    <span v-if="asso.names?.length > 1">{{ asso.names.length > 2 ? 'Anciens noms' : 'Ancien nom' }} :</span>
                    <ul v-if="asso.names?.length > 1">
                        <li v-for="name in asso.names.slice(1)" :key="name">
                            {{ name }}
                        </li>
                    </ul>
                    <span v-if="asso.logos?.length > 1">{{ asso.logos.length > 2 ? 'Anciens logos' : 'Ancien logo' }} :</span>
                    <div v-if="asso.logos?.length > 1" class="logos">
                        <img v-for="logo in asso.logos.slice(1)" :key="logo" :src="logo" width="64" height="64" />
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
