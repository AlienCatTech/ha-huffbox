<script lang="ts">
	import { onMount } from 'svelte';
	import { Flexilte } from '@flexilte/core';

	import { stateStore } from '$lib/stores';
	import type { LayoutConfig } from '@flexilte/core';
	import { components } from '$lib/default';
	import { setModeCurrent } from '@skeletonlabs/skeleton';
	import { fancyLogging } from '$lib/common';
	import { dev } from '$app/environment';
	import { fade } from 'svelte/transition';
	const loadingLayout: LayoutConfig<typeof components> = {
		rows: [
			{
				posX: 'middle',
				posY: 'middle',
				nodeClass: 'h-svh',

				cols: [
					{
						component: 'ImageBoxOG',
						props: {
							url: 'favicon.png'
						},
						posX: 'middle',
						posY: 'middle',
						wrapperClass: 'h-full w-56'
					}
				]
			}
		]
	};

	let layoutConfig: LayoutConfig<typeof components> = {};
	let currentLayout = '';

	async function loadConfig(option: string): Promise<LayoutConfig<typeof components>> {
		try {
			const urlDict: Record<string, string> = {
				default: 'default-layout.json',
				'fullscreen-image': 'fullscreen-image.json',
				'fullscreen-text': 'fullscreen-text.json',
				'fullscreen-video': 'fullscreen-video.json'
			};
			const url = option in urlDict ? urlDict[option] : option;
			currentLayout = option;
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error('Primary API failed');
			}
			return await response.json();
		} catch (error) {
			console.error('Failed to load layout');
			return {};
		}
	}

	function transformDict(input: { [key: string]: { [key: string]: any } }): { [key: string]: any } {
		let result: { [key: string]: any } = {};
		for (const key in input) {
			if (input[key] && typeof input[key] === 'object') {
				result[key] = input[key]['state'];
			}
		}
		return result;
	}
	onMount(async () => {
		setModeCurrent(true);

		window.addEventListener('message', async (event) => {
			const { msg, data } = event.data;
			console.log(msg, data);
			if (!data) {
				return;
			}
			const payload = transformDict(data);
			const newLayout = payload['select.huffbox_select_dashboard'];

			if (Object.keys(layoutConfig).length === 0 || newLayout !== currentLayout) {
				layoutConfig = await loadConfig(newLayout);
				fancyLogging('init', data);
			}
			stateStore.set(payload);
		});
		if (dev) {
			stateStore.set({
				'text.huffbox_subject_picture': 'https://placedog.net/500',
				'text.huffbox_subject_name': 'test',
				'text.huffbox_live_chat': 'live-chat.json',
				'text.huffbox_video_link':
					'https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4',
				'sensor.huffbox_heart_rate': '50',
				'sensor.huffbox_pulse': '50',
				'sensor.huffbox_spo2': '50',
				'sensor.huffbox_resp': '50',
				'sensor.huffbox_temp': '50',
				'lock.huffbox_lock': 'locked',
				'light.huffbox_light': 'on',
				'fan.huffbox_fan': 'on',
				'text.huffbox_banner': 'MEOW',
				'time.huffbox_time': '12:34:56'
			});
			layoutConfig = await loadConfig('default');
		}
	});
</script>

{#if Object.keys(layoutConfig).length === 0}
	<div transition:fade>
		<Flexilte {components} layoutConfig={loadingLayout} />
	</div>
{:else}
	<div transition:fade>
		<Flexilte {components} {layoutConfig} />
	</div>
{/if}
