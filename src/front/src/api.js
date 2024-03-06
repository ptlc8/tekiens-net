const baseUrl = import.meta.env.VITE_BASE_URL ?? "";

const Api = {
    assos: {
        get(params={}) {
            return sendApiRequest("GET", "assos", params, "Getting assos")
                .then(assos => assos.map(parseAsso));
        },
        getOne(id) {
            return sendApiRequest("GET", "assos/" + encodeURIComponent(id), {}, "Getting asso " + id)
                .then(parseAsso);
        },
        getEvents(id, params={}) {
            return sendApiRequest("GET", "assos/" + encodeURIComponent(id) + "/events", params, "Getting asso " + id + " events")
                .then(events => events.map(parseEvent));
        },
        update(id, asso, session=localStorage.getItem("session")) {
            return sendApiRequest("PUT", "assos/" + encodeURIComponent(id), { ...asso, session }, "Updating asso " + id);
        },
    },
    events: {
        get(params={}) {
            return sendApiRequest("GET", "events", params, "Getting events")
                .then(events => events.map(parseEvent));
        },
        getOne(id) {
            return sendApiRequest("GET", "events/" + encodeURIComponent(id), {}, "Getting event " + id)
                .then(parseEvent);
        },
        update(id, event, session=localStorage.getItem("session")) {
            return sendApiRequest("PUT", "events/" + encodeURIComponent(id), { ...event, session }, "Updating event " + id);
        },
        create(event, session=localStorage.getItem("session")) {
            return sendApiRequest("POST", "events", { ...event, session }, "Adding event");
        },
        delete(id, session=localStorage.getItem("session")) {
            return sendApiRequest("DELETE", "events/" + encodeURIComponent(id), { session }, "Deleting event " + id);
        }
    },
    sessions: {
        async create(assoId, password) { //authentificate the user and return a session id if success
            //the user call the api to get a challenge
            let challenge = await sendApiRequest("POST", "sessions", { asso: assoId }, "Challenge session"); 

            let hash_password = await hash(password);
            
            let hash_challenge = await hash(challenge + hash_password);

            //the user send the hash of the challenge and the password
            return await sendApiRequest("POST", "sessions", { asso: assoId, hash: hash_challenge }, "Creating session");

        },
        getOne(id) {
            return sendApiRequest("GET", "sessions/" + encodeURIComponent(id), {}, "Getting session");
        },
        delete(id) {
            return sendApiRequest("DELETE", "sessions/" + encodeURIComponent(id), {}, "Deleting session");
        }
    }
};


function parseAsso(asso) {
    if (asso.logos)
        asso.logos = asso.logos.map(logo => baseUrl + logo);
    return asso;
}

function parseEvent(event) {
    if (event.poster)
        event.poster = baseUrl + event.poster;
    return event;
}


function sendApiRequest(method, endpoint, parameters={}, message=undefined) {
    return new Promise(function (resolve, reject) {
        if (message !== undefined) {
            console.info("[API] " + message);
        }
        var urlParameters = Object.entries(parameters)
            .filter(([_, v]) => v !== undefined)
            .map(([k, v]) =>
                v instanceof Array ?
                    v.map(i => k + "[]=" + encodeURIComponent(i)).join("&")
                : v instanceof Date ?
                    k + "=" + encodeURIComponent(v.toISOString())
                : v === null ?
                    k + "="
                :
                    k + "=" + encodeURIComponent(v)
            ).join("&");
        var options = { method };
        if (method == "GET") {
            endpoint += "?" + urlParameters;
        } else {
            options.body = urlParameters;
            options.headers = { "Content-Type": "application/x-www-form-urlencoded" };
        }
        fetch(baseUrl + "/api/" + endpoint, options)
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

//a function to hash a string with sha256 and return the hash in hex
async function hash(string) {
    const sourceBytes = new TextEncoder().encode(string);
    const disgest = await crypto.subtle.digest("SHA-256", sourceBytes);
    const hash = Array.from(new Uint8Array(disgest)).map(b => b.toString(16).padStart(2, "0")).join(""); 
    return hash;
}

export default Api;