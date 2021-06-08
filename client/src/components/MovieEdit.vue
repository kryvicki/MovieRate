<template>
    <div>
        <div v-if="errors.length">
            <h4 class="errors">Correct the following errors:</h4>
            <ul>
                <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </div>
        <p class="input-row">
            <label for="title">Title:</label><br/>
            <input type="text" placeholder="title" id="title" v-model="localMovie.title">
        </p>
        <p class="input-row">
            <label for="description">Description:</label><br/>
            <textarea id="description" placeholder="description" v-model="localMovie.description"></textarea>
        </p>
        <p class="input-row">
            <label for="description">Genres:</label><br/>
            <select v-model="selectedGenres" multiple>
                <option v-for="genre in genres" :key="genre.id" :value="genre">{{genre.name}}</option>
            </select>
        </p>
        
        <button @click="saveMovie()" class="custom-btn btn-logout black">Save Movie</button>
    </div>
</template>

<script>
    export default ({
        name: "MovieEdit",
        props: ['movie', 'token', 'genres'],
        data() {
            return {
                localMovie: {...this.movie},
                selectedGenres: [],
                errors: []
            } 
        },
        watch: {
            movie: function(newValue, oldValue) {
                if (newValue !== oldValue) {
                    this.localMovie = {...this.movie}
                }
            }
        },
        methods: {
            saveMovie() {
                if (!this.checkForm()) {
                    return
                }
                if (this.movie.id) {
                    fetch(`http://127.0.0.1:8000/core/movies/${this.movie.id}/`, {
                        method: 'put',
                        headers: {
                            'Content-Type' : 'application/json',
                            'authorization': `Token ${this.token}`
                        },
                        body: JSON.stringify({title: this.localMovie.title, 
                                            description: this.localMovie.description, 
                                            genres: this.selectedGenres})
                        
                    })
                    .then(() => {
                        this.$emit('updated');
                    })
                    .catch(error => console.log(error))
                } else {
                    fetch(`http://127.0.0.1:8000/core/movies/`, {
                        method: 'post',
                        headers: {
                            'Content-Type' : 'application/json',
                            'authorization': `Token ${this.token}`
                        },
                        body: JSON.stringify({title: this.localMovie.title, 
                                            description: this.localMovie.description, 
                                            genres: this.selectedGenres})
                        
                    })
                    .then(() => {
                        this.$emit('updated');
                    })
                    .catch(error => console.log(error))
                }
            },
            checkForm() {
                if(this.localMovie.title && this.localMovie.description && this.selectedGenres.length) 
                    return true;

                this.errors = [];
                if(!this.localMovie.title) 
                    this.errors.push("Title is required.");
                if(!this.localMovie.description) 
                    this.errors.push("Description is required.");
                if(!this.selectedGenres.length) 
                    this.errors.push("Select at least one genre.");

                return false;
            }
        },
        created() {
            if (this.localMovie.id > 0) {
                this.selectedGenres = this.localMovie.genres;
            }
        }
    })
</script>
<style scoped>
    h3 {
        margin: 1rem 0rem;
    }
    .black {
        font-size: 15px;
        margin: 1rem 0rem;
    }
    .pointer {
        cursor: pointer;
    }
    .input-row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0rem;
    }
    input, select, textarea {
        width: 50%;
        padding: 0.2rem 0.5rem;
        border: 1px solid black;
        background-color: white;
    }
    .errors {
        margin-bottom: 1rem;
    }

</style>
