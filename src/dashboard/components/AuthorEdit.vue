<template>
    <div>
      <div class="d-flex justify-content-center align-middle mb-3" v-if="$fetchState.pending">
        <b-spinner label="Loading..."></b-spinner>
      </div>
      
      <div v-else>
        <div v-if="error">
          <Notification :message="error" />
        </div>

        <div v-else-if="success">
          <Notification :message="success"  type="success"/>
        </div>

        <b-form-group id="input-group-1">
          <b-form-input
            id="author-edit-name"
            v-model="author.name"
            placeholder="Name"
            required
          ></b-form-input>
        </b-form-group>

        <h3>Books</h3>

        <EditableTable 
          striped hover 
          v-model="author.books" 
          :fields="fields"
          item="Book"
          >
        </EditableTable>

        <div class="text-right">
          <b-button variant="primary" @click="handleSubmit">Save</b-button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import EditableTable from '~/components/EditableTable'
  import Notification from '~/components/Notification'
  export default {
    components: {
      EditableTable,
      Notification,
    },
    name: 'AuthorEdit',
    props: ['authorId'],
    data() {
      return {
        success: null,
        error: null,
        author: {},
        fields: [
          {
            key: "name",
            label: "Name",
            type: "text",
          }, 
          {
            key: "number_of_pages",
            label: "Number of Pages",
            type: "text",
          },
          { key: "edit", label: "", type: "edit" }
        ],
      }
    },
    async fetch() {
      if(this.authorId) {
        try {
          this.author = await this.$axios.$get(`/api/authors/${this.authorId}`);
        } catch (e) {
          this.error = e.response.data.detail;
        }
      }
    },
    methods: {
      async handleSubmit() {
        if(this.authorId) {
          try {
            await this.$axios.$patch(`/api/authors/${this.authorId}`, this.author);
          } catch (e) {
            this.error = e.response.data.detail;
          }
          this.success = "Author updated successfully.";
        } else {
          try {
            await this.$axios.$post(`/api/authors`, this.author);
          } catch (e) {
            this.error = e.response.data.detail;
          }
          this.success = "Author created successfully.";
        }
        this.$nuxt.refresh();
      },
    },
  }
  </script>