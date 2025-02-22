import bcrypt from "bcryptjs";

export const baseUrl = import.meta.env.VITE_BASE_URL ?? "";
export const origin = import.meta.env.VITE_BACKEND_ORIGIN ?? "";

const Api = {
    assos: {
        get(params = {}) {
            return sendApiRequest("GET", "assos", params, "Getting assos")
                .then(assos => mapResponse(assos, parseAsso));
        },
        getOne(id) {
            return sendApiRequest("GET", "assos/" + encodeURIComponent(id), {}, "Getting asso " + id)
                .then(parseAsso);
        },
        getEvents(id, params = {}) {
            return sendApiRequest("GET", "assos/" + encodeURIComponent(id) + "/events", params, "Getting asso " + id + " events ")
                .then(events => mapResponse(events, parseEvent));
        },
        update(id, asso, session = localStorage.getItem("session")) {
            return sendApiRequest("PUT", "assos/" + encodeURIComponent(id), { ...unparseAsso(asso), session }, "Updating asso " + id);
        },
    },
    events: {
        get(params = {}) {
            return sendApiRequest("GET", "events", params, "Getting events")
                .then(events => mapResponse(events, parseEvent));
        },
        getOne(id) {
            return sendApiRequest("GET", "events/" + encodeURIComponent(id), {}, "Getting event " + id)
                .then(parseEvent);
        },
        update(id, event, session = localStorage.getItem("session")) {
            return sendApiRequest("PUT", "events/" + encodeURIComponent(id), { ...event, session }, "Updating event " + id);
        },
        create(event, session = localStorage.getItem("session")) {
            return sendApiRequest("POST", "events", { ...event, session }, "Adding event");
        },
        delete(id, session = localStorage.getItem("session")) {
            return sendApiRequest("DELETE", "events/" + encodeURIComponent(id), { session }, "Deleting event " + id);
        }
    },
    sessions: {
        async create(assoId, password) { //authentificate the user and return a session id if success
            //the user call the api to get a challenge

            let { challenge, salt } = await sendApiRequest("POST", "sessions", { asso: assoId }, "Challenge session");


            let hash_password = await bcrypt.hash(password, salt);

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
    },
    templates: {
        get() {
            return sendApiRequest("GET", "templates", {}, "Getting templates");
        },
        getOne(id) {
            return sendApiRequest("GET", "templates/" + encodeURIComponent(id), {}, "Getting template " + id);
        },
        getEmail(id, eventId) {
            return sendApiRequest("GET", "templates/" + encodeURIComponent(id) + "/" + encodeURIComponent(eventId), { event: eventId }, "Getting template " + id + " for event " + eventId);
        },
        send(id, eventId, recipients, session = localStorage.getItem("session")) {
            return sendApiRequest("POST", "templates/" + encodeURIComponent(id) + "/" + encodeURIComponent(eventId) + "/send", { recipients, session }, "Sending email for event " + eventId + "with template " + id);
        }
    },
    emails: {
        get() {
            return sendApiRequest("GET", "emails", {}, "Getting emails");
        }
    },
    socials: {
        get() {
            return sendApiRequest("GET", "socials", {}, "Getting socials");
        }
    },
    campus: {
        get() {
            return sendApiRequest("GET", "campus", {}, "Getting campus");
        }
    }
};


function parseAsso(asso) {
    if (asso.logos)
        asso.logos = asso.logos.map(logo => origin + baseUrl + logo);
    return asso;
}

function unparseAsso(asso) {
    if (asso.socials)
        asso.socials = asso.socials.map(social => social.id + ":" + social.value);
    return asso;
}

function parseEvent(event) {
    if (event.poster)
        event.poster = origin + baseUrl + event.poster;
    return event;
}

function mapResponse(arrayResponse, callbackfn) {
    var result = arrayResponse.map(callbackfn);
    result.count = arrayResponse.count;
    return result;
}


function sendApiRequest(method, endpoint, parameters = {}, message = undefined) {
    return new Promise(function (resolve, reject) {
        if (message !== undefined) {
            console.info("[API] " + message);
        }
        var urlParameters = Object.entries(parameters)
            .filter(([_, v]) => v !== undefined)
            .map(([k, v]) =>
                v instanceof Array ? (
                    v.length == 0 ?
                        k + "[]=%00"
                    : v.map(i => k + "[]=" + encodeURIComponent(i)).join("&")
                ) : v instanceof Date ?
                    k + "=" + encodeURIComponent(v.toISOString())
                : v === null ?
                    k + "=%00"
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
        fetch(origin + baseUrl + "/api/" + endpoint, options)
            .then(res => {
                if (res.headers.get("Content-Type") === "application/json")
                    return res.json();
                else
                    throw new Error(res.statusText);
            })
            .then(function (response) {
                if (!response.success) {
                    console.error("[API] " + response.error);
                    reject(response.error);
                } else {
                    let data = response.data;
                    if (response.count !== undefined)
                        data.count = response.count;
                    resolve(data);
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
