<script>
import { Ckeditor } from "@ckeditor/ckeditor5-vue"
import { Bold, Italic, Strikethrough, Code } from "@ckeditor/ckeditor5-basic-styles";
import { ClassicEditor } from "@ckeditor/ckeditor5-editor-classic";
import { Essentials } from "@ckeditor/ckeditor5-essentials";
import { Heading } from "@ckeditor/ckeditor5-heading";
import { List } from "@ckeditor/ckeditor5-list";
import { Link } from "@ckeditor/ckeditor5-link";
import { Paragraph } from "@ckeditor/ckeditor5-paragraph";
import { Markdown } from "@ckeditor/ckeditor5-markdown-gfm";
import { BlockQuote } from "@ckeditor/ckeditor5-block-quote";
import { Image, ImageInsertViaUrl } from "@ckeditor/ckeditor5-image";
import { Table, TableToolbar } from "@ckeditor/ckeditor5-table";
import { HorizontalLine } from "@ckeditor/ckeditor5-horizontal-line";
import { Autoformat } from "@ckeditor/ckeditor5-autoformat";

export default {
    components: {
        Ckeditor
    },
    props: {
        value: {
            type: String,
            default: ""
        },
        placeholder: {
            type: String,
            default: ""
        }
    },
    emits: ['input'],
    data() {
        return {
            editor: ClassicEditor,
            config: {
                plugins: [
                    Markdown,
                    Autoformat,
                    Essentials,
                    Heading,
                    HorizontalLine,
                    Bold,
                    Italic,
                    Strikethrough,
                    Code,
                    BlockQuote,
                    Table,
                    TableToolbar,
                    Link,
                    Image,
                    ImageInsertViaUrl,
                    Paragraph,
                    List,
                ],
                placeholder: this.placeholder,
                toolbar: {
                    items: [
                        "heading", "horizontalLine",
                        "|", "bold", "italic", "strikethrough",
                        "|", "code", "blockQuote", "insertTable",
                        "|", "link", "imageInsert",
                        "|", "bulletedList", "numberedList",
                        "|", "undo", "redo",
                    ],
                },
                table: {
                    defaultHeadings: {
                        rows: 1
                    },
                    contentToolbar: [ "tableColumn", "tableRow" ],
                }
            },
        }
    },
    methods: {
        onInput(value) {
            this.$emit('input', value);
        }
    }
}
</script>

<template>
    <Ckeditor :model-value="value" @input="onInput" :editor="editor" :config="config" />
</template>
