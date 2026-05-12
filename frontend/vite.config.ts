import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig } from 'vite';
// @ts-ignore
import pxtorem from 'postcss-pxtorem';

// https://vite.dev/config/
export default defineConfig({
	plugins: [react()],
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src/'),
			'@app': path.resolve(__dirname, 'src/app'),
			'@entities': path.resolve(__dirname, 'src/entities'),
			'@features': path.resolve(__dirname, 'src/features'),
			'@widgets': path.resolve(__dirname, 'src/widgets'),
			'@pages': path.resolve(__dirname, 'src/pages'),
			'@shared': path.resolve(__dirname, 'src/shared'),
		},
	},
	server: {
		port: 3000,
		proxy: {
			'/api': 'http://localhost:8000',
			'/uploads': 'http://localhost:8000',
		},
	},
	css: {
		postcss: {
			plugins: [
				pxtorem({
					rootValue: 16, // 1rem = 16px
					propList: ['*'], // конвертировать все свойства
					unitPrecision: 5, // округление до 5 знаков
					minPixelValue: 2, // не трогать мелкие значения (например, границы в 1px)
				}),
			],
		},
		preprocessorOptions: {
			scss: {
				additionalData: `@use "@/app/styles/helpers" as *;`,
			},
		},
	},
});
