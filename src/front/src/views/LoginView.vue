<script>
import Api from "../api";
import { useSessionStore } from "../stores/session";

export default {
    setup() {
        var sessionStore = useSessionStore();
        return { sessionStore };
    },
    data() {
        return {
            asso: "",
            password: "",
            error: ""
        }
    },
    methods: {
        login() {
            Api.sessions.create(this.asso, this.password).then(session => {
                this.sessionStore.sessionId = session.id;
                this.$router.push(this.$route.query.redirect ?? '/');
            }).catch(error => {
                this.error = error;
            });
        }
    }
}
</script>

<template>
    <section>
        <form class="login" @submit.prevent="login">
            <h2>Connexion</h2>
            <input type="text" v-model="asso" placeholder="Id de l'association" autocomplete="username" />
            <input type="password" v-model="password" placeholder="Mot de passe" autocomplete="current-password" />
            <button>Se connecter</button>
            <span class="error">{{ error }}</span>
        </form>
    </section>
</template>

<style scoped lang="scss">
.login {
    align-items: center;

    input, button {
        width: 24em;
        max-width: 100%;
    }

    .error {
        color: red;
    }
}
</style>