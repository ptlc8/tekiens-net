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
                return this.iso2local(this.modelValue);
            },
            set(value) {
                console.log(this.local2iso(value));
                this.$emit('update:modelValue', this.local2iso(value));
            }
        }
    },
    methods: {
        local2iso(local) {
            return new Date(local).toLocaleString("sv-SE", {timeZone:"UTC"});
        },
        iso2local(iso) {
            return new Date(iso + 'Z').toLocaleString("sv-SE");
        }
    }
};
</script>

<template>
    <input v-bind="$attrs" :value="value" @focusout="e => value = e.target.value" type="datetime-local" />
</template>