<script>
import Api from '../api';
import Switch from '../components/Switch.vue';
import AssoPreview from '../components/AssoPreview.vue';

export default {
    components: {
        Switch,
        AssoPreview
    },
    data() {
        return {
            assos: [],
            selectedCampus: {}
        }
    },
    beforeRouteEnter(_to, _from, next) {
        Api.assos.get()
            .then(assos => {
                next(view => {
                    view.assos = assos;
                    view.selectedCampus = assos.reduce((allCampus, asso) => {
                        allCampus[asso.campus] = true;
                        return allCampus;
                    }, {});
                });
            })
            .catch(error => next(view => view.$state.error = error));
    },
    computed: {
        past: {
            get() {
                return 'past' in this.$route.query;
            },
            set(value) {
                value = value ? null : undefined;
                this.$router.replace({ query: { ...this.$route.query, past: value } });
            }
        },
        filteredAssos() {
            return this.assos
                .filter(asso => this.selectedCampus[asso.campus])
                .filter(asso => this.past || !asso.end || asso.end > new Date().getFullYear());
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
                        <Switch v-model="selectedCampus[campus]" />
                    </label>
                </template>
            </div>
            <div>
                <label>
                    Afficher les anciennes associations
                    <Switch v-model="past" class="switch" />
                </label>
            </div>
        </article>
        <article v-if="assos.length == 0">
            <h2>Aucune association</h2>
            <p>Revenez plus tard.</p>
        </article>
        <article v-else>
            <h2>Associations</h2>
            <div class="assos">
                <AssoPreview v-for="asso in filteredAssos" :key="asso.id" :asso="asso">
                    <img :src="asso.logos?.[0]" width="200" height="200">
                    <h3>{{ asso.names?.[0] }}</h3>
                    {{ asso.theme }}
                </AssoPreview>
                <span v-for="i in new Array(10)"></span>
            </div>
        </article>
    </section>
</template>

<style scoped lang="scss">
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

.assos {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;

    > :empty {
        flex: 200px 1 1;
        margin: 0 1em;
    }
}
</style>