import { defineStore } from 'pinia';
import Api from '../api';
import { ref, watch } from 'vue';

async function getSession(id) {
    if (!id) return null;
    const session = await Api.sessions.getOne(localStorage.getItem("session"));
    session.asso = await Api.assos.getOne(session.asso_id);
    return session;
}

export const useSessionStore = defineStore('session', () => {
    const sessionId = ref(undefined);
    const session = ref(undefined);

    watch(sessionId, async (id, oldId) => {
        if (id) {
            localStorage.setItem("session", id);
            session.value = await getSession(id);
        } else {
            localStorage.removeItem("session");
            session.value = null;
        }
        if (oldId)
            Api.sessions.delete(oldId);
    });

    sessionId.value = localStorage.getItem("session");

    return { sessionId, session };
});