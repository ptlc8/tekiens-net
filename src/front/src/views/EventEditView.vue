<script>
import Api from '../api';
import { eventStatus } from '../eventStatus';
import { useSessionStore } from "../stores/session";
import DateTimeInput from '../components/DateTimeInput.vue';
import ImageInput from '../components/ImageInput.vue';
import DurationInput from '../components/DurationInput.vue';
import Editor from '../components/Editor.vue';

const baseUrl = import.meta.env.VITE_BASE_URL ?? '';

export default {
    setup() {
        return {
            sessionStore: useSessionStore(),
            eventStatus
        }
    },
    data() {
        return {
            event: {},
            asso: {},
            originalEvent: {},
            error: null
        }
    },
    beforeRouteEnter(to, _from, next) {
        Api.events.getOne(to.params.id)
            .then(event => next(view => view.originalEvent = JSON.parse(JSON.stringify(view.event = event))))
            .catch(error => next(view => view.$state.error = error));
    },
    beforeRouteUpdate(to, _from, next) {
        Api.events.getOne(to.params.id)
            .then(event => this.originalEvent = JSON.parse(JSON.stringify(this.event = event)))
            .catch(error => this.$state.error = error)
            .finally(next);
    },
    mounted() {
        if (this.isNotGranted)
            this.$router.push('/events/' + this.$route.params.id);
    },
    methods: {
        editEvent() {
            let fields = {};
            for (let field in this.event)
                if (this.event[field] != this.originalEvent[field])
                    fields[field] = this.event[field];
            Api.events.update(this.event.id, fields)
                .then(() => this.$router.push('/events/' + this.$route.params.id))
                .catch(error => this.error = error);
        }
    },
    computed: {
        backgroundColor() {
            return this.asso?.color + '44';
        },
        isNotGranted() {
            if (this.sessionStore.session === null) // not logged in
                return true;
            if (this.sessionStore.session === undefined || !this.event.asso_id) // not loaded
                return undefined;
            return this.sessionStore.session.asso_id != this.event.asso_id;
        },
        eventUrl() {
            return 'https://' + location.host + baseUrl + '/events/' + this.$route.params.id;
        },
    },
    watch: {
        event(event) {
            Api.assos.getOne(event.asso_id)
                .then(asso => this.asso = asso);
        },
        isNotGranted(isNotGranted) {
            if (isNotGranted)
                this.$router.push('/events/' + this.$route.params.id);
        }
    },
    components: {
        DateTimeInput,
        ImageInput,
        DurationInput,
        Editor
    }
}
</script>

<template>
    <section>
        <article :style="{ '--accent-color': asso?.color, '--bg-color': backgroundColor }">
            <h2>Éditer un événement</h2>
            <form @submit.prevent="editEvent">
                <label for="title">Titre</label>
                <input v-model="event.title" id="title" name="title" type="text" required maxlength="255" placeholder="Nom de l'événement" />
                <label for="date">Date et heure</label>
                <DateTimeInput v-model="event.date" id="date" name="date" type="datetime-local" required />
                <label for="place">Lieu</label>
                <input v-model="event.place" id="place" name="place" type="text" required maxlength="255" placeholder="Bâtiment Cauchy" />
                <label for="poster">Affiche (optionnel)</label>
                <ImageInput v-model="event.poster" id="poster" name="poster" :placeholder="originalEvent.poster" />
                <label for="description">Description (optionnel)</label>
                <Editor v-model="event.description" placeholder="Cet événement sera intéressant, venez !" />
                <label for="price">Prix (optionnel)</label>
                <input v-model="event.price" id="price" name="price" type="text" maxlength="255" placeholder="Gratuit" />
                <label for="duration">Durée (optionnel)</label>
                <DurationInput v-model="event.duration" id="duration" name="duration" />
                <label for="link">Lien du QR code (optionnel)</label>
                <input v-model="event.link" id="link" name="link" type="text" maxlength="255" :placeholder="eventUrl" />
                <label for="access">Qui peut participer ? (optionnel)</label>
                <input v-model="event.access" id="access" name="access" type="text" maxlength="255" placeholder="Ouvert à tous" />
                <label for="status">Statut</label>
                <select v-model="event.status" id="status" name="status" >
                    <option v-for="name, status in eventStatus" :value="status">{{ name }}</option>
                </select>
                <label for="capacity">Capacité (optionnel)</label>
                <input v-model="event.capacity" id="capacity" name="capacity" type="number" min="0" placeholder="100 places" />
                <button type="submit">Publier les modifications</button>
                <span v-if="error" class="error">{{ error }}</span>
            </form>
        </article>
    </section>
</template>

<style scoped lang="scss">
form {
    .error {
        color: red;
    }
}
</style>
