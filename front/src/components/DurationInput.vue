<script>
export default {
    props: {
        modelValue: {
            type: Number,
            default: 60
        }
    },
    emits: ['update:modelValue'],
    computed: {
        days: {
            get() {
                return this.modelValue ? Math.floor(this.modelValue / 60 / 24) : '';
            },
            set(value) {
                this.emitValue(value, this.hours, this.minutes);
            }
        },
        hours: {
            get() {
                return this.modelValue ? Math.floor(this.modelValue / 60 % 24) : '';
            },
            set(value) {
                this.emitValue(this.days, value, this.minutes);
            }
        },
        minutes: {
            get() {
                return this.modelValue ? this.modelValue % 60 : '';
            },
            set(value) {
                this.emitValue(this.days, this.hours, value);
            }
        }
    },
    methods: {
        emitValue(days, hours, minutes) {
            let value = days || hours || minutes ? days * 60 * 24 + hours * 60 + minutes * 1 : null;
            this.$emit('update:modelValue', value);
        }
    }
};
</script>

<template>
    <div class="duration-input">
        <div>
            <input v-model="days" type="number" min="0" placeholder="-" />
            <span>jour{{ days > 1 ? 's' : '' }}</span>
        </div>
        <div>
            <input v-model="hours" type="number" min="0" max="23" placeholder="-" />
            <span>heure{{ hours > 1 ? 's' : '' }}</span>
        </div>
        <div>
            <input v-model="minutes" type="number" min="0" max="59" placeholder="-" />
            <span>minute{{ minutes > 1 ? 's' : '' }}</span>
        </div>
    </div>
</template>

<style scoped lang="scss">
.duration-input {
    display: flex;
    flex-direction: row;
    gap: 1em;

    div {
        flex: 1;
        display: flex;
        align-items: center;
        border-radius: 4px;
        box-shadow: 0 0 10px 2px #0000001a;
        margin-bottom: 10px;
        background-color: #fff;
        color: #404040;

        input {
            box-shadow: none;
            margin: 0;
        }

        span {
            margin: 0 .5em;
        }
    }

    @media (max-width: 600px) {
        flex-direction: column;
        gap: 0;
    }
}
</style>