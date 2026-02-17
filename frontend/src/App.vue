<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6">
    <h1 class="text-3xl font-bold text-gray-800 mb-8">Découpeur de PDF</h1>
    <UploadZone @upload-success="onUploadSuccess" />
    <div v-if="sessionId" class="mt-6 text-green-700 font-medium">
      PDF chargé — {{ pageCount }} page(s)
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import UploadZone from './components/UploadZone.vue'

const sessionId = ref(null)
const pageCount = ref(0)

function onUploadSuccess({ session_id, page_count }) {
  sessionId.value = session_id
  pageCount.value = page_count
}
</script>
