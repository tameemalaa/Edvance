<template>
  <div class="home">
    <h> blaa </h>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "HomeView",
  beforeCreate() {
    this.$store.commit("initializeStore");
    const access = this.$store.state.access;
    if (access) {
      axios.defaults.headers.common["Authorization"] = "JWT " + access;
    } else {
      axios.defaults.headers.common["Authorizaton"] = "";
    }
  },
};
</script>
