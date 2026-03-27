import { writable} from "svelte/store";
type Session={
    isLoggedIn: boolean;
    isModerator: boolean;
}

export const session = writable<Session>({
    isLoggedIn: false,
    isModerator: false
});

