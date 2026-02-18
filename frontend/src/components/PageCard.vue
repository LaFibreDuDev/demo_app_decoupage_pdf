<template>
  <button
    @click="$emit('toggle')"
    :class="[
      'relative w-20 h-24 rounded-lg border-2 overflow-hidden transition-all cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-blue-500',
      selected
        ? 'border-blue-500 shadow-md'
        : 'border-gray-200 bg-white hover:border-gray-400'
    ]"
  >
    <!-- Thumbnail -->
    <img
      v-if="thumbUrl"
      :src="thumbUrl"
      :alt="`Page ${page}`"
      class="absolute inset-0 w-full h-full object-cover"
      :class="selected ? 'brightness-90' : ''"
    />

    <!-- Fallback background when no thumbnail -->
    <span
      v-else
      :class="['absolute inset-0 flex flex-col items-center justify-center gap-1', selected ? 'bg-blue-50' : 'bg-white']"
    >
      <span :class="['text-xl font-semibold', selected ? 'text-blue-700' : 'text-gray-500']">
        {{ page }}
      </span>
      <span :class="['text-xs', selected ? 'text-blue-500' : 'text-gray-400']">page</span>
    </span>

    <!-- Page number overlay (visible on top of thumbnail) -->
    <span
      v-if="thumbUrl"
      class="absolute bottom-0 inset-x-0 text-center text-xs font-medium py-0.5 bg-black/40 text-white"
    >
      {{ page }}
    </span>

    <!-- Checkmark -->
    <span
      v-if="selected"
      class="absolute top-1 right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center"
    >
      <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
      </svg>
    </span>
  </button>
</template>

<script setup lang="ts">
const { page, selected = false, thumbUrl } = defineProps<{
  page: number
  selected?: boolean
  thumbUrl?: string
}>()

defineEmits<{
  toggle: []
}>()
</script>
