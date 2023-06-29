<template>
  <section class="section">
    <div class="container">
      <h1 class="title">DC Full Stack Code Challenge</h1>
    </div>
  </section>
</template>

<script>
export default{
  middleware({ redirect }) {
    return redirect('/authors');
  }
}
</script>