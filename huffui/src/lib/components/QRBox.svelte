<script lang="ts">
	import QRCode from 'qrcode';
	import { onMount } from 'svelte';
	export let type: string = 'text';
	export let title: string = '';
	export let data: string;

	let dataUrl = '';
	onMount(() => {
		if (type === 'wifi') {
			const parts = data.split('||');
			data = `WIFI:T:WPA;S:${parts[0]};P:${parts[1]};;`;
		}

		QRCode.toDataURL(data, { color: { light: 'ffffff00', dark: '0d3d56ff' } }).then((url) => {
			dataUrl = url;
		});
	});
</script>

<div class="flex">
	<div class="w-full h-full">
		<div class="text-center text-2xl">
			<div>{title}</div>
		</div>
		<img src={dataUrl} alt="qrcode" class="mx-auto object-contain" />
	</div>
</div>
