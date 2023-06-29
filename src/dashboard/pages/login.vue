<template>
  <b-container>
    <b-row class="vh-100 text-center" align-v="center">
      <b-col>
        <div>
          <div v-if="error" class="px-5">
            <Notification :message="error" />
          </div>

          <h3 class="text-left px-5 py-3">Hi, Welcome Back</h3>

          <b-form @submit.prevent="login" class="text-left mb-3 px-5">
            <b-form-group id="input-group-1">
              <b-form-input
                id="username"
                v-model="username"
                placeholder="Username"
                required
              ></b-form-input>
            </b-form-group>

            <b-input-group id="input-group-2" class="mb-3">
              <b-form-input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" placeholder="Password" required></b-form-input>
              <b-input-group-append>
                <b-button variant="info" @click="showPassword = !showPassword">{{showPassword ? 'Show' : "Hide"}}</b-button>
              </b-input-group-append>
            </b-input-group>

            <div class="text-center">
              <b-button type="submit" variant="primary" class="w-75">Login</b-button>
            </div>
          </b-form>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Notification from '~/components/Notification'

export default {
  components: {
    Notification,
  },

  data() {
    return {
      username: '',
      password: '',
      error: null,
      showPassword: false,
    }
  },

  methods: {
    async login() {
      try {
        await this.$auth.loginWith('local', {
          data: {
            username: this.username,
            password: this.password
          }
        });

        this.$router.push('/authors')
      } catch (e) {
        this.error = e.response.data.detail
      }
    }
  }
}
</script>