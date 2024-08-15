<script lang="ts">
	import { callHass } from '$lib/common';
	import { stateStore } from '$lib/stores';

	export let state = '';
	export let url = '';
	export let alt = '';
	let value = '';
	let inputRef: HTMLInputElement;

	if (state) {
		stateStore.subscribe((states: Record<string, any>) => {
			value = states[state];
		});
	} else {
		value = url;
	}

	const handleClick = () => {
		inputRef.click();
	};
	const handleFileChange = (event: Event) => {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = (e) => {
				const fileBytes = e.target?.result as ArrayBuffer;

				callHass('uploadImage', {
					bytes: fileBytes,
					name: file.name,
					type: file.type
				});
			};
			reader.readAsArrayBuffer(file);
		}
	};
</script>

<div class="w-full h-full overflow-hidden flex items-center justify-center">
	<img src={value} {alt} class="max-w-full max-h-full object-contain" on:click={handleClick} />
	<input
		type="file"
		accept="image/*"
		class={value ? 'hidden' : ''}
		bind:this={inputRef}
		on:change={handleFileChange}
	/>
</div>
