<script>
import Api from '../api';
import EventPreview from '../components/EventPreview.vue';

export default {
    components: {
        EventPreview
    },
    data() {
        return {
            _events: [],
            error: null,
            //campus: {}
        }
    },
    computed: {
        events() {
            return this._events.filter(event => {
                return /*this.campus[event.campus] &&*/ new Date(event.date) > new Date();
            });
        }
    },
    methods: {
        getEvents() {
            Api.events.get()
                .then((events) => {
                    this._events = events;
                    /*this.campus = events.reduce((campus, event) => {
                        campus[event.campus] = true;
                        return campus;
                    }, {});*/
                })
                .catch((error) => {
                    this.error = error;
                });
        },
        getMonday(date) {
            date = new Date(date);
            let weekday = (date.getDay() || 7) - 1;
            let monday = new Date((date.getTime() - weekday * 24 * 60 * 60 * 1000));
            return new Date(monday.getFullYear(), monday.getMonth(), monday.getDate());
        },
        getEventsByWeek() {
            return this.events.reduce((o, event) => {
                const monday = this.getMonday(new Date(event.date));
                const key = `${monday.getFullYear()}-${monday.getMonth()+1}-${monday.getDate()}`;
                if (!o[key]) o[key] = [];
                o[key].push(event);
                return o;
            }, {});
        },
        getWeekName(date) {
            let monday = this.getMonday(date);
            if (monday.getTime() == this.getMonday(new Date()).getTime())
                return 'Cette semaine';
            if (monday.getTime() == this.getMonday(new Date(new Date().getTime() + 7 * 24*60*60*1000)).getTime())
                return 'La semaine prochaine';
            return 'Semaine du ' + new Date(monday).toLocaleDateString("FR-fr");
        }
    },
    mounted() {
        this.getEvents();
    }
};
</script>

<template>
    <section>
        <!--<div class="campus">
            <template v-for="c, name in campus">
                <input type="checkbox" v-model="campus[name]" />
                {{ name }}
            </template>
        </div>-->
        <span v-if="error">Erreur: {{ error }}</span>
        <div v-for="(events, monday) in getEventsByWeek()" :key="monday">
            <h2>{{ getWeekName(monday) }}</h2>
            <div class="events">
                <EventPreview v-for="event in events" :key="event.id" :event="event" />
            </div>
        </div>
    </section>
</template>

<style lang="scss" scoped>
.events {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
</style>