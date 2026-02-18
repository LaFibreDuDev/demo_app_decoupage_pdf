<template>
  <div class="flex flex-col items-center gap-3">
    <!-- Sélecteur de mode de sortie -->
    <div class="flex rounded-lg border border-gray-200 overflow-hidden text-sm">
      <button
        @click="outputMode = 'merged'"
        :class="[
          'px-4 py-2 font-medium transition-colors',
          outputMode === 'merged'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-50'
        ]"
      >
        Fichier fusionné
      </button>
      <button
        @click="outputMode = 'separate'"
        :class="[
          'px-4 py-2 font-medium transition-colors border-l border-gray-200',
          outputMode === 'separate'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-50'
        ]"
      >
        Un fichier par page
      </button>
    </div>

    <button
      @click="download"
      :disabled="selectedPages.length === 0 || loading"
      class="px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
    >
      <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
      <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5m0 0l5-5m-5 5V4" />
      </svg>
      {{ loading ? 'Découpage en cours…' : labelButton }}
    </button>

    <div
      v-if="error"
      class="px-4 py-2.5 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
    >
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const { sessionId, originalFilename, selectedPages = [] } = defineProps<{
  sessionId: string
  originalFilename: string
  selectedPages?: number[]
}>()

const emit = defineEmits<{
  'download-success': []
}>()

const loading = ref<boolean>(false)
const error = ref<string | null>(null)
const outputMode = ref<'merged' | 'separate'>('merged')

const labelButton = computed(() => {
  const n = selectedPages.length
  if (outputMode.value === 'separate') {
    return `Télécharger le ZIP (${n} fichier${n > 1 ? 's' : ''})`
  }
  return `Télécharger le ZIP (${n} page${n > 1 ? 's' : ''} fusionnée${n > 1 ? 's' : ''})`
})

async function download(): Promise<void> {
  error.value = null
  loading.value = true

  try {
    const response = await fetch('/split', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        original_filename: originalFilename,
        pages: selectedPages,
        output_mode: outputMode.value,
      }),
    })

    if (!response.ok) {
      const data = await response.json()
      error.value = data.detail ?? `Erreur serveur (${response.status}).`
      return
    }

    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${originalFilename}_split.zip`
    a.click()
    URL.revokeObjectURL(url)

    outputMode.value = 'merged'
    emit('download-success')
  } catch {
    error.value = 'Impossible de contacter le serveur.'
  } finally {
    loading.value = false
  }
}
</script>
