<script lang="ts">
	import { stateStore } from '$lib/stores';

	export let text;
	export let textTop;
	export let textBottom;
</script>

<div class=" ">
	<div class="flex flex-col items-center">
		<div class=" flex items-center justify-center relative">
			<span
				class="text-7xl text-transparent bg-clip-text bg-gradient-to-t from-gray-400 to-transparent absolute transform -translate-x-1"
			>
				{textTop}
			</span>
			<button class=" hover:text-gray-600 relative z-10"> ▲ </button>
		</div>
		<div class="font-bold text-8xl my-4 flex items-center">{text}</div>
		<div class=" flex items-center justify-center relative">
			<button class=" hover:text-gray-600 relative z-10"> ▼ </button>
			<span
				class="text-7xl text-transparent bg-clip-text bg-gradient-to-b from-gray-400 to-transparent absolute transform -translate-x-1"
			>
				{textBottom}
			</span>
		</div>
	</div>
</div>
