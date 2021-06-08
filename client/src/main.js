import { createApp } from 'vue'
import App from './App.vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faFilm, faStar, faTrash, faEdit } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import router from './router'
import cookie from './plugins/cookie'

library.add(faFilm, faStar, faEdit, faTrash);


createApp(App)
    .use(cookie)
    .use(router)
    .component("font-awesome-icon", FontAwesomeIcon)
    .mount('#app')
