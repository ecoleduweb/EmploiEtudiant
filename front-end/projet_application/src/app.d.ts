// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
    namespace App {
        // interface Error {}
        // interface Locals {}
        // interface PageData {}
        // interface PageState {}
        // interface Platform {}
    }
}
declare module 'svelte-share-buttons-component' {
    import type { Component } from 'svelte';
    interface ShareButtonsProps {
        url?: string;
        title?: string;
        text?: string;
        subject?: string;
        body?: string;
    }


    export const WhatsApp: Component<ShareButtonsProps>;
    export const LinkedIn: Component<ShareButtonsProps>;
    export const X: Component<ShareButtonsProps>;
    export const Email: Component<ShareButtonsProps>;


}
export { }
