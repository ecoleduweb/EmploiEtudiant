<script lang="ts">
    import { onMount, onDestroy } from "svelte"
    import { Editor } from "@tiptap/core"
    import StarterKit from "@tiptap/starter-kit"
    import Underline from "@tiptap/extension-underline"

    interface Props {
        description?: string | null
        element?: any
        onchange?: (content: string) => void
    }

    let {
        description = $bindable(null),
        element = $bindable(null),
        onchange,
    }: Props = $props()

    let editor: any = $state(null)

    onMount(() => {
        editor = new Editor({
            element: element,
            extensions: [StarterKit, Underline],
            content: description || "",
            onTransaction: () => {
                editor = editor
            },
        })

        const editorElement = element.querySelector(".ProseMirror")
        if (editorElement) {
            editorElement.style.textAlign = "left"
            editorElement.style.minHeight = "200px"
            editorElement.style.padding = "10px"
            editorElement.style.fontSize = "16px"
            editorElement.style.lineHeight = "1.5"
            editorElement.style.color = "#333"
        }

        editor.on("update", ({ editor }: any) => {
            const content = editor.getHTML()
            description = content
            onchange?.(content)
        })
    })

    onDestroy(() => {
        if (editor) {
            editor.destroy()
        }
    })
</script>

<div class="editor-wrapper">
    {#if editor}
        <div class="rich-text-toolbar">
            <button
                onclick={(e) => {
                    e.preventDefault()
                    editor.chain().focus().toggleBold().run()
                }}
                class:active={editor.isActive("bold")}
                title="Gras"
            >
                <strong>G</strong>
            </button>
            <button
                onclick={(e) => {
                    e.preventDefault()
                    editor.chain().focus().toggleItalic().run()
                }}
                class:active={editor.isActive("italic")}
                title="Italique"
            >
                <i>I</i>
            </button>
            <button
                onclick={(e) => {
                    e.preventDefault()
                    editor.chain().focus().toggleUnderline().run()
                }}
                class:active={editor.isActive("underline")}
                title="Souligné"
            >
                <u>U</u>
            </button>
            <div class="toolbar-divider"></div>
            <button
                onclick={(e) => {
                    e.preventDefault()
                    editor.chain().focus().toggleHeading({ level: 2 }).run()
                }}
                class:active={editor.isActive("heading", { level: 2 })}
                title="Titre"
            >
                Titre
            </button>
            <button
                onclick={(e) => {
                    e.preventDefault()
                    editor.chain().focus().toggleBulletList().run()
                }}
                class={editor.isActive("bulletList") ? "is-active" : ""}
                title="Liste à puces"
            >
                <div class="bullet-list">
                    <span>&#8226; -</span>
                    <span>&#8226; -</span>
                    <span>&#8226; -</span>
                </div>
            </button>
            <button
                onclick={(e) => {
                    e.preventDefault()
                    editor.chain().focus().toggleOrderedList().run()
                }}
                class={editor.isActive("orderedList") ? "is-active" : ""}
                title="Liste numérotée"
            >
                <div class="ordered-list">
                    <span>1 -</span>
                    <span>2 -</span>
                    <span>3 -</span>
                </div>
            </button>
            <div class="undo-redo">
                <button
                    onclick={(e) => {
                        e.preventDefault()
                        editor.chain().focus().undo().run()
                    }}
                    disabled={!editor.can().chain().focus().undo().run()}
                    title="Retour en arrière"
                    style="font-size: 1.1em;"
                >
                    ↶
                </button>
                <button
                    onclick={(e) => {
                        e.preventDefault()
                        editor.chain().focus().redo().run()
                    }}
                    disabled={!editor.can().chain().focus().redo().run()}
                    title="Retour en avant"
                    style="font-size: 1.1em;"
                >
                    ↷
                </button>
            </div>
        </div>
    {/if}
    <div class="rich-text-content" bind:this={element}></div>
</div>

<style>
    .editor-wrapper {
        border: 1px solid #ccc;
        border-radius: 4px;
        transition: border-color 0.3s ease;
    }
    .rich-text-toolbar {
        display: flex;
        align-items: center;
        padding: 5px 10px;
        background-color: #f0f0f0;
        border-bottom: 1px solid #ddd;
    }
    .rich-text-toolbar button {
        background: none;
        border: none;
        color: #333;
        padding: 5px 10px;
        margin: 0 2px;
        cursor: pointer;
        border-radius: 3px;
        transition: background-color 0.3s ease;
    }
    .rich-text-toolbar button:hover:not(:disabled) {
        background-color: #e0e0e0;
    }
    .rich-text-toolbar button.active {
        background-color: #e0e0e0;
        color: black;
    }
    .rich-text-toolbar button:disabled {
        color: #ccc;
    }
    .toolbar-divider {
        width: 1px;
        height: 20px;
        background-color: #ccc;
        margin: 0 10px;
    }
    .bullet-list {
        display: flex;
        flex-direction: column;
        line-height: 0.5;
        font-size: 0.7rem;
    }
    .ordered-list {
        display: flex;
        flex-direction: column;
        line-height: 0.7;
        font-size: 0.7rem;
    }
    .undo-redo {
        margin-left: auto;
        display: flex;
    }
    .undo-redo button {
        border-radius: 0;
        margin: 0;
        padding: 5px 8px;
        border: 1px solid #ccc;
    }
    .undo-redo button:first-child {
        border-radius: 3px 0 0 3px;
        border-right: none;
    }
    .undo-redo button:last-child {
        border-radius: 0 3px 3px 0;
    }
</style>
