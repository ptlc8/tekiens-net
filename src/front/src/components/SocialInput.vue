<script>
const socials = [
    { name: 'Site web', value: 'web', placeholder: 'tekiens.net' },
    { name: 'Telegram', value: 'telegram', placeholder: '+wtd86pl51' },
    { name: 'Twitter', value: 'twitter', placeholder: 'Tekiens' },
    { name: 'Discord', value: 'discord', placeholder: 'ml51rbn113' },
    { name: 'Instagram', value: 'instagram', placeholder: 'super_asso' },
    { name: 'Email', value: 'email', placeholder: 'contact@tekiens.net' },
    { name: 'Page de liens', value: 'links', placeholder: 'tekiens.net/links' },
    { name: 'Facebook', value: 'facebook', placeholder: 'profile.php?id=518651113' },
    { name: 'LinkedIn', value: 'linkedin', placeholder: 'company/tekiens' }
];

export default {
    setup() {
        return { socials };
    },
    props: {
        modelValue: {
            type: String,
            default: 'web:'
        }
    },
    data() {
        return {
            social: this.modelValue.split(':')[0],
            value: this.modelValue.substring(this.modelValue.indexOf(':') + 1)
        };
    },
    watch: {
        modelValue() {
            this.social = this.modelValue.split(':')[0];
            this.value = this.modelValue.substring(this.modelValue.indexOf(':') + 1);
        },
        social(social) {
            this.$emit('update:modelValue', social + ':' + this.value);
        },
        value(value) {
            this.$emit('update:modelValue', this.social + ':' + value);
        }
    }
}
</script>

<template>
    <select v-model="social">
        <option v-for="social in socials" :value="social.value">{{ social.name }}</option>
    </select>
    <input v-model="value" type="text" :placeholder="socials[social]?.placeholder" />
</template>