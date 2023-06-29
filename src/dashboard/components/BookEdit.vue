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

        <b-form-group 
          id="input-group-book-name"
          label="Book Name"
          label-for="book-edit-name"
        >
          <b-form-input
            id="book-edit-name"
            v-model="book.name"
            placeholder="Name"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group 
          id="input-group-number-of-pages"
          label="Number of Pages"
          label-for="book-edit-number-of-pages"
        >
          <b-form-input
            id="book-edit-number-of-pages"
            v-model="book.number_of_pages"
            placeholder="Number of Pages"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-1"
          label="Author"
          label-for="book-author"
        >
          <treeselect id="book-author" v-model="book.author_id" :multiple="false" :options="options" />
        </b-form-group>

        <div class="text-right">
          <b-button variant="primary" @click="handleSubmit">Save</b-button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Treeselect from '@riophae/vue-treeselect'
  import '@riophae/vue-treeselect/dist/vue-treeselect.css'

  export default {
    components: {
      Treeselect,
    },
    name: 'BookEdit',
    props: ['bookId'],
    data() {
      return {
        book: {},
        options: [],
        authors: [],
        fields: [
          {
            key: "name",
            label: "Name",
          }, 
          {
            key: "number_of_pages",
            label: "Number of Pages",
          },
        ],
      }
    },
    async fetch() {
      if(this.bookId) {
        try {
          this.book = await this.$axios.$get(`/api/books/${this.bookId}`);
        } catch (e) {
          this.error = e.response.data.detail;
        }
      }

      try {
        this.authors = await this.$axios.$get(`/api/authors`);
      } catch (e) {
        this.error = e.response.data.detail;
      }
      this.options = this.authors.map(function(author) { return {id: author.id, label: author.name};})
    },
    methods: {
      async handleSubmit() {
        if(this.bookId) {
          try {
            await this.$axios.$patch(`/api/books/${this.bookId}`, this.book);
          } catch (e) {
            this.error = e.response.data.detail;
          }
          this.success = "Book updated successfully.";
        } else {
          try {
            await this.$axios.$post(`/api/books`, this.book);
          } catch (e) {
            this.error = e.response.data.detail;
          }
          this.success = "Book created successfully.";
        }
        this.$nuxt.refresh();
      },
    },
  }
  </script>