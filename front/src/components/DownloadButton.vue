<template>
    <div>
        <a :href="origin + baseUrl + downloadUrl" :download="fileName">
            <button>
                <slot>Télécharger</slot>
            </button>
        </a>
    </div>
</template>

<script>
import { origin, baseUrl } from '../api';

export default {
  props: {
    downloadUrl: {
      type: String,
      required: true,
    },
    fileName: {
      type: String,
      required: true,
    }
  },
  setup() {
    return { origin, baseUrl };
  }
};
</script>

<style scoped>
button {
    width: 100%;
}
</style>
