import type { components } from './default';
import type { LayoutConfig } from './flexilte';

export async function loadConfig(): Promise<LayoutConfig<typeof components>> {
	try {
		const response = await fetch('/local/layout.json');
		if (!response.ok) {
			throw new Error('Primary API failed');
		}
		return await response.json();
	} catch (error) {
		console.warn('Failed to load from primary API, trying backup...');
		try {
			const backupResponse = await fetch('default.json');
			if (!backupResponse.ok) {
				throw new Error('Backup API failed');
			}
			return await backupResponse.json();
		} catch (backupError) {
			console.error('Failed to load from backup API');
			throw backupError;
		}
	}
}
