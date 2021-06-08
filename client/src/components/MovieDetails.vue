<template>
    <div>
        <h2>{{movie.title}}</h2>
        <p class="description">{{movie.description}}</p>
        <div class="genres-container">
            <span v-for="genre in movie.genres" :key="genre.id" class="genre">{{genre.name}}</span>
        </div>
        <button type="button" v-if="isAdmin" class="collapsible" @click="open = !open">Rental Certificate</button>
        <div class="content" :class="[open ? 'display-block' : 'display-none']">
            <RentalCertificate v-if="isAdmin" :token="token" :movie="movie"/>
        </div>
        <div class="mb-2"></div>
        <font-awesome-icon icon="star" :class="[movie.average_rating > 0 ? 'orange' : '']"/>
        <font-awesome-icon icon="star" :class="[movie.average_rating > 1 ? 'orange' : '']"/>
        <font-awesome-icon icon="star" :class="[movie.average_rating > 2 ? 'orange' : '']"/>
        <font-awesome-icon icon="star" :class="[movie.average_rating > 3 ? 'orange' : '']"/>
        <font-awesome-icon icon="star" :class="[movie.average_rating > 4 ? 'orange' : '']"/>
        ({{movie.ratings_amount}})

        <hr>
        <h2>Rate it!</h2>
        <font-awesome-icon icon="star" class="bigger"
            v-for=" star in stars" :key="star"
            :class="[highlighted > star - 1 ? 'red' : '']"
            @mouseenter="highlighted = star"
            @mouseleave="highlighted = -1"
            @click="ratingSelected(star)"
        />
    </div>
</template>

<script>
import RentalCertificate from './RentalCertificate.vue'

export default ({
    name: "MovieDetails",
    components: {
        RentalCertificate
    },
    props: ['movie', 'token', 'isAdmin'],
    data() {
        return {
            stars: [0,1,2,3,4],
            highlighted: 4,
            open: false
        }
    },
    methods: {
        ratingSelected(rate) {
            fetch(`http://127.0.0.1:8000/core/movies/${this.movie.id}/rate_movie/`, {
            method: 'post',
            headers: {
                'Content-Type' : 'application/json',
                'authorization': `Token ${this.token}`
            },
            body: JSON.stringify({stars: rate + 1})
        })
        .then(res => res.json())
        .then(res => {
            this.$emit('updated');
            console.log(res);
        })
        .catch(error => console.log(error))
        },
    }
})
</script>

<style scoped>
    hr {
        margin: 1rem;
        background-color: #9c1a38;
    }
    h2 {
        margin-bottom: 1rem;
    }
    .description {
        text-align: start;
        padding: 0.5rem;
    }
    .orange {
        color: #974f60;
    }
    .red {
        color: #9c1a38;
    }
    .bigger {
        font-size: 2rem;
    }
    .genres-container {
        margin: 1.5rem 0.5rem;
        display: flex;
        height: 100%;
        flex-wrap: wrap;
    }
    .genre {
        padding: 0.8rem 0.3rem;
        margin: 0.3rem;
        color: #9c1a38;
        border: 1px solid #9c1a38;
        border-radius: 5px;
    }
    .collapsible {
        background-color: transparent;
        border: 1px solid black;
        color: black;
        cursor: pointer;
        padding: 1rem;
        margin: 0rem 0.5rem;
        width: 100%;
        text-align: left;
        outline: none;
        font-size: 15px;
    }

    .content {
        padding: 0 1rem;
        display: none;
        overflow: hidden;
        border: 1px solid black;
        margin: 0rem 0.5rem;
        width: 100%;
        background-color: white;
    }

    .mb-2 {
        margin-bottom: 2rem;
    }

    .display-none {
        display: none;
    }

    .display-block {
        display: block;
    }
</style>
