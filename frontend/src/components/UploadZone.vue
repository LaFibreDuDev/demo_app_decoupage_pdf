<template>
  <div class="w-full max-w-md">
    <!-- Zone de sélection / dépôt -->
    <div
      :class="[
        'border-2 border-dashed rounded-xl p-10 flex flex-col items-center gap-4 transition-colors',
        isDragging
          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
          : 'border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-blue-400 dark:hover:border-primary'
      ]"
      @dragenter.prevent="onDragEnter"
      @dragleave.prevent="onDragLeave"
      @dragover.prevent
      @drop.prevent="onDrop"
    >
      <svg
        class="w-12 h-12 text-gray-400 dark:text-slate-500"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
        />
      </svg>
      <p class="text-gray-600 dark:text-slate-300 text-sm text-center">
        <span v-if="isDragging" class="font-medium text-blue-600 dark:text-blue-400">Déposez votre PDF ici</span>
        <template v-else>
          Glissez-déposez un PDF ou<br />
          <span class="text-gray-400 dark:text-slate-500 text-xs">Taille maximale : {{ maxSizeMb }} Mo</span>
        </template>
      </p>
      <button
        @click="openFilePicker"
        :disabled="loading"
        class="px-5 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
      >
        <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
        {{ loading ? 'Envoi en cours…' : 'Choisir un PDF' }}
      </button>
      <!-- Input caché -->
      <input
        ref="fileInput"
        type="file"
        accept="application/pdf"
        class="hidden"
        @change="onFileSelected"
      />
    </div>

    <!-- Message d'erreur -->
    <div
      v-if="error"
      class="mt-3 px-4 py-2.5 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400 text-sm"
    >
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface UploadSuccessPayload {
  session_id: string
  page_count: number
  original_filename: string
  file_size_mo: string
}

const emit = defineEmits<{
  'upload-success': [payload: UploadSuccessPayload]
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const loading = ref<boolean>(false)
const error = ref<string | null>(null)
const dragCounter = ref<number>(0)
const isDragging = computed<boolean>(() => dragCounter.value > 0)

const maxSizeMb = parseInt(import.meta.env.VITE_UPLOAD_MAX_SIZE_MB, 10)
const MAX_SIZE = maxSizeMb * 1024 * 1024

function openFilePicker(): void {
  error.value = null
  fileInput.value?.click()
}

async function processFile(file: File | undefined): Promise<void> {
  if (!file) return
  if (loading.value) return

  if (file.type !== 'application/pdf') {
    error.value = 'Le fichier doit être un PDF.'
    return
  }
  if (file.size > MAX_SIZE) {
    error.value = `Le fichier ne doit pas dépasser ${maxSizeMb} Mo.`
    return
  }

  error.value = null
  loading.value = true

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/upload', {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.detail ?? `Erreur serveur (${response.status}).`
      return
    }

    emit('upload-success', {
      session_id: data.session_id,
      page_count: data.page_count,
      original_filename: data.original_filename,
      file_size_mo: (file.size / (1024 * 1024)).toFixed(1),
    })
  } catch {
    error.value = 'Impossible de contacter le serveur.'
  } finally {
    loading.value = false
  }
}

function onFileSelected(event: Event): void {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  processFile(file)
}

function onDragEnter(): void {
  dragCounter.value++
}

function onDragLeave(): void {
  dragCounter.value--
}

function onDrop(event: DragEvent): void {
  dragCounter.value = 0
  const file = event.dataTransfer?.files[0]
  processFile(file)
}
</script>
