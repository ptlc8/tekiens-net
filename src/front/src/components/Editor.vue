<script>
import CKEditor from "@ckeditor/ckeditor5-vue"
import { Bold, Italic, Strikethrough, Code } from "@ckeditor/ckeditor5-basic-styles";
import { ClassicEditor } from "@ckeditor/ckeditor5-editor-classic";
import { Essentials } from "@ckeditor/ckeditor5-essentials";
import { Heading } from "@ckeditor/ckeditor5-heading";
import { List } from "@ckeditor/ckeditor5-list";
import { Link } from "@ckeditor/ckeditor5-link";
import { Paragraph } from "@ckeditor/ckeditor5-paragraph";
import { Markdown } from "@ckeditor/ckeditor5-markdown-gfm";

export default {
	data() {
		return {
			editor: ClassicEditor,
			config: {
				plugins: [
					Markdown,
					Essentials,
					Heading,
					Bold,
					Italic,
					Strikethrough,
					Code,
					Link,
					Paragraph,
					List,
				],
				placeholder: this.placeholder,
				toolbar: {
					items: ["heading", "bold", "italic", "strikethrough", "code", "link", "bulletedList", "numberedList", "undo", "redo"],
				},
			}
		}
	},
	props: {
		value: String,
		placeholder: String
	},
	methods: {
		onInput(value) {
			this.$emit('input', value);
		}
	},
	components: {
		ckeditor: CKEditor.component
	}
}
</script>

<template>
	<ckeditor :model-value="value" @input="onInput" :editor="editor" :config="config"></ckeditor>
</template>
