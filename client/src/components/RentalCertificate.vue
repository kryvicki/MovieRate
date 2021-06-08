<template>
    <div>
        <div v-if="certificate && certificate.number">
            <h3>Rental Certificate: </h3>
            <p>Number: {{certificate.number}}</p>
            <p>Country: {{certificate.country}}</p>
            <button v-if="!formVisible" class="custom-btn btn-logout black" @click="setCertificate()">Update Certificate</button>
            &nbsp;
            <font-awesome-icon class="pointer" icon="trash" @click="deleteCertificate()"/>
        </div>
        <div v-else>
            <h3>No rental certificate</h3>
            <button  v-if="!formVisible" class="custom-btn btn-logout black" @click="setCertificate()">Add Certificate</button>
        </div>
        <div>
            <div v-if="formVisible">
                <div v-if="errors.length">
                    <h4 class="errors">Correct the following errors:</h4>
                    <ul>
                        <li v-for="error in errors" :key="error">{{ error }}</li>
                    </ul>
                </div>

                <p class="input-row">
                    <label for="name">Number: </label>
                    <input
                    id="name"
                    v-model="number"
                    type="text"
                    name="name"
                    >
                </p>

                <p class="input-row">
                    <label for="age">Country: </label>
                    <select name="movie" id="movie" v-model="country">
                        <option v-for="c in countriesList" :key="c" :value="c">{{c}}</option>
                    </select>
                </p>

                <p class="input-row">
                    <label for="movie">For movie: </label>
                    <input type="text" disabled readonly v-model="selectedMovie.title">
                </p>

                <p>
                    <button @click="checkForm()" class="custom-btn btn-logout black">Save</button>
                </p>
            </div>
        </div>
    </div>
    
</template>

<script>

export default ({
    name: "Movies",
    props: ['movie', 'token'],
    data() {
        return {
            certificate: null,
            formVisible: false,
            selectedMovie: {...this.movie},
            errors: [],
            number: '',
            country: '',
            countriesList: ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"], 
        }
    }, 
    methods: {
        getCertificate() {
            if (this.movie.id) {
                fetch(`http://127.0.0.1:8000/core/rental_certificates/${this.movie.id}/`, {
                    method: 'get',
                    headers: {
                        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                        'authorization': `Token ${this.token}`
                        }
                })
                .then(certificate => certificate.json())
                .then(certificate => {
                    this.certificate = certificate;
                })
                .catch(error => {
                    this.certificate = null;
                    console.log(error);
                })
            }
            
        }, 
        saveCertificate() {
            if (this.certificate && this.certificate.number) {
                fetch(`http://127.0.0.1:8000/core/rental_certificates/${this.movie.id}/`, {
                    method: 'put',
                    headers: {
                        'Content-Type' : 'application/json',
                        'authorization': `Token ${this.token}`
                    },
                    body: JSON.stringify({number: this.number, 
                                          country: this.country})
                    
                })
                .then(() => {
                    this.getCertificate();
                })
                .catch(error => console.log(error))
            } else {
                fetch(`http://127.0.0.1:8000/core/rental_certificates/`, {
                    method: 'post',
                    headers: {
                        'Content-Type' : 'application/json',
                        'authorization': `Token ${this.token}`
                    },
                    body: JSON.stringify({number: this.number, 
                                          country: this.country,
                                          movie_id: this.movie.id})
                    
                })
                .then(() => {
                    this.getCertificate();
                })
                .catch(error => console.log(error))
            }
            this.formVisible = false;
        }, 
        checkForm() {
            if(this.number && this.country) 
                this.saveCertificate();

            this.errors = [];
            if(!this.number) 
                this.errors.push("Number is required.");
            if(!this.country) 
                this.errors.push("Country is required.");
        },
        setCertificate() {
            if (this.certificate && this.certificate.number) {
                this.number = this.certificate.number,
                this.country = this.certificate.country
            }
            this.formVisible = true;
        },
        
        deleteCertificate() {
            if (this.certificate && this.certificate.number) {
                fetch(`http://127.0.0.1:8000/core/rental_certificates/${this.movie.id}/`, {
                    method: 'delete',
                    headers: {
                        'Content-Type' : 'application/json',
                        'authorization': `Token ${this.token}`
                    },
                })
                .then(() => {
                    this.getCertificate();
                })
                .catch(error => console.log(error))
            }
        },
    },
    watch: { 
        movie: function(newValue, oldValue) {
            if (newValue !== oldValue) {
                this.formVisible = false;
                this.number = '';
                this.country = '';
                this.selectedMovie = {...this.movie};
                this.getCertificate()
            }
        }
    },
    created() {
        this.getCertificate()
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
    input, select {
        width: 50%;
        padding: 0.2rem 0.5rem;
        border: 1px solid black;
        background-color: white;
    }
    .errors {
        margin-bottom: 1rem;
    }
</style>
