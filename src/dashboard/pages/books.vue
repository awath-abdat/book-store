<template>
  <div class="p-5">
    <b-modal 
      id="modal-book" 
      title="Add or Edit Book"
      size="xl"
      hide-footer
    >
      <BookEdit :bookId="bookSelected"></BookEdit>
    </b-modal>
    <b-row class="text-center" align-v="center">
      <b-col cols="10">
        <b-form-group id="input-group-book-search">
          <b-form-input
            id="search"
            v-model="book_search"
            placeholder="Search Books"
            required
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col>
        <b-form-group id="input-group-books-add">
          <b-button variant="primary" class="w-100" v-b-modal.modal-book @click="book_selected=null">Add</b-button>
        </b-form-group>
      </b-col>
    </b-row>

    <div class="d-flex justify-content-center align-middle mb-3" v-if="$fetchState.pending">
      <b-spinner label="Loading..."></b-spinner>
    </div>

    <div v-else-if="error">
      <Notification :message="error" />
    </div>

    <div>
      <b-table 
        striped hover 
        :items="books" 
        :fields="fields"
        :per-page="perPage"
        :current-page="currentPage"
        :filter="book_search"
        :filter-included-fields="['name']"
        @row-clicked="handleRowClicked"
        >
      </b-table>

      <b-pagination
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        aria-controls="my-table"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import BookEdit from '~/components/BookEdit'
import Notification from '~/components/Notification'

  export default {
    components: {
      BookEdit,
      Notification
    },
    data() {
      return {
        book_search: '',
        book_selected: null,
        perPage: 10,
        currentPage: 1,
        books: [],
        error: null,
        fields: [
          {
            key: "name",
            label: "Name",
          }, 
          {
            key: "number_of_pages",
            label: "Number of pages",
          },
          {
            key: "author.name",
            label: "Author",
          }
        ],
      }
    },
    methods: {
      handleRowClicked(item, index, event) {
        this.book_selected = item.id;
        this.$bvModal.show('modal-book');
      }
    },
    computed: {
      rows() {
        if(this.book_search == '')
          return this.books.length;
        else
          return this.books.filter(book => book.name.search(this.book_search) > -1).length;
      },
      bookSelected() {
        return this.book_selected;
      }
    },
    async fetch() {
      try {
        this.books = await this.$axios.$get('/api/books')
      } catch (e) {
        this.error = e.response.data.detail;
      }
    }
  }
</script>