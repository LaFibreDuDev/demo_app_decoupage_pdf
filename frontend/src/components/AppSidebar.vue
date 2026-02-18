<template>
  <!-- Backdrop mobile -->
  <div
    v-if="mobileOpen"
    class="fixed top-16 inset-x-0 bottom-0 bg-black/50 z-30 md:hidden"
    @click="$emit('close')"
  />

  <!-- Sidebar -->
  <aside
    :class="[
      'w-80 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 flex flex-col gap-8 overflow-y-auto shrink-0 transition-transform duration-300',
      mobileOpen
        ? 'flex fixed top-16 bottom-0 left-0 z-40 shadow-2xl'
        : 'hidden md:flex'
    ]"
  >
    <!-- Bouton fermeture (mobile uniquement) -->
    <button
      class="md:hidden self-end -mt-2 -mr-2 p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-slate-500"
      @click="$emit('close')"
    >
      <span class="material-symbols-outlined">close</span>
    </button>

    <!-- Configuration -->
    <section>
      <h2 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-4">Configuration</h2>
      <div class="space-y-3">
        <div
          :class="[
            'p-4 rounded-xl border-2 transition-all cursor-pointer',
            outputMode === 'merged'
              ? 'border-primary bg-primary/5 dark:bg-primary/10'
              : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
          ]"
          @click="$emit('update:output-mode', 'merged')"
        >
          <label class="flex items-center gap-3 cursor-pointer">
            <input
              type="radio"
              name="split-mode"
              :checked="outputMode === 'merged'"
              class="w-4 h-4 text-primary focus:ring-primary border-slate-300 dark:border-slate-700"
              @change="$emit('update:output-mode', 'merged')"
            />
            <div>
              <p class="text-sm font-semibold text-slate-800 dark:text-slate-200">Fichier fusionné</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">Extraire dans un seul PDF</p>
            </div>
          </label>
        </div>
        <div
          :class="[
            'p-4 rounded-xl border-2 transition-all cursor-pointer',
            outputMode === 'separate'
              ? 'border-primary bg-primary/5 dark:bg-primary/10'
              : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
          ]"
          @click="$emit('update:output-mode', 'separate')"
        >
          <label class="flex items-center gap-3 cursor-pointer">
            <input
              type="radio"
              name="split-mode"
              :checked="outputMode === 'separate'"
              class="w-4 h-4 text-primary focus:ring-primary border-slate-300 dark:border-slate-700"
              @change="$emit('update:output-mode', 'separate')"
            />
            <div>
              <p class="text-sm font-semibold text-slate-800 dark:text-slate-200">Fichiers individuels</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">Un fichier par page extraite</p>
            </div>
          </label>
        </div>
      </div>
    </section>

    <!-- Sélection rapide -->
    <section v-if="hasSession">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-500">Sélection</h2>
        <button
          @click="$emit('select-all')"
          class="text-xs font-semibold text-primary hover:underline"
        >
          Tout sélectionner
        </button>
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          @click="$emit('select-even')"
          class="px-3 py-1.5 text-xs font-medium rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-300"
        >
          Pages paires
        </button>
        <button
          @click="$emit('select-odd')"
          class="px-3 py-1.5 text-xs font-medium rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-300"
        >
          Pages impaires
        </button>
        <button
          @click="$emit('reset-selection')"
          class="px-3 py-1.5 text-xs font-medium rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-300"
        >
          Réinitialiser
        </button>
      </div>
    </section>

    <!-- Sécurité & Confidentialité -->
    <section class="border-t border-slate-100 dark:border-slate-800 pt-6">
      <h2 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-4 flex items-center gap-2">
        <span class="material-symbols-outlined text-sm">verified_user</span>
        Sécurité &amp; Confidentialité
      </h2>
      <div class="space-y-3">
        <div class="flex items-start gap-3">
          <div class="mt-0.5 w-7 h-7 rounded-lg bg-green-500/10 flex items-center justify-center text-green-600 dark:text-green-500 shrink-0">
            <span class="material-symbols-outlined text-[18px]">lock</span>
          </div>
          <p class="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
            Fichiers chiffrés sur le serveur
          </p>
        </div>
        <div class="flex items-start gap-3">
          <div class="mt-0.5 w-7 h-7 rounded-lg bg-orange-500/10 flex items-center justify-center text-orange-600 dark:text-orange-500 shrink-0">
            <span class="material-symbols-outlined text-[18px]">history</span>
          </div>
          <p class="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
            Suppression automatique après 24h
          </p>
        </div>
      </div>
    </section>

    <!-- Résumé + Bouton Télécharger -->
    <div class="mt-auto space-y-4 pt-4">
      <div v-if="hasSession" class="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
        <div class="flex justify-between text-sm">
          <span class="text-slate-500">Sélectionné :</span>
          <span class="font-bold text-slate-800 dark:text-slate-200">{{ selectedCount }} page{{ selectedCount > 1 ? 's' : '' }}</span>
        </div>
      </div>

      <button
        v-if="hasSession"
        @click="download"
        :disabled="selectedCount === 0 || loading"
        class="w-full bg-primary hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-2xl shadow-lg shadow-primary/20 flex items-center justify-center gap-2 transition-all active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed disabled:active:scale-100"
      >
        <span v-if="loading" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
        <span v-else class="material-symbols-outlined">download</span>
        {{ loading ? 'Découpage…' : `Télécharger (${selectedCount})` }}
      </button>

      <div
        v-if="error"
        class="px-4 py-2.5 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-700 dark:text-red-400 text-xs"
      >
        {{ error }}
      </div>
    </div>

  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  outputMode: 'merged' | 'separate'
  selectedCount: number
  hasSession: boolean
  sessionId: string
  originalFilename: string
  selectedPages: number[]
  mobileOpen: boolean
}>()

const emit = defineEmits<{
  'update:output-mode': [mode: 'merged' | 'separate']
  'select-all': []
  'select-even': []
  'select-odd': []
  'reset-selection': []
  'download-success': []
  'close': []
}>()

const loading = ref<boolean>(false)
const error = ref<string | null>(null)

async function download(): Promise<void> {
  error.value = null
  loading.value = true
  try {
    const response = await fetch('/split', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: props.sessionId,
        original_filename: props.originalFilename,
        pages: props.selectedPages,
        output_mode: props.outputMode,
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
    a.download = `${props.originalFilename}_split.zip`
    a.click()
    URL.revokeObjectURL(url)
    emit('download-success')
  } catch {
    error.value = 'Impossible de contacter le serveur.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
