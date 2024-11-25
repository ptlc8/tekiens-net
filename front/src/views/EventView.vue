<script>
import Api from '../api';
import { getEventStatus } from '../eventStatus';
import { marked } from 'marked';
import { mangle } from 'marked-mangle';
import DOMPurify from 'dompurify';
import { useSessionStore } from '../stores/session';
import { RouterLink } from 'vue-router';
import QRCode from '../components/QRCode.vue'

marked.use(mangle(), { breaks: true });

export default {
    components: {
        RouterLink,
        QRCode
    },
    setup() {
        return {
            sessionStore: useSessionStore()
        }
    },
    data() {
        return {
            event: null,
            asso: {}
        }
    },
    computed: {
        backgroundColor() {
            return this.asso?.color + '44';
        },
        description() {
            if (!this.event.description)
                return '';
            return DOMPurify.sanitize(marked.parse(this.event.description));
        },
        editable() {
            if (!this.sessionStore.session) // not logged in
                return false;
            return this.sessionStore.session.asso_id == this.event.asso_id;
        },
        status() {
            return getEventStatus(this.event);
        },
        duration() {
            if (!this.event.duration)
                return undefined;
            var days = Math.floor(this.event.duration / 60 / 24);
            var hours = Math.floor(this.event.duration / 60) % 24;
            var minutes = this.event.duration % 60;
            return `${days}j ${hours}h ${minutes}min`.replace(/ 0min/, '').replace(/ 0h/, '').replace(/^0j /, '');
        },
        warning() {
            if (this.event.status != 'programmed')
                return "⚠️ Attention ! Cette événement est " + getEventStatus(this.event, true) + ".";
            return undefined;
        }
    },
    methods: {
        formatDate(date) {
            return new Date(date + 'Z').toLocaleString('FR-fr', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
        },
        formatTime(date) {
            return new Date(date + 'Z').toLocaleTimeString('FR-fr', { hour: '2-digit', minute: '2-digit' });
        },
        formatDateTime(date) {
            return new Date(date + 'Z').toLocaleString('FR-fr', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
        },
        canShare() {
            return 'share' in navigator;
        },
        share() {
            navigator.share({
                title: this.event.title,
                text: "Découvre l'événement " + this.event.title,
                url: location.href
            });
        },
        deleteEvent() {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cet événement ?'))
                return;
            Api.events.delete(this.event.id)
                .then(() => this.$router.push('/assos/' + encodeURIComponent(this.event.asso_id)))
                .catch(error => this.$state.error = error);
        }
    },
    watch: {
        event(event) {
            document.title = `${event.title} - Tekiens.net`;
            Api.assos.getOne(event.asso_id)
                .then(asso => this.asso = asso);
        }
    },
    beforeRouteEnter(to, _from, next) {
        Api.events.getOne(to.params.id)
            .then(event => next(view => view.event = event))
            .catch(error => next(view => view.$state.error = error));
    },
    beforeRouteUpdate(to, _from, next) {
        Api.events.getOne(to.params.id)
            .then(event => this.event = event)
            .catch(error => this.$state.error = error)
            .finally(next);
    }
}
</script>

<template>
    <section>
        <article :style="{ '--accent-color': asso?.color, '--bg-color': backgroundColor }">
            <div v-if="warning" class="warning">{{ warning }}</div>
            <div v-if="event" class="event">
                <div class="main">
                    <h2>{{ event.title }}</h2>
                    <div class="description">
                        <img v-if="event.poster" :src="event.poster" class="poster" alt="Affiche de l'événement" width="400" height="400" />
                        <div v-html="description" class="markdown"></div>
                        <div class="clear"></div>
                    </div>
                </div>
                <div class="infos">
                    <RouterLink :to="'/assos/' + encodeURIComponent(event.asso_id)">
                        <img :src="asso.logos?.[0]" class="logo" alt="Logo de l'association" width="200" height="200" />
                        <span class="asso">{{ asso.names?.[0] }}</span>
                    </RouterLink>
                    <hr />
                    <button v-if="canShare()" @click="share">Partager l'événement</button>
                    <template v-if="editable">
                        <RouterLink :to="'/events/' + event.id + '/edit'">
                            <button>Éditer l'événement</button>
                        </RouterLink>
                        <RouterLink :to="'/templates?event=' + event.id">
                            <button>Générer un mail</button>
                        </RouterLink>
                        <button @click="deleteEvent">Supprimer l'événement</button>
                        <hr />
                    </template>
                    <span>📅 Le {{ formatDate(event.date) }}</span>
                    <span>⌚ À {{ formatTime(event.date) }}</span>
                    <span>📍 {{ event.place }}</span>
                    <span v-if="duration">🕓 {{ duration }}</span>
                    <span v-if="event.price">💲 {{ event.price }}</span>
                    <span v-if="event.access">🔒 {{ event.access }}</span>
                    <span v-if="event.status">{{ status }}</span>
                    <span v-if="event.capacity">👥 {{ event.capacity }} places</span>
                    <span>📝 Crée le {{ formatDateTime(event.createDate) }}</span>
                    <span>🔄 Dernière mise à jour le {{ formatDateTime(event.lastUpdateDate) }}</span>
                    <a :href="event.link" target="_blank">
                        <QRCode class="qr-code" :value="event.link" />
                        <button v-if="event.link">🖇 Lien de l'événement</button>
                    </a>
                </div>
            </div>
        </article>
    </section>
</template>

<style lang="scss" scoped>
.warning {
    margin-bottom: 1em;
    padding: 1em 2em;
    border-radius: 8px;
    background-color: var(--warning-color);
    text-align: center;
    font-weight: bold;
}

.event {
    display: flex;
    gap: 1em;

    .main {
        flex: 4;
        display: flex;
        flex-direction: column;

        h2 {
            border-radius: 8px;
            background-color: var(--bg-color);
            padding: 0.5em;
            margin-top: 0;
            text-align: center;
        }

        .description {
            flex: 1;
            padding: 1em;
            border-radius: 8px;
            background-color: var(--bg-color);

            .poster {
                float: right;
                width: 40%;
                height: auto;
                margin: 0 0 1em 1em;
                border-radius: 8px;
                box-shadow: 0 0 10px 2px rgba(0, 0, 0, .1);
            }

            .clear {
                clear: both;
            }
        }
    }

    .infos {
        display: flex;
        flex-direction: column;
        flex: 1;
        padding: 1em;
        border-radius: 8px;
        background-color: var(--bg-color);

        .logo {
            display: block;
            margin: .5em auto;
            width: 8em;
            height: auto;
        }

        .asso {
            display: block;
            text-align: center;
            font-weight: bold;
        }

        button {
            width: 100%;
        }

        .qr-code {
            width: 10em;
            margin: 1em auto;
        }
    }

    @media (max-width: 600px) {
        flex-direction: column;

        .main .description .poster {
            float: none;
            width: 100%;
            margin: 0;
        }
    }
}
</style>