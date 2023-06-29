<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">Code Challenge</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-navbar-nav>
            <b-nav-item href="/authors" v-if="isAuthenticated">Authors</b-nav-item>
            <b-nav-item href="/books" v-if="isAuthenticated">Books</b-nav-item>
          </b-navbar-nav>
          <b-nav-item-dropdown right v-if="isAuthenticated">
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>{{ loggedInUser.username }}</em>
            </template>
            <b-dropdown-item @click="logout">Log Out</b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item href="/login" v-else>Login</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>
  
<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  },
  methods: {
      async logout() {
        await this.$auth.logout();
        this.$router.push('/login');
      },
  },

}
</script>