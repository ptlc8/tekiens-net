<template>
    URL de l'agenda :
    <input type="text" :value="url" readonly />
    <a target="_blank" :href="'webcall://' + url">
        <button>
            <slot>Ajouter à mon agenda</slot>
        </button>
    </a>
</template>

<script>
import { baseUrl, origin } from '../api';
const host = origin.replace(/^https?:\/\//, '');

export default {
    props: {
        path: {
          type: String,
          required: true,
        },
    },
    computed: {
        url() {
            return `${host}${baseUrl}${this.path}`
        }
    },
};
</script>

<style scoped>
button {
    width: 100%;
}
</style>
