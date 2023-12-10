<script>
import Api from '../api';
import EventPreview from '../components/EventPreview.vue';
import Switch from '../components/Switch.vue';

export default {
    components: {
        EventPreview,
        Switch
    },
    data() {
        return {
            assos: [],
            _events: [],
            error: null,
            selectedCampus: {}
        }
    },
    computed: {
        events() {
            let events = this._events.filter(event => {
                let campus = this.getAssoById(event.asso_id)?.campus;
                if (campus && !this.selectedCampus[campus])
                    return false;
                if (this.past)
                    return new Date(event.date + 'Z') <= new Date();
                return new Date(Date.parse(event.date + 'Z') + (event.duration ?? 0) * 60 * 1000) > new Date();
            });
            if (this.past)
                events.reverse();
            return events;
        },
        past: {
            get() {
                return 'past' in this.$route.query;
            },
            set(value) {
                value = value ? null : undefined;
                this.$router.replace({ query: { ...this.$route.query, past: value } });
            }
        }
    },
    mounted() {
        this.getEvents();
        this.getAssos();
    },
    methods: {
        getEvents() {
            Api.events.get()
                .then(events => this._events = events)
                .catch(error => this.error = error);
        },
        getAssos() {
            Api.assos.get()
                .then(assos => {
                    this.assos = assos;
                    this.selectedCampus = assos.reduce((allCampus, asso) => {
                        allCampus[asso.campus] = true;
                        return allCampus;
                    }, {});
                })
                .catch(error => this.error = error);
        },
        getMonday(date) {
            date = new Date(date);
            let weekday = (date.getDay() || 7) - 1;
            let monday = new Date((date.getTime() - weekday * 24 * 60 * 60 * 1000));
            return new Date(monday.getFullYear(), monday.getMonth(), monday.getDate());
        },
        getEventsByWeek() {
            return this.events.reduce((o, event) => {
                const monday = this.getMonday(new Date(event.date + 'Z'));
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
            if (monday.getTime() == this.getMonday(new Date(new Date().getTime() - 7 * 24*60*60*1000)).getTime())
                return 'La semaine dernière';
            return 'Semaine du ' + new Date(monday).toLocaleDateString('FR-fr');
        },
        getAssoById(id) {
            return this.assos.find(asso => asso.id == id);
        }
    }
};
</script>

<template>
    <section>
        <article class="parameters">
            <div v-if="Object.keys(selectedCampus).length > 1">
                Campus :
                <template v-for="_, campus in selectedCampus">
                    <label>
                        {{ campus }}
                        <input type="checkbox" v-model="selectedCampus[campus]" />
                    </label>
                </template>
            </div>
            <div>
                <label>
                    Afficher les événements passés
                    <Switch v-model="past" class="switch" />
                </label>
            </div>
        </article>
        <span v-if="error">Erreur: {{ error }}</span>
        <article v-for="(events, monday) in getEventsByWeek()" :key="monday">
            <h2>{{ getWeekName(monday) }}</h2>
            <div class="events">
                <EventPreview v-for="event in events" :key="event.id" :event="event" :asso="getAssoById(event.asso_id)" />
            </div>
        </article>
        <article v-if="this.events.length == 0">
            <h2>Aucun événement à venir</h2>
            <p>Revenez plus tard, ou consultez la liste des événements passés.</p>
        </article>
    </section>
</template>

<style lang="scss" scoped>
.parameters {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1em;

    label {
        margin: 0 .5em;

        input, .switch {
            margin: 0 4px;
        }
    }

}

.events {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
</style>