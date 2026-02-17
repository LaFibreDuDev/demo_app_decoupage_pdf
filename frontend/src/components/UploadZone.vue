<template>
  <div class="w-full max-w-md">
    <!-- Zone de sélection -->
    <div
      class="border-2 border-dashed border-gray-300 rounded-xl p-10 flex flex-col items-center gap-4 bg-white hover:border-blue-400 transition-colors"
    >
      <svg
        class="w-12 h-12 text-gray-400"
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
      <p class="text-gray-600 text-sm text-center">
        Sélectionnez un fichier PDF<br />
        <span class="text-gray-400 text-xs">Taille maximale : {{ maxSizeMb }} Mo</span>
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
      class="mt-3 px-4 py-2.5 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
    >
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['upload-success'])

const fileInput = ref(null)
const loading = ref(false)
const error = ref(null)

const maxSizeMb = parseInt(import.meta.env.VITE_UPLOAD_MAX_SIZE_MB, 10)
const MAX_SIZE = maxSizeMb * 1024 * 1024

function openFilePicker() {
  error.value = null
  fileInput.value.click()
}

async function onFileSelected(event) {
  const file = event.target.files[0]
  if (!file) return

  // Reset input pour permettre re-sélection du même fichier
  event.target.value = ''

  // Validation client
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
    })
  } catch {
    error.value = 'Impossible de contacter le serveur.'
  } finally {
    loading.value = false
  }
}
</script>
