<template>
    <div :class="[type && `card-${type}`]" class="card">
        <div class="card-image" v-if="$slots.image">
            <slot name="image"></slot>
        </div>
        <div :class="headerClasses" class="card-header" v-if="$slots.header || title">
            <slot name="header">
                <h4 class="card-title">{{title}}</h4>
                <p class="card-category" v-if="subTitle">{{subTitle}}</p>
            </slot>
        </div>
        <div :class="bodyClasses" class="card-body" v-if="$slots.default">
            <slot></slot>
        </div>
        <slot name="raw-content"></slot>
        <div :class="footerClasses" class="card-footer" v-if="$slots.footer">
            <slot name="footer"></slot>
        </div>
    </div>
</template>
<script>
    export default {
        name: "card",
        props: {
            title: {
                type: String,
                description: "Card title"
            },
            subTitle: {
                type: String,
                description: "Card subtitle"
            },
            type: {
                type: String,
                description: "Card type (e.g primary/danger etc)"
            },
            headerClasses: {
                type: [String, Object, Array],
                description: "Card header css classes"
            },
            bodyClasses: {
                type: [String, Object, Array],
                description: "Card body css classes"
            },
            footerClasses: {
                type: [String, Object, Array],
                description: "Card footer css classes"
            }
        }
    };
</script>
<style>
</style>
