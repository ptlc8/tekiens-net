import pluginVue from 'eslint-plugin-vue'
import pluginVueScopedCSS from 'eslint-plugin-vue-scoped-css';
export default [
    ...pluginVue.configs['flat/recommended'],
    ...pluginVueScopedCSS.configs['flat/recommended'],
    {
        rules: {
            "vue/html-indent": ["error", 4],
            "vue/max-attributes-per-line": "off",
            "vue/attributes-order": "off",
            "vue/html-self-closing": ["error", {
                html: {
                    void: "always",
                    normal: "never",
                }
            }],
            "vue/singleline-html-element-content-newline": "off",
            "vue/multi-word-component-names": "off",
            "vue/no-v-html": "off",
            "vue/order-in-components": ["warn", {
                "order": [
                    "name",
                    "extends",
                    "components",
                    "emits",
                    "setup",
                    "data",
                    "computed",
                    "methods",
                    "watch",
                    "LIFECYCLE_HOOKS",
                    "ROUTER_GUARDS"
                ]
            }]
        }
    }
]