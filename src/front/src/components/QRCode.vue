<script>
import QRCode from 'qrcodejs2-fix';

export default {
    props: {
        value: String
    },
    data() {
        return {
            qrcode: null
        };
    },
    mounted() {
        this.qrcode = new QRCode(this.$refs.qrcode, this.value);
    },
    watch: {
        value() {
            this.qrcode.clear();
            this.qrcode.makeCode(this.value);
        }
    }
};
</script>

<template>
    <div ref="qrcode"></div>
</template>