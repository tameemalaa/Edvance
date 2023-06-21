<template>
<!-- <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cedarville+Cursive&display=swap" rel="stylesheet"> -->

    <!-- <div id="video-background">
      <div class="video-foreground">
    <iframe width="1280" height="720" :src=link  title="Rick Roll (Different link + no ads)" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
  
  </div>

  </div> -->

  <h1> Edvance </h1>
  
</template>

<script>
import axios from "axios";
const memes = [
  "xvFZjo5PgG0",
  "9ZDTIhfgueg",
  "IJNR2EpS0jw"
];
export default {
  name: "HomeView",
  data(){
    return{
      link: `https://www.youtube.com/embed/${memes[Math.floor(Math.random()*memes.length)]}?controls=0&showinfo=0&rel=0&autoplay=1`,
    }
  },

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
<style scoped>
h1 {
  /* font-family: 'Cedarville Cursive', cursive; */
  font-size: 500px;
  color: black;
  }

  #video-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
}
.video-foreground {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
.video-foreground iframe {
    width: 100%;
    height: 100%;
}
</style>
