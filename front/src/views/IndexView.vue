<script>
import { RouterLink } from 'vue-router';
import Api from '../api';
import EventPreview from '../components/EventPreview.vue';
import AssoPreview from '../components/AssoPreview.vue';

export default {
    components: {
        EventPreview,
        AssoPreview
    },
    data() {
        return {
            events: [],
            assos: [],
        }
    },
    beforeRouteEnter(to, _from, next) {
        Promise.all([
            Api.events.get({ after: new Date(), limit: 10 }),
            Api.assos.get({ after: new Date().getUTCFullYear(), order: 'random' })
        ]).then(([events, assos]) => next(view => {
            view.events = events;
            view.assos = assos;
        })).catch(error => next(view => view.$state.error = error));
    }
};
</script>

<template>
    <section>
        <article>
            <h2>Événements à venir</h2>
            <div class="events">
                <EventPreview v-for="event in events" :key="event.id" :event="event" :asso="assos.find(a => a.id == event.asso_id)" />
                <RouterLink to="/events" class="more">Voir tous les événements</RouterLink>
            </div>
        </article>
    </section>
    <section>
        <article>
            <h2>Associations</h2>
            <div class="assos">
                <AssoPreview v-for="asso in assos.slice(0, 6)" :key="asso.id" :asso="asso" />
                <RouterLink to="/assos" class="more">Découvrir les associations</RouterLink>
            </div>
        </article>
    </section>
</template>

<style lang="scss" scoped>
.events, .assos {
    display: flex;
    overflow: auto;

    .more {
        margin: .3125em;
        border-radius: 4px;
        box-shadow: 0 0 10px 2px #0000001a;
        text-decoration: none;
        display: flex;
        align-items: center;
        text-transform: uppercase;
        font-size: 1.6em;
        text-align: center;
        padding: 0.6em;
        background-color: white;
    }
}
</style>
