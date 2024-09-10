<script>
import Api from '../api';
import { useSessionStore } from "../stores/session";
import ArrayInput from '../components/ArrayInput.vue';
import SocialInput from '../components/SocialInput.vue';
import ImageInput from '../components/ImageInput.vue';
import Editor from '../components/Editor.vue';

export default {
    components: {
        ArrayInput,
        SocialInput,
        ImageInput,
        Editor
    },
    setup() {
        return {
            sessionStore: useSessionStore()
        }
    },
    data() {
        return {
            asso: {},
            originalAsso: {},
            sendingRequest: false,
            error: null
        }
    },
    computed: {
        isNotGranted() {
            if (this.sessionStore.session === null) // not logged in
                return true;
            if (this.sessionStore.session === undefined || !this.originalAsso.id) // not loaded
                return undefined;
            return this.sessionStore.session.asso_id != this.originalAsso.id;
        }
    },
    methods: {
        editAsso() {
            let fields = {};
            for (let field in this.asso)
                if (this.asso[field] != this.originalAsso[field])
                    fields[field] = this.asso[field];
            this.sendingRequest = true;
            Api.assos.update(this.originalAsso.id, fields)
                .then(() => this.$router.push('/assos/' + encodeURIComponent(this.asso.id)))
                .catch(error => this.error = error)
                .finally(() => this.sendingRequest = false);
        }
    },
    watch: {
        isNotGranted(isNotGranted) {
            if (isNotGranted)
                this.$router.push('/assos/' + encodeURIComponent(this.$route.params.id));
        }
    },
    mounted() {
        if (this.isNotGranted)
            this.$router.push('/assos/' + encodeURIComponent(this.$route.params.id));
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
    }
}
</script>

<template>
    <section :style="{ '--accent-color': asso.color }">
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
                    <ImageInput @update:model-value="onUpdate" :model-value="value" :placeholder="placeholder" />
                </ArrayInput>
                <label for="theme">Thème</label>
                <input v-model="asso.theme" id="theme" name="theme" type="text" required maxlength="255" placeholder="Thème intéressant" />
                <label for="campus">Campus</label>
                <input v-model="asso.campus" id="campus" name="campus" type="text" required maxlength="255" placeholder="Cergy" />
                <label for="room">Local associatif (facultatif)</label>
                <input v-model="asso.room" id="room" name="room" type="text" maxlength="255" placeholder="CY 211" />
                <label for="color">Couleur</label>
                <input v-model="asso.color" id="color" name="color" type="color" placeholder="#000" />
                <label for="start">Année de création (facultatif)</label>
                <input v-model="asso.start" id="start" name="start" type="number" placeholder="1983" />
                <label for="end">Année de dissolution (facultatif)</label>
                <input v-model="asso.end" id="end" name="end" type="number" placeholder="jamais" />
                <label for="description">Description (facultatif)</label>
                <Editor v-model="asso.description" placeholder="Cette association est intéressante, venez !" />
                <label for="socials">Réseaux sociaux (facultatif)</label>
                <ArrayInput v-model="asso.socials" v-slot="{ onUpdate, value }" :default="{ id: 'web', value: '' }">
                    <SocialInput @update:model-value="onUpdate" :model-value="value" />
                </ArrayInput>
                <button type="submit" :disabled="sendingRequest">Publier les modifications</button>
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
    button[type="submit"] {
        &:disabled, &[disabled] {
            cursor: progress;
        }
    }
}
</style>
