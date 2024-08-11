<script>
import Api from '../api';
import EventPreview from '../components/EventPreview.vue';
import SwitchButton from '../components/SwitchButton.vue';

export default {
    components: {
        EventPreview,
        SwitchButton
    },
    data() {
        return {
            assos: [],
            events: [],
            selectedCampus: {}
        }
    },
    computed: {
        filteredEvents() {
            let events = this.events.filter(event => {
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
    methods: {
        getMonday(date) {
            date = new Date(date);
            let weekday = (date.getDay() || 7) - 1;
            let monday = new Date((date.getTime() - weekday * 24 * 60 * 60 * 1000));
            return new Date(monday.getFullYear(), monday.getMonth(), monday.getDate());
        },
        getEventsByWeek() {
            return this.filteredEvents.reduce((o, event) => {
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
    },
    beforeRouteEnter(to, from, next) {
        Promise.all([
            Api.events.get(),
            Api.assos.get()
        ])
            .then(([events, assos]) => {
                next(view => {
                    view.events = events;
                    view.assos = assos;
                    view.selectedCampus = assos.reduce((allCampus, asso) => {
                        allCampus[asso.campus] = true;
                        return allCampus;
                    }, {});
                });
            })
            .catch(error => next(view => view.$state.error = error));
    }
};
</script>

<template>
    <section>
        <article class="parameters">
            <div v-if="Object.keys(selectedCampus).length > 1">
                Campus :
                <template v-for="_, campus in selectedCampus" :key="campus">
                    <label>
                        {{ campus }}
                        <SwitchButton v-model="selectedCampus[campus]" />
                    </label>
                </template>
            </div>
            <div>
                <label>
                    Afficher les événements passés
                    <SwitchButton v-model="past" class="switch" />
                </label>
            </div>
        </article>
        <article v-for="(weekEvents, monday) in getEventsByWeek()" :key="monday">
            <h2>{{ getWeekName(monday) }}</h2>
            <div class="events">
                <EventPreview v-for="event in weekEvents" :key="event.id" :event="event" :asso="getAssoById(event.asso_id)" />
            </div>
        </article>
        <article v-if="filteredEvents.length == 0">
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

        .switch {
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