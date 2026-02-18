<template>
  <div class="px-4 md:px-8 py-4 flex items-center justify-between border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
    <div class="flex items-center gap-2 md:gap-4 min-w-0">
      <span class="material-symbols-outlined text-slate-400 shrink-0">description</span>
      <span class="font-medium truncate max-w-[120px] md:max-w-[300px] text-slate-800 dark:text-slate-200">{{ filename }}</span>
      <span class="hidden md:inline px-2 py-0.5 bg-slate-100 dark:bg-slate-800 text-[10px] font-bold rounded uppercase text-slate-500">
        {{ pageCount }} pages
      </span>
    </div>
    <div class="flex items-center gap-2">
      <button
        @click="$emit('zoom-out')"
        :disabled="zoomLevel <= zoomMin"
        class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg text-slate-500 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        <span class="material-symbols-outlined">zoom_out</span>
      </button>
      <span class="text-sm font-medium text-slate-400 px-2">{{ zoomPercent }}%</span>
      <button
        @click="$emit('zoom-in')"
        :disabled="zoomLevel >= zoomMax"
        class="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg text-slate-500 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        <span class="material-symbols-outlined">zoom_in</span>
      </button>

      <div class="h-6 w-px bg-slate-200 dark:bg-slate-700 mx-1"></div>

      <button
        @click="$emit('new-pdf')"
        class="flex items-center gap-1.5 px-2 md:px-3 py-2 rounded-lg text-slate-500 hover:text-primary hover:bg-primary/5 dark:hover:bg-primary/10 transition-colors text-sm font-medium"
        title="Charger un nouveau PDF"
      >
        <span class="material-symbols-outlined text-[20px]">upload_file</span>
        <span class="hidden md:inline">Nouveau PDF</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  filename: string
  pageCount: number
  zoomLevel: number
  zoomMin: number
  zoomMax: number
}>()

defineEmits<{
  'zoom-in': []
  'zoom-out': []
  'new-pdf': []
}>()

const ZOOM_PERCENTS: Record<number, number> = { 1: 60, 2: 70, 3: 80, 4: 90, 5: 100 }

const zoomPercent = computed(() => ZOOM_PERCENTS[props.zoomLevel] ?? 80)
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
