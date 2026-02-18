<template>
  <div class="font-display bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 h-screen flex flex-col transition-colors duration-300 overflow-hidden">

    <AppHeader :is-dark="isDark" @toggle-dark-mode="toggleDarkMode" @toggle-sidebar="sidebarOpen = !sidebarOpen" />

    <main class="flex flex-1 overflow-hidden">

      <AppSidebar
        :output-mode="outputMode"
        :selected-count="selectedPages.length"
        :has-session="!!sessionId"
        :session-id="sessionId ?? ''"
        :original-filename="originalFilename"
        :selected-pages="selectedPages"
        :mobile-open="sidebarOpen"
        @update:output-mode="outputMode = $event"
        @select-all="pageGridRef?.selectAll()"
        @select-even="pageGridRef?.selectEven()"
        @select-odd="pageGridRef?.selectOdd()"
        @reset-selection="pageGridRef?.clearSelection()"
        @download-success="onDownloadSuccess"
        @close="sidebarOpen = false"
      />

      <div class="flex-1 flex flex-col h-full overflow-hidden">

        <template v-if="sessionId">
          <PageToolbar
            :filename="originalFilename"
            :page-count="pageCount"
            :zoom-level="zoomLevel"
            :zoom-min="ZOOM_MIN"
            :zoom-max="ZOOM_MAX"
            @zoom-in="zoomLevel = Math.min(zoomLevel + 1, ZOOM_MAX)"
            @zoom-out="zoomLevel = Math.max(zoomLevel - 1, ZOOM_MIN)"
            @new-pdf="resetSession"
          />
          <PageGrid
            ref="pageGridRef"
            :page-count="pageCount"
            :session-id="sessionId"
            :zoom-level="zoomLevel"
            @update:selected-pages="selectedPages = $event"
          />
        </template>

        <div v-else class="flex-1 flex items-center justify-center p-8">
          <UploadZone @upload-success="onUploadSuccess" />
        </div>

      </div>
    </main>

    <UploadToast
      v-if="showToast"
      :filename="toastFilename"
      :file-size-mo="toastFileSizeMo"
      @close="showToast = false"
    />

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import PageToolbar from './components/PageToolbar.vue'
import PageGrid from './components/PageGrid.vue'
import UploadZone from './components/UploadZone.vue'
import UploadToast from './components/UploadToast.vue'

const ZOOM_MIN = 1
const ZOOM_MAX = 5

const sessionId = ref<string | null>(null)
const pageCount = ref<number>(0)
const originalFilename = ref<string>('')
const selectedPages = ref<number[]>([])
const outputMode = ref<'merged' | 'separate'>('merged')
const zoomLevel = ref<number>(3)
const isDark = ref<boolean>(false)
const sidebarOpen = ref<boolean>(false)
const showToast = ref<boolean>(false)
const toastFilename = ref<string>('')
const toastFileSizeMo = ref<string>('')
const pageGridRef = ref<InstanceType<typeof PageGrid> | null>(null)

let toastTimer: ReturnType<typeof setTimeout> | null = null

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})

function toggleDarkMode(): void {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

function onUploadSuccess(payload: {
  session_id: string
  page_count: number
  original_filename: string
  file_size_mo: string
}): void {
  sessionId.value = payload.session_id
  pageCount.value = payload.page_count
  originalFilename.value = payload.original_filename
  selectedPages.value = []

  toastFilename.value = payload.original_filename
  toastFileSizeMo.value = payload.file_size_mo
  showToast.value = true
  sidebarOpen.value = false

  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { showToast.value = false }, 5000)
}

function onDownloadSuccess(): void {
  selectedPages.value = []
  pageGridRef.value?.clearSelection()
}

function resetSession(): void {
  sessionId.value = null
  pageCount.value = 0
  originalFilename.value = ''
  selectedPages.value = []
  zoomLevel.value = 3
  sidebarOpen.value = false
}
</script>
