<template>
    <div class="item">
        <h2 @click="$emit('movie-selected', movie.id)">{{movie.title}}</h2>
        <h2 v-if="display">
            <font-awesome-icon icon="trash" @click="$emit('movie-delete', movie.id)"/>
            &nbsp;
            <font-awesome-icon icon="edit" @click="$emit('movie-edit', movie.id)"/>
        </h2>
    </div>
</template>

<script>
export default ({
    name: "MovieItem",
    props: ['movie', 'display']
})
</script>

<style scoped>
    .item {
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
    }
    h2 {
        padding: 0;
        margin: 0;
        cursor: pointer;
    }
</style>
