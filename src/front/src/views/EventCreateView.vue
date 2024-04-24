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
            event: {
                status: 'programmed'
            },
            error: null
        }
    },
    mounted() {
        if (this.isNotGranted)
            this.$router.push('/events/');
    },
    methods: {
        createEvent() {
            Api.events.create(this.event)
                .then(event => this.$router.push('/events/' + event.id))
                .catch(error => this.error = error);
        }
    },
    computed: {
        color() {
            return '#' + this.sessionStore.session?.asso?.color?.toString(16)?.padStart(6, 0);
        },
        backgroundColor() {
            return this.color + '44';
        },
        isNotGranted() {
            if (this.sessionStore.session === null) // not logged in
                return true;
            if (this.sessionStore.session === undefined) // not loaded
                return undefined;
            return false;
        },
        eventUrl() {
            return 'https://' + location.host + baseUrl + '/events/$id';
        },
    },
    watch: {
        isNotGranted(isNotGranted) {
            if (isNotGranted)
                this.$router.push('/events/');
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
        <article :style="{ '--accent-color': color, '--bg-color': backgroundColor }">
            <h2>Créer un événement</h2>
            <form @submit.prevent="createEvent">
                <label for="title">Titre</label>
                <input v-model="event.title" id="title" name="title" type="text" required maxlength="255" placeholder="Nom de l'événement" />
                <label for="date">Date et heure</label>
                <DateTimeInput v-model="event.date" id="date" name="date" type="datetime-local" required />
                <label for="place">Lieu</label>
                <input v-model="event.place" id="place" name="place" type="text" required maxlength="255" placeholder="Bâtiment Cauchy" />
                <label for="poster">Affiche (optionnel)</label>
                <ImageInput v-model="event.poster" id="poster" name="poster" />
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
                <button type="submit">Créer l'événement</button>
                <span v-if="error" class="error">{{ error }}</span>
            </form>
        </article>
    </section>
</template>

<style scoped lang="scss">
form {
    label {
        margin-left: 1em;
    }

    img {
        height: 200px;
        object-fit: contain;
    }

    .error {
        color: red;
    }
}
</style>
