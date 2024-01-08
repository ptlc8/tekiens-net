<script>
import { RouterLink } from 'vue-router';
import Api from '../api';
import EventPreview from '../components/EventPreview.vue';

export default {
    components: {
        EventPreview
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
            Api.assos.get({ after: new Date().getUTCFullYear() })
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
                <RouterLink v-for="asso, i in assos" :key="asso.id" :to="'/assos/' + asso.id">
                    <img :src="asso.logos[0]" :alt="asso.names[0]" :style="{
                        top:  50 - Math.cos((i%2 ? (i+1)/2 : -i/2) / assos.length * 2*Math.PI)*40 + '%',
                        left: 50 + Math.sin((i%2 ? (i+1)/2 : -i/2) / assos.length * 2*Math.PI)*40 + '%'
                    }" width="100" height="100" />
                </RouterLink>
                <RouterLink to="/assos">
                    <h3 class="title">Découvrir les assos</h3>
                </RouterLink>
            </div>
        </article>
    </section>
</template>

<style lang="scss" scoped>
.events {
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
    }
}
.assos {
    position: relative;
    height: 16em;

    .title {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        margin: 0;
    }

    img {
        position: absolute;
        width: 4em;
        height: auto;
        transform: translate(-50%, -50%);
    }
}
</style>