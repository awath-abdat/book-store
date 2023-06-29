<template>
    <b-alert show dismissible :variant="type == 'success' ? 'info' : 'danger'">{{ message }}</b-alert>
  </template>
  
  <script>
  export default {
    name: 'Notification',
    props: ['message', 'type']
  }
  </script>