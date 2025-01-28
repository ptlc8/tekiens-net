<script>
import Api from '../api';
import { useSessionStore } from '../stores/session';
import ArrayInput from '../components/ArrayInput.vue';

export default {
    components: {
        ArrayInput
    },
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
            presets: [],
            usePresets: true,
            presetRecipients: [""],
            customRecipients: [""]
        }
    },
    computed: {
        mightShowSendModal() {
            const session = this.sessionStore.session;
            const event = this.events.find(e => e.id == this.selectedEventId);
            return session != null && event != undefined && session.asso_id == event.asso_id;
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
            const recipients = this.usePresets ? this.presetRecipients : this.customRecipients
            if (recipients.length == 0) {
                e.preventDefault()
                this.sendEmailError = "Au moins une addresse email requise"
                return
            }
            Api.templates.send(this.selectedTemplate, this.selectedEventId, recipients)
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
            view.presets = emails;
        })).catch(error => next(view => view.$state.error = error));
    }
}
</script>

<template>
    <section>
        <dialog ref="sendDialog">
            <form method="dialog" @submit="sendEmail">
                <div class="buttons tabs">
                    <button type="button" :aria-current="usePresets" @click="usePresets = true">Groupe CYU</button>
                    <button type="button" :aria-current="!usePresets" @click="usePresets = false">Personnalisé</button>
                </div>
                <div v-if="usePresets">
                    <label for="preset">Envoyer à des groupes CYU</label>
                    <ArrayInput no-order v-model="presetRecipients" v-slot="{ onInput, value }" id="preset">
                        <select @input="onInput" :value="value" required>
                            <option v-for="email in presets" :key="email.email" :value="email.email">{{ email.name }}</option>
                        </select>
                    </ArrayInput>
                </div>
                <div v-else>
                    <label for="custom">Adresses personnalisées</label>
                    <ArrayInput no-order v-model="customRecipients" v-slot="{ onInput, value }" id="custom">
                        <input @input="onInput" :value="value" type="email" required placeholder="foo.bar@example.com" />
                    </ArrayInput>
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

.error {
    color: red;
}
</style>