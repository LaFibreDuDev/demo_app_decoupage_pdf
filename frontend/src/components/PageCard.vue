<template>
  <div
    class="relative group cursor-pointer"
    :class="selected ? '' : 'opacity-70 hover:opacity-100 transition-all'"
    @click="$emit('toggle')"
  >
    <!-- Card -->
    <div
      :class="[
        'relative aspect-[3/4] bg-white dark:bg-slate-800 rounded-xl shadow-md border-4 transition-all overflow-hidden',
        selected
          ? 'border-primary ring-4 ring-primary/20'
          : 'border-transparent hover:border-slate-300 dark:hover:border-slate-600'
      ]"
    >
      <!-- Miniature -->
      <img
        v-if="thumbUrl"
        :src="thumbUrl"
        :alt="`Aperçu page ${page}`"
        class="w-full h-full object-cover transition-all"
        :class="selected ? '' : 'grayscale group-hover:grayscale-0'"
      />

      <!-- Skeleton pendant le chargement de la miniature -->
      <div
        v-else
        class="absolute inset-0 animate-pulse bg-slate-200 dark:bg-slate-700"
      >
        <span class="absolute top-2 left-2 text-xs font-bold px-1.5 py-0.5 rounded bg-slate-300/70 dark:bg-slate-600/70 text-slate-500 dark:text-slate-400">
          {{ page }}
        </span>
      </div>

      <!-- Checkmark (sélectionné) -->
      <div
        v-if="selected"
        class="absolute top-3 right-3 w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white shadow-lg"
      >
        <span class="material-symbols-outlined text-[20px]">check</span>
      </div>

      <!-- Overlay "+" au survol (non sélectionné) -->
      <div
        v-else
        class="page-overlay absolute inset-0 bg-slate-900/10 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
      >
        <div class="w-12 h-12 bg-white/90 dark:bg-slate-800/90 rounded-full flex items-center justify-center text-primary shadow-xl">
          <span class="material-symbols-outlined">add</span>
        </div>
      </div>
    </div>

    <!-- Numéro + label -->
    <div class="mt-3 flex items-center justify-between px-1">
      <span
        :class="[
          'text-sm font-bold px-2 py-0.5 rounded',
          selected
            ? 'bg-primary text-white'
            : 'text-slate-400 border border-slate-300 dark:border-slate-700'
        ]"
      >
        {{ page }}
      </span>
      <span v-if="selected" class="text-xs font-medium text-primary">Inclus</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  page: number
  selected?: boolean
  thumbUrl?: string
}>()

defineEmits<{
  toggle: []
}>()
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
