<template>
  <button
    @click="$emit('toggle')"
    :class="[
      'relative w-20 h-24 rounded-lg border-2 flex flex-col items-center justify-center gap-1 transition-all cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-blue-500',
      selected
        ? 'border-blue-500 bg-blue-50 shadow-md'
        : 'border-gray-200 bg-white hover:border-gray-400'
    ]"
  >
    <!-- Checkmark -->
    <span
      v-if="selected"
      class="absolute top-1 right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center"
    >
      <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
      </svg>
    </span>

    <!-- Page number -->
    <span :class="['text-xl font-semibold', selected ? 'text-blue-700' : 'text-gray-500']">
      {{ page }}
    </span>
    <span :class="['text-xs', selected ? 'text-blue-500' : 'text-gray-400']">page</span>
  </button>
</template>

<script setup>
defineProps({
  page: { type: Number, required: true },
  selected: { type: Boolean, default: false },
})

defineEmits(['toggle'])
</script>
