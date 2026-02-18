<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="open"
        class="fixed inset-0 z-50 flex items-end md:items-center justify-center"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black/50 backdrop-blur-sm"
          @click="$emit('close')"
        />

        <!-- Panel -->
        <div class="relative w-full md:max-w-lg bg-white dark:bg-slate-900 rounded-t-2xl md:rounded-2xl shadow-2xl px-6 pt-6 pb-8 md:p-8 z-10">

          <!-- Handle bar (mobile only) -->
          <div class="md:hidden w-10 h-1 bg-slate-200 dark:bg-slate-700 rounded-full mx-auto mb-5" />

          <!-- Header -->
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                <span class="material-symbols-outlined text-[18px]">help</span>
              </div>
              <h2 class="text-base font-bold text-slate-900 dark:text-slate-100">Comment ça marche ?</h2>
            </div>
            <button
              @click="$emit('close')"
              class="p-1.5 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
              title="Fermer"
            >
              <span class="material-symbols-outlined text-[20px]">close</span>
            </button>
          </div>

          <!-- Steps -->
          <ol class="space-y-5">
            <li
              v-for="step in steps"
              :key="step.number"
              class="flex items-start gap-4"
            >
              <div class="shrink-0 w-11 h-11 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                <span class="material-symbols-outlined">{{ step.icon }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-[10px] font-bold uppercase tracking-wider text-primary bg-primary/10 rounded-full px-2 py-0.5">
                    Étape {{ step.number }}
                  </span>
                </div>
                <p class="text-sm font-semibold text-slate-800 dark:text-slate-200">{{ step.title }}</p>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed">{{ step.description }}</p>
              </div>
            </li>
          </ol>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { watchEffect } from 'vue'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const steps = [
  {
    number: 1,
    icon: 'upload_file',
    title: 'Chargez votre PDF',
    description: 'Glissez-déposez votre fichier PDF dans la zone prévue, ou cliquez sur "Choisir un PDF" pour le sélectionner depuis votre appareil (max 5 Mo).',
  },
  {
    number: 2,
    icon: 'touch_app',
    title: 'Sélectionnez vos pages',
    description: 'Cliquez sur les pages à extraire pour les inclure. Utilisez les raccourcis de la barre latérale pour tout sélectionner, ou les pages paires/impaires.',
  },
  {
    number: 3,
    icon: 'download',
    title: 'Téléchargez le résultat',
    description: 'Choisissez le mode de sortie (fichier fusionné ou un PDF par page), puis cliquez sur "Télécharger" pour récupérer vos pages dans un ZIP.',
  },
]

watchEffect((onCleanup) => {
  if (!props.open) return
  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') emit('close')
  }
  window.addEventListener('keydown', onKeydown)
  onCleanup(() => window.removeEventListener('keydown', onKeydown))
})
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .relative {
  transform: translateY(20px);
}
.modal-leave-to .relative {
  transform: translateY(20px);
}
</style>
