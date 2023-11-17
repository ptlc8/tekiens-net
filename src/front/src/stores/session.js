import { defineStore } from 'pinia';
import Api from '../api';
import { ref } from 'vue';

async function getSession(id) {
    if (!id) return null;
    const session = await Api.sessions.getOne(localStorage.getItem("session"));
    session.asso = await Api.assos.getOne(session.asso_id);
    return session;
}

export const useSessionStore = defineStore('session', () => {
    const sessionId = ref(undefined);
    const session = ref(undefined);
    
    async function setSessionId(id) {
        sessionId.value = id;
        if (id) {
            localStorage.setItem("session", id);
            session.value = await getSession(id);
        } else {
            localStorage.removeItem("session");
            session.value = null;
        }
    }

    setSessionId(localStorage.getItem("session"));

    return { sessionId, session, setSessionId };
});