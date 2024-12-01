<script>
import Api from '../api';
import { useSessionStore } from '../stores/session';

export default {
    setup() {
        return {
            sessionStore: useSessionStore()
        }
    },
    data() {
        return {
            selectedTemplate: null,
            selectedEventId: null,
            templates: [],
            events: [],
            html: "",
            error: null,
            sendEmailError: null,
            emails: [],
            sendToPreset: true
        }
    },
    computed: {
        mightShowSendModal() {
            const session = this.sessionStore.session
            const event = this.events.find(e => e.id === this.selectedEventId)
            return session !== null && event !== undefined && session.asso_id === event.asso_id
        },
    },
    methods: {
        refreshHTML() {
            if (this.selectedTemplate && this.selectedEventId)
                Api.templates.getEmail(this.selectedTemplate, this.selectedEventId)
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
        },
        async sendEmail(e) {
            const data = new FormData(e.target)
            const preset = data.get('preset') ?? ''
            const custom = data.get('custom') ?? ''
            const email = this.sendToPreset ? preset : custom
            if (email.length === 0) {
                e.preventDefault()
                this.sendEmailError = "Addresse email requise"
                return
            }
            Api.templates.send(this.selectedTemplate, this.selectedEventId, email)
                   .then(() => alert("Mail envoyé !"))
                   .catch(() => alert("Une erreur s'est produite lors de l'envoi du mail"))
        },
        showSendModal() {
            this.$refs.sendDialog.showModal()
        },
        hideSendModal() {
            this.$refs.sendDialog.close()
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
            Api.templates.get(),
            Api.emails.get(),
        ]).then(([events, templates, emails]) => next(view => {
            view.events = events;
            view.templates = templates;
            view.selectedEventId = to.query.event ?? events[0].id;
            view.selectedTemplate = to.query.template ?? templates[0];
            view.emails = emails;
        })).catch(error => next(view => view.$state.error = error));
    }
}
</script>

<template>
    <section>
        <dialog ref="sendDialog" v-if="mightShowSendModal">
            <form method="dialog" @submit="sendEmail">
                <div class="buttons tabs">
                    <button type="button" :aria-current="sendToPreset" @click="sendToPreset = true">Groupe CYU</button>
                    <button type="button" :aria-current="!sendToPreset" @click="sendToPreset = false">Personnalisé</button>
                </div>
                <div v-show="sendToPreset">
                    <label for="preset">Envoyer à un groupe CYU</label>
                    <select id="preset" name="preset">
                        <option v-for="email in emails" :key="email.email" :value="email.email">{{ email.name }}</option>
                    </select>
                </div>
                <div v-show="!sendToPreset">
                    <label for="custom">Adresse personnalisée</label>
                    <input name="custom" id="custom" type="email" placeholder="foo.bar@example.com" />
                </div>
                <span v-if="sendEmailError" class="error">{{ sendEmailError }}</span>
                <button type="submit">Envoyer</button>
                <button type="button" @click="hideSendModal">Annuler</button>
            </form>
        </dialog>
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
                    <button type="button" @click="showSendModal" v-if="mightShowSendModal">Envoyer le mail</button>
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

.tabs.buttons button[aria-current=false] {
    background: unset;
    color: unset;
}

/* HACK: To avoid width difference beetween tabs */
dialog :is(select, input) {
    width: auto;
}
dialog :has(>:is(select, input)) {
    display: flex;
    flex-direction: column;
}
/* End of Hack */

.error {
    color: red;
}
</style>