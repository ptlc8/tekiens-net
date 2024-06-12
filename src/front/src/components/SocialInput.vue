<script>
import Api from '../api';

var socials = [];
Api.socials.get()
    .then(s => socials = s);

export default {
    setup() {
        return { socials };
    },
    props: {
        modelValue: {
            type: Object,
            default: () => ({ id: 'web', value: '' })
        }
    },
    data() {
        return {
            social: this.modelValue.id,
            value: this.modelValue.value
        };
    },
    watch: {
        modelValue() {
            this.social = this.modelValue.id;
            this.value = this.modelValue.value;
        },
        social(social) {
            this.$emit('update:modelValue', { id: social, value: this.value });
        },
        value(value) {
            this.$emit('update:modelValue', { id: this.social, value });
        }
    }
}
</script>

<template>
    <select v-model="social">
        <option v-for="social, socialId in socials" :value="socialId">{{ social.name }}</option>
    </select>
    <input v-model="value" type="text" :placeholder="socials[social]?.placeholder" />
    <a target="_blank" :href="socials[social]?.link?.replace('{0}', value)">Tester</a>
</template>