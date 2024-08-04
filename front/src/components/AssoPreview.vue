<script>
export default {
    props: {
        asso: {
            type: Object,
            required: true
        }
    }
};
</script>

<template>
    <RouterLink :to="'/assos/' + encodeURIComponent(asso.id)" class="asso" :style="{ '--accent-color': asso.color }">
        <img :src="asso.logos?.[0]" width="200" height="200" />
        <h3>{{ asso.names?.[0] }}</h3>
        {{ asso.theme }}
    </RouterLink>
</template>

<style scoped lang="scss">
.asso {
    width: 200px;
    flex: 200px 1 0;
    max-width: calc(50% - 2em);
    margin: 0.5em;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5em;
    border-radius: 4px;
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, .1);
    text-decoration: none;
    text-align: center;
    background-color: white;

    img {
        object-fit: contain;
        width: 100%;
        aspect-ratio: 1;
        height: auto;
    }
}
</style>