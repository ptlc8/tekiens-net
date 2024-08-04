<script>
import Api from '../api';
import { getEventStatus } from '../eventStatus';
import { marked } from 'marked';
import { mangle } from 'marked-mangle';
import DOMPurify from 'dompurify';
import { useSessionStore } from "../stores/session";
import { RouterLink } from 'vue-router';

marked.use(mangle(), { breaks: true });

export default {
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
            return `${days}j ${hours}h ${minutes}min`.replace(/0j /, '').replace(/0h /, '').replace(/ 0min/, '');
        }
    },
    methods: {
        formatDate(date) {
            return new Date(date + 'Z').toLocaleString('FR-fr', { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' });
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
                    <span>📍 {{ event.place }}</span>
                    <span v-if="duration">🕓 {{ duration }}</span>
                    <span v-if="event.price">💲 {{ event.price }}</span>
                    <span v-if="event.link">🖇 <a :href="event.link">Lien de l'événement</a></span>
                    <span v-if="event.access">🔒 {{ event.access }}</span>
                    <span v-if="event.status">{{ status }}</span>
                    <span v-if="event.capacity">👥 {{ event.capacity }} places</span>
                    <span>📝 Crée le {{ formatDate(event.createDate) }}</span>
                    <span>🔄 Dernière mise à jour le {{ formatDate(event.lastUpdateDate) }}</span>
                </div>
            </div>
        </article>
    </section>
</template>

<style lang="scss" scoped>
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

        a > * {
            width: 100%;
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