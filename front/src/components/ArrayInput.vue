<script>
export default {
    props: {
        modelValue: {
            type: Array,
            default: () => []
        },
        placeholder: {
            type: Array,
            default: null
        },
        name: undefined,
        default: undefined
    },
    emits: ['update:modelValue'],
    data() {
        return {
            values: this.modelValue
        };
    },
    methods: {
        add() {
            this.values.push(this.default);
        },
        remove(index) {
            this.values.splice(index, 1);
        },
        moveUp(index) {
            if (index == 0) return;
            const value = this.values[index];
            this.values.splice(index, 1);
            this.values.splice(index - 1, 0, value);
        },
        moveDown(index) {
            if (index == this.values.length - 1) return;
            const value = this.values[index];
            this.values.splice(index, 1);
            this.values.splice(index + 1, 0, value);
        }
    },
    watch: {
        values: {
            handler(values) {
                this.$emit('update:modelValue', values);
            },
            deep: true
        },
        modelValue: {
            handler(modelValue) {
                this.values = modelValue;
            },
            deep: true
        }
    }
}
</script>

<template>
    <div class="array-input" tabindex="0">
        <template v-for="_, index in values" :key="index">
            <div class="value">
                <slot :value="values[index]" :placeholder="placeholder ? placeholder[index] : null" :on-input="e => values[index] = e.target.value" :on-update="v => values[index] = v"></slot>
                <button type="button" @click="moveUp(index)" v-if="index != 0" title="Déplacer vers le haut">⬆</button>
                <button type="button" @click="moveDown(index)" v-if="index != values.length - 1" title="Déplacer vers le bas">⬇</button>
                <button type="button" @click="remove(index)" title="Supprimer">✖</button>
            </div>
        </template>
        <button type="button" @click="add()" title="Ajouter">✚</button>
    </div>
</template>

<style scoped lang="scss">
.array-input {
    display: flex;
    flex-direction: column;
    border-radius: 4px;
    padding: 4px 8px;
    box-shadow: 0 0 10px 2px #0000001a;
    margin-bottom: 10px;
    background-color: #fff;

    .value {
        display: flex;
        gap: .5em;

        button {
            flex: 1;
        }
    }
}
</style>