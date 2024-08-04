<script>
import { RouterLink } from 'vue-router';

export default {
    props: {
        event: {
            type: Object,
            required: true,
        },
        asso: {
            type: Object,
            default: null,
        }
    }
};
</script>

<template>
    <RouterLink :to="'/events/' + event.id" class="event" :style="{ '--accent-color': asso?.color }">
        <div class="poster">
            <img v-if="event.poster" :src="event.poster" :alt="event.title" width="300" />
        </div>
        <div class="infos">
            <div class="date">
                <span class="month">{{ new Date(event.date + 'Z').toLocaleString('FR-fr', { month: 'short' }) }}</span>
                <span class="day">{{ new Date(event.date + 'Z').toLocaleString('FR-fr', { day: '2-digit' }) }}</span>
                <span class="weekday">{{ new Date(event.date + 'Z').toLocaleString('FR-fr', { weekday: 'long' }) }}</span>
            </div>
            <div class="data">
                <span class="title">{{ event.title }}</span>
                <RouterLink :to="'/assos/' + encodeURIComponent(event.asso_id)">{{ asso?.names?.[0] ?? event.asso_id }}</RouterLink>
                <span class="place">📍 {{ event.place }}</span>
                <span class="time">🕓 {{ new Date(event.date + 'Z').toLocaleString('FR-fr', { hour: '2-digit', minute: '2-digit' }) }}</span>
            </div>
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
        height: 16em;
        background-color: var(--accent-color);

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }

    .infos {
        display: flex;
        margin: .5em 1em;

        .date {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-right: 0.2em solid var(--accent-color);
            margin-right: 0.5em;
            padding-right: 0.5em;
            line-height: 1;

            .month {
                font-size: 1.2em;
                text-transform: uppercase;
            }

            .day {
                font-size: 2.4em;
            }
        }

        .data {
            display: flex;
            flex-direction: column;
            line-height: 1.2;

            * {
                max-height: 1.2em;
                overflow: hidden;
                display: -webkit-box;
                -webkit-line-clamp: 1;
                line-clamp: 1;
                -webkit-box-orient: vertical;
            }

            .title {
                font-weight: bold;
            }
        }
    }
}
</style>