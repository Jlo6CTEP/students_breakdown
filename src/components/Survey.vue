<template>
    <div class="survey">
        <div class="card box-shadow">
            <!--      <img class="card-img-top"-->
            <!--           data-src="holder.js/100px225?theme=thumb&amp;bg=55595c&amp;fg=eceeef&amp;text=Thumbnail"-->
            <!--           alt="Thumbnail [100%x225]" style="height: 225px; width: 100%; display: block;"-->
            <!--           src="data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22348%22%20height%3D%22225%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20348%20225%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_16a2315e0ef%20text%20%7B%20fill%3A%23eceeef%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20monospace%3Bfont-size%3A17pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_16a2315e0ef%22%3E%3Crect%20width%3D%22348%22%20height%3D%22225%22%20fill%3D%22%2355595c%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%22116.5%22%20y%3D%22120.3%22%3EThumbnail%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E"-->
            <!--           data-holder-rendered="true">-->
            <div class="card-body">
                <h4 class="card-title"><strong>{{project_name}}</strong></h4>
                <p class="card-text">Course: {{course}}</p>
                <p class="card-text ">Description: {{description}}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                        <button @click="show" class="btn btn-sm btn-primary formed" type="button" v-if="is_formed">
                            Formed
                        </button>
                        <button @click="show" class="btn btn-sm btn-primary closed" type="button"
                                v-else-if="is_closed(due_date)">
                            Closed
                        </button>
                        <button @click="show" class="btn btn-sm btn-primary open" type="button" v-else>Fill now
                        </button>
                    </div>
                    <small class="text-muted">Due: {{due_date_format}}</small>
                    <modals-container/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import ModalWindow from "./ModalWindow";

    export default {
        name: "Survey",
        data() {
            return {
                isModalVisible: false,
            };
        },
        props: {
            course: {
                type: String,
                required:
                    true
            }
            ,
            project_name: {
                type: String,
                required:
                    true
            }
            ,
            description: {
                type: String,
                // default: 'lol'
                default:
                    'This is a description for survey with supporting text below as a natural lead-in to additional content. This content is a little bit longer'
            }
            ,
            due_date: {
                type: String,
                required:
                    true,
                validator:
                    due_date => {
                        return due_date instanceof Date && !isNaN(due_date);
                    }
            }
            ,
            is_formed: {
                type: Boolean,
                default:
                    false
            }
            ,
        },
        computed: {
            due_date_format() {
                let convert_date = new Date(this.due_date);
                return convert_date.getDate() + '-' + (convert_date.getMonth() + 1) + '-' + convert_date.getFullYear();
            }
        },
        methods: {
            is_closed(due_date) {
                let current_date = new Date();
                return (new Date(due_date) <= current_date);
            },
            show() {
                this.$modal.show(ModalWindow, {
                    text: 'This text is passed as a property',
                    project_name: this.project_name,
                    course: this.course,
                    description: this.description,
                    due_date_format: this.due_date_format,
                    is_formed: this.is_formed,
                    is_closed: this.is_closed(this.due_date)
                }, {
                    height: 'auto',
                    scrollable: true,
                    draggable: ".window-header",
                    adaptive: true
                }, {
                    'before-close': (event) => {
                        console.log('this will be called before the modal closes');
                    }
                }, {
                    draggable: true
                });
            },
            hide() {
                this.$modal.hide('dialog');
            },
            beforeOpen(event) {
                console.log(event.params.foo);
            }
        },
        components: {}
    }
</script>

<style scoped>
    .formed {
        background-color: cornflowerblue;
        border-color: cornflowerblue;
    }

    .closed {
        background-color: crimson;
        border-color: crimson;
    }

    .open {
        background-color: #42b983;
        border-color: #42b983;
    }

    .survey {
        display: flex;
        margin: 20px;
    }

    .modal-mask {
        position: fixed;
        z-index: 9998;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, .5);
        display: table;
        transition: opacity .3s ease;
    }

    .modal-wrapper {
        display: table-cell;
        vertical-align: middle;
    }

    .modal-container {
        width: 300px;
        margin: 0px auto;
        padding: 20px 30px;
        background-color: #fff;
        border-radius: 2px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
        transition: all .3s ease;
        font-family: Helvetica, Arial, sans-serif;
    }

    .modal-header h3 {
        margin-top: 0;
        color: #42b983;
    }

    .modal-body {
        margin: 20px 0;
    }

    .modal-default-button {
        float: right;
    }

    /*
     * The following styles are auto-applied to elements with
     * transition="modal" when their visibility is toggled
     * by Vue.js.
     *
     * You can easily play with the modal transition by editing
     * these styles.
     */

    .modal-enter {
        opacity: 0;
    }

    .modal-leave-active {
        opacity: 0;
    }

    .modal-enter .modal-container,
    .modal-leave-active .modal-container {
        -webkit-transform: scale(1.1);
        transform: scale(1.1);
    }

</style>

