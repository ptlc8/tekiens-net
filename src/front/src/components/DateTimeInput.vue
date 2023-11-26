<script>
export default {
    props: {
        modelValue: Date
    },
    emits: ['update:modelValue'],
    computed: {
        value: {
            get() {
                if (!this.modelValue)
                    return '';
                return this.modelValue.toLocaleString("sv-SE", { timeZone: 'Europe/Paris' });
            },
            set(value) {
                this.$emit('update:modelValue', this.fromLocaleISOString(value, 'Europe/Paris'));
            }
        }
    },
    methods: {
        fromLocaleISOString(isoDate, timeZone) {
            let localeDate = new Date(isoDate + 'Z');
            let offset = this.getGMTOffset(timeZone);
            let date = new Date(localeDate.toGMTString().replace('GMT', offset));
            if (this.getGMTOffset(timeZone, date) !== offset) {
                offset = this.getGMTOffset(timeZone, date);
                date = new Date(localeDate.toGMTString().replace('GMT', offset));
            }
            return date;
        },
        getGMTOffset(timeZone, date = new Date()) {
            return Intl.DateTimeFormat("US-en", { timeZoneName:"short", timeZone }).formatToParts(date).find((i) => i.type === "timeZoneName").value;
        }
    }
};
</script>

<template>
    <input v-bind="$attrs" :value="value" @focusout="e => value = e.target.value" type="datetime-local" />
</template>