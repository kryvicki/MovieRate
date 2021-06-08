<template>
    <div>
        <button class="custom-btn btn-logout white" @click="logout()">Logout</button>
        <div class="layout">
            <div class="box">
                <MovieItem 
                    v-for="movie in movies" 
                    :key="movie.id"
                    :movie="movie"
                    :display="isAdmin"
                    @movie-selected="movieSelected($event)"
                    @movie-delete="movieDelete($event)"
                    @movie-edit="movieEdit($event)"
                />
                <button class="custom-btn btn-logout black" v-if="isAdmin" @click="addNewMovie()">New Movie</button>
            </div>
            <div></div>
            <div class="box" v-if="selectedMovie || editedMovie">
                <MovieDetails v-if="selectedMovie" :isAdmin="isAdmin" :movie="selectedMovie" @updated="updated()" :token="token"/>
                <MovieEdit v-if="editedMovie" :movie="editedMovie" :genres="genres" @updated="updated()" :token="token"/>
            </div>
        </div>
    </div>
</template>

<script>
import MovieItem from './MovieItem'
import MovieDetails from './MovieDetails'
import MovieEdit from './MovieEdit'

export default ({
    name: "Movies",
    components: { 
        MovieItem,
        MovieDetails,
        MovieEdit
    },
    data() {
        return {
            movies: [],
            genres: [],
            selectedMovie: null,
            editedMovie: null,
            token: '',
            isAdmin: false
        }
    },
    methods: {
        movieSelected(movieId) {
            this.editedMovie = null;
            this.selectedMovie = this.movies.find(movie => movie.id === movieId);
        },
        movieDelete(movieId) {
            fetch(`http://127.0.0.1:8000/core/movies/${movieId}/`, {
                method: 'delete',
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                    'authorization': `Token ${this.token}`
                }
            })
            .then(() => {
                this.movies = this.movies.filter(movie => movie.id !== movieId);
                console.log(this.selectedMovie);
                console.log(this.editedMovie);
                if (this.selectedMovie && this.selectedMovie.id === movieId) {
                    this.selectedMovie = null;
                }
                if (this.editedMovie && this.editedMovie.id === movieId) {
                    this.editedMovie = null;
                }
            })
            .catch(error => console.log(error))
        },
        movieEdit(movieId) {
            this.selectedMovie = null;
            this.editedMovie = this.movies.find(movie => movie.id === movieId);
        },
        addNewMovie() {
            this.selectedMovie = null;
            this.editedMovie = {title: '', description: '', genres: []};
        },
        updated() {
            this.editedMovie = null;
            this.getMovies();
        },
        getMovies() {
            fetch('http://127.0.0.1:8000/core/movies/', {
                method: 'get',
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                    'authorization': `Token ${this.token}`
                }
            })
            .then(movies => movies.json())
            .then(movies => {
                this.movies = movies;
                if (this.selectedMovie) {
                    this.selectedMovie = this.movies.find(movie => movie.id === this.selectedMovie.id);
                }
            })
            .catch(error => console.log(error))
        },
        getGenres() {
            fetch('http://127.0.0.1:8000/core/genres/', {
                method: 'get',
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                    'authorization': `Token ${this.token}`
                }
            })
            .then(genres => genres.json())
            .then(genres => {
                this.genres = genres;
            })
            .catch(error => console.log(error))
        },
        checkAdmin() {
            fetch(`http://127.0.0.1:8000/core/movies/0/is_admin/`, {
                    method: 'post',
                    headers: {
                    'Content-Type' : 'application/json',
                    'authorization': `Token ${this.token}`
                }
            })
            .then(res => res.json())
            .then((res) => {
                const isAdmin = res.is_admin;
                this.isAdmin = isAdmin;
            })
            .catch(error => console.log(error))
        },
        logout() {
            this.$cookie.remove('auth-token');
            this.$router.push("/auth");
        }
    },
    created() {
        if (this.$cookie.get("auth-token")) {
            this.token = this.$cookie.get("auth-token");
            this.checkAdmin();
            this.getMovies();
            this.getGenres();
        } else {
            this.$router.push("/auth");
        }
    },
})
</script>

<style scoped>
    .layout {
        margin-top: 2rem;
        display: grid;
        grid-template-columns: 10fr 1fr 10fr;
    }
</style>