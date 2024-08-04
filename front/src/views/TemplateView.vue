<script>
import Api from '../api';

export default {
    data() {
        return {
            selectedTemplate: null,
            selectedEventId: null,
            templates: [],
            events: [],
            html: "",
            error: null
        }
    },
    methods: {
        refreshHTML() {
            if (this.selectedTemplate)
                Api.templates.getOne(this.selectedTemplate, this.selectedEventId)
                    .then(html => this.html = html)
                    .catch(error => this.error = error);
            else
                this.html = '';
        },
        async copyEmail() {
            var success = false;
            if (typeof navigator.clipboard.write === 'function' && window.ClipboardItem !== undefined) {
                try {
                    await navigator.clipboard.write([new window.ClipboardItem({ 'text/html': new Blob([this.html], { type: 'text/html' }) })]);
                    success = true;
                } catch {}
            }
            if (!success) { 
                var listener = e => {
                    e.clipboardData.setData("text/html", this.html);
                    e.preventDefault();
                    success = true;
                }
                document.addEventListener("copy", listener);
                document.execCommand("copy");
                document.removeEventListener("copy", listener);
            }
            if (success)
                alert('Mail copié ! Vous pouvez le coller dans votre client mail.');
            else
                alert('Impossible de copier le mail. Veuillez le copier manuellement.');
        },
        async copyHTML() {
            await navigator.clipboard.writeText(this.html);
            alert('HTML copié !');
        }
    },
    watch: {
        selectedEventId() {
            this.refreshHTML();
        },
        selectedTemplate() {
            this.refreshHTML();
        }
    },
    beforeRouteEnter(to, _from, next) {
        Promise.all([
            Api.events.get({ /*after: new Date()*/ }),
            Api.templates.get()
        ]).then(([events, templates]) => next(view => {
            view.events = events;
            view.templates = templates;
            view.selectedEventId = to.query.event ?? events[0].id;
            view.selectedTemplate = to.query.template ?? templates[0];
        })).catch(error => next(view => view.$state.error = error));
    }
}
</script>

<template>
    <section>
        <article>
            <h2>Générer un mail</h2>
            <form>
                <label for="template">Template de mail</label>
                <select v-model="selectedTemplate" id="template">
                    <option v-for="template in templates" :key="template" :value="template">Template « {{ template }} »</option>
                </select>
                <label for="event">Événement</label>
                <select v-model="selectedEventId" id="event">
                    <option v-for="event in events" :key="event.id" :value="event.id">{{ event.asso_id }} - {{ event.title }}</option>
                </select>
                <div class="buttons">
                    <button type="button" @click="copyEmail">Copier le mail</button>
                    <button type="button" @click="copyHTML">Copier le HTML</button>
                </div>
                <span v-if="error" class="error">{{ error }}</span>
            </form>
        </article>
        <article v-html="html"></article>
    </section>
</template>

<style lang="scss" scoped>
.buttons {
    display: flex;
    gap: 1em;
}
.error {
    color: red;
}
</style>