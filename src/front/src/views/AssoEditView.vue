<script>
import Api from '../api';
import { useSessionStore } from "../stores/session";
import ArrayInput from '../components/ArrayInput.vue';
import SocialInput from '../components/SocialInput.vue';
import ImageInput from '../components/ImageInput.vue';

export default {
    setup() {
        return {
            sessionStore: useSessionStore()
        }
    },
    data() {
        return {
            asso: {},
            originalAsso: {},
            error: null
        }
    },
    beforeRouteEnter(to, _from, next) {
        Api.assos.getOne(to.params.id)
            .then(asso => next(view => view.originalAsso = JSON.parse(JSON.stringify(view.asso = asso))))
            .catch(error => next(view => view.$state.error = error));
    },
    beforeRouteUpdate(to, _from, next) {
        Api.assos.getOne(to.params.id)
            .then(asso => this.originalAsso = JSON.parse(JSON.stringify(this.asso = asso)))
            .catch(error => this.$state.error = error)
            .finally(next);
    },
    mounted() {
        if (this.isNotGranted)
            this.$router.push('/assos/' + encodeURIComponent(this.$route.params.id));
    },
    methods: {
        editAsso() {
            let fields = {};
            for (let field in this.asso)
                if (this.asso[field] != this.originalAsso[field])
                    fields[field] = this.asso[field];
            Api.assos.update(this.originalAsso.id, fields)
                .then(() => this.$router.push('/assos/' + encodeURIComponent(this.asso.id)))
                .catch(error => this.error = error);
        }
    },
    computed: {
        isNotGranted() {
            if (this.sessionStore.session === null) // not logged in
                return true;
            if (this.sessionStore.session === undefined || !this.originalAsso.id) // not loaded
                return undefined;
            return this.sessionStore.session.asso_id != this.originalAsso.id;
        },
        color: {
            get() {
                return '#' + Number(this.asso.color).toString(16).padStart(6, '0');
            },
            set(value) {
                this.asso.color = parseInt(value.substr(1), 16);
            }
        }
    },
    watch: {
        isNotGranted(isNotGranted) {
            if (isNotGranted)
                this.$router.push('/assos/' + encodeURIComponent(this.$route.params.id));
        }
    },
    components: {
        ArrayInput,
        SocialInput,
        ImageInput
    }
}
</script>

<template>
    <section :style="{ '--accent-color': color }">
        <article>
            <h2>Éditer une association</h2>
            <form @submit.prevent="editAsso">
                <label for="id">Identifiant (sert à se connecter et s'affiche dans l'URL)</label>
                <input v-model="asso.id" id="id" name="id" type="text" required maxlength="255" placeholder="super-asso" />
                <label>Noms</label>
                <ArrayInput v-model="asso.names" v-slot="{ onInput, value }" default="">
                    <input @input="onInput" :value="value" name="names[]" type="text" required maxlength="255" placeholder="Super Association" />
                </ArrayInput>
                <label for="logos">Logos</label>
                <ArrayInput v-model="asso.logos" v-slot="{ onUpdate, value, placeholder }" :placeholder="originalAsso.logos" default="">
                    <ImageInput @update:modelValue="onUpdate" :modelValue="value" :placeholder="placeholder" />
                </ArrayInput>
                <label for="theme">Thème</label>
                <input v-model="asso.theme" id="theme" name="theme" type="text" required maxlength="255" placeholder="Thème intéressant" />
                <label for="campus">Campus</label>
                <input v-model="asso.campus" id="campus" name="campus" type="text" required maxlength="255" placeholder="Cergy" />
                <label for="room">Local associatif (facultatif)</label>
                <input v-model="asso.room" id="room" name="room" type="text" maxlength="255" placeholder="CY 211" />
                <label for="color">Couleur</label>
                <input v-model="color" id="color" name="color" type="color" placeholder="#000" />
                <label for="start">Année de création (facultatif)</label>
                <input v-model="asso.start" id="start" name="start" type="number" placeholder="1983" />
                <label for="end">Année de dissolution (facultatif)</label>
                <input v-model="asso.end" id="end" name="end" type="number" placeholder="jamais" />
                <label for="description">Description (facultatif)</label>
                <textarea v-model="asso.description" id="description" name="description" maxlength="65535" rows="12" placeholder="Cette association est intéressante, venez !"></textarea>
                <label for="socials">Réseaux sociaux (facultatif)</label>
                <ArrayInput v-model="asso.socials" v-slot="{ onUpdate, value }" default="web:">
                    <SocialInput @update:modelValue="onUpdate" :modelValue="value" />
                </ArrayInput>
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