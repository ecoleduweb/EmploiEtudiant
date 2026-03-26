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
    export class WhatsApp extends Component { }
    export class LinkedIn extends Component { }
    export class X extends Component { }
    export class Email extends Component { }
    export class SMS extends Component { }

}
export { }
