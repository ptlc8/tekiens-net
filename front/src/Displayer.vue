<script>
import Api from './api';
import QRCode from './components/QRCode.vue';
import { getEventStatus } from './eventStatus';

const EVENT_DURATION = 10_000;
const UPDATE_TIMEOUT = 60 * 1_000;
const RELOAD_TIMEOUT = 60 * 60 * 1_000;
const baseUrl = import.meta.env.VITE_BASE_URL ?? '';

export default {
    components: { QRCode },
    setup() {
        return {
            EVENT_DURATION
        };
    },
    data() {
        return {
            assos: {},
            events: [],
            eventIndex: 0,
            timers: []
        };
    },
    computed: {
        event() {
            return this.events[this.eventIndex];
        },
        asso() {
            return this.assos[this.event?.asso_id];
        },
        date() {
            let date = new Date(this.event.date + 'Z');
            let now = new Date();
            if (now.getDate() == date.getDate() && now.getMonth() == date.getMonth() && now.getFullYear() == date.getFullYear())
                return 'Aujourd\'hui';
            var tomorrow = new Date();
            tomorrow.setDate(now.getDate() + 1);
            if (tomorrow.getDate() == date.getDate() && tomorrow.getMonth() == date.getMonth() && tomorrow.getFullYear() == date.getFullYear())
                return 'Demain';
            return date.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
        },
        time() {
            return new Date(this.event.date + 'Z').toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }).replace(':', 'h');
        },
        duration() {
            if (!this.event.duration)
                return undefined;
            var days = Math.floor(this.event.duration / 60 / 24);
            var hours = Math.floor(this.event.duration / 60 % 24);
            var minutes = this.event.duration % 60;
            return `${days}j ${hours}h ${minutes}min`.replace(/0j /, '').replace(/0h /, '').replace(/ 0min/, '');
        },
        status() {
            return getEventStatus(this.event);
        },
        color() {
            return this.event?.color ?? this.asso?.color ?? "ffffff";
        },
        textColor() {
            return this.calcLuminance(this.color) > 0.25 ? '#000000' : '#ffffff';
        },
        link() {
            if (this.event.link)
                return this.event.link;
            return location.origin + baseUrl + '/events/' + this.event.id;
        }
    },
    methods: {
        async update() {
            this.assos = (await Api.assos.get()).reduce((acc, asso) => {
                acc[asso.id] = asso;
                return acc;
            }, {});
            this.events = await Api.events.get({ after: new Date() });
            this.events.push({
                id: -1,
                title: 'Ajoutez vos événements sur tekiens.net pour qu\'ils s\'affichent ici',
                place: location.host + baseUrl,
                link: location.origin + baseUrl + '/login',
                access: 'Réservé aux associations',
                color: '#ef6c00'
            });
        },
        next() {
            this.eventIndex = this.eventIndex >= this.events.length - 1 ? 0 : this.eventIndex + 1;
        },
        previous() {
            this.eventIndex = this.eventIndex <= 0 ? this.events.length - 1 : this.eventIndex - 1;
        },
        calcLuminance(hex) {
            let rgb = parseInt('0x' + hex.replace('#', ''));
            let r = (rgb & 0xff0000) >> 16;
            let g = (rgb & 0xff00) >> 8;
            let b = (rgb & 0xff);
            return (r * 0.299 + g * 0.587 + b * 0.114) / 256;
        }
    },
    mounted() {
        this.update();
        this.timers.push(setInterval(this.update, UPDATE_TIMEOUT));
        this.timers.push(setInterval(this.next, EVENT_DURATION));
        this.timers.push(setTimeout(() => window.location.reload(), RELOAD_TIMEOUT));
    },
    beforeUnmount() {
        for (let timer of this.timers)
            clearInterval(timer);
    }
};
</script>

<template>
    <section @keyup.right="next" @keyup.left="previous" @click.left="next" @click.right.prevent="previous" tabindex="0">
        <TransitionGroup name="fade" tag="div" class="events">
            <article v-if="event" :key="event.id" class="event" :style="{ backgroundColor: color, color: textColor }">
                <h1>{{ event.title }}</h1>
                <div class="main">
                    <img v-if="event.poster" class="poster" :src="event.poster" />
                    <div class="details">
                        <span v-if="asso" class="asso">
                            <img class="logo" :src="asso?.logos?.[0]" />
                            {{ asso?.names?.[0] }}
                        </span>
                        <span v-if="event.date">📅 {{ date }} à {{ time }}</span>
                        <span v-if="event.place">📍 {{ event.place }}</span>
                        <span v-if="event.price">💲 {{ event.price }}</span>
                        <span v-if="event.duration">🕓 {{ duration }}</span>
                        <span v-if="event.access">🔒 {{ event.access }}</span>
                        <span v-if="event.capacity">👥 {{ event.capacity }} places</span>
                        <span v-if="event.status">{{ status }}</span>
                        <QRCode v-if="event.link" class="qr-code" :value="event.link" />
                    </div>
                </div>
            </article>
        </TransitionGroup>
        <div class="progress" :style="{ backgroundColor: color }">
            <div class="progress-bar" :style="{ animationDuration: EVENT_DURATION + 'ms' }"></div>
            <span class="progress-value">{{ eventIndex + 1 + "/" + events.length }}</span>
        </div>
    </section>
</template>

<style lang="scss" scoped>
section {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 0;
    font-size: 1.25vmin;
    cursor: none;
}

.events {
    flex: 1;
    position: relative;
    overflow: hidden;
    padding: 2%;

    .event {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-size: 2em;
        transition: opacity ease .5s, transform ease .5s;
        transform: translate(0);
        opacity: 1;

        h1 {
            text-align: center;
            font-size: 2em;
            margin: .5em
        }

        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1em;

            .poster {
                width: 16em;
                height: 28em;
                object-fit: contain;
                filter: drop-shadow(0 0 1em rgba(0, 0, 0, .5));
            }
        
            .details {
                display: flex;
                flex-direction: column;
                gap: .2em;
                font-size: 1.2em;
            }
        
            .asso {
                font-size: 1.4em;

                .logo {
                    max-height: 2em;
                    max-width: 3em;
                    vertical-align: middle;
                }
            }
        
            .qr-code {
                width: 100%;
                height: 8em;
            }
        }

        &.fade-enter-active, &.fade-leave-active {
            opacity: 1;
        }
        &.fade-enter-from, &.fade-leave-to {
            opacity: 0;
        }

        &.up-enter-active, &.up-leave-active {
            transform: translateY(0);
        }
        &.up-enter-from {
            transform: translateY(100%);
        }
        &.up-leave-to {
            transform: translateY(-100%);
        }
    }
}

.progress {
    height: 3em;
    position: relative;
    mix-blend-mode: difference;
    background: white;
    z-index: 10;
    transition: background-color ease .5s;

    .progress-bar {
        height: 100%;
        background: white;
        mix-blend-mode: difference;
        filter: invert(.75);
        animation: progress-bar linear 10s infinite;
    }

    .progress-value {
        position: absolute;
        right: 0;
        top: 0;
        font-size: 1.6em;
        margin: .2em;
        line-height: 1;
    }
}

@keyframes progress-bar {
    0% {
        width: 0%;
    }

    100% {
        width: 100%;
    }
}</style>