import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify } from 'quasar'
import router from './router'

// Import Quasar css
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'

// Import Tailwind CSS
import './assets/css/main.css'

// Import root component
import App from './App.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: {
    Notify
  },
  config: {
    notify: {
      position: 'top-right',
      timeout: 3000,
      textColor: 'white'
    }
  }
})

app.mount('#app')
