<script>
export default {
    props: {
        modelValue: {
            type: String,
            default: null
        },
        placeholder: {
            type: String,
            default: null
        }
    },
    emits: ['update:modelValue'],
    data() {
        return {
            dragging: false
        }
    },
    computed: {
        value: {
            get() {
                return this.modelValue;
            },
            set(value) {
                this.$emit('update:modelValue', value);
            }
        }
    },
    methods: {
        click() {
            this.$refs.input.click();
        },
        onChange(e) {
            const file = e.target.files[0];
            if (!file)
                return;
            const reader = new FileReader();
            reader.onload = e => this.value = e.target.result;
            reader.readAsDataURL(file);
        },
        onDrop(e) {
            this.dragging = false;
            const file = e.dataTransfer.files[0];
            if (!file)
                return;
            const reader = new FileReader();
            reader.onload = e => this.value = e.target.result;
            reader.readAsDataURL(file);
        },
        clear() {
            this.value = null;
        },
        reset() {
            this.value = this.placeholder;
        }
    }
};
</script>

<template>
    <div @click="click" @keyup.space.prevent="click" @drop.prevent="onDrop" @dragover.prevent @dragenter.prevent.stop="dragging = true" @dragleave.stop="dragging = false" :class="{ dragging, 'image-input': true }" tabindex="0">
        <input ref="input" v-bind="$attrs" @change="onChange" type="file" accept="image/*" />
        <img v-if="value" :src="value" width="200" height="200" />
        <span v-else>Sélectionnez ou glissez une image</span>
        <div class="buttons">
            <button v-if="value" @click.stop="clear">Supprimer</button>
            <button v-if="placeholder && value != placeholder" @click.stop="reset">Annuler</button>
        </div>
    </div>
</template>

<style scoped lang="scss">
.image-input {
    width: 100%;
    display: flex;
    min-height: 8em;
    justify-content: center;
    align-items: center;
    position: relative;
    border-radius: 4px;
    padding: 2px;
    box-shadow: 0 0 10px 2px #0000001a;
    margin-bottom: 10px;
    background-color: #fff;
    color: #404040;
    cursor: pointer;

    input[type=file] {
        display: none;
    }

    img {
        width: 100%;
        height: 200px;
        object-fit: contain;
    }

    &.dragging {
        border: 2px dashed #ccc;
        padding: 0;
    }

    .buttons {
        position: absolute;
        top: 0;
        right: 0;
        width: auto;
        margin: .5em;
    }
}
</style>