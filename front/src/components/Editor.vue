<script>
import "ckeditor5/ckeditor5.css"
import { Ckeditor } from "@ckeditor/ckeditor5-vue"
import {
  Bold,
  Italic,
  Strikethrough,
  Code,
  ClassicEditor,
  Essentials,
  Heading,
  List,
  Link,
  Paragraph,
  Markdown,
  BlockQuote,
  Image,
  ImageInsertViaUrl,
  Table,
  TableToolbar,
  HorizontalLine,
  Autoformat,
} from 'ckeditor5';

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
