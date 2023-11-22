<script>
import { RouterLink } from 'vue-router';

export default {
    props: {
        event: Object,
        asso: {
            type: Object,
            default: null,
        }
    },
    computed: {
        color() {
            return '#' + this.asso?.color?.toString(16)?.padStart(6, 0);
        }
    }
};
</script>

<template>
    <RouterLink :to="'/events/' + event.id" class="event" :style="{ '--accent-color': color }">
        <div class="poster" :style="{ backgroundColor: color }">
            <img v-if="event.poster" :src="event.poster" :alt="event.title" width="300" />
        </div>
        <div class="infos">
            <span class="title">{{ event.title }}</span>
            <RouterLink :to="'/assos/' + event.asso_id">{{ asso?.names?.[0] ?? event.asso_id }}</RouterLink>
            {{ new Date(event.date).toLocaleString('FR-fr', { weekday:'long', hour:'2-digit', minute:'2-digit' }) }}
        </div>
    </RouterLink>
</template>

<style lang="scss" scoped>
.event {
    flex: 16em 1 0;
    max-width: 32em;
    margin: 0.5em;
    border-radius: 4px;
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, .1);
    overflow: hidden;
    color: inherit;
    text-decoration: none;
    background-color: white;

    .poster {
        height: 12em;
        overflow: hidden;

        img {
            width: 100%;
        }
    }

    .infos {
        display: flex;
        flex-direction: column;
        margin: .5em 1em;

        .title {
            font-weight: bold;
        }
    }
}
</style>