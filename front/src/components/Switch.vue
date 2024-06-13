<template>
    <span class="switch" @click="toggle" :class="{ 'checked': checked }" tabindex="0">
        <span class="slider"></span>
    </span>
</template>

<script>
export default {
    props: {
        modelValue: {
            type: Boolean,
            default: false
        }
    },
    emits: ['update:modelValue'],
    data() {
        return {
            checked: this.modelValue
        };
    },
    watch: {
        modelValue(value) {
            this.checked = value;
        }
    },
    methods: {
        toggle() {
            this.checked = !this.checked;
            this.$emit('update:modelValue', this.checked);
        }
    }
};
</script>

<style scoped lang="scss">
.switch {
    display: inline-block;
    position: relative;
    width: 2em;
    height: 1.15em;
    background-color: #ccc;
    border-radius: 1.15em;
    transition: background-color .3s;
    vertical-align: text-bottom;

    .slider {
        position: absolute;
        cursor: pointer;
        left: .075em;
        top: .075em;
        width: 1em;
        bottom: .075em;
        background-color: #fff;
        border-radius: 50%;
        transition: left .3s;
    }

    &.checked {
        background-color: var(--accent-color);

        .slider {
            left: 0.925em;
            left: calc(100% - 1.075em);
        }

    }
}
</style>
