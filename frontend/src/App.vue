<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center p-6 gap-8">
    <h1 class="text-3xl font-bold text-gray-800 mt-8">Découpeur de PDF</h1>

    <UploadZone @upload-success="onUploadSuccess" />

    <template v-if="sessionId">
      <PageGrid
        ref="pageGridRef"
        :page-count="pageCount"
        @update:selected-pages="selectedPages = $event"
      />

      <DownloadButton
        :session-id="sessionId"
        :original-filename="originalFilename"
        :selected-pages="selectedPages"
        @download-success="onDownloadSuccess"
      />
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import UploadZone from './components/UploadZone.vue'
import PageGrid from './components/PageGrid.vue'
import DownloadButton from './components/DownloadButton.vue'

const sessionId = ref(null)
const pageCount = ref(0)
const originalFilename = ref('')
const selectedPages = ref([])
const pageGridRef = ref(null)

function onUploadSuccess({ session_id, page_count, original_filename }) {
  sessionId.value = session_id
  pageCount.value = page_count
  originalFilename.value = original_filename
  selectedPages.value = []
}

function onDownloadSuccess() {
  selectedPages.value = []
  if (pageGridRef.value) {
    pageGridRef.value.clearSelection()
  }
}
</script>
