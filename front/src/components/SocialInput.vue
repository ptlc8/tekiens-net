<script>
import Api from '../api';

var socials = [];
Api.socials.get()
    .then(s => socials = s);

export default {
    props: {
        modelValue: {
            type: Object,
            default: () => ({ id: 'web', value: '' })
        }
    },
    emits: ['update:modelValue'],
    setup() {
        return { socials };
    },
    data() {
        return {
            socialId: this.modelValue.id,
            value: this.modelValue.value
        };
    },
    watch: {
        modelValue() {
            this.socialId = this.modelValue.id;
            this.value = this.modelValue.value;
        },
        socialId(socialId) {
            this.$emit('update:modelValue', { id: socialId, value: this.value });
        },
        value(value) {
            this.$emit('update:modelValue', { id: this.socialId, value });
        }
    }
}
</script>

<template>
    <select v-model="socialId">
        <option v-for="s, sId in socials" :key="sId" :value="sId">{{ s.name }}</option>
    </select>
    <input v-model="value" type="text" :placeholder="socials[socialId]?.placeholder" />
    <a target="_blank" :href="socials[socialId]?.link?.replace('{0}', value)">Tester</a>
</template>