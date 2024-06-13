<template>
    <section :class="{ nyan: Math.random() < 0.4 }">
        <article>
            <h2>Page inexistante : 404</h2>
        </article>
    </section>
</template>

<style lang="scss" scoped>
section {
    flex: 1;
    background: url('/assets/fintz-colere.webp') no-repeat center/cover;
    
    &.nyan {
        background-image: url('/assets/nyan-cat.gif');
    }

    h2 {
        text-align: center;
        color: #000;
        text-shadow: 2px 2px #fff;
    }
}
</style>