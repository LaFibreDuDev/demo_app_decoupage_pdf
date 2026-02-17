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

<script setup lang="ts">
import { ref } from 'vue'
import UploadZone from './components/UploadZone.vue'
import PageGrid from './components/PageGrid.vue'
import DownloadButton from './components/DownloadButton.vue'

const sessionId = ref<string | null>(null)
const pageCount = ref<number>(0)
const originalFilename = ref<string>('')
const selectedPages = ref<number[]>([])
const pageGridRef = ref<InstanceType<typeof PageGrid> | null>(null)

function onUploadSuccess(payload: { session_id: string; page_count: number; original_filename: string }): void {
  sessionId.value = payload.session_id
  pageCount.value = payload.page_count
  originalFilename.value = payload.original_filename
  selectedPages.value = []
}

function onDownloadSuccess(): void {
  selectedPages.value = []
  pageGridRef.value?.clearSelection()
}
</script>
