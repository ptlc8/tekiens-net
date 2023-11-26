<script>
import Api from '../api';
import { useSessionStore } from "../stores/session";
import DateTimeInput from '../components/DateTimeInput.vue';

export default {
    setup() {
        return {
            sessionStore: useSessionStore()
        }
    },
    data() {
        return {
            event: {},
            error: null
        }
    },
    mounted() {
        if (this.isNotGranted)
            this.$router.push('/events/' + this.$route.params.id);
        Api.events.getOne(this.$route.params.id)
            .then(event => this.event = event)
            .catch(error => this.error = error);
    },
    methods: {
        getEventUrl() {
            return 'https://' + location.host + '/events/' + this.$route.params.id;
        },
        editEvent() {
            Api.events.update(this.event.id, this.event)
                .then(() => this.$router.push('/events/' + this.$route.params.id))
                .catch(error => this.error = error);
        }
    },
    computed: {
        isNotGranted() {
            if (this.sessionStore.session === null) // not logged in
                return true;
            if (this.sessionStore.session === undefined || !this.event.asso_id) // not loaded
                return undefined;
            return this.sessionStore.session.asso_id != this.event.asso_id;
        },
        date: {
            get() {
                return this.event.date ? new Date(this.event.date + 'Z') : undefined;
            },
            set(date) {
                this.event.date = date.toISOString().slice(0, 19);
            }
        }
    },
    watch: {
        isNotGranted(isNotGranted) {
            if (isNotGranted)
                this.$router.push('/events/' + this.$route.params.id);
        }
    },
    components: {
        DateTimeInput
    }
}
</script>

<template>
    <section>
        <article>
            <h2>Éditer un événement</h2>
            <form @submit.prevent="editEvent">
                <label for="title">Titre</label>
                <input v-model="event.title" id="title" name="title" type="text" required maxlength="255" placeholder="Nom de l'événement" />
                <label for="date">Date et heure</label>
                <DateTimeInput v-model="date" id="date" name="date" type="datetime-local" required />
                <label for="place">Lieu</label>
                <input v-model="event.place" id="place" name="place" type="text" required maxlength="255" placeholder="Bâtiment Cauchy" />
                <label for="poster">Url de l'affiche (optionnel)</label>
                <input v-model="event.poster" id="poster" name="poster" type="text" maxlength="255" placeholder="https://tekiens.net/assets/super-affiche.jpg" />
                <img v-if="event.poster" :src="event.poster" alt="Affiche de l'événement" width="200" height="200" />
                <label for="description">Description (optionnel)</label>
                <textarea v-model="event.description" id="description" name="description" type="text" maxlength="128" rows="12" placeholder="Cet événement sera intéressant, venez !"></textarea>
                <label for="price">Prix (optionnel)</label>
                <input v-model="event.price" id="price" name="price" type="text" maxlength="255" placeholder="Gratuit" />
                <!--<label for="duration">Durée (optionnel)</label>
                <input v-model="event.duration" id="duration" name="duration" type="text" maxlength="255" placeholder="2h" />-->
                <label for="link">Lien du QR code (optionnel)</label>
                <input v-model="event.link" id="link" name="link" type="text" maxlength="255" :placeholder="getEventUrl()" />
                <label for="access">Qui peut participer ? (optionnel)</label>
                <input v-model="event.access" id="access" name="access" type="text" maxlength="255" placeholder="Ouvert à tous" />
                <label for="status">Statut (optionnel)</label>
                <input v-model="event.status" id="status" name="status" type="text" maxlength="255" placeholder="Programmé" />
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