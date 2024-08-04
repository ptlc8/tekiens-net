<script>
import QRCode from 'qrcodejs2-fix';

export default {
    props: {
        value: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            qrcode: null
        };
    },
    watch: {
        value() {
            this.qrcode.clear();
            this.qrcode.makeCode(this.value);
        }
    },
    mounted() {
        this.qrcode = new QRCode(this.$refs.qrcode, this.value);
    }
};
</script>

<template>
    <div ref="qrcode" class="qr-code"></div>
</template>

<style>
.qr-code img {
    object-fit: contain;
    width: 100%;
    height: 100%;
}
</style>