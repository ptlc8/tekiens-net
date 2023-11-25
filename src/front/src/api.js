const baseUrl = import.meta.env.VITE_BASE_URL ?? '';
const Api = {
    assos: {
        get: function (params={}) {
            return sendApiRequest("GET", "assos", params, "Getting assos");
        },
        getOne: function (id) {
            return sendApiRequest("GET", "assos/" + encodeURIComponent(id), {}, "Getting asso " + id);
        },
        getEvents: function (id, params={}) {
            return sendApiRequest("GET", "assos/" + encodeURIComponent(id) + "/events", params, "Getting asso " + id + " events");
        },
        update: function (id, asso, session=localStorage.getItem("session")) {
            return sendApiRequest("PUT", "assos/" + encodeURIComponent(id), { ...asso, session }, "Updating asso " + id);
        },
    },
    events: {
        get: function (params={}) {
            return sendApiRequest("GET", "events", params, "Getting events");
        },
        getOne: function (id) {
            return sendApiRequest("GET", "events/" + encodeURIComponent(id), {}, "Getting event " + id);
        },
        update: function (id, event, session=localStorage.getItem("session")) {
            return sendApiRequest("PUT", "events/" + encodeURIComponent(id), { ...event, session }, "Updating event " + id);
        },
        create: function (event, session=localStorage.getItem("session")) {
            return sendApiRequest("POST", "events", { ...event, session }, "Adding event");
        },
        delete: function (id, session=localStorage.getItem("session")) {
            return sendApiRequest("DELETE", "events/" + encodeURIComponent(id), { session }, "Deleting event " + id);
        }
    },
    sessions: {
        create: function (assoId, password) {
            return sendApiRequest("POST", "sessions", { asso: assoId, password }, "Creating session");
        },
        getOne: function (id) {
            return sendApiRequest("GET", "sessions/" + encodeURIComponent(id), {}, "Getting session");
        }
    }
};


function sendApiRequest(method, endpoint, parameters={}, message=undefined) {
    return new Promise(function (resolve, reject) {
        if (message !== undefined) {
            console.info("[API] " + message);
        }
        var urlParameters = Object.entries(parameters)
            .filter(([_, v]) => v !== null && v !== undefined)
            .map(([k, v]) =>
                v instanceof Array ?
                    v.map(i => k + "[]=" + encodeURIComponent(i)).join("&")
                : v instanceof Date ?
                    k + "=" + encodeURIComponent(v.toISOString())
                :
                    k + "=" + encodeURIComponent(v)
            ).join("&");
        var options = { method };
        fetch(baseUrl + "/api/" + endpoint + "?" + urlParameters, options)
            .then(res => res.json())
            .then(function (response) {
                if (!response.success) {
                    console.error("[API] " + response.error);
                    reject(response.error);
                } else {
                    resolve(response.data);
                }
            })
            .catch(reject);
    });
}

export default Api;