<template>
<div> Activating</div>
</template>
        
    <script>
    import { defineComponent} from "vue";
    import { verifyActivationToken} from '../services/auth'
    import router from "../router";
    
    export default defineComponent({
      components: {
      }, 
      props: {
        token: {
          type: String,
          required: true
        },
        uid: {
          type: String,
          required: true
        }}, 

      async mounted()  {        
          if ( await verifyActivationToken(this.token,this.uid)) {
            console.log("Success:");
            router.push("/login");
          } else {
            router.push("/login");
          }
        }
    },
    );
    </script>
