<script>
import Api from '../api';
import EventPreview from '../components/EventPreview.vue';
import SwitchButton from '../components/SwitchButton.vue';
import WebCalLink from '../components/WebCalLink.vue';

const baseUrl = import.meta.env.VITE_BASE_URL ?? '';
const eventsPerPage = 50;

export default {
    components: {
        EventPreview,
        SwitchButton,
        WebCalLink
    },
    data() {
        return {
            assos: [],
            events: [],
            allCampus: []
        }
    },
    computed: {
        past: {
            get() {
                return 'past' in this.$route.query;
            },
            set(value) {
                value = value ? null : undefined;
                this.$router.replace({ query: { ...this.$route.query, past: value, page: undefined } });
            }
        },
        page: {
            get() {
                return parseInt(this.$route.query.page) || 1;
            },
            set(value) {
                if (value <= 1)
                    value = undefined;
                this.$router.push({ query: { ...this.$route.query, page: value } });
            }
        },
        selectedCampus: {
            get() {
                if (this.$route.query.campus === null)
                    return [];
                return this.$route.query.campus?.split(',');
            },
            set(value) {
                value = !value ? undefined : value.length == 0 ? null : value.join(',');
                this.$router.replace({ query: { ...this.$route.query, campus: value, page: undefined } });
            }
        },
        pageMax() {
            return Math.ceil(this.events.count / eventsPerPage);
        },
        rssUrl() {
            return location.protocol + '//' + location.host + baseUrl + '/events.rss';
        },
        icsPath() {
            return location.host + baseUrl + '/events.ics';
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
        },
        isCampusSelected(campus) {
            if (!this.selectedCampus)
                return true;
            return this.selectedCampus.includes(campus);
        },
        selectCampus(campus, selected) {
            if (selected) {
                if (this.selectedCampus)
                    this.selectedCampus = this.selectedCampus.concat([campus]);
                else 
                    this.selectedCampus = [ campus ];
            } else {
                if (this.selectedCampus)
                    this.selectedCampus = this.selectedCampus.filter(c => c != campus);
                else
                    this.selectedCampus = this.allCampus.filter(c => c != campus);
            }
        }
    },
    beforeRouteEnter(to, from, next) {
        Promise.all([
            Api.events.get({
                limit: eventsPerPage,
                offset: ((to.query.page ?? 1) - 1) * eventsPerPage,
                campus: to.query.campus?.split(','),
                after: 'past' in to.query ? undefined : new Date(),
                before: 'past' in to.query ? new Date() : undefined,
                desc: 'past' in to.query ? true : undefined
            }),
            Api.assos.get()
        ])
            .then(([events, assos]) => {
                next(view => {
                    view.events = events;
                    view.assos = assos;
                    view.allCampus = assos.reduce((allCampus, asso) => {
                        if (asso.campus && !allCampus.includes(asso.campus))
                            allCampus.push(asso.campus);
                        return allCampus;
                    }, []);
                });
            })
            .catch(error => next(view => view.$state.error = error));
    },
    beforeRouteUpdate(to, from, next) {
        Api.events.get({
            limit: eventsPerPage,
            offset: ((to.query.page ?? 1) - 1) * eventsPerPage,
            campus: to.query.campus?.split(','),
            after: 'past' in to.query ? undefined : new Date(),
            before: 'past' in to.query ? new Date() : undefined,
            desc: 'past' in to.query ? true : undefined
        })
            .then(events => {
                this.events = events;
                next();
            })
            .catch(error => this.$state.error = error);
    }
};
</script>

<template>
    <section>
        <article class="parameters">
            <div v-if="allCampus.length > 1">
                Campus :
                <template v-for="c in allCampus" :key="c">
                    <label>
                        {{ c }}
                        <SwitchButton @update:model-value="v => selectCampus(c, v)" :model-value="isCampusSelected(c)" />
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
        <article v-if="events.length == 0">
            <h2>Aucun événement trouvé</h2>
            <p>Revenez plus tard, ou essayer de changer les paramètres.</p>
        </article>
        <article class="pages">
            <div>
                <button v-if="page > 1" @click="page--">Page précédente</button>
                <template v-for="n in 3" :key="n">
                    <button v-if="0 < page - 4 + n && page - 4 + n <= pageMax" @click="page -= 4 + n">{{ page - 4 + n }}</button>
                </template>
                <button disabled>{{ page }}</button>
                <template v-for="n in 3" :key="n">
                    <button v-if="0 < page + n && page + n <= pageMax" @click="page += n">{{ page + n }}</button>
                </template>
                <button v-if="page < pageMax" @click="page++">Page suivante</button>
            </div>
            <div>
                {{ events.count }} événements correspondant aux critères sélectionnés
            </div>
        </article>
    </section>
    <section>
        <article class="feeds">
            <h2>Flux RSS et agenda</h2>
            URL du flux RSS :
            <input type="text" :value="rssUrl" readonly />
            <a target="_blank" :href="rssUrl">
                <button>Ajouter le flux RSS</button>
            </a>
            <WebCalLink :path="icsPath">
                Ajouter tous les événements à mon agenda
            </WebCalLink>
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

.pages {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 2em;

    button {
        margin-left: 5px;
        margin-right: 5px;
        min-width: 2em;
    }
}

.feeds {
    display: flex;
    flex-direction: column;

    button {
        width: 100%;
    }
}
</style>