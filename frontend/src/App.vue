<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center p-6 gap-8">
    <h1 class="text-3xl font-bold text-gray-800 mt-8">Découpeur de PDF</h1>

    <UploadZone @upload-success="onUploadSuccess" />

    <template v-if="sessionId">
      <PageGrid
        ref="pageGridRef"
        :page-count="pageCount"
        :session-id="sessionId ?? ''"
        @update:selected-pages="selectedPages = $event"
      />

      <DownloadButton
        :session-id="sessionId"
        :original-filename="originalFilename"
        :selected-pages="selectedPages"
        @download-success="onDownloadSuccess"
      />
    </template>
    <div class="flex items-center gap-6 text-xs text-gray-400 mt-2">
      <span class="flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        Fichiers chiffrés sur le serveur
      </span>
      <span class="flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        Suppression automatique après téléchargement ou 24h
      </span>
    </div>
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
