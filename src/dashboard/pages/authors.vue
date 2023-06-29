<template>
  <div class="p-5">
    <b-modal 
      id="modal-1" 
      title="Add or Edit Author"
      size="xl"
      hide-footer
    >
      <AuthorEdit :authorId="authorSelected"></AuthorEdit>
    </b-modal>
    <b-row class="text-center" align-v="center">
      <b-col cols="10">
        <b-form-group id="input-group-1">
          <b-form-input
            id="search"
            v-model="author_search"
            placeholder="Search Authors"
            required
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col>
        <b-form-group id="input-group-2">
          <b-button variant="primary" class="w-100" v-b-modal.modal-1>Add</b-button>
        </b-form-group>
      </b-col>
    </b-row>

    <div class="d-flex justify-content-center align-middle mb-3" v-if="$fetchState.pending">
      <b-spinner label="Loading..."></b-spinner>
    </div>

    <div v-else-if="error">
      <Notification :message="error" />
    </div>

    <div v-else>
      <b-table 
        striped hover 
        :items="authors" 
        :fields="fields"
        :per-page="perPage"
        :current-page="currentPage"
        :filter="author_search"
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
import AuthorEdit from '~/components/AuthorEdit'
import Notification from '~/components/Notification'

  export default {
    components: {
      AuthorEdit,
      Notification
    },
    data() {
      return {
        author_search: '',
        author_selected: null,
        perPage: 10,
        currentPage: 1,
        authors: [],
        error: null,
        fields: [
          {
            key: "name",
            label: "Name",
          }, 
          {
            key: "books.length",
            label: "Number of Books",
          }
        ],
      }
    },
    methods: {
      handleRowClicked(item, index, event) {
        this.author_selected = item.id;
        console.log("Item Id:", item.id);
        this.$bvModal.show('modal-1');
      }
    },
    computed: {
      rows() {
        if(this.author_search == '')
          return this.authors.length;
        else
          return this.authors.filter(author => author.name.search(this.author_search) > -1).length;
      },
      authorSelected() {
        return this.author_selected;
      }
    },
    async fetch() {
      try {
        this.authors = await this.$axios.$get('/api/authors');
      } catch (e) {
        this.error = e.response.data.detail;
      }
    }
  }
</script>